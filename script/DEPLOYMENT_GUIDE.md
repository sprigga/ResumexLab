# Docker Compose 部署指南

## 📋 概述

ResumeXLab 提供兩個 Docker Compose 配置檔案:
- **docker-compose.yml**: 生產環境配置 (GCP VM)
- **docker-compose.dev.yml**: 開發環境配置 (本地開發)

---

## 🚀 生產環境部署 (GCP VM)

### 端口配置
- **前端**: `58432:80` (訪問履歷網站)
- **後端**: `58433:8000` (API 服務)

### 部署步驟

```bash
# 1. 建置並啟動服務
docker-compose up -d --build

# 2. 查看容器狀態
docker-compose ps

# 3. 查看日誌
docker-compose logs -f

# 4. 停止服務
docker-compose down

# 5. 重新建置
docker-compose up -d --build
```

### 訪問地址
- **前台履歷**: `http://<GCP-VM-IP>:58432`
- **API 文件**: `http://<GCP-VM-IP>:58433/docs`
- **API 端點**: `http://<GCP-VM-IP>:58433/api`

### 防火牆設定 (GCP)

記得在 GCP Console 設定防火牆規則:
```bash
# 允許 TCP 58432 (前端)
# 允許 TCP 58433 (後端)
```

---

## 💻 開發環境部署 (本地)

### 端口配置
- **前端**: `8000:80` (非特權端口)
- **後端**: `8001:8000` (非特權端口)

### 部署步驟

```bash
# 1. 使用開發配置建置並啟動
docker-compose -f docker-compose.dev.yml up -d --build

# 2. 查看容器狀態
docker-compose -f docker-compose.dev.yml ps

# 3. 查看日誌
docker-compose -f docker-compose.dev.yml logs -f

# 4. 停止服務
docker-compose -f docker-compose.dev.yml down

# 5. 重新建置
docker-compose -f docker-compose.dev.yml up -d --build
```

### 訪問地址
- **前台履歷**: `http://localhost:8000`
- **API 文件**: `http://localhost:8001/docs`
- **API 端點**: `http://localhost:8001/api`

---

## 🔧 常用命令

### 查看日誌
```bash
# 所有服務日誌
docker-compose logs -f

# 特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 進入容器
```bash
# 進入後端容器
docker-compose exec backend /bin/bash

# 進入前端容器
docker-compose exec frontend /bin/sh
```

### 重啟服務
```bash
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart backend
```

### 清理系統
```bash
# 停止並移除容器
docker-compose down

# 停止並移除容器與 volumes
docker-compose down -v

# 移除未使用的映像
docker image prune -a
```

---

## 🐛 故障排除

### 端口衝突 (WSL2)

**問題**: `listen tcp 0.0.0.0:58433: bind: An attempt was made to access a socket in a way forbidden by its access permissions.`

**原因**: WSL2 動態端口保留問題

**解決**: 使用開發配置
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 容器無法啟動

```bash
# 查看詳細錯誤
docker-compose logs backend

# 重新建置映像
docker-compose build --no-cache
```

### 資料庫權限問題

```bash
# 修正資料庫目錄權限
sudo chown -R $USER:$USER ./backend/data

# 或在容器內修正
docker-compose exec backend chown -R app:app /app/data
```

---

## 📦 備份與還原

### 備份資料庫
```bash
# 備份 SQLite 資料庫
cp backend/data/resume.db backup/resume-$(date +%Y%m%d).db
```

### 還原資料庫
```bash
# 還原資料庫
cp backup/resume-20250112.db backend/data/resume.db

# 重啟後端服務
docker-compose restart backend
```

---

## 🔐 生產環境建議

1. **修改 SECRET_KEY**: 在 docker-compose.yml 中設定強密碼
2. **HTTPS 配置**: 使用 Nginx 反向代理 + Let's Encrypt
3. **定期備份**: 設定 cron job 自動備份資料庫
4. **監控**: 使用 Docker healthcheck 監控服務狀態
5. **日誌管理**: 設定日誌輪替避免磁碟滿載

---

## 📝 環境差異比較

| 項目 | 生產環境 | 開發環境 |
|------|---------|---------|
| 配置檔案 | docker-compose.yml | docker-compose.dev.yml |
| 前端端口 | 58432 | 8000 |
| 後端端口 | 58433 | 8001 |
| 熱重載 | 否 | 可選 (需註釋 volumes) |
| 資料庫 | SQLite (持久化) | SQLite (持久化) |
| CORS | 允許生產域名 | 允許 localhost |

---

**文件版本**: 1.0
**最後更新**: 2025-01-12
**作者**: Polo (林鴻全)
