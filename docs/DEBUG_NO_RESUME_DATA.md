# 解決 "No resume data available" 問題 - 完整除錯指南

## 問題描述
首次連線網頁時,會顯示 "No resume data available" 訊息

## 解決方案總覽

### ❌ 不推薦: 使用 Nginx 設定

**為什麼不推薦:**
- Nginx 只是反向代理,無法修改 API 回應內容
- Nginx 無法解決後端 API 回傳 404 錯誤的根本問題
- 這不是正確的解決層級

### ✅ 推薦: 修改後端 API 設計 (已完成)

**解決思路:**
當資料庫沒有資料時,API 應該回傳:
- 列表端點: 空陣列 `[]` (已經是這樣設計)
- 單一資源端點: 空物件而不是 404 錯誤 (需要修改)

---

## 已完成的修改

### 1. 修改 personal_info API
**檔案:** `backend/app/api/endpoints/personal_info.py:13-40`

```python
@router.get("/", response_model=PersonalInfoInDB)
async def get_personal_info(db: Session = Depends(get_db)):
    """Get personal information (public endpoint)

    已修改於 2025-01-12，原因：當沒有個人資訊時，回傳預設空物件而不是 404 錯誤
    這樣可以避免前端顯示 "No resume data available" 訊息
    """
    info = db.query(PersonalInfo).first()
    if not info:
        # 回傳預設的空物件結構，讓前端可以正常渲染
        return PersonalInfoInDB(
            id=0,
            name_zh="",
            name_en="",
            phone="",
            email="",
            address_zh="",
            address_en="",
            objective_zh="",
            objective_en="",
            personality_zh="",
            personality_en="",
            summary_zh="",
            summary_en="",
            created_at=None,
            updated_at=None
        )
    return info
```

### 2. 修改 Schema 允許 None 值
**檔案:** `backend/app/schemas/personal_info.py:32-41`

```python
class PersonalInfoInDB(PersonalInfoBase):
    """Personal info database schema"""
    id: int
    # 已修改於 2025-01-12，原因：允許 created_at 和 updated_at 為 None
    # 這樣當資料庫沒有個人資訊時，可以回傳空物件而不是 404 錯誤
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

---

## 除錯步驟

### 步驟 1: 測試後端 API

```bash
# 進入後端目錄
cd /home/ubuntu/ResumexLab/backend

# 啟動後端服務
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 在另一個終端執行測試腳本
./test_api.sh
```

### 步驟 2: 檢查 API 回應

**預期結果:**
```bash
# GET /api/personal-info/ 應該回傳 200,內容為:
{
  "id": 0,
  "name_zh": "",
  "name_en": "",
  "phone": "",
  "email": "",
  ...
}

# 其他列表端點應該回傳 200,內容為 []
```

**如果有問題:**
1. 檢查後端日誌: `uv run uvicorn app.main:app --log-level debug`
2. 檢查資料庫狀態: `sqlite3 backend/data/resume.db "SELECT * FROM personal_info;"`
3. 檢查 API 錯誤回應: `curl -v http://localhost:8000/api/personal-info/`

### 步驟 3: 測試前端行為

1. 清空瀏覽器快取
2. 開啟瀏覽器開發者工具 (F12)
3. 造訪履歷頁面
4. 檢查 Network 標籤:
   - 所有 API 請求應該回傳 200
   - `/api/personal-info/` 應該回傳空物件
   - 其他 API 應該回傳空陣列 `[]`

5. 檢查 Console 標籤:
   - 不應該有錯誤訊息
   - 不應該顯示 "No resume data available"

---

## 常見問題排查

### 問題 1: 仍然顯示 "No resume data available"

**可能原因:**
- 後端修改未生效 → 需要重啟後端服務
- 前端快取未清除 → 清除瀏覽器快取或使用無痕模式
- API 回應格式錯誤 → 檢查 API 回應內容

**解決方法:**
```bash
# 1. 重啟後端
cd /home/ubuntu/ResumexLab/backend
# Ctrl+C 停止舊的程序
uv run uvicorn app.main:app --reload

# 2. 清除前端快取並重新建置
cd /home/ubuntu/ResumexLab/frontend
rm -rf node_modules/.vite
npm run build

# 3. 如果使用 Docker
docker-compose down
docker-compose up --build
```

### 問題 2: API 回傳 500 錯誤

**檢查後端日誌:**
```bash
cd /home/ubuntu/ResumexLab/backend
uv run uvicorn app.main:app --log-level debug
```

**可能原因:**
- Schema 定義錯誤
- 資料庫連線問題
- 欄位類型不匹配

### 問題 3: 前端載入時間很長

**檢查:**
- 網路延遲: 檢查 API 回應時間
- Nginx 設定: 確認 proxy_pass 正確
- 後端效能: 檢查資料庫查詢效率

---

## 前端優化建議 (可選)

如果想要更好的使用者體驗,可以修改前端:

### 選項 1: 顯示載入中訊息

```vue
<!-- 在 ResumeView.vue -->
<el-card v-loading="loading" element-loading-text="載入中...">
  <!-- 履歷內容 -->
</el-card>

<!-- 不要顯示 empty state -->
<el-empty v-if="!loading && !personalInfo" description="No resume data available" />
```

### 選項 2: 顯示空的履歷模板

```vue
<!-- 當沒有資料時,顯示空的履歷模板 -->
<template v-if="!loading && personalInfo && personalInfo.id === 0">
  <el-alert
    type="info"
    title="歡迎使用履歷管理系統"
    description="請先在後台新增您的履歷資料"
    :closable="false"
  />
</template>
```

---

## Nginx 相關設定 (僅供參考)

雖然 Nginx 不能直接解決這個問題,但可以優化快取設定:

### frontend/nginx.conf 優化建議

```nginx
# API 請求不快取
location /api {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # 已新增於 2025-01-12，原因：確保 API 回應不被快取
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    add_header Pragma "no-cache";
    add_header Expires "0";
}
```

---

## 測試檢查清單

- [ ] 後端 API 修改已完成
- [ ] 執行測試腳本 `./test_api.sh` 確認所有端點回傳 200
- [ ] `/api/personal-info/` 回傳空物件而不是 404
- [ ] 其他列表端點回傳空陣列 `[]`
- [ ] 前端清除快取後重新載入
- [ ] 瀏覽器開發者工具檢查 Network 標籤
- [ ] 確認不再顯示 "No resume data available"
- [ ] 測試新增履歷資料功能正常

---

## 總結

1. **最佳解決方案**: 修改後端 API,回傳空物件而不是 404 錯誤
2. **Nginx 不是正確的解決層級**: 無法修改 API 回應內容
3. **除錯重點**: 使用測試腳本檢查 API 回應,確認所有端點都回傳 200
4. **前端優化**: 可以加上更友善的空狀態提示

如果問題仍然存在,請執行測試腳本並檢查後端日誌。
