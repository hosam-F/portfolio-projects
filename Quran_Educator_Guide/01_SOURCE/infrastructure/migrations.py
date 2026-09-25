"""Controlled local migration foundation; not a production release system."""
from pathlib import Path
from sqlalchemy import Integer, String, select, inspect, text
from sqlalchemy.orm import Mapped, mapped_column
from quran_educator.infrastructure.db import Base, create_session_factory
from quran_educator.infrastructure.backup import create_manual_backup, restore_verified, verify_backup

CURRENT_SCHEMA_VERSION = "v1-data-layer-2"


class SchemaVersion(Base):
    __tablename__ = "schema_versions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)


def _has_column(engine, table: str, column: str) -> bool:
    return any(item["name"] == column for item in inspect(engine).get_columns(table))


def _migration_v1_to_v2(connection) -> None:
    if not _has_column(connection.engine, "audit_entries", "timestamp"):
        connection.execute(text("ALTER TABLE audit_entries ADD COLUMN timestamp DATETIME"))
        connection.execute(text("UPDATE audit_entries SET timestamp = CURRENT_TIMESTAMP WHERE timestamp IS NULL"))


MIGRATIONS = {"v1-data-layer-1": _migration_v1_to_v2}


def _current_versions(session):
    return [row.version for row in session.scalars(select(SchemaVersion).order_by(SchemaVersion.id))]


def _migration_audit(factory, actor_id: str, action: str, entity_id: str, outcome: str, reason: str | None = None) -> None:
    from quran_educator.infrastructure.db import AuditEntry
    with factory() as session:
        session.add(AuditEntry(actor_id=actor_id, action=action, entity_type="Migration", entity_id=entity_id, outcome=outcome, reason=reason))
        session.commit()


def migrate_to_current(factory) -> None:
    # Schema creation is owned by create_session_factory(). Keep migration
    # handling focused on version checks and explicit migrations.
    with factory() as session:
        versions = _current_versions(session)
        if not versions:
            session.add(SchemaVersion(version=CURRENT_SCHEMA_VERSION))
            session.commit()
            return
        current = versions[-1]
        if current == CURRENT_SCHEMA_VERSION:
            return
        if current not in MIGRATIONS:
            raise RuntimeError(f"Missing migration from schema version: {current}")
        try:
            MIGRATIONS[current](session.connection())
            session.add(SchemaVersion(version=CURRENT_SCHEMA_VERSION))
            session.commit()
        except Exception:
            session.rollback()
            raise


def initialize_database(database_path: Path):
    factory = create_session_factory(database_path)
    try:
        Base.metadata.create_all(factory._quran_engine)
        migrate_to_current(factory)
        return factory
    except Exception:
        factory._quran_engine.dispose()
        raise


def migrate_with_backup(database_path: Path, backup_path: Path, actor_id: str = "SYSTEM", force_failure: bool = False):
    """Official controlled path: backup -> verify -> migrate -> verify; restore on failure."""
    database_path = Path(database_path)
    backup_path = Path(backup_path)
    factory = initialize_database(database_path)
    try:
        create_manual_backup(database_path, backup_path, factory=factory, actor_id=actor_id)
        if not verify_backup(backup_path, factory=factory, actor_id=actor_id):
            raise RuntimeError("Pre-migration backup verification failed")
        if force_failure:
            raise RuntimeError("Intentional synthetic migration failure")
        factory._quran_engine.dispose()
        result = initialize_database(database_path)
        _migration_audit(result, actor_id, "MIGRATION_SUCCEEDED", f"{CURRENT_SCHEMA_VERSION}", "SUCCESS")
        if not verify_backup(backup_path, factory=result, actor_id=actor_id):
            raise RuntimeError("Post-migration verification failed")
        return result
    except Exception as exc:
        try:
            factory._quran_engine.dispose()
        except Exception:
            pass
        restore_factory = initialize_database(database_path)
        restore_verified(backup_path, database_path, factory=restore_factory, actor_id=actor_id)
        _migration_audit(restore_factory, actor_id, "MIGRATION_FAILED", f"{CURRENT_SCHEMA_VERSION}", "FAILURE", type(exc).__name__)
        restore_factory._quran_engine.dispose()
        return initialize_database(database_path)
