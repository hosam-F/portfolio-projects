# CURRICULUM & MENTOR WORKFLOW DESIGN V1

## Vertical Slice

Organization → Circle → Group → Teacher → Student → Curriculum → CurriculumUnit → StudentAssignment → Session → Attendance → Progress → MentorObservation → Close → Audit → Backup → Restore → Verify.

## State Machines

| Entity | States | Allowed transitions |
|---|---|---|
| Curriculum | DRAFT, ACTIVE, ARCHIVED | DRAFT→ACTIVE→ARCHIVED |
| Session | DRAFT, OPEN, CLOSED | DRAFT→OPEN→CLOSED |
| Assignment | ASSIGNED, STARTED, COMPLETED, CANCELLED | DB constrained; duplicate student/unit denied |
| Observation | ACTIVE, ARCHIVED | closed-session creation denied |
| Progress | PLANNED, IN_PROGRESS, REVIEWED, MASTERED | completion 0–100 |

## Content Boundary

Progress stores metadata and a synthetic source contract only. No Quran text, ayah text, tafsir, translation, audio, image, or external asset enters the slice.

## Mentor Boundary

Mentor is a functional description of a teacher workflow, not a new Role. Existing roles remain ADMIN, TEACHER, and TRAINEE_TEACHER. Observations are recorded verbatim as synthetic text; no religious or professional judgment is generated.

## Audit and Recovery

Sensitive CREATE, ASSIGN, ATTENDANCE, PROGRESS, OBSERVATION, OPEN_SESSION, CLOSE_SESSION, ACTIVATE, ARCHIVE, and DENIED paths are represented in the slice. The final scenario verifies backup, SHA-256, restore, and byte-level restored-state equality.
