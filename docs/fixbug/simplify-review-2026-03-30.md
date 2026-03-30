# Code Simplification Review — 2026-03-30

對 `/backend/` 和 `/frontend/` 最近幾個 commit（HEAD~5..HEAD）進行 code review，找出並修正以下問題。

---

## 審查範圍

涵蓋以下新增/修改的檔案：

| 檔案 | 異動類型 |
|------|----------|
| `backend/app/api/crud_base.py` | 新增 |
| `backend/app/api/endpoints/certifications.py` | 重構 |
| `backend/app/api/endpoints/education.py` | 重構 |
| `backend/app/api/endpoints/github_projects.py` | 重構 |
| `backend/app/api/endpoints/languages.py` | 重構 |
| `backend/app/api/endpoints/publications.py` | 重構 |
| `frontend/src/api/createCrudApi.js` | 新增 |
| `frontend/src/api/resume.js` | 重構 |
| `frontend/src/stores/crudFactory.js` | 新增 |
| `frontend/src/stores/resume.js` | 重構 |
| `frontend/src/composables/useCrudPanel.js` | 新增 |
| `frontend/src/views/admin/CertificationEdit.vue` | 重構 |
| `frontend/src/views/admin/EducationEdit.vue` | 重構 |
| `frontend/src/views/admin/GithubProjectEdit.vue` | 重構 |
| `frontend/src/views/admin/PublicationEdit.vue` | 重構 |

---

## 發現的問題與修正

### 問題 1 — Pydantic v2 deprecated `.dict()` 呼叫

**檔案：** `backend/app/api/crud_base.py` (line 52, 63)

**問題描述：**
專案使用 `pydantic==2.5.0`（見 `backend/requirements.txt`），但 `crud_base.py` 仍使用 Pydantic v1 的 `.dict()` API。在 Pydantic v2 中，`.dict()` 是相容性 shim，每次呼叫都會發出 `PydanticDeprecatedSince20` 警告，未來版本將移除。每次 POST 和 PUT 請求都會觸發此警告。

**修正前：**
```python
db_item = model(**item_data.dict())
# ...
for key, value in item_data.dict(exclude_unset=True).items():
```

**修正後：**
```python
db_item = model(**item_data.model_dump())
# ...
for key, value in item_data.model_dump(exclude_unset=True).items():
```

---

### 問題 2 — stringly-typed delete 回應訊息

**檔案：** `backend/app/api/crud_base.py` (line 76)

**問題描述：**
刪除成功的回應訊息透過字串操作從 `not_found_detail` 推導 entity 名稱：

```python
return {"message": f"{not_found_detail.replace(' not found', '')} deleted successfully"}
```

此做法有兩個問題：
1. 若 `not_found_detail` 格式不符合 `"X not found"` 模式，回應訊息會出錯
2. 實際上已造成問題：`"Education record not found"` → `"Education record deleted successfully"`（多餘的 "record"）

**修正方式：**
在 `create_crud_router` 新增獨立的 `entity_name` 參數，直接用於成功訊息，避免任何字串操作。

**修正前：**
```python
def create_crud_router(
    model,
    create_schema, update_schema, response_schema,
    not_found_detail: str = "Record not found",
    order_by_field: str = "display_order",
) -> APIRouter:
    # ...
    return {"message": f"{not_found_detail.replace(' not found', '')} deleted successfully"}
```

**修正後：**
```python
def create_crud_router(
    model,
    create_schema, update_schema, response_schema,
    not_found_detail: str = "Record not found",
    order_by_field: str = "display_order",
    entity_name: str = "Record",          # 新增參數
) -> APIRouter:
    # ...
    return {"message": f"{entity_name} deleted successfully"}
```

各 endpoint 同步新增 `entity_name` 參數：

| 檔案 | entity_name |
|------|-------------|
| `certifications.py` | `"Certification"` |
| `education.py` | `"Education record"` |
| `github_projects.py` | `"GitHub project"` |
| `languages.py` | `"Language"` |
| `publications.py` | `"Publication"` |

---

### 問題 3 — save/delete 後多餘的 `fetch()` 網路請求

**檔案：** `frontend/src/composables/useCrudPanel.js` (line 62, 84)

**問題描述：**
`handleSave` 和 `handleDelete` 在 CRUD 操作完成後都呼叫了 `await fetch()` 重新載入全部資料。

然而 `frontend/src/stores/crudFactory.js` 中的 store actions 已在每次操作後即時更新本地 state：
- `create`：直接 `items.value.push(response.data)`
- `update`：直接 `items.value[index] = response.data`
- `remove`：直接 `items.value = items.value.filter(...)`

因此每次 save/delete 都會多打一次 `GET /` 的 API，取回與 store 現有 state 完全相同的資料，是純粹的冗餘請求。

**修正前：**
```js
// handleSave
dialogVisible.value = false
await fetch()   // 多餘

// handleDelete
await del(id)
ElMessage.success('Deleted successfully')
await fetch()   // 多餘
```

**修正後：**
```js
// handleSave
dialogVisible.value = false
// 移除 await fetch()

// handleDelete
await del(id)
ElMessage.success('Deleted successfully')
// 移除 await fetch()
```

---

### 問題 4 — 誤導性的 style 區塊註解

**檔案：** 以下四個 Vue 元件的 `<style scoped>` 開頭：
- `frontend/src/views/admin/CertificationEdit.vue`
- `frontend/src/views/admin/EducationEdit.vue`
- `frontend/src/views/admin/GithubProjectEdit.vue`
- `frontend/src/views/admin/PublicationEdit.vue`

**問題描述：**
每個檔案 style 區塊最頂端都有如下三行註解：

```css
/* Applying global styles from style.css */
/* Created on 2025-11-30 */
/* Reason: Managing certification and language data in admin panel */
```

這些註解有兩個問題：
1. **說法不實**：樣式並非「來自 style.css」，而是各元件自行複製的局部樣式。`frontend/src/style.css` 已在 `:root` 定義相同屬性，這裡是重複定義。
2. **無資訊量**：日期與 Reason 是純粹的變更歷程紀錄，在 git log 中才有價值，放在 source code 裡只增加雜訊。

**修正：** 直接刪除這三行註解。

---

## 未修正項目（標記為已知問題）

以下為審查中發現但本次未修正的問題，留待後續處理：

### upload_utils 重複程式碼
`backend/app/api/endpoints/work_experience.py` 和 `projects.py` 各自定義了完全相同的 `ensure_upload_dir`、`validate_file`、`parse_date_string` 函式，以及 `UPLOAD_DIR`、`ALLOWED_EXTENSIONS`、`MAX_FILE_SIZE` 常數。這兩個檔案不在本次重構範圍（它們含有複雜的 file upload 邏輯），但值得後續提取到 `backend/app/api/upload_utils.py`。

### 共用 `loading` ref 的 race condition
`crudFactory.js` 中所有 entity actions 共用 store 裡同一個 `loading` ref。若多個 action 並發執行，最先完成的 action 會提早將 `loading` 設為 `false`。目前沒有任何 template 直接讀取 `resumeStore.loading`（已確認），所以不會產生可見 bug，但仍是潛在隱患。

### admin view 樣式重複
11 個 admin Vue 元件各自複製了幾乎相同的 `<style scoped>` 區塊（font-family、el-card、el-button、header 等）。理想做法是提取到 `AdminLayout.vue` 的 scoped style 或獨立的 `admin-common.css`，但範圍較大，留待獨立處理。
