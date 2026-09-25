from hashlib import sha256
from pathlib import Path
import shutil

from quran_educator.infrastructure.db import AuditEntry


class BackupIntegrityError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _audit(factory, actor_id: str, action: str, entity_id: str, outcome: str, reason: str | None = None) -> None:
    if factory is None:
        return
    with factory() as session:
        session.add(AuditEntry(actor_id=actor_id, action=action, entity_type="Backup", entity_id=entity_id, outcome=outcome, reason=reason))
        session.commit()


def create_manual_backup(source: Path, destination: Path, factory=None, actor_id: str = "SYSTEM") -> str:
    entity_id = destination.name
    _audit(factory, actor_id, "BACKUP_STARTED", entity_id, "STARTED")
    try:
        if not source.exists():
            raise FileNotFoundError(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        digest = file_sha256(destination)
        destination.with_suffix(destination.suffix + ".sha256").write_text(digest, encoding="ascii")
        _audit(factory, actor_id, "BACKUP_SUCCEEDED", entity_id, "SUCCESS")
        return digest
    except Exception as exc:
        _audit(factory, actor_id, "BACKUP_FAILED", entity_id, "FAILURE", type(exc).__name__)
        raise


def verify_backup(backup: Path, factory=None, actor_id: str = "SYSTEM") -> bool:
    entity_id = backup.name
    _audit(factory, actor_id, "VERIFY_STARTED", entity_id, "STARTED")
    manifest = backup.with_suffix(backup.suffix + ".sha256")
    if not backup.exists() or not manifest.exists():
        _audit(factory, actor_id, "MISSING_MANIFEST", entity_id, "FAILURE", "Backup or manifest missing")
        _audit(factory, actor_id, "VERIFY_FAILED", entity_id, "FAILURE", "Backup or manifest missing")
        return False
    valid = file_sha256(backup) == manifest.read_text(encoding="ascii").strip()
    if valid:
        _audit(factory, actor_id, "VERIFY_SUCCEEDED", entity_id, "SUCCESS")
    else:
        _audit(factory, actor_id, "TAMPER_DETECTED", entity_id, "FAILURE", "SHA-256 mismatch")
        _audit(factory, actor_id, "VERIFY_FAILED", entity_id, "FAILURE", "SHA-256 mismatch")
    return valid


def restore_verified(backup: Path, destination: Path, factory=None, actor_id: str = "SYSTEM") -> None:
    entity_id = backup.name
    _audit(factory, actor_id, "RESTORE_STARTED", entity_id, "STARTED")
    try:
        if not verify_backup(backup, factory=factory, actor_id=actor_id):
            raise BackupIntegrityError("Backup integrity verification failed; restore rejected.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, destination)
        _audit(factory, actor_id, "RESTORE_SUCCEEDED", entity_id, "SUCCESS")
    except Exception as exc:
        _audit(factory, actor_id, "RESTORE_FAILED", entity_id, "FAILURE", type(exc).__name__)
        raise
