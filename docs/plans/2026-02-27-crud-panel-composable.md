# useCrudPanel Composable Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extract the duplicated CRUD panel script logic from 4 admin components into a single `useCrudPanel()` composable, reducing each component's script section from ~100 lines to ~15 lines.

**Architecture:** Create `frontend/src/composables/useCrudPanel.js` that encapsulates dialog visibility, loading state, form data management, and CRUD handler functions. Each admin component calls the composable with its entity-specific config (defaultForm + store methods), then uses the returned refs/handlers directly in its existing template (templates are NOT modified).

**Tech Stack:** Vue 3 Composition API, Pinia store (already refactored), Element Plus (ElMessage, ElMessageBox)

---

### Task 1: Create the worktree

**Files:**
- No file changes — just setup

**Step 1: Create a git worktree**

```bash
git worktree add .worktrees/crud-panel-composable -b feature/crud-panel-composable
cd .worktrees/crud-panel-composable
```

**Step 2: Verify baseline tests pass**

```bash
cd backend && python -m pytest tests/ -q
```

Expected: `20 passed, 11 failed` (pre-existing failures in test_auth_required.py)

**Step 3: Commit (nothing to commit — this is setup only)**

---

### Task 2: Create the `useCrudPanel` composable

**Files:**
- Create: `frontend/src/composables/useCrudPanel.js`

**Step 1: Create the composables directory and file**

```bash
mkdir -p frontend/src/composables
```

**Step 2: Write `useCrudPanel.js`**

Create `frontend/src/composables/useCrudPanel.js` with this exact content:

```javascript
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

/**
 * Composable that encapsulates the repeated CRUD panel pattern:
 * dialog visibility, loading state, form data, and CRUD handlers.
 *
 * @param {object} config
 * @param {object} config.defaultForm   - Plain object with default empty form values
 * @param {Function} config.fetch       - () => Promise  — load all items
 * @param {Function} config.create      - (data) => Promise — create new item
 * @param {Function} config.update      - (id, data) => Promise — update item
 * @param {Function} config.delete      - (id) => Promise — delete item
 * @param {string}  config.entityName   - Human-readable name for messages (e.g. "Education")
 */
export function useCrudPanel({ defaultForm, fetch, create, update, delete: del, entityName }) {
  const loading = ref(false)
  const dialogVisible = ref(false)
  const isEditing = ref(false)
  const formData = ref({ ...defaultForm })

  const resetForm = () => {
    formData.value = { ...defaultForm }
  }

  const loadData = async () => {
    loading.value = true
    try {
      await fetch()
    } catch {
      ElMessage.error(`Failed to load ${entityName}`)
    } finally {
      loading.value = false
    }
  }

  const handleAdd = () => {
    resetForm()
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
        await update(formData.value.id, formData.value)
        ElMessage.success(`${entityName} updated successfully`)
      } else {
        await create(formData.value)
        ElMessage.success(`${entityName} created successfully`)
      }
      dialogVisible.value = false
      await fetch()
    } catch {
      ElMessage.error(`Failed to save ${entityName}`)
    } finally {
      loading.value = false
    }
  }

  const handleDelete = async (id) => {
    try {
      await ElMessageBox.confirm(
        `Are you sure to delete this ${entityName}?`,
        'Warning',
        { confirmButtonText: 'Confirm', cancelButtonText: 'Cancel', type: 'warning' }
      )
      loading.value = true
      await del(id)
      ElMessage.success('Deleted successfully')
      await fetch()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error(`Failed to delete ${entityName}`)
      }
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    dialogVisible,
    isEditing,
    formData,
    loadData,
    handleAdd,
    handleEdit,
    handleSave,
    handleDelete,
  }
}
```

**Step 3: Commit**

```bash
git add frontend/src/composables/useCrudPanel.js
git commit -m "feat: add useCrudPanel composable for CRUD panel logic"
```

---

### Task 3: Refactor `EducationEdit.vue`

**Files:**
- Modify: `frontend/src/views/admin/EducationEdit.vue` (script section only, lines 1–110)

**Step 1: Replace the entire `<script setup>` block**

The new script section (replace lines 1–110, keep `<template>` and `<style>` unchanged):

```vue
<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

const {
  loading, dialogVisible, isEditing, formData,
  loadData, handleAdd, handleEdit, handleSave, handleDelete,
} = useCrudPanel({
  defaultForm: {
    school_zh: '', school_en: '',
    degree_zh: '', degree_en: '',
    major_zh: '', major_en: '',
    start_date: '', end_date: '',
    description_zh: '', description_en: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchEducation(),
  create: (data) => resumeStore.createEducation(data),
  update: (id, data) => resumeStore.updateEducation(id, data),
  delete: (id) => resumeStore.deleteEducation(id),
  entityName: 'Education',
})

onMounted(loadData)
</script>
```

**Step 2: Verify template still references the same names**

The template uses: `loading`, `dialogVisible`, `isEditing`, `formData`, `handleAdd`, `handleEdit`, `handleSave`, `handleDelete` — all returned by the composable. Also uses `resumeStore.education` for table data (unchanged).

**Step 3: Verify the app compiles**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

Expected: Build completes without errors.

**Step 4: Commit**

```bash
git add frontend/src/views/admin/EducationEdit.vue
git commit -m "refactor: use useCrudPanel in EducationEdit"
```

---

### Task 4: Refactor `GithubProjectEdit.vue`

**Files:**
- Modify: `frontend/src/views/admin/GithubProjectEdit.vue` (script section only, lines 1–100)

**Step 1: Replace the entire `<script setup>` block**

```vue
<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

const {
  loading, dialogVisible, isEditing, formData,
  loadData, handleAdd, handleEdit, handleSave, handleDelete,
} = useCrudPanel({
  defaultForm: {
    name_zh: '', name_en: '',
    description_zh: '', description_en: '',
    url: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchGithubProjects(),
  create: (data) => resumeStore.createGithubProject(data),
  update: (id, data) => resumeStore.updateGithubProject(id, data),
  delete: (id) => resumeStore.deleteGithubProject(id),
  entityName: 'GitHub project',
})

onMounted(loadData)
</script>
```

**Step 2: Verify template still references the same names**

Template uses: `loading`, `dialogVisible`, `isEditing`, `formData`, `handleAdd`, `handleEdit`, `handleSave`, `handleDelete`, `resumeStore.githubProjects` (unchanged).

**Step 3: Verify build**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

**Step 4: Commit**

```bash
git add frontend/src/views/admin/GithubProjectEdit.vue
git commit -m "refactor: use useCrudPanel in GithubProjectEdit"
```

---

### Task 5: Refactor `PublicationEdit.vue`

**Files:**
- Modify: `frontend/src/views/admin/PublicationEdit.vue` (script section only, lines 1–100)

**Step 1: Replace the entire `<script setup>` block**

```vue
<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

const {
  loading, dialogVisible, isEditing, formData,
  loadData, handleAdd, handleEdit, handleSave, handleDelete,
} = useCrudPanel({
  defaultForm: {
    title: '', authors: '', publication: '',
    year: null, pages: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchPublications(),
  create: (data) => resumeStore.createPublication(data),
  update: (id, data) => resumeStore.updatePublication(id, data),
  delete: (id) => resumeStore.deletePublication(id),
  entityName: 'Publication',
})

onMounted(loadData)
</script>
```

**Step 2: Verify build**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

**Step 3: Commit**

```bash
git add frontend/src/views/admin/PublicationEdit.vue
git commit -m "refactor: use useCrudPanel in PublicationEdit"
```

---

### Task 6: Refactor `CertificationEdit.vue`

**Context:** This component manages two entities (Certifications + Languages) on one page. The composable is called twice — once per entity — with different variable names to avoid conflicts.

**Files:**
- Modify: `frontend/src/views/admin/CertificationEdit.vue` (script section only, lines 1–184)

**Step 1: Replace the entire `<script setup>` block**

```vue
<script setup>
import { onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import { useCrudPanel } from '@/composables/useCrudPanel'

const resumeStore = useResumeStore()

// Certifications panel
const {
  loading,
  dialogVisible: certDialogVisible,
  isEditing: isEditingCert,
  formData: certFormData,
  loadData: loadCerts,
  handleAdd: handleAddCert,
  handleEdit: handleEditCert,
  handleSave: handleSaveCert,
  handleDelete: handleDeleteCert,
} = useCrudPanel({
  defaultForm: {
    name_zh: '', name_en: '',
    issuer: '', issue_date: '',
    certificate_number: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchCertifications(),
  create: (data) => resumeStore.createCertification(data),
  update: (id, data) => resumeStore.updateCertification(id, data),
  delete: (id) => resumeStore.deleteCertification(id),
  entityName: 'Certification',
})

// Languages panel — second composable instance, rename all returned values
const {
  loading: langLoading,
  dialogVisible: langDialogVisible,
  isEditing: isEditingLang,
  formData: langFormData,
  loadData: loadLangs,
  handleAdd: handleAddLang,
  handleEdit: handleEditLang,
  handleSave: handleSaveLang,
  handleDelete: handleDeleteLang,
} = useCrudPanel({
  defaultForm: {
    language_zh: '', language_en: '',
    proficiency_zh: '', proficiency_en: '',
    test_name: '', score: '',
    display_order: 0,
  },
  fetch: () => resumeStore.fetchLanguages(),
  create: (data) => resumeStore.createLanguage(data),
  update: (id, data) => resumeStore.updateLanguage(id, data),
  delete: (id) => resumeStore.deleteLanguage(id),
  entityName: 'Language',
})

onMounted(async () => {
  await Promise.all([loadCerts(), loadLangs()])
})
</script>
```

**Step 2: Verify the template variable names match**

The original template uses these names — confirm they still resolve correctly:

| Template variable | Source |
|---|---|
| `loading` | cert composable's `loading` |
| `certDialogVisible` | cert composable's `dialogVisible` |
| `isEditingCert` | cert composable's `isEditing` |
| `certFormData` | cert composable's `formData` |
| `handleAddCert` / `handleEditCert` / `handleSaveCert` / `handleDeleteCert` | cert composable |
| `langDialogVisible` | lang composable's `dialogVisible` |
| `isEditingLang` | lang composable's `isEditing` |
| `langFormData` | lang composable's `formData` |
| `handleAddLang` / `handleEditLang` / `handleSaveLang` / `handleDeleteLang` | lang composable |
| `resumeStore.certifications` / `resumeStore.languages` | store (unchanged) |

Note: The `loading` ref from the cert composable covers both sections on this page (they share the same visual loading state). `langLoading` is declared but not used in the template — this is acceptable.

**Step 3: Verify build**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

**Step 4: Commit**

```bash
git add frontend/src/views/admin/CertificationEdit.vue
git commit -m "refactor: use useCrudPanel (x2) in CertificationEdit"
```

---

### Task 7: Final verification and push

**Step 1: Run backend tests (regression check)**

```bash
cd backend && python -m pytest tests/ -q
```

Expected: same as baseline — `20 passed, 11 failed`

**Step 2: Count lines saved**

```bash
wc -l frontend/src/views/admin/EducationEdit.vue \
        frontend/src/views/admin/GithubProjectEdit.vue \
        frontend/src/views/admin/PublicationEdit.vue \
        frontend/src/views/admin/CertificationEdit.vue \
        frontend/src/composables/useCrudPanel.js
```

**Step 3: Push and open PR**

```bash
git push -u origin feature/crud-panel-composable
gh pr create --title "refactor: extract useCrudPanel composable from admin components" \
  --base main --head feature/crud-panel-composable
```

---

## Summary

| File | Before | After (est.) | Reduction |
|------|--------|--------------|-----------|
| `EducationEdit.vue` | 299 lines | ~210 lines | ~30% |
| `GithubProjectEdit.vue` | 273 lines | ~195 lines | ~29% |
| `PublicationEdit.vue` | 237 lines | ~160 lines | ~33% |
| `CertificationEdit.vue` | 414 lines | ~310 lines | ~25% |
| `useCrudPanel.js` (new) | — | ~75 lines | (new) |
| **Net reduction** | **~1,223** | **~950** | **~-270 lines** |

Templates are 100% untouched — zero visual regression risk.
