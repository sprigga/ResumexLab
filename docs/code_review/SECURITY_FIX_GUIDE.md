# Security Fixes Implementation Guide

**Purpose:** Step-by-step guide to fix critical security issues identified in code review.
**Priority:** CRITICAL - Complete immediately

---

## Fix 1: Add Authentication to All Write Operations

### Impact: CRITICAL
**Files Affected:** education.py, certifications.py, languages.py, publications.py, github_projects.py, projects.py, work_experience.py

### Template Code

Use this pattern for all unprotected endpoints:

#### Before (Vulnerable):
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db

@router.post("/", response_model=EducationResponse)
def create_education(education: EducationCreate, db: Session = Depends(get_db)):
    """Create a new education record"""
    db_education = Education(**education.model_dump())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education
```

#### After (Secure):
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.endpoints.auth import get_current_user  # ADD THIS
from app.models.user import User  # ADD THIS

@router.post("/", response_model=EducationResponse)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ADD THIS
):
    """Create a new education record (requires authentication)"""
    db_education = Education(**education.model_dump())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education
```

### Files to Update

#### 1. education.py

Add at top of file:
```python
from app.api.endpoints.auth import get_current_user
from app.models.user import User
```

Update endpoints:
```python
@router.post("/", response_model=EducationResponse)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.put("/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: int,
    education: EducationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.delete("/{education_id}")
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
```

#### 2. certifications.py

Same changes as education.py.

#### 3. languages.py

Same changes as education.py.

#### 4. publications.py

Same changes as education.py.

#### 5. github_projects.py

Same changes as education.py.

#### 6. projects.py

Update all write endpoints:
```python
@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.post("/upload", response_model=ProjectResponse)
async def create_project_with_file(
    # ... existing parameters ...
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.put("/{project_id}/upload", response_model=ProjectResponse)
async def update_project_with_file(
    # ... existing parameters ...
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.patch("/{project_id}/attachment-name", response_model=ProjectResponse)
def update_project_attachment_name(
    project_id: int,
    attachment_name: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
```

#### 7. work_experience.py

Update all write endpoints:
```python
@router.post("/", response_model=WorkExperienceInDB, status_code=status.HTTP_201_CREATED)
async def create_work_experience(
    experience_data: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.post("/upload", response_model=WorkExperienceInDB, status_code=status.HTTP_201_CREATED)
async def create_work_experience_with_file(
    # ... existing parameters ...
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.put("/{experience_id}/upload", response_model=WorkExperienceInDB)
async def update_work_experience_with_file(
    # ... existing parameters ...
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.put("/{experience_id}", response_model=WorkExperienceInDB)
async def update_work_experience(
    experience_id: int,
    experience_data: WorkExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
```

---

## Fix 2: File Upload DoS Vulnerability

### Impact: CRITICAL
**File:** import_data.py

### Before (Vulnerable):
```python
@router.post("/database/import/")
async def import_database(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.db'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .db files are allowed"
        )

    # VULNERABLE: Reads entire file before size check
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > MAX_DB_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_DB_FILE_SIZE / (1024 * 1024):.0f}MB"
        )

    await file.seek(0)
```

### After (Secure):
```python
@router.post("/database/import/")
async def import_database(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.db'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .db files are allowed"
        )

    # Check file.size first if available from headers
    if file.size and file.size > MAX_DB_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_DB_FILE_SIZE / (1024 * 1024):.0f}MB"
        )

    # Read with incremental size checking
    CHUNK_SIZE = 8192
    file_content = b''
    bytes_read = 0

    while chunk := await file.read(CHUNK_SIZE):
        bytes_read += len(chunk)
        if bytes_read > MAX_DB_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {MAX_DB_FILE_SIZE / (1024 * 1024):.0f}MB"
            )
        file_content += chunk
```

---

## Fix 3: Replace .dict() with .model_dump()

### Impact: HIGH
**Files:** education.py, certifications.py, languages.py, publications.py, github_projects.py, projects.py

### Find and Replace Pattern:

**Search:** `.dict(`
**Replace:** `.model_dump(`

**Example:**
```python
# Before
db_education = Education(**education.dict())
for key, value in education.dict(exclude_unset=True).items():

# After
db_education = Education(**education.model_dump())
for key, value in education.model_dump(exclude_unset=True).items():
```

---

## Fix 4: Add Transaction Rollback

### Impact: HIGH
**Files:** All write operations

### Template:

```python
@router.post("/", response_model=EducationResponse)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new education record (requires authentication)"""
    try:
        db_education = Education(**education.model_dump())
        db.add(db_education)
        db.commit()
        db.refresh(db_education)
        return db_education
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create education record"
        )
```

---

## Fix 5: Fix File Validation

### Impact: MEDIUM
**Files:** projects.py, work_experience.py

### Before:
```python
def validate_file(file: UploadFile) -> bool:
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False

    # SILENTLY SKIPS IF size ATTRIBUTE MISSING
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        return False

    return True
```

### After:
```python
def validate_file(file: UploadFile, content: bytes) -> bool:
    """Validate file type and size"""
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False

    # ALWAYS check content size
    if len(content) > MAX_FILE_SIZE:
        return False

    return True
```

### Update Usage:

```python
# Before
if file and file.filename:
    if not validate_file(file):
        raise HTTPException(...)

# After
if file and file.filename:
    file_content = await file.read()
    if not validate_file(file, file_content):
        raise HTTPException(...)
    await file.seek(0)  # Reset for later reading
```

---

## Fix 6: Remove Duplicate Imports

### Impact: LOW
**File:** work_experience.py

### Remove Lines 21-22:
```python
# DELETE THESE DUPLICATE LINES:
import os
from pathlib import Path
```

(These are already imported at lines 4 and 7)

---

## Fix 7: Replace Print with Logging

### Impact: LOW
**File:** work_experience.py

### Add at top:
```python
import logging
logger = logging.getLogger(__name__)
```

### Replace:
```python
# Before
print(f"Warning: Could not delete old file {old_path}: {e}")

# After
logger.warning(f"Could not delete old file {old_path}: {e}")
```

---

## Fix 8: Update Module Exports

### Impact: MEDIUM
**File:** __init__.py

### Replace entire file with:
```python
from app.api.endpoints import (
    auth,
    personal_info,
    work_experience,
    education,
    certifications,
    languages,
    publications,
    github_projects,
    projects,
    import_data
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
    "import_data"
]
```

---

## Testing Checklist

After implementing fixes, verify:

- [ ] Unauthenticated requests to POST/PUT/DELETE return 401
- [ ] Authenticated requests with valid token succeed
- [ ] File upload >100MB is rejected before full read
- [ ] Database errors trigger rollback
- [ ] All endpoints use `.model_dump()`
- [ ] File validation works for both extension and size
- [ ] No duplicate imports remain
- [ ] Logging used instead of print
- [ ] All modules properly exported

---

## Estimated Effort

| Fix | Files Affected | Time Estimate |
|-----|----------------|---------------|
| Add Authentication | 7 files | 2 hours |
| Fix DoS Vulnerability | 1 file | 30 minutes |
| Replace .dict() | 6 files | 30 minutes |
| Add Transaction Rollback | 7 files | 1 hour |
| Fix File Validation | 2 files | 30 minutes |
| Remove Duplicate Imports | 1 file | 5 minutes |
| Replace Print with Logging | 1 file | 15 minutes |
| Update Module Exports | 1 file | 5 minutes |
| **Total** | | **5 hours** |

---

**End of Security Fix Guide**
