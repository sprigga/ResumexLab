# ResumeXLab - 個人履歷管理系統

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/Vue-3.5-brightgreen.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-red.svg)](https://fastapi.tiangolo.com/)

一個功能完整的全端履歷管理系統，採用 Vue 3 前端與 FastAPI 後端架構，支援中英文雙語切換、進階履歷管理功能，並提供 Docker 容器化部署。

A comprehensive full-stack resume management system with Vue 3 frontend and FastAPI backend, featuring bilingual support (Traditional Chinese/English), advanced resume management, and Docker containerization.

---

## 📋 專案概述 (Project Overview)

### 功能特色 (Key Features)

**前台功能 (Public Features)**
- ✅ 專業履歷展示頁面 — 響應式設計，支援各種裝置
- ✅ 中英文雙語切換 — 即時切換語言，LocalStorage 記憶偏好
- ✅ 優雅的使用者體驗 — 載入動畫、專案折疊/展開（預設顯示前 5 筆）
- ✅ HTML 富文本展示 — 支援 Quill 編輯器輸出（DOMPurify XSS 清理）

**後台管理 (Admin Features)**
- 🔐 JWT 身份驗證 — Token 24 小時有效，OAuth2 Bearer 方式傳遞
- 📊 Dashboard 儀表板 — 直觀的管理介面
- ✏️ 完整的 CRUD 功能 — 管理所有履歷資料
  - 個人資訊（姓名、聯絡方式、個人摘要、個性描述）
  - 工作經歷（公司、職位、時間、附件上傳）
  - 專案經驗（技術堆疊、工具、環境、子細節、附件）
  - 教育背景（學校、學位、科系）
  - 證照管理（名稱、發證機關、編號）
  - 語言能力（語言、熟練度、測驗成績）
  - 學術著作（論文、出版品）
  - GitHub 專案展示
- 💾 資料庫匯入 / 匯出 — SQLite 全庫備份與還原（HTTP API）

**技術優勢 (Technical Highlights)**
- 🐳 Docker 容器化 — 一鍵部署，隔離環境
- 🔄 資料庫遷移 — Alembic 冪等遷移腳本（IF NOT EXISTS 防衝突）
- 📝 自動 API 文件 — Swagger UI (`/docs`) / ReDoc (`/redoc`)
- 🛡️ 安全性 — JWT、bcrypt、CORS、XSS 防護、管理員憑證環境變數化
- 📁 檔案附件系統 — 支援 PDF/Word/圖片上傳（100MB 上限）

---

## 🏗️ 系統架構 (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    ResumeXLab System                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue 3)              │  Backend (FastAPI)         │
│                                │                            │
│  ┌─────────────────────────┐   │   ┌─────────────────────┐  │
│  │ Vue Components          │   │   │ API Endpoints       │  │
│  │ ─────────────────────   │   │   │ ─────────────────   │  │
│  │ - ResumeView            │   │   │ - /api/auth         │  │
│  │ - AdminLayout           │   │   │ - /api/personal-info│  │
│  │ - LoginView             │   │   │ - /api/work-exp     │  │
│  │ - DashboardView         │   │   │ - /api/projects     │  │
│  │ - PersonalInfoEdit      │   │   │ - /api/education    │  │
│  │ - WorkExperienceEdit    │   │   │ - /api/certifications│ │
│  │ - ProjectEdit           │   │   │ - /api/languages    │  │
│  │ - EducationEdit         │   │   │ - /api/publications │  │
│  │ - CertificationEdit     │   │   │ - /api/github-projects│ │
│  │ - PublicationEdit       │   │   │ - /api/import       │  │
│  │ - GithubProjectEdit     │   │   └─────────────────────┘  │
│  │ - ImportDataView        │   │                            │
│  └─────────────────────────┘   │   Database: SQLite         │
│                                │   Auth: JWT (HS256)        │
│  State: Pinia                  │   ORM: SQLAlchemy 2.0      │
│  UI: Element Plus              │   Validation: Pydantic 2   │
│  i18n: Vue I18n                │   Migration: Alembic       │
│  Router: Vue Router            │   Password: bcrypt         │
│  HTTP: Axios                   │                            │
└─────────────────────────────────────────────────────────────┘
│                            Docker                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Frontend (Nginx)│  │Backend (Uvicorn)│  │  Database    │ │
│  │  Port: 58432    │  │  Port: 58433    │  │  (SQLite)    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 資料流程圖 (Data Flow)

```
┌──────────────┐      HTTP/HTTPS       ┌──────────────┐
│   Browser    │ ◄──────────────────► │   Nginx      │
│              │                       │  (Frontend)  │
└──────────────┘                       └──────┬───────┘
                                              │
                                     Vue.js SPA (Vite Build)
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  Axios (proxy)   │
                                     │  /api/* → Backend│
                                     └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  FastAPI Server  │
                                     │  (Uvicorn)       │
                                     └────────┬─────────┘
                                              │
                        ┌─────────────────────┼─────────────┐
                        ▼                     ▼             ▼
              ┌──────────────┐      ┌──────────────┐  ┌──────────────┐
              │   SQLite DB  │      │   Alembic    │  │   uploads/   │
              │ data/resume  │      │  Migrations  │  │ (靜態附件)   │
              └──────────────┘      └──────────────┘  └──────────────┘
```

---

## 🛠️ 技術堆疊 (Tech Stack)

### Frontend（前端）

| 技術 | 版本 | 說明 |
|------|------|------|
| **Vue 3** | 3.5.24 | 前端框架 (Composition API) |
| **Pinia** | 3.0.4 | 狀態管理 |
| **Vue Router** | 4.6.3 | 路由管理 |
| **Element Plus** | 2.11.9 | UI 元件庫 |
| **Vue I18n** | 9.14.5 | 多語言支援 (zh-TW / en-US) |
| **Axios** | 1.13.2 | HTTP 客戶端（含自動重試） |
| **Vite** | 7.2.4 | 建置工具 |
| **DOMPurify** | 3.3.1 | XSS 防護，HTML 清理 |
| **@vueup/vue-quill** | 1.2.0 | 富文本編輯器 |
| **Nginx** | latest | 生產環境 Web 伺服器 |

### Backend（後端）

| 技術 | 版本 | 說明 |
|------|------|------|
| **FastAPI** | 0.104.1 | Web 框架 |
| **SQLAlchemy** | 2.0.23 | ORM |
| **SQLite** | 3.x | 資料庫 |
| **Alembic** | 1.12.1 | 資料庫遷移 |
| **python-jose[cryptography]** | 3.3.0 | JWT 身份驗證 |
| **passlib[bcrypt]** | 1.7.4 | 密碼加密 |
| **bcrypt** | 4.3.0 | bcrypt 實作 |
| **Pydantic** | 2.5.0 | 資料驗證 |
| **pydantic-settings** | 2.1.0 | 環境變數配置 |
| **python-multipart** | 0.0.6 | 檔案上傳支援 |
| **Uvicorn** | 0.24.0 | ASGI 伺服器 |
| **PyPDF2** | 3.0.1 | PDF 處理 |
| **email-validator** | 2.1.1 | Email 格式驗證 |
| **python-dateutil** | 2.8.2 | 日期解析 |
| **Python** | 3.10+ | 程式語言 |

### DevOps（部署與開發）

| 工具 | 說明 |
|------|------|
| **Docker** | 容器化技術 |
| **Docker Compose** | 多容器編排（生產 / 開發兩套配置） |
| **Git** | 版本控制 |
| **uv** | Python 套件管理器 |
| **npm** | Node.js 套件管理器 |

---

## 📁 專案結構 (Project Structure)

```
resumexlab/
├── backend/                          # FastAPI 後端應用
│   ├── alembic/                      # 資料庫遷移工具
│   │   ├── versions/
│   │   │   ├── d711f173f9e3_初始化資料庫表.py     # 初始 Schema（冪等）
│   │   │   └── ce10aaa23747_添加附件欄位.py       # 新增附件欄位
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── auth.py               # 登入 / 登出 / Token 驗證
│   │   │   ├── personal_info.py      # 個人資訊 CRUD
│   │   │   ├── work_experience.py    # 工作經歷 CRUD + 附件上傳
│   │   │   ├── projects.py           # 專案 CRUD + 附件管理
│   │   │   ├── education.py          # 教育背景 CRUD
│   │   │   ├── certifications.py     # 證照 CRUD
│   │   │   ├── languages.py          # 語言能力 CRUD
│   │   │   ├── publications.py       # 學術著作 CRUD
│   │   │   ├── github_projects.py    # GitHub 專案 CRUD
│   │   │   └── import_data.py        # 資料庫匯入 / 匯出
│   │   ├── core/
│   │   │   ├── config.py             # 設定（含 ADMIN_USERNAME/PASSWORD 必填）
│   │   │   └── security.py           # JWT 生成 / 驗證 / bcrypt
│   │   ├── crud/                     # CRUD 操作層
│   │   ├── db/
│   │   │   ├── base.py               # SQLAlchemy engine / session
│   │   │   └── init_db.py            # 初始化管理員帳號
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── personal_info.py
│   │   │   ├── work_experience.py
│   │   │   ├── project.py            # Project + ProjectDetail + ProjectAttachment
│   │   │   ├── education.py
│   │   │   ├── certification.py
│   │   │   └── publication.py        # Publication + GithubProject
│   │   ├── schemas/                  # Pydantic 驗證模型
│   │   │   ├── user.py
│   │   │   ├── personal_info.py
│   │   │   ├── work_experience.py
│   │   │   ├── project.py
│   │   │   ├── education.py
│   │   │   ├── certification.py
│   │   │   ├── language.py
│   │   │   ├── publication.py
│   │   │   └── github_project.py
│   │   └── main.py                   # FastAPI 應用入口
│   ├── tests/
│   │   ├── test_init_db.py           # 管理員帳號初始化測試
│   │   ├── test_auth_required.py     # 認證保護測試
│   │   ├── test_file_upload_dos.py   # 檔案上傳 DoS 防禦測試
│   │   └── test_admin_credentials_config.py
│   ├── data/                         # SQLite 資料庫目錄
│   │   └── resume.db
│   ├── uploads/                      # 上傳附件目錄
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── run.py
│   └── .env.example
│
├── frontend/                         # Vue 3 前端應用
│   ├── src/
│   │   ├── api/
│   │   │   ├── axios.js              # Axios 實例（JWT 攔截、自動重試）
│   │   │   ├── auth.js               # 認證 API
│   │   │   └── resume.js             # 履歷資料 API
│   │   ├── assets/css/               # 全域樣式
│   │   ├── components/
│   │   │   ├── APITestComponent.vue  # API 測試工具（開發用）
│   │   │   └── HelloWorld.vue
│   │   ├── locales/
│   │   │   ├── zh-TW.js              # 繁體中文翻譯
│   │   │   ├── en-US.js              # 英文翻譯
│   │   │   └── index.js              # Vue i18n 配置
│   │   ├── router/
│   │   │   └── index.js              # 路由定義（含 Navigation Guard）
│   │   ├── stores/
│   │   │   ├── auth.js               # 認證狀態（Pinia）
│   │   │   └── resume.js             # 履歷資料狀態（Pinia）
│   │   ├── views/
│   │   │   ├── ResumeView.vue        # 公開履歷展示
│   │   │   └── admin/
│   │   │       ├── AdminLayout.vue
│   │   │       ├── LoginView.vue
│   │   │       ├── DashboardView.vue
│   │   │       ├── PersonalInfoEdit.vue
│   │   │       ├── WorkExperienceEdit.vue
│   │   │       ├── ProjectEdit.vue
│   │   │       ├── EducationEdit.vue
│   │   │       ├── CertificationEdit.vue
│   │   │       ├── LanguageEdit.vue
│   │   │       ├── PublicationEdit.vue
│   │   │       ├── GithubProjectEdit.vue
│   │   │       └── ImportDataView.vue
│   │   └── App.vue
│   ├── public/media/                 # 靜態媒體資源
│   ├── package.json
│   ├── vite.config.js                # Vite 配置（含 API proxy）
│   ├── Dockerfile
│   └── nginx.conf
│
├── script/                           # 工具腳本
│   ├── create_database.py            # 資料庫初始化
│   ├── check_users.py
│   ├── check_db_users.py
│   ├── import_resume_data.py
│   ├── migrate_project_details.py
│   ├── test_upload.sh
│   ├── docker-build-optimized.sh
│   ├── rebuild_and_restart_docker.sh
│   └── DEPLOYMENT_GUIDE.md
│
├── docs/                             # 文件目錄
│   ├── DOCKER_COMPOSE_USAGE.md
│   ├── code_review/
│   └── plans/
│
├── docker-compose.yml                # 生產環境 Docker 配置
├── docker-compose.dev.yml            # 開發環境 Docker 配置
├── .gitignore
├── README.md
├── CLAUDE.md
└── .env.example
```

---

## 🚀 快速開始 (Quick Start)

### 前置需求 (Prerequisites)

- Python 3.10+
- Node.js 20+
- npm
- Docker & Docker Compose（可選，推薦）
- uv（Python 套件管理器）

---

### 方法一：Docker 部署（推薦）

#### 生產環境

```bash
# 1. 克隆專案
git clone <repository-url>
cd resumexlab

# 2. 設定環境變數
cp backend/.env.example backend/.env
# 編輯 backend/.env，填入必填項目：
#   SECRET_KEY  → 執行 python -c "import secrets; print(secrets.token_urlsafe(32))" 生成
#   ADMIN_USERNAME → 管理員帳號（必填，無預設值）
#   ADMIN_PASSWORD → 管理員密碼（必填，無預設值）

# 3. 啟動生產環境
docker-compose up -d --build

# 4. 訪問應用
# 前端:    http://<YOUR-IP>:58432
# 後端:    http://<YOUR-IP>:58433
# API 文件: http://<YOUR-IP>:58433/docs
```

#### 開發環境

```bash
# 啟動開發環境
docker-compose -f docker-compose.dev.yml up -d

# 前端: http://localhost:8000
# 後端: http://localhost:8001
# API 文件: http://localhost:8001/docs
```

詳細部署說明請參考 [`docs/DOCKER_COMPOSE_USAGE.md`](./docs/DOCKER_COMPOSE_USAGE.md) 及 [`script/DEPLOYMENT_GUIDE.md`](./script/DEPLOYMENT_GUIDE.md)。

---

### 方法二：手動部署（本地開發）

#### 啟動後端

```bash
cd backend

# 建立虛擬環境並安裝依賴
uv venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

uv pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env，設定 ADMIN_USERNAME、ADMIN_PASSWORD、SECRET_KEY

# 初始化資料庫
python ../script/create_database.py

# 啟動伺服器
python run.py
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

後端運行於 `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 啟動前端

```bash
cd frontend
npm install
npm run dev
```

前端運行於 `http://localhost:5173`（Vite 開發伺服器，自動 proxy `/api` 至後端 8000 port）

---

## 📡 API 端點 (API Endpoints)

### 認證 (Authentication)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/auth/login` | POST | 登入（OAuth2 password） | ❌ |
| `/api/auth/verify` | GET | 驗證 Token，回傳當前使用者 | ✅ |
| `/api/auth/logout` | POST | 登出 | ✅ |

### 個人資訊 (Personal Info)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/personal-info/` | GET | 取得個人資訊 | ❌ |
| `/api/personal-info/` | POST | 新增個人資訊 | ✅ |
| `/api/personal-info/` | PUT | 更新個人資訊 | ✅ |

### 工作經歷 (Work Experience)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/work-experience/` | GET | 取得所有工作經歷（含所屬專案） | ❌ |
| `/api/work-experience/` | POST | 新增工作經歷（支援附件上傳） | ✅ |
| `/api/work-experience/{id}` | GET | 取得特定工作經歷 | ❌ |
| `/api/work-experience/{id}` | PUT | 更新工作經歷 | ✅ |
| `/api/work-experience/{id}` | DELETE | 刪除工作經歷 | ✅ |

### 專案 (Projects)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/projects/` | GET | 取得所有專案 | ❌ |
| `/api/projects/` | POST | 新增專案（支援附件上傳，100MB） | ✅ |
| `/api/projects/{id}` | GET | 取得特定專案 | ❌ |
| `/api/projects/{id}` | PUT | 更新專案 | ✅ |
| `/api/projects/{id}` | DELETE | 刪除專案 | ✅ |

### 教育背景 (Education)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/education/` | GET | 取得所有教育背景 | ❌ |
| `/api/education/` | POST | 新增教育背景 | ✅ |
| `/api/education/{id}` | GET | 取得特定教育背景 | ❌ |
| `/api/education/{id}` | PUT | 更新教育背景 | ✅ |
| `/api/education/{id}` | DELETE | 刪除教育背景 | ✅ |

### 證照 (Certifications)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/certifications/` | GET | 取得所有證照 | ❌ |
| `/api/certifications/` | POST | 新增證照 | ✅ |
| `/api/certifications/{id}` | GET | 取得特定證照 | ❌ |
| `/api/certifications/{id}` | PUT | 更新證照 | ✅ |
| `/api/certifications/{id}` | DELETE | 刪除證照 | ✅ |

### 語言能力 (Languages)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/languages/` | GET | 取得所有語言能力 | ❌ |
| `/api/languages/` | POST | 新增語言能力 | ✅ |
| `/api/languages/{id}` | GET | 取得特定語言能力 | ❌ |
| `/api/languages/{id}` | PUT | 更新語言能力 | ✅ |
| `/api/languages/{id}` | DELETE | 刪除語言能力 | ✅ |

### 學術著作 (Publications)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/publications/` | GET | 取得所有學術著作 | ❌ |
| `/api/publications/` | POST | 新增學術著作 | ✅ |
| `/api/publications/{id}` | GET | 取得特定學術著作 | ❌ |
| `/api/publications/{id}` | PUT | 更新學術著作 | ✅ |
| `/api/publications/{id}` | DELETE | 刪除學術著作 | ✅ |

### GitHub 專案 (GitHub Projects)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/github-projects/` | GET | 取得所有 GitHub 專案 | ❌ |
| `/api/github-projects/` | POST | 新增 GitHub 專案 | ✅ |
| `/api/github-projects/{id}` | GET | 取得特定 GitHub 專案 | ❌ |
| `/api/github-projects/{id}` | PUT | 更新 GitHub 專案 | ✅ |
| `/api/github-projects/{id}` | DELETE | 刪除 GitHub 專案 | ✅ |

### 資料庫匯入 / 匯出 (Database Import / Export)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/import/database/export/` | GET | 匯出 SQLite 資料庫（完整備份） | ✅ |
| `/api/import/database/import/` | POST | 匯入 SQLite 資料庫（100MB 上限） | ✅ |

### 系統端點 (System)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/` | GET | API 根端點（版本資訊） | ❌ |
| `/health` | GET | 健康檢查 | ❌ |
| `/uploads/{path}` | GET | 靜態附件存取 | ❌ |

---

## 💾 資料庫模型 (Database Models)

### 資料表總覽

| 資料表 | 說明 | 主要欄位 |
|--------|------|----------|
| `users` | 使用者帳號 | id, username, password_hash, email |
| `personal_info` | 個人資訊 | name_zh/en, phone, email, address_zh/en, objective_zh/en, personality_zh/en, summary_zh/en |
| `work_experience` | 工作經歷 | company_zh/en, position_zh/en, location_zh/en, start_date, end_date, is_current, attachment_* |
| `projects` | 專案經驗 | title_zh/en, description_zh/en, technologies, tools, environment, work_experience_id (FK) |
| `project_details` | 專案細節 | project_id (FK), description_zh/en (HTML), display_order |
| `project_attachments` | 專案附件 | project_detail_id (FK), file_name, file_url, file_type, file_size |
| `education` | 教育背景 | school_zh/en, degree_zh/en, major_zh/en, start_date, end_date |
| `certifications` | 證照 | name_zh/en, issuer, issue_date, certificate_number |
| `languages` | 語言能力 | language_zh/en, proficiency_zh/en, test_name, score |
| `publications` | 學術著作 | title, authors, publication, year, pages |
| `github_projects` | GitHub 專案 | name_zh/en, description_zh/en, url |

### 資料表關係 (Relationships)

```
work_experience
    └── projects (work_experience_id FK, cascade delete)
            └── project_details (project_id FK, cascade delete)
                    └── project_attachments (project_detail_id FK, cascade delete)
```

所有資料表均包含 `display_order` 欄位用於排序，以及 `created_at` / `updated_at` 時間戳記。

### 資料庫遷移歷史 (Migration History)

| 版本 | 說明 |
|------|------|
| `d711f173f9e3` | 初始 Schema — 建立所有資料表（使用 IF NOT EXISTS 冪等設計） |
| `ce10aaa23747` | 新增附件欄位 — 在 work_experience 及 projects 新增 attachment_* 欄位 |

---

## 🔐 安全性 (Security)

### JWT 認證

- **演算法**: HS256
- **Token 有效期**: 24 小時（`ACCESS_TOKEN_EXPIRE_MINUTES=1440`）
- **傳送方式**: `Authorization: Bearer <token>`
- **前端儲存**: localStorage

### 密碼安全

- **加密**: bcrypt（passlib 實作）
- **不儲存明文**: 僅儲存 bcrypt hash
- 初始管理員帳號由 `ADMIN_USERNAME` / `ADMIN_PASSWORD` 環境變數建立，**無硬編碼預設值**

### 管理員帳號設定

> **重要**: `ADMIN_USERNAME` 和 `ADMIN_PASSWORD` 為**必填環境變數**。應用程式啟動時若未設定，將拒絕運行。

```bash
# 生成安全的 SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### CORS 配置

```python
BACKEND_CORS_ORIGINS = [
    "http://localhost:5173",   # Vite 開發伺服器
    "http://localhost:3000",
    "http://localhost:58432",  # Docker 生產前端
    "http://localhost:8000",   # Docker 開發前端
]
```

### 其他防護

- DOMPurify HTML 清理（XSS 防護）
- SQLAlchemy ORM 參數化查詢（SQL Injection 防護）
- Pydantic 輸入驗證
- 檔案上傳類型限制（.pdf, .doc, .docx, .txt, .jpg, .jpeg, .png）
- 檔案大小上限：100MB

---

## ⚙️ 環境變數 (Environment Variables)

### Backend (`backend/.env`)

```env
# 應用設定
PROJECT_NAME="Resume Management System"
VERSION="1.0.0"
API_V1_STR="/api"

# 資料庫
DATABASE_URL="sqlite:///./data/resume.db"

# JWT（必填，請生成隨機密鑰）
SECRET_KEY="<執行 python -c \"import secrets; print(secrets.token_urlsafe(32))\" 生成>"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","http://localhost:58432"]

# 管理員帳號（必填，無預設值）
ADMIN_USERNAME="your-admin-username"
ADMIN_PASSWORD="change-this-before-deploying"
```

### Frontend (`frontend/.env`)

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_BASE_URL_DOCKER=http://localhost:58433/api
```

---

## 🔌 端口配置 (Port Configuration)

| 環境 | 前端端口 | 後端端口 | 說明 |
|------|----------|----------|------|
| **本地開發** | 5173 | 8000 | Vite dev server & Uvicorn |
| **Docker 生產環境** | 58432 | 58433 | Nginx & Uvicorn in Docker |
| **Docker 開發環境** | 8000 | 8001 | Docker Compose dev |

---

## 🧪 測試 (Testing)

```bash
# 後端測試
cd backend
pytest

# 測試內容涵蓋：
# - 管理員帳號初始化（環境變數注入）
# - 認證保護驗證
# - 檔案上傳 DoS 防禦
# - 管理員憑證配置
```

---

## 📝 開發指南 (Development Guide)

### 後端

```bash
# 程式碼格式化
black app/
isort app/

# 資料庫遷移
alembic revision --autogenerate -m "migration message"
alembic upgrade head

# 開發模式（熱重載）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
# 開發模式
npm run dev

# 程式碼檢查
npm run lint

# 建置生產版本
npm run build

# 預覽生產版本
npm run preview
```

---

## 🚢 部署 (Deployment)

### Docker 生產部署

```bash
# 部署
docker-compose up -d --build

# 查看狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 停止
docker-compose down
```

### Docker 資源限制（針對 GCP e2-micro 優化）

| 服務 | 最大記憶體 | 最大 CPU | 保留記憶體 | 保留 CPU |
|------|-----------|---------|-----------|---------|
| Backend | 512MB | 1.0 | 256MB | 0.5 |
| Frontend | 256MB | 0.5 | 128MB | 0.25 |

Uvicorn 配置（`run.py`）：
- Workers: 1
- Timeout keep-alive: 60s
- Limit concurrency: 20
- Limit max requests: 100（定期重啟 worker 釋放記憶體）

### 雲端平台建議

**後端**: Railway、Render、PythonAnywhere、GCP/AWS/Azure
**前端**: Netlify、Vercel、GitHub Pages、AWS S3 + CloudFront

---

## 🔍 故障排除 (Troubleshooting)

| 問題 | 排查方向 |
|------|---------|
| 後端無法啟動 | 確認 `ADMIN_USERNAME` 和 `ADMIN_PASSWORD` 已設定於 `.env` |
| API 無法訪問 | 檢查 CORS 設定是否包含前端 origin |
| JWT 驗證失敗 | 確認 `SECRET_KEY` 一致，Token 是否過期（24h） |
| 資料庫連線失敗 | 確認 `backend/data/` 目錄存在且有寫入權限 |
| Docker 容器啟動失敗 | 確認端口未被佔用；執行 `docker-compose logs` 查看詳情 |
| 前端無法加載圖片 | 確認 `frontend/public/media/` 中有對應圖片 |
| Alembic 遷移衝突 | 遷移腳本已使用 IF NOT EXISTS，直接執行 `alembic upgrade head` |

---

## 📄 授權 (License)

MIT License — Copyright (c) 2025 Polo (林鴻全)

---

## 👨‍💻 作者 (Author)

**Polo (林鴻全)**
Email: sprigga@gmail.com
Issues & 功能請求: GitHub Issues

---

**版本**: 1.0.0 | **最後更新**: 2026年2月 | **狀態**: Production Ready ✅
