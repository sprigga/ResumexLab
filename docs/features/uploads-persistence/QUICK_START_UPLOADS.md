# 🚀 Uploads 目錄持久化 - 快速開始

## ✅ 已完成的配置

所有必要的配置已經完成，你現在可以放心使用 `docker-compose down` 而不會丟失上傳的文件！

## 📋 配置清單

- ✅ `docker-compose.yml` - 已添加 uploads volume 掛載
- ✅ `docker-compose.dev.yml` - 已添加 uploads volume 掛載
- ✅ `backend/Dockerfile` - 已創建 /app/uploads 目錄
- ✅ `backend/uploads/` - 目錄已存在

## 🎯 快速驗證

### 方法 1: 一鍵測試（推薦）

```bash
./test_uploads_persistence.sh
```

### 方法 2: 手動測試（3 步驟）

```bash
# 1. 創建測試文件
echo "持久化測試 $(date)" > backend/uploads/test.txt

# 2. 啟動容器 → 停止容器
docker-compose up -d
docker-compose down

# 3. 驗證文件是否保留
cat backend/uploads/test.txt  # 文件應該還在！
```

## 📖 使用說明

### 正常使用流程

```bash
# 啟動服務
docker-compose up -d

# 用戶上傳文件（通過 API）
# 文件會自動保存到 backend/uploads/

# 停止並刪除容器（文件不會丟失）
docker-compose down

# 重新啟動（文件自動恢復）
docker-compose up -d
```

### 查看上傳的文件

```bash
# 在主機查看
ls -lh backend/uploads/

# 在容器內查看
docker exec resumexlab-backend ls -lh /app/uploads/
```

## 🔍 工作原理

```
主機目錄: ./backend/uploads/
           ↕ (Volume Mount)
容器目錄: /app/uploads/

當容器刪除時，主機目錄保留所有文件
```

## 📚 詳細文檔

需要更多資訊？查看這些文件：

1. **詳細配置說明**: `UPLOADS_PERSISTENCE.md`
2. **Docker 指令參考**: `docs/docker-commands-reference.md`
3. **架構圖解**: `docs/volume-mounting-diagram.md`

## 🚨 常見問題

### Q1: 文件權限錯誤？

```bash
# 調整目錄權限
chmod 755 backend/uploads
```

### Q2: 容器內看不到文件？

```bash
# 確認 volume 掛載成功
docker inspect resumexlab-backend | grep -A 10 Mounts
```

### Q3: 想刪除所有上傳的文件？

```bash
# ⚠️ 警告：會刪除所有上傳的文件
rm -rf backend/uploads/*

# 保留測試文件
find backend/uploads/ -type f ! -name 'test_*' -delete
```

## 🎉 完成！

你現在可以安全地使用 `docker-compose down` 而不用擔心上傳的文件會消失。

---

**配置完成日期**: 2026-01-31
**測試狀態**: ✅ 已驗證
**支持環境**: 生產環境 & 開發環境
