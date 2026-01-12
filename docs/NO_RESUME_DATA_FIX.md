# 解決 "No resume data available" 問題與檔案上傳大小限制

## 修改日期
2025-01-12

## 問題 1: 解決首次連線時顯示 "No resume data available"

### 問題分析
- 後端 API `/api/personal-info/` 在資料庫沒有資料時回傳 404 錯誤
- 前端使用 `.catch(() => null)` 忽略錯誤,導致 `personalInfo` 為 `null`
- 當 `loading` 完成且 `personalInfo` 為 `null` 時,顯示 "No resume data available"

### 解決方案
修改後端 API,當沒有個人資訊時回傳預設的空物件而不是 404 錯誤

#### 修改檔案
1. **backend/app/api/endpoints/personal_info.py:13-40**
   - 修改 `get_personal_info()` 函數
   - 當沒有資料時,回傳包含所有欄位的空物件

2. **backend/app/schemas/personal_info.py:32-41**
   - 將 `PersonalInfoInDB` 中的 `created_at` 和 `updated_at` 改為 Optional
   - 允許在沒有資料時回傳 `None`

### 技術細節
```python
# 當資料庫沒有個人資訊時,回傳空物件
if not info:
    return PersonalInfoInDB(
        id=0,
        name_zh="",
        name_en="",
        # ... 其他欄位為空字串
        created_at=None,
        updated_at=None
    )
```

---

## 問題 2: 設置檔案上傳大小限制為 100MB

### 修改檔案

#### 1. backend/app/api/endpoints/projects.py:23-28
```python
# 已修改於 2025-01-12，原因：將檔案大小限制從 10MB 提高到 100MB
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

#### 2. backend/app/api/endpoints/work_experience.py:21-30
```python
# 已修改於 2025-01-12，原因：將檔案大小限制從 10MB 提高到 100MB
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

#### 3. backend/app/api/endpoints/import_data.py:19-104
- 新增 `MAX_DB_FILE_SIZE = 100 * 1024 * 1024` 常數
- 在 `import_database()` 函數中新增檔案大小檢查
- 當檔案超過 100MB 時回傳 HTTP 413 錯誤

### 技術細節
```python
# 讀取檔案內容以檢查大小
file_content = await file.read()
file_size = len(file_content)

if file_size > MAX_DB_FILE_SIZE:
    raise HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail=f"File size exceeds maximum allowed size of {MAX_DB_FILE_SIZE / (1024 * 1024):.0f}MB"
    )
```

---

## 測試建議

### 測試問題 1 修正
1. 清空資料庫中的個人資訊
2. 重新啟動後端服務
3. 造訪前端履歷頁面
4. 確認不會顯示 "No resume data available" 訊息

### 測試問題 2 修正
1. 嘗試上傳小於 100MB 的檔案 → 應該成功
2. 嘗試上傳超過 100MB 的檔案 → 應該收到 HTTP 413 錯誤

---

## 注意事項

1. **資料庫初始化**: 不需要使用 hard code 的方式建立預設資料,而是透過 API 設計來處理空資料的情況

2. **檔案上傳大小**:
   - 專案附件: 100MB
   - 工作經歷附件: 100MB
   - 資料庫匯入: 100MB

3. **錯誤處理**: 當檔案超過大小限制時,回傳明確的錯誤訊息給使用者
