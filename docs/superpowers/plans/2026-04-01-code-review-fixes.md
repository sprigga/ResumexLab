# Code Review Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 4 remaining open issues from the 2025-01-31 API code review (#5 rollback, #6 info leakage, #8 status codes, #9 module exports).

**Architecture:** Fix the CRUD factory (`crud_base.py`) for rollback and status codes to cover 5 entities at once, then patch the 3 non-factory endpoint files (`projects.py`, `work_experience.py`, `personal_info.py`). Fix `import_data.py` for info leakage. Update `__init__.py` for module exports. Finally update the review doc's cross-reference table.

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic v2, pytest

---

## File Map

| File | Responsibility | Issues |
|------|---------------|--------|
| `backend/app/api/crud_base.py` | CRUD router factory (5 entities) | #5, #8 |
| `backend/app/api/endpoints/projects.py` | Projects endpoints (hand-written) | #5, #8 |
| `backend/app/api/endpoints/work_experience.py` | Work experience endpoints | #5 |
| `backend/app/api/endpoints/personal_info.py` | Personal info endpoints | #5 |
| `backend/app/api/endpoints/import_data.py` | DB import/export endpoints | #6 |
| `backend/app/api/endpoints/__init__.py` | Package exports | #9 |
| `docs/code_review/API_ENDPOINTS_CODE_REVIEW.md` | Review tracking document | docs update |

---

### Task 1: Add transaction rollback to `crud_base.py` factory

**Files:**
- Modify: `backend/app/api/crud_base.py`

- [ ] **Step 1: Add `status` import and wrap create endpoint in try/except**

Replace the create endpoint (lines 54-64) with rollback handling:

```python
from fastapi import APIRouter, Depends, HTTPException, status
```

Then replace the create function body:

```python
    @router.post("/", response_model=response_schema)
    def create(
        item_data: create_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = model(**item_data.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 2: Wrap update endpoint in try/except**

Replace the update function body (lines 66-80):

```python
    @router.put("/{item_id}", response_model=response_schema)
    def update(
        item_id: int,
        item_data: update_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = db.query(model).filter(model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
            for key, value in item_data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 3: Wrap delete endpoint in try/except**

Replace the delete function body (lines 82-93):

```python
    @router.delete("/{item_id}")
    def delete(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = db.query(model).filter(model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
            db.delete(db_item)
            db.commit()
            return {"message": f"{entity_name} deleted successfully"}
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 4: Fix raw `status_code=404` in get_one endpoint (Issue #8)**

Replace the get_one function (lines 47-52):

```python
    @router.get("/{item_id}", response_model=response_schema)
    def get_one(item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
        return item
```

- [ ] **Step 5: Run existing tests to verify no regressions**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All existing tests pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/crud_base.py
git commit -m "fix: add transaction rollback and standardize status codes in CRUD factory

Issues #5 and #8: wrap create/update/delete in try/except with
db.rollback(), replace raw 404 with status.HTTP_404_NOT_FOUND.
Covers 5 factory-based entities (education, certifications,
languages, publications, github_projects)."
```

---

### Task 2: Add transaction rollback to `projects.py`

**Files:**
- Modify: `backend/app/api/endpoints/projects.py`

- [ ] **Step 1: Wrap create_project in try/except**

Replace the create_project function body (lines 41-48):

```python
@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new project"""
    try:
        db_project = Project(**project.model_dump())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 2: Wrap update_project in try/except, fix raw 404 (Issue #8)**

Replace the update_project function body (lines 51-63):

```python
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update a project"""
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        for key, value in project.model_dump(exclude_unset=True).items():
            setattr(db_project, key, value)

        db.commit()
        db.refresh(db_project)
        return db_project
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 3: Wrap delete_project in try/except, fix raw 404 (Issue #8)**

Replace the delete_project function body (lines 66-75):

```python
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a project"""
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        db.delete(db_project)
        db.commit()
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 4: Fix raw 404 in get_project (Issue #8)**

Replace line 37:

```python
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
```

- [ ] **Step 5: Wrap create_project_with_file in try/except**

The function body (lines 80-131) should be wrapped. The existing `HTTPException` raises (file validation) must be re-raised, so use `except HTTPException: raise` before the generic catch:

```python
@router.post("/upload", response_model=ProjectResponse)
async def create_project_with_file(
    # ... same parameters ...
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create project with file attachment"""
    try:
        # Validate file if provided
        if file and file.filename:
            if not validate_file(file):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file type or size. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG. Max size: 100MB"
                )

        # ... same project_data and file handling as current ...
        project_data = {
            "work_experience_id": work_experience_id,
            "title_zh": title_zh,
            "title_en": title_en,
            "description_zh": description_zh,
            "description_en": description_en,
            "technologies": technologies,
            "tools": tools,
            "environment": environment,
            "start_date": parse_date_string(start_date),
            "end_date": parse_date_string(end_date),
            "display_order": display_order,
        }

        if file and file.filename:
            project_data.update(await save_upload_file(file))

        db_project = Project(**project_data)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 6: Wrap update_project_with_file in try/except**

Same pattern — wrap the body of the function at lines 136-207, re-raise HTTPException before generic catch.

- [ ] **Step 7: Wrap update_project_attachment_name in try/except**

Wrap the body of the function at lines 213-244, re-raise HTTPException before generic catch.

- [ ] **Step 8: Run existing tests**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 9: Commit**

```bash
git add backend/app/api/endpoints/projects.py
git commit -m "fix: add transaction rollback and standardize status codes in projects.py

Issues #5 and #8: wrap all 6 write endpoints in try/except with
db.rollback(), replace raw 404 with status.HTTP_404_NOT_FOUND."
```

---

### Task 3: Add transaction rollback to `work_experience.py`

**Files:**
- Modify: `backend/app/api/endpoints/work_experience.py`

- [ ] **Step 1: Wrap create_work_experience in try/except**

Wrap lines 100-105 (the db operations after docstring and validation):

```python
    try:
        db_experience = WorkExperience(**experience_data.model_dump())
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 2: Wrap create_work_experience_with_file in try/except**

Wrap the db operations in lines 130-164. Keep the file validation HTTPException outside the try (it raises before db ops), or use `except HTTPException: raise` pattern.

- [ ] **Step 3: Wrap update_work_experience_with_file in try/except**

Wrap the db operations in lines 209-256. Use `except HTTPException: raise` pattern.

- [ ] **Step 4: Wrap update_work_experience in try/except**

Wrap lines 274-280:

```python
    try:
        update_data = experience_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(experience, field, value)
        db.commit()
        db.refresh(experience)
        return experience
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 5: Wrap delete_work_experience in try/except**

Wrap lines 298-304:

```python
    try:
        delete_upload_file(experience.attachment_path)
        db.delete(experience)
        db.commit()
        return None
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 6: Run existing tests**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 7: Commit**

```bash
git add backend/app/api/endpoints/work_experience.py
git commit -m "fix: add transaction rollback to work_experience.py

Issue #5: wrap all 5 write endpoints in try/except with db.rollback()."
```

---

### Task 4: Add transaction rollback to `personal_info.py`

**Files:**
- Modify: `backend/app/api/endpoints/personal_info.py`

- [ ] **Step 1: Wrap create_personal_info in try/except**

Wrap lines 58-62:

```python
    try:
        db_info = PersonalInfo(**info_data.model_dump())
        db.add(db_info)
        db.commit()
        db.refresh(db_info)
        return db_info
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 2: Wrap update_personal_info in try/except**

Wrap lines 76-86 (the if/else branch with db operations):

```python
    try:
        if not info:
            info = PersonalInfo(**info_data.model_dump())
            db.add(info)
        else:
            update_data = info_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(info, field, value)
        db.commit()
        db.refresh(info)
        return info
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
```

- [ ] **Step 3: Run existing tests**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/api/endpoints/personal_info.py
git commit -m "fix: add transaction rollback to personal_info.py

Issue #5: wrap create and update endpoints in try/except with
db.rollback()."
```

---

### Task 5: Fix information leakage in `import_data.py`

**Files:**
- Modify: `backend/app/api/endpoints/import_data.py`

- [ ] **Step 1: Add logging import and logger at module level**

Add after the existing imports (after line 20):

```python
import logging

logger = logging.getLogger(__name__)
```

- [ ] **Step 2: Fix export_database exception handler (line 73-77)**

Replace:

```python
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting database: {str(e)}"
        )
```

With:

```python
    except Exception as e:
        logger.error(f"Error exporting database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error exporting database"
        )
```

- [ ] **Step 3: Fix import verification exception handler (lines 171-175)**

Replace:

```python
        except Exception as verify_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Imported database file is not valid: {str(verify_error)}"
            )
```

With:

```python
        except Exception as verify_error:
            logger.error(f"Database import validation failed: {verify_error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Imported database file is not valid"
            )
```

- [ ] **Step 4: Fix import exception handler (lines 187-191)**

Replace:

```python
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing database: {str(e)}"
        )
```

With:

```python
    except Exception as e:
        logger.error(f"Error importing database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error importing database"
        )
```

- [ ] **Step 5: Run existing tests**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/endpoints/import_data.py
git commit -m "fix: remove internal error details from client responses

Issue #6: replace str(e) with generic messages in import_data.py,
log full errors server-side with logging.getLogger()."
```

---

### Task 6: Fix module exports in `__init__.py`

**Files:**
- Modify: `backend/app/api/endpoints/__init__.py`

- [ ] **Step 1: Update imports and __all__**

Replace the entire file content:

```python
from app.api.endpoints import (
    auth, personal_info, work_experience,
    education, certifications, languages,
    publications, github_projects, projects,
    import_data,
)

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

- [ ] **Step 2: Run existing tests**

Run: `cd backend && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 3: Commit**

```bash
git add backend/app/api/endpoints/__init__.py
git commit -m "fix: add missing module exports to endpoints __init__.py

Issue #9: add 7 missing modules (education, certifications, languages,
publications, github_projects, projects, import_data) to __all__."
```

---

### Task 7: Update cross-reference table in review document

**Files:**
- Modify: `docs/code_review/API_ENDPOINTS_CODE_REVIEW.md`

- [ ] **Step 1: Update the cross-reference table (lines 557-572)**

Replace with:

```markdown
## Cross-Reference: Overall Review Issue Status

| Issue # | Severity | Description | 2025-01-31 | 2026-04-01 Validation |
|---------|----------|-------------|------------|----------------------|
| 1 | CRITICAL | Missing auth on write operations | Identified | **FIXED** |
| 2 | CRITICAL | File upload DoS in import_data.py | Identified | **FIXED** |
| 3 | HIGH | Pydantic V2 `.dict()` deprecation | Identified | **FIXED** |
| 4 | HIGH | SQL injection via dict expansion | Identified | **MITIGATED** (Pydantic schemas restrict fields) |
| 5 | HIGH | Missing transaction rollback | Identified | **FIXED** |
| 6 | HIGH | Information leakage in error messages | Identified | **FIXED** |
| 7 | MEDIUM | Silent file validation failures | Identified | **FIXED** |
| 8 | MEDIUM | Inconsistent error handling | Identified | **FIXED** |
| 9 | MEDIUM | Missing module exports | Identified | **FIXED** |
| 10 | MEDIUM | Duplicate imports | Identified | **FIXED** |
| 11 | LOW | Debug print statements | Identified | **FIXED** |
| 12 | LOW | Potential path traversal | Identified | **FIXED** |
```

- [ ] **Step 2: Commit**

```bash
git add docs/code_review/API_ENDPOINTS_CODE_REVIEW.md
git commit -m "docs: update code review cross-reference table

All 12 issues now resolved or mitigated. Updated status for
issues #2, #4, #5, #6, #8, #9, #12 based on 2026-04-01 audit."
```
