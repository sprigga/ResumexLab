# Code Review Fixes Design

**Date:** 2026-04-01
**Scope:** Fix 4 remaining open issues from the 2025-01-31 API endpoints code review
**Approach:** Explicit per-endpoint fixes with factory-level coverage

---

## Background

The 2025-01-31 code review identified 12 issues across the API endpoint layer. A re-audit on 2026-04-01 found that 4 issues were already fixed (#2, #7, #12) and 1 is mitigated by Pydantic schemas (#4). This spec covers the 4 truly open issues.

---

## Issue #5: Missing Transaction Rollback (HIGH)

### Problem

All `db.commit()` calls across endpoint files lack `try/except` with `db.rollback()`. If commit or refresh fails, partial data may remain in an inconsistent state.

### Files to Modify

| File | Endpoints Affected | Coverage |
|------|--------------------|----------|
| `backend/app/api/crud_base.py` | create, update, delete (factory) | Covers 5 entities |
| `backend/app/api/endpoints/projects.py` | 6 write endpoints | Individual |
| `backend/app/api/endpoints/work_experience.py` | ~4 write endpoints | Individual |
| `backend/app/api/endpoints/personal_info.py` | 1 write endpoint | Individual |

### Pattern

Each write operation will be wrapped:

```python
try:
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
except Exception:
    db.rollback()
    raise HTTPException(status_code=500, detail="Database error occurred")
```

### Factory Change (crud_base.py)

Add `status` import and wrap all 3 write endpoints (create, update, delete) in `try/except` with `db.rollback()`.

### Non-Factory Files

Apply the same `try/except` pattern to every `db.commit()` in `projects.py`, `work_experience.py`, and `personal_info.py`.

---

## Issue #6: Information Leakage in Error Messages (HIGH)

### Problem

`import_data.py` exposes internal database errors to clients via `str(e)` and `str(verify_error)`, potentially revealing schema info, file paths, or configuration.

### File to Modify

`backend/app/api/endpoints/import_data.py` — 2 locations:

1. **Line 74-77** (export exception handler): `detail=f"Error exporting database: {str(e)}"`
2. **Line 171-175** (import verification failure): `detail=f"Imported database file is not valid: {str(verify_error)}"`
3. **Line 188-191** (import exception handler): `detail=f"Error importing database: {str(e)}"`

### Fix

- Add `import logging` and `logger = logging.getLogger(__name__)` at module level
- Replace `str(e)` / `str(verify_error)` with generic messages
- Log the full error server-side with `logger.error()`

---

## Issue #8: Inconsistent Error Handling (MEDIUM)

### Problem

Mix of raw integers (`status_code=404`) and `status.HTTP_404_NOT_FOUND` constants across files.

### Files to Modify

1. **`backend/app/api/crud_base.py`**: 2 occurrences of `status_code=404` in `get_one` and `update` endpoints
2. **`backend/app/api/endpoints/projects.py`**: 3 occurrences of `status_code=404` in `get_project`, `update_project`, `delete_project`

### Fix

- Add `from fastapi import status` import to `crud_base.py`
- Replace all raw `status_code=404` with `status.HTTP_404_NOT_FOUND`

---

## Issue #9: Missing Module Exports (MEDIUM)

### Problem

`__init__.py` only exports 3 of 10 endpoint modules.

### File to Modify

`backend/app/api/endpoints/__init__.py`

### Fix

Add all 7 missing modules to `__all__`:

```python
__all__ = [
    "auth",
    "personal_info",
    "work_experience",
    "education",
    "certifications",
    "languages",
    "publications",
    "github_projects",
    "projects",
    "import_data",
]
```

---

## Cross-Reference Table Update

After all fixes are applied, update the cross-reference table in `docs/code_review/API_ENDPOINTS_CODE_REVIEW.md` to reflect:

| Issue | Status |
|-------|--------|
| #2 | FIXED (file upload DoS) |
| #4 | MITIGATED (Pydantic schema restricts fields) |
| #5 | FIXED (rollback added) |
| #6 | FIXED (generic error messages + logging) |
| #7 | FIXED (file validation) |
| #8 | FIXED (standardized status constants) |
| #9 | FIXED (module exports complete) |
| #12 | FIXED (path traversal protected via .resolve()) |

## Testing

Run existing tests to verify no regressions:

```bash
pytest tests/
```
