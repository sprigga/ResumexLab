# Nginx 逾時設定說明 - 解決前端載入時間長的問題

## 修改日期
2025-01-12

## 問題描述
**問題 3: 前端載入時間很長**

### 常見症狀
- 頁面載入時間超過 5 秒
- API 請求逾時
- 顯示 504 Gateway Timeout 錯誤
- 檔案上傳時連線中斷

### 可能原因
1. **Nginx 逾時設定太短** ← 這裡可以解決
2. 後端 API 處理時間太長
3. 資料庫查詢效率低
4. 網路延遲過高

---

## ✅ 解決方案: 調整 Nginx 逾時設定

### 修改檔案
**frontend/nginx.conf**

### 修改內容

#### 1. API 請求逾時設定 (已修改)

```nginx
# API 請求代理到後端
location /api {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;

    # 已新增於 2025-01-12，原因：設定逾時時間以延長 API 回應等待時間
    # 解決問題 3: 前端載入時間很長的問題
    # 連線逾時: 60 秒 (預設 60 秒)
    proxy_connect_timeout 60s;
    # 傳送逾時: 60 秒 (預設 60 秒)
    proxy_send_timeout 60s;
    # 讀取逾時: 60 秒 (預設 60 秒,這是等待後端回應的時間)
    proxy_read_timeout 60s;
    # HTTP 版本逾時
    send_timeout 60s;

    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;

    # 已新增於 2025-01-12，原因：確保 API 回應不被快取
    add_header Cache-Control "no-cache, no-store, must-revalidate" always;
    add_header Pragma "no-cache" always;
    add_header Expires "0" always;
}
```

#### 2. 檔案上傳逾時設定 (已修改)

```nginx
# 上傳文件代理到後端
location ^~ /uploads/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;

    # 檔案上傳需要更長的逾時時間
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
    proxy_read_timeout 300s;
    send_timeout 300s;

    # 檔案上傳相關設定
    client_max_body_size 100M;
    client_body_buffer_size 10M;
    client_body_timeout 300s;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # 禁止快取上傳的檔案
    add_header Cache-Control "no-cache, no-store, must-revalidate" always;
    add_header Pragma "no-cache" always;
    add_header Expires "0" always;
}
```

---

## Nginx 逾時參數說明

### proxy_* 逾時參數 (針對後端連線)

| 參數 | 預設值 | 說明 | 建議值 |
|------|--------|------|--------|
| `proxy_connect_timeout` | 60s | 與後端建立連線的逾時時間 | 60s |
| `proxy_send_timeout` | 60s | 將請求傳送到後端的逾時時間 | 60s |
| `proxy_read_timeout` | 60s | **等待後端回應的逾時時間** | 60s-300s |
| `send_timeout` | 60s | 回應給客戶端的逾時時間 | 60s |

### client_* 逾時參數 (針對客戶端連線)

| 參數 | 預設值 | 說明 | 建議值 |
|------|--------|------|--------|
| `client_body_timeout` | 60s | 讀取客戶端請求主體的逾時時間 | 300s (上傳) |
| `client_header_timeout` | 60s | 讀取客戶端請求標頭的逾時時間 | 60s |

---

## 逾時設定建議

### 場景 1: 一般 API 請求 (讀取資料)

```nginx
location /api {
    proxy_read_timeout 60s;   # 60 秒足夠大多數 API
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
}
```

**說明:**
- 適用於大部分 CRUD 操作
- 如果 API 回應時間 < 5 秒,這個設定足夠
- 如果 API 回應時間 > 60 秒,應該優化後端效能

### 場景 2: 檔案上傳

```nginx
location /uploads/ {
    proxy_read_timeout 300s;  # 5 分鐘
    client_max_body_size 100M; # 100MB
    client_body_timeout 300s;
}
```

**說明:**
- 檔案上傳需要更長時間
- 100MB 檔案在 1Mbps 網速下需要約 13 分鐘
- 300 秒 (5 分鐘) 適用於大多數情況

### 場景 3: 長時間處理的 API

```nginx
location /api/export {
    proxy_read_timeout 600s;  # 10 分鐘
}
```

**說明:**
- 適用於資料匯出、報表生成等長時間操作
- 但應考慮使用非同步任務 + 輪詢的方式

---

## 測試與驗證

### 步驟 1: 測試 API 回應時間

```bash
# 執行逾時測試腳本
cd /home/ubuntu/ResumexLab/backend
./test_api_timeout.sh
```

**預期結果:**
- 所有 API 回應時間應該 < 5 秒
- 如果有 API > 10 秒,需要檢查後端效能

### 步驟 2: 檢查 Nginx 設定是否生效

```bash
# 如果使用 Docker
docker-compose exec frontend nginx -t

# 應該顯示:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 步驟 3: 重新載入 Nginx 設定

```bash
# 如果使用 Docker
docker-compose restart frontend

# 或
docker-compose exec frontend nginx -s reload
```

### 步驟 4: 測試前端載入時間

1. 清除瀏覽器快取
2. 開啟開發者工具 (F12)
3. 造問履歷頁面
4. 查看 Network 標籤:
   - 所有 API 請求應該在合理時間內完成
   - 不應該出現 504 Gateway Timeout

---

## 除錯流程

### 1. 確認是 Nginx 逾時還是後端慢

**Nginx 逾時的症狀:**
- 回傳 504 Gateway Timeout
- 錯誤日誌顯示 `upstream timed out`

**後端慢的症狀:**
- API 回應時間 > 5 秒
- 瀏覽器顯示 "Loading..." 很久

**檢查方法:**
```bash
# 直接測試後端 (不經過 Nginx)
curl -w "@curl-format.txt" http://localhost:8000/api/personal-info/

# 建立 curl-format.txt 檔案:
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer: %{time_pretransfer}\n
# time_redirect:    %{time_redirect}\n
# time_starttransfer: %{time_starttransfer}\n
# ----------\n
# time_total:       %{time_total}\n
```

### 2. 檢查 Nginx 錯誤日誌

```bash
# 如果使用 Docker
docker-compose logs frontend | grep timeout

# 或
docker-compose exec frontend cat /var/log/nginx/error.log | grep timeout
```

**常見錯誤訊息:**
- `upstream timed out (110: Connection timed out)`
- `client intended to send too large body`

### 3. 根據問題調整設定

**問題 A: 一般 API 逾時**
```nginx
# 增加 proxy_read_timeout
location /api {
    proxy_read_timeout 120s;  # 從 60s 增加到 120s
}
```

**問題 B: 檔案上傳逾時**
```nginx
location /uploads/ {
    proxy_read_timeout 600s;  # 增加到 10 分鐘
    client_max_body_size 200M; # 增加到 200MB
}
```

**問題 C: 後端真的太慢 (非 Nginx 問題)**
- 檢查資料庫查詢效率
- 增加資料庫索引
- 使用快取機制
- 考慮非同步處理

---

## 效能優化建議

### 1. 如果 API 回應時間 1-3 秒 (正常)

**不需要修改 Nginx 逾時**

但可以優化:
- 啟用 HTTP/2
- 使用 CDN
- 壓縮回應 (已有 gzip)

### 2. 如果 API 回應時間 3-10 秒 (偏慢)

**可以調整 Nginx 逾時到 120s**

但應該檢查:
- 資料庫查詢是否有 N+1 問題
- 是否有不必要的資料載入
- 網路延遲是否正常

### 3. 如果 API 回應時間 > 10 秒 (太慢)

**調整 Nginx 逾時到 300s (暫時方案)**

**必須優化後端:**
- 新增資料庫索引
- 使用快取 (Redis)
- 分頁載入資料
- 非同步處理長時間任務

---

## 常見問題 Q&A

### Q1: 為什麼設定 60s 還是逾時?

**可能原因:**
1. Nginx 設定沒有重新載入
2. 設定檔語法錯誤
3. 後端真的超過 60 秒

**解決方法:**
```bash
# 1. 檢查設定檔語法
docker-compose exec frontend nginx -t

# 2. 重新載入設定
docker-compose restart frontend

# 3. 如果後端真的很慢,增加到 300s
```

### Q2: 應該設定多長的逾時時間?

**建議:**
- 一般 API: 60s (已足夠)
- 檔案上傳: 300s
- 資料匯出: 600s

**不建議:**
- 設定過長 (如 3600s) 會導致資源浪費
- 如果超過 300s,應該改用非同步任務

### Q3: 除了 Nginx 逾時,還有什麼原因導致載入慢?

**其他原因:**
1. **前端效能:**
   - JavaScript 執行時間太長
   - DOM 元素過多
   - 沒有使用虛擬滾動

2. **後端效能:**
   - 資料庫查詢慢 (最常見)
   - 沒有使用索引
   - N+1 查詢問題

3. **網路問題:**
   - 延遲高
   - 頻寬不足
   - DNS 解析慢

---

## 測試檢查清單

- [ ] 修改 nginx.conf 設定檔
- [ ] 執行 `nginx -t` 檢查語法
- [ ] 重新載入 Nginx 設定
- [ ] 執行 `./test_api_timeout.sh` 測試回應時間
- [ ] 清除瀏覽器快取
- [ ] 測試前端載入時間
- [ ] 檢查 Network 標籤確認沒有 504 錯誤
- [ ] 如果還是慢,檢查後端效能

---

## 總結

### ✅ Nginx 可以解決的問題
1. API 逾時 (504 Gateway Timeout)
2. 檔案上傳連線中斷
3. 快取造成的資料陳舊

### ❌ Nginx 不能解決的問題
1. 後端 API 真的很慢 (需要優化程式碼)
2. 資料庫查詢效率低 (需要優化 SQL)
3. 前端渲染慢 (需要優化前端程式碼)

### 🎯 最佳實踐
1. 先設定合理的逾時時間 (60-300s)
2. 測試 API 回應時間
3. 如果還是慢,找出真正的瓶頸並優化
4. 不要無限增加逾時時間,這樣會掩蓋真正的問題

**記住: 逾時設定是暫時的解決方案,真正的解決方案是優化後端效能!**
