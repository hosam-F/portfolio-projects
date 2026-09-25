from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def _write_report(output_path: Path, title: str, lines: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    pdf.setTitle(title)
    y = 780
    pdf.drawString(72, y, title)
    y -= 24
    for line in lines:
        pdf.drawString(72, y, line)
        y -= 20
        if y < 72:
            pdf.showPage()
            y = 780
    pdf.save()


def _context_lines(context: dict | None) -> list[str]:
    if not context:
        return []
    return [f"{label}: {value}" for label, value in context.items() if value]


def create_synthetic_status_report(output_path: Path, context: dict | None = None) -> None:
    _write_report(output_path, "Controlled Development Status", _context_lines(context) + [
        "SYNTHETIC DATA ONLY — NOT A PRODUCTION REPORT",
        "NOT REAL PERSON DATA — NOT QURAN CONTENT",
        "CONTENT_GATE=NO-GO; RELEASE_GATE=NO-GO",
    ])


def create_student_report(output_path: Path, student_label: str = "TEST DATA ONLY", context: dict | None = None) -> None:
    _write_report(output_path, "Synthetic Student Report", _context_lines(context) + [
        "TEST DATA ONLY — NOT REAL PERSON DATA",
        f"Student: {student_label}",
        "Attendance: PRESENT / ABSENT / EXCUSED — synthetic summary",
        "Sessions: synthetic session records",
        "Progress: metadata-only completion",
        "Mentor observations: TEST OBSERVATION ONLY",
        "No Quran text or external content included",
    ])


def create_circle_report(output_path: Path, circle_label: str = "TEST DATA ONLY", context: dict | None = None) -> None:
    _write_report(output_path, "Synthetic Circle Report", _context_lines(context) + [
        "TEST DATA ONLY — NOT REAL PERSON DATA",
        f"Circle: {circle_label}",
        "Students: synthetic count",
        "Attendance and activity: synthetic summary",
        "Progress: metadata-only summary",
        "CONTENT_GATE=NO-GO; RELEASE_GATE=NO-GO",
    ])


def create_session_report(output_path: Path, session_label: str = "TEST DATA ONLY", context: dict | None = None) -> None:
    _write_report(output_path, "Synthetic Session Report", _context_lines(context) + [
        "TEST DATA ONLY — NOT REAL PERSON DATA",
        f"Session: {session_label}",
        "Attendance: synthetic records",
        "Progress: metadata-only record",
        "Mentor observation: TEST OBSERVATION ONLY",
        "No Quran text or external content included",
    ])
