# Code Simplification Analysis - ResumeXLab

**Date**: 2026-02-27
**Status**: Analysis Complete
**Priority**: Medium

## Executive Summary

This document analyzes the ResumeXLab codebase for code simplification opportunities. The analysis identifies significant code duplication patterns across the frontend and backend, particularly in CRUD operations and bilingual field management. Implementing the recommended changes could reduce codebase size by approximately **30-40%** while improving maintainability.

**Key Findings:**
- **~3,000 lines of repetitive CRUD code** across frontend and backend
- **100% field duplication** for bilingual support (`_zh`/`_en` variants)
- **11 nearly identical API endpoint files** with only model/schema names changing
- **8 similar admin edit components** with duplicated form/dialog patterns

---

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [Detailed Findings](#detailed-findings)
3. [Refactoring Proposals](#refactoring-proposals)
4. [Implementation Priority](#implementation-priority)
5. [Risk Assessment](#risk-assessment)

---

## Critical Issues

### 1. Massive CRUD Duplication (High Impact)

**Location:** `frontend/src/stores/resume.js` (629 lines)

**Problem:**
The resume store contains 7 nearly identical CRUD function groups:
- `fetch{Entity}() / create{Entity}() / update{Entity}() / delete{Entity}()`
- Each follows the exact same pattern with only the API call and state variable changing

**Example Pattern (repeated 7 times):**

```javascript
// Pattern repeated for: WorkExperience, Projects, Education, Certifications,
// Languages, Publications, GithubProjects

async function fetchWorkExperiences() {
  loading.value = true
  error.value = null
  try {
    const response = await resumeAPI.getWorkExperiences()
    workExperiences.value = response.data
    return response.data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

async function createWorkExperience(data) {
  loading.value = true
  error.value = null
  try {
    const response = await resumeAPI.createWorkExperience(data)
    workExperiences.value.push(response.data)
    return response.data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}
// ... same pattern for update/delete
```

**Impact:** ~280 lines of duplicated logic

---

### 2. API Endpoint Duplication (High Impact)

**Location:** `backend/app/api/endpoints/*.py` (11 files)

**Problem:**
Each endpoint file repeats the same CRUD patterns:
- `GET /` (list all)
- `GET /{id}` (get one)
- `POST /` (create)
- `PUT /{id}` (update)
- `DELETE /{id}` (delete)

Only the model/schema imports and variable names change.

**Example Comparison:**

`work_experience.py` (lines 58-93):
```python
@router.get("/", response_model=List[WorkExperienceWithProjects])
async def get_work_experiences(db: Session = Depends(get_db)):
    experiences = db.query(WorkExperience)\
        .options(joinedload(WorkExperience.projects))\
        .order_by(WorkExperience.display_order)\
        .all()
    return experiences
```

`education.py` (nearly identical):
```python
@router.get("/", response_model=List[EducationInDB])
async def get_education(db: Session = Depends(get_db)):
    education = db.query(Education)\
        .order_by(Education.display_order)\
        .all()
    return education
```

**Impact:** ~1,374 lines across 11 files with ~60% duplication

---

### 3. Bilingual Field Explosion (High Impact)

**Location:**
- Backend: `app/models/*.py`, `app/schemas/*.py`
- Frontend: All admin edit components, stores, API calls

**Problem:**
Every data field has `_zh` and `_en` variants, doubling:
- Model columns (2x per field)
- Schema fields (2x per field)
- Form inputs (2x per field)
- API payload size (2x per field)

**Example - PersonalInfo Model (20 columns for 10 fields):**
```python
class PersonalInfo(Base):
    name_zh = Column(String(100))     # 1
    name_en = Column(String(100))     # 2
    address_zh = Column(Text)         # 3
    address_en = Column(Text)         # 4
    objective_zh = Column(Text)       # 5
    objective_en = Column(Text)       # 6
    personality_zh = Column(Text)     # 7
    personality_en = Column(Text)     # 8
    summary_zh = Column(Text)         # 9
    summary_en = Column(Text)         # 10
    # ... pattern continues
```

**Impact:**
- 2x database schema size
- 2x API payload size
- 2x form input fields in every admin component
- Increased cognitive load for developers

---

### 4. Admin Component Pattern Duplication (Medium Impact)

**Location:** `frontend/src/views/admin/*.vue` (8 files)

**Problem:**
Each admin edit component follows the same structure:
- Form data refs
- Dialog visibility management
- Loading states
- CRUD operation handlers
- File upload handling (where applicable)

**Files affected:**
- `PersonalInfoEdit.vue` (319 lines)
- `WorkExperienceEdit.vue` (725 lines)
- `ProjectEdit.vue`
- `EducationEdit.vue`
- `CertificationEdit.vue`
- `LanguageEdit.vue`
- `PublicationEdit.vue`
- `GithubProjectEdit.vue`

**Common pattern extracted:**
```javascript
// Repeated in each component:
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({...})

const handleAdd = () => { /* same pattern */ }
const handleEdit = (row) => { /* same pattern */ }
const handleSave = async () => { /* same pattern */ }
const handleDelete = async (id) => { /* same pattern */ }
```

**Impact:** ~3,868 lines with ~50% duplication

---

### 5. API Client Repetition (Low Impact)

**Location:** `frontend/src/api/resume.js` (192 lines)

**Problem:**
Each entity has 4-5 similar API methods:
```javascript
get{Entity}s()        // list all
get{Entity}(id)       // get one (sometimes omitted)
create{Entity}(data)  // create
update{Entity}(id, data)  // update
delete{Entity}(id)    // delete
```

**Impact:** ~130 lines of similar patterns

---

## Detailed Findings

### File-by-File Analysis

| File | Lines | Duplication | Potential Reduction |
|------|-------|-------------|---------------------|
| `frontend/src/stores/resume.js` | 629 | ~45% | ~280 lines |
| `backend/app/api/endpoints/*.py` | 1,374 | ~60% | ~820 lines |
| `frontend/src/views/admin/*.vue` | 3,868 | ~50% | ~1,900 lines |
| `frontend/src/api/resume.js` | 192 | ~40% | ~75 lines |
| `backend/app/schemas/*.py` | ~300 | ~30% | ~90 lines |
| `backend/app/models/*.py` | ~250 | ~20% | ~50 lines |
| **TOTAL** | **~6,613** | **~48%** | **~3,215 lines** |

---

## Refactoring Proposals

### Proposal 1: Generic CRUD Factory Pattern (Backend)

**Objective:** Create a reusable CRUD router builder to eliminate endpoint duplication.

**Implementation:**

```python
# backend/app/api/crud_base.py

from typing import Type, TypeVar, Generic, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from pydantic import BaseModel
from sqlalchemy import Model

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

def create_crud_router(
    model: Type[ModelType],
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    response_schema: Type[ResponseSchemaType],
    prefix: str,
    tags: List[str],
    get_current_user: Optional[callable] = None,
    order_by: Optional[str] = None,
) -> APIRouter:
    """Factory function to create a complete CRUD router"""

    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("/", response_model=List[response_schema])
    async def get_all(db: Session = Depends(get_db)):
        query = db.query(model)
        if order_by:
            query = query.order_by(getattr(model, order_by))
        return query.all()

    @router.get("/{item_id}", response_model=response_schema)
    async def get_one(item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        return item

    @router.post("/", response_model=response_schema, status_code=201)
    async def create(
        item_data: create_schema,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user) if get_current_user else None
    ):
        db_item = model(**item_data.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.put("/{item_id}", response_model=response_schema)
    async def update(
        item_id: int,
        item_data: update_schema,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user) if get_current_user else None
    ):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @router.delete("/{item_id}", status_code=204)
    async def delete(
        item_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user) if get_current_user else None
    ):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(item)
        db.commit()
        return None

    return router
```

**Usage Example:**

```python
# backend/app/api/endpoints/education.py (simplified)

from app.api.crud_base import create_crud_router
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationUpdate, EducationInDB
from app.api.endpoints.auth import get_current_user

router = create_crud_router(
    model=Education,
    create_schema=EducationCreate,
    update_schema=EducationUpdate,
    response_schema=EducationInDB,
    prefix="/education",
    tags=["education"],
    get_current_user=get_current_user,
    order_by="display_order"
)
```

**Benefits:**
- Reduces each endpoint file from ~120 lines to ~15 lines
- Single source of truth for CRUD logic
- Easier to add new features (e.g., filtering, pagination)
- Consistent error handling across all endpoints

**Trade-offs:**
- Less flexibility for custom endpoint behavior (can be mitigated with extension hooks)

---

### Proposal 2: Generic Store Factory (Frontend)

**Objective:** Create a reusable Pinia store factory for CRUD operations.

**Implementation:**

```javascript
// frontend/src/stores/crudFactory.js

import { ref } from 'vue'
import { defineStore } from 'pinia'

export function createCrudStore(entityName, apiMethods) {
  return defineStore(entityName, () => {
    const items = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchAll = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await apiMethods.getAll()
        items.value = response.data
        return response.data
      } catch (err) {
        error.value = err.message
        throw err
      } finally {
        loading.value = false
      }
    }

    const create = async (data) => {
      loading.value = true
      error.value = null
      try {
        const response = await apiMethods.create(data)
        items.value.push(response.data)
        return response.data
      } catch (err) {
        error.value = err.message
        throw err
      } finally {
        loading.value = false
      }
    }

    const update = async (id, data) => {
      loading.value = true
      error.value = null
      try {
        const response = await apiMethods.update(id, data)
        const index = items.value.findIndex(item => item.id === id)
        if (index !== -1) {
          items.value[index] = response.data
        }
        return response.data
      } catch (err) {
        error.value = err.message
        throw err
      } finally {
        loading.value = false
      }
    }

    const remove = async (id) => {
      loading.value = true
      error.value = null
      try {
        await apiMethods.delete(id)
        items.value = items.value.filter(item => item.id !== id)
      } catch (err) {
        error.value = err.message
        throw err
      } finally {
        loading.value = false
      }
    }

    return {
      items,
      loading,
      error,
      fetchAll,
      create,
      update,
      remove,
    }
  })
}
```

**Usage Example:**

```javascript
// frontend/src/stores/workExperience.js

import { createCrudStore } from './crudFactory'
import { resumeAPI } from '@/api/resume'

export const useWorkExperienceStore = createCrudStore('workExperience', {
  getAll: resumeAPI.getWorkExperiences,
  create: resumeAPI.createWorkExperience,
  update: resumeAPI.updateWorkExperience,
  delete: resumeAPI.deleteWorkExperience,
})
```

**Benefits:**
- Reduces store file from ~90 lines to ~10 lines per entity
- Consistent CRUD behavior across all entities
- Easier to test (single factory to test)
- Simplified error handling

---

### Proposal 3: JSON-Based Translation System

**Objective:** Replace `_zh`/`_en` column pairs with a single JSON column for translations.

**Database Schema Change:**

```python
# Before (10 columns for 5 fields):
class PersonalInfo(Base):
    name_zh = Column(String(100))
    name_en = Column(String(100))
    address_zh = Column(Text)
    address_en = Column(Text)
    # ... 6 more columns

# After (5 columns with embedded translations):
class PersonalInfo(Base):
    name = Column(JSON)  # {"zh": "...", "en": "..."}
    address = Column(JSON)
    objective = Column(JSON)
    personality = Column(JSON)
    summary = Column(JSON)
```

**Schema Change:**

```python
class PersonalInfoBase(BaseModel):
    name: Optional[Dict[str, str]] = None
    address: Optional[Dict[str, str]] = None
    objective: Optional[Dict[str, str]] = None
    personality: Optional[Dict[str, str]] = None
    summary: Optional[Dict[str, str]] = None
```

**Helper Functions:**

```python
# backend/app/core/translations.py

def get_translation(field: dict, lang: str) -> str:
    """Get translated value from a JSON field"""
    return field.get(lang) or field.get('en') or ''

def set_translation(value_zh: str, value_en: str) -> dict:
    """Create translation dict from zh/en values"""
    return {'zh': value_zh, 'en': value_en}
```

**Frontend Helper:**

```javascript
// frontend/src/composables/useTranslations.js

export function useTranslations() {
  const getLocale = () => localStorage.getItem('locale') || 'en'

  const t = (field) => {
    return field?.[getLocale()] || field?.en || ''
  }

  return { t }
}
```

**Template Usage:**

```vue
<!-- Before: -->
<el-input v-model="formData.name_zh" />
<el-input v-model="formData.name_en" />

<!-- After: -->
<el-input v-model="formData.name[getLocale()]" />
<!-- OR with helper: -->
<el-input :model-value="t(formData.name)" @input="formData.name[getLocale()] = $event" />
```

**Benefits:**
- 50% reduction in database columns
- 50% reduction in form fields
- Easier to add new languages (just add new key to JSON)
- Cleaner API responses

**Trade-offs:**
- Less database-level validation (can be mitigated with check constraints)
- Slightly more complex queries (can be mitigated with PostgreSQL JSON operators)
- Migration required for existing data

---

### Proposal 4: Generic Admin Edit Component

**Objective:** Create a reusable admin edit component with schema-driven rendering.

**Implementation:**

```vue
<!-- frontend/src/components/GenericCrudEdit.vue -->

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  // Store with CRUD methods
  store: {
    type: Object,
    required: true
  },
  // Field configuration
  fields: {
    type: Array,
    required: true
  },
  // Entity name for display
  entityName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['saved', 'deleted'])

const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const formData = ref({})

const fieldDefaults = () => {
  const defaults = {}
  props.fields.forEach(field => {
    defaults[field.key] = field.default || ''
  })
  return defaults
}

const handleAdd = () => {
  formData.value = fieldDefaults()
  isEditing.value = false
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formData.value = { ...row }
  isEditing.value = true
  dialogVisible.value = true
}

const handleSave = async () => {
  loading.value = true
  try {
    if (isEditing.value) {
      await props.store.update(formData.value.id, formData.value)
    } else {
      await props.store.create(formData.value)
    }
    ElMessage.success(`Saved successfully`)
    dialogVisible.value = false
    emit('saved')
  } catch (error) {
    ElMessage.error('Failed to save')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  await props.store.remove(id)
  ElMessage.success('Deleted successfully')
  emit('deleted')
}

defineExpose({ handleAdd, handleEdit, handleDelete })
</script>

<template>
  <div class="generic-crud-edit">
    <el-table :data="store.items" stripe>
      <el-table-column
        v-for="field in fields"
        :key="field.key"
        :prop="field.key"
        :label="field.label"
        :width="field.width"
      />
      <el-table-column label="Actions" width="150">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? `Edit ${entityName}` : `Add ${entityName}`"
      width="80%"
    >
      <el-form :model="formData" label-width="150px">
        <el-form-item
          v-for="field in fields"
          :key="field.key"
          :label="field.label"
        >
          <el-input
            v-if="field.type === 'text'"
            v-model="formData[field.key]"
            :type="field.inputType || 'text'"
          />
          <el-date-picker
            v-else-if="field.type === 'date'"
            v-model="formData[field.key]"
            type="date"
            value-format="YYYY-MM-DD"
          />
          <el-checkbox
            v-else-if="field.type === 'checkbox'"
            v-model="formData[field.key]"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>
```

**Usage Example:**

```vue
<!-- frontend/src/views/admin/LanguageEdit.vue (simplified) -->

<script setup>
import GenericCrudEdit from '@/components/GenericCrudEdit.vue'
import { useLanguageStore } from '@/stores/language'

const languageStore = useLanguageStore()

const fields = [
  { key: 'name_zh', label: 'Language (Chinese)', type: 'text', width: 200 },
  { key: 'name_en', label: 'Language (English)', type: 'text', width: 200 },
  { key: 'proficiency', label: 'Proficiency', type: 'text', width: 150 },
  { key: 'display_order', label: 'Order', type: 'number', width: 100 },
]

onMounted(() => {
  languageStore.fetchAll()
})
</script>

<template>
  <div class="language-edit">
    <h1>Manage Languages</h1>
    <GenericCrudEdit
      :store="languageStore"
      :fields="fields"
      entity-name="Language"
      @saved="languageStore.fetchAll()"
      @deleted="languageStore.fetchAll()"
    />
  </div>
</template>
```

**Benefits:**
- Reduces each admin component from ~300-700 lines to ~30 lines
- Consistent UI/UX across all admin pages
- Single source of truth for CRUD behavior
- Easier to add new features (e.g., bulk actions)

---

### Proposal 5: Dynamic API Client Generator

**Objective:** Generate API methods dynamically based on entity configuration.

**Implementation:**

```javascript
// frontend/src/api/createCrudApi.js

import apiClient from './axios'

export function createCrudApi(entityPath) {
  const path = entityPath

  return {
    getAll: () => apiClient.get(`/${path}/`),
    get: (id) => apiClient.get(`/${path}/${id}`),
    create: (data) => apiClient.post(`/${path}/`, data),
    update: (id, data) => apiClient.put(`/${path}/${id}`, data),
    delete: (id) => apiClient.delete(`/${path}/${id}`),
  }
}
```

**Usage:**

```javascript
// frontend/src/api/resume.js (simplified)

import { createCrudApi } from './createCrudApi'

export const resumeAPI = {
  workExperience: createCrudApi('work-experience'),
  projects: createCrudApi('projects'),
  education: createCrudApi('education'),
  certifications: createCrudApi('certifications'),
  languages: createCrudApi('languages'),
  publications: createCrudApi('publications'),
  githubProjects: createCrudApi('github-projects'),

  // Keep special endpoints separate
  personalInfo: {
    get: () => apiClient.get('/personal-info/'),
    update: (data) => apiClient.put('/personal-info/', data),
  },

  importPdf: (file, importType) => { /* ... */ },
  // ... other special endpoints
}
```

**Benefits:**
- Reduces API client from ~190 lines to ~40 lines
- Consistent API calling patterns
- Type-safety with TypeScript (if adopted)

---

## Implementation Priority

### Phase 1: High-Impact, Low-Risk Changes

1. **Generic API Client Generator** (Proposal 5)
   - Impact: ~150 lines reduction
   - Risk: Very low
   - Effort: 2-3 hours
   - Breakage: None (wrapper around existing calls)

2. **Backend CRUD Factory** (Proposal 1)
   - Impact: ~800 lines reduction
   - Risk: Low (can adopt incrementally)
   - Effort: 1-2 days
   - Breakage: Requires testing each migrated endpoint

### Phase 2: Medium-Impact Changes

3. **Frontend Store Factory** (Proposal 2)
   - Impact: ~280 lines reduction
   - Risk: Medium (affects all components)
   - Effort: 1 day
   - Breakage: Requires component updates

4. **Generic Admin Component** (Proposal 4)
   - Impact: ~1,900 lines reduction
   - Risk: Medium-High (major UI refactor)
   - Effort: 2-3 days
   - Breakage: Visual regressions possible

### Phase 3: High-Impact, High-Risk Changes

5. **JSON Translation System** (Proposal 3)
   - Impact: ~50% reduction in schema size
   - Risk: High (requires data migration)
   - Effort: 3-5 days
   - Breakage: Requires migration script, extensive testing

---

## Risk Assessment

| Proposal | Complexity | Risk Level | Testing Required |
|----------|------------|------------|------------------|
| API Client Generator | Low | Very Low | Unit tests |
| Backend CRUD Factory | Medium | Low | Integration tests |
| Frontend Store Factory | Medium | Medium | Component tests |
| Generic Admin Component | High | Medium-High | E2E tests |
| JSON Translation System | Very High | High | Full regression suite |

**Mitigation Strategies:**

1. **Incremental Adoption:** Migrate one entity at a time
2. **Feature Flags:** Use feature flags to enable new patterns gradually
3. **Comprehensive Testing:** Write tests before refactoring
4. **Backup Plans:** Keep old code accessible during transition
5. **Documentation:** Document new patterns thoroughly

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Implement API Client Generator** - Quickest win, low risk
2. **Create CRUD Factory Prototype** - Prove the pattern with one entity

### Short-Term (Next Sprint)

3. **Migrate 2-3 endpoints** to use CRUD factory
4. **Create Store Factory** and migrate corresponding stores

### Long-Term (Next Quarter)

5. **Design Generic Admin Component** with stakeholder input
6. **Plan Translation System Migration** with data team

### Not Recommended (At This Time)

- Complete rewrite of authentication system (works well as-is)
- Migration to TypeScript (would add complexity before simplification)
- Changing database engine (SQLite is sufficient for current scale)

---

## Conclusion

The ResumeXLab codebase has significant opportunities for simplification through the elimination of duplicated CRUD patterns. The proposed refactoring could reduce the codebase by **30-40%** while improving maintainability and reducing the likelihood of bugs.

**Key Success Factors:**
- Incremental implementation
- Comprehensive testing
- Team buy-in and training
- Clear documentation of new patterns

**Estimated Total Effort:** 8-12 development days
**Estimated Code Reduction:** ~3,200 lines (48% of analyzed code)
**Estimated Maintenance Cost Reduction:** 40-50%

---

## Appendix: Code Metrics

### Backend Lines of Code

| Directory/Module | Files | Lines | Notes |
|------------------|-------|-------|-------|
| `app/api/endpoints/` | 11 | 1,374 | CRUD endpoints |
| `app/models/` | 9 | ~250 | SQLAlchemy models |
| `app/schemas/` | 9 | ~300 | Pydantic schemas |
| `app/core/` | 2 | ~100 | Config, security |
| **Total Backend** | **31** | **~2,024** | |

### Frontend Lines of Code

| Directory/Module | Files | Lines | Notes |
|------------------|-------|-------|-------|
| `src/stores/` | 2 | 700 | Pinia stores |
| `src/views/admin/` | 8 | 3,868 | Admin components |
| `src/api/` | 3 | ~250 | API clients |
| `src/router/` | 1 | ~100 | Routes |
| **Total Frontend** | **14** | **~4,918** | |

### Duplication Analysis

```
Backend Duplication:
├── API Endpoints: ~60% (~820 lines)
├── Schemas: ~30% (~90 lines)
└── Models: ~20% (~50 lines)

Frontend Duplication:
├── Admin Components: ~50% (~1,900 lines)
├── Stores: ~45% (~280 lines)
└── API Clients: ~40% (~75 lines)

Total Potential Reduction: ~3,215 lines (48%)
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-27
**Next Review:** After implementation of Phase 1
