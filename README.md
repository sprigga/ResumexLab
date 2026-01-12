# ResumeXLab - 個人履歷管理系統

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/Vue-3.5-brightgreen.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-red.svg)](https://fastapi.tiangolo.com/)

一個功能完整的全端履歷管理系統，採用 Vue 3 前端與 FastAPI 後端架構，支援中英文雙語切換、進階履歷管理功能，並提供 Docker 容器化部署。

A comprehensive full-stack resume management system with Vue 3 frontend and FastAPI backend, featuring bilingual support (Chinese/English), advanced resume management capabilities, and Docker containerization.

## 📋 專案概述 (Project Overview)

### 功能特色 (Key Features)

這是一個全端履歷管理系統，提供：

**前台功能 (Public Features)**
- ✅ 專業履歷展示頁面 - 響應式設計，支援各種裝置
- ✅ 中英文雙語切換 - 即時切換語言，Localstorage 記憶偏好
- ✅ 優雅的使用者體驗 - 載入動畫、專案折疊/展開功能
- ✅ SEO 友善 - 優化 meta 標籤與結構化資料

**後台管理 (Admin Features)**
- 🔐 JWT 身份驗證 - 安全的登入系統，Token 24 小時有效
- 📊 Dashboard 儀表板 - 直觀的管理介面
- ✏️ 完整的 CRUD 功能 - 管理所有履歷資料
  - 個人資訊（姓名、聯絡方式、履歷摘要）
  - 工作經歷（公司、職位、專案描述）
  - 專案經驗（技術堆疊、工具、環境）
  - 專案附件管理（檔案上傳與管理）
  - 教育背景（學校、學位、科系）
  - 證照管理（證照名稱、發證機關）
  - 語言能力（語言、熟練度、測驗成績）
  - 學術著作（論文、出版品）
  - GitHub 專案展示
- 📥 批量資料匯入 - 快速匯入履歷資料

**技術優勢 (Technical Highlights)**
- 🐳 Docker 容器化 - 一鍵部署，隔離環境
- 🔄 資料庫遷移 - Alembic 自動化管理
- 📝 自動 API 文件 - Swagger UI / ReDoc
- 🛡️ 安全性防護 - JWT、bcrypt、CORS、XSS 防護
- 📱 響應式設計 - Mobile-first 原則

This is a full-stack resume management system that provides:

**Public Features**
- ✅ Professional resume display page - Responsive design for all devices
- ✅ Bilingual support (Chinese/English) - Real-time language switching with Localstorage preference
- ✅ Elegant user experience - Loading animations, project collapse/expand
- ✅ SEO friendly - Optimized meta tags and structured data

**Admin Features**
- 🔐 JWT authentication - Secure login system with 24-hour token validity
- 📊 Dashboard interface - Intuitive management UI
- ✏️ Complete CRUD functionality - Manage all resume data
  - Personal info (name, contact, summary)
  - Work experience (company, position, project description)
  - Project experience (tech stack, tools, environment)
  - Project attachment management (file upload)
  - Education background (school, degree, major)
  - Certification management (name, issuer)
  - Language proficiency (language, level, test scores)
  - Academic publications (papers, publications)
  - GitHub project showcase
- 📥 Batch data import - Quick import of resume data

**Technical Highlights**
- 🐳 Docker containerization - One-click deployment, isolated environments
- 🔄 Database migrations - Alembic automation
- 📝 Auto API documentation - Swagger UI / ReDoc
- 🛡️ Security protection - JWT, bcrypt, CORS, XSS prevention
- 📱 Responsive design - Mobile-first approach

## 🏗️ 系統架構 (System Architecture)

### 整體架構圖 (Overall Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    ResumeXLab System                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue 3)              │  Backend (FastAPI)         │
│                                │                            │
│  ┌─────────────────────────┐   │   ┌─────────────────────┐  │
│  │ Vue Components          │   │   │ API Endpoints       │  │
│  │ ─────────────────────   │   │   │ ─────────────────   │  │
│  │ - ResumeView           │   │   │ - /api/auth         │  │
│  │ - AdminLayout          │   │   │ - /api/personal-info│  │
│  │ - LoginView            │   │   │ - /api/work-exp     │  │
│  │ - Dashboard            │   │   │ - /api/projects     │  │
│  │ - PersonalInfoEdit     │   │   │ - /api/education    │  │
│  │ - WorkExperienceEdit   │   │   │ - /api/certifications│ │
│  │ - ProjectEdit          │   │   │ - /api/languages    │  │
│  │ - EducationEdit        │   │   │ - /api/publications │  │
│  │ - CertificationEdit    │   │   │ - /api/github-projects│ │
│  │ - ImportDataView       │   │   │ - /api/import       │  │
│  └─────────────────────────┘   │   └─────────────────────┘  │
│                                │                            │
│  State: Pinia                  │   Database: SQLite         │
│  UI: Element Plus              │   Auth: JWT                │
│  I18n: Vue I18n                │   ORM: SQLAlchemy 2.0     │
│  Router: Vue Router            │   Validation: Pydantic 2  │
│  HTTP: Axios                   │   Migration: Alembic      │
└─────────────────────────────────────────────────────────────┘
│                            Docker                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Frontend (Nginx)│  │ Backend (Uvicorn)│ │ Database    │ │
│  │  Port: 58432    │  │   Port: 58433   │ │ (SQLite)    │ │
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
                                     │  API Proxy       │
                                     │  /api/* → Backend│
                                     └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  FastAPI Server  │
                                     │  (Uvicorn)       │
                                     └────────┬─────────┘
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        │                     │                     │
                        ▼                     ▼                     ▼
              ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
              │   SQLite DB  │      │   Alembic    │      │   Static     │
              │              │      │  (Migrations)│      │   Files      │
              └──────────────┘      └──────────────┘      └──────────────┘
```

## 🛠️ 技術堆疊 (Tech Stack)

### Frontend（前端技術）

| 技術 | 版本 | 說明 |
|------|------|------|
| **Vue 3** | 3.5.24 | 前端框架 (Composition API) |
| **Pinia** | 3.0.4 | 狀態管理 |
| **Vue Router** | 4.6.3 | 路由管理 |
| **Element Plus** | 2.11.9 | UI 元件庫 |
| **Vue I18n** | 9.14.5 | 多語言支援 |
| **Axios** | 1.13.2 | HTTP 客戶端 |
| **Vite** | 7.2.4 | 建置工具 |
| **DOMPurify** | latest | XSS 防護 |
| **@vueup/vue-quill** | latest | 富文本編輯器 |
| **Nginx** | latest | 生產環境 Web 伺服器 |

### Backend（後端技術）

| 技術 | 版本 | 說明 |
|------|------|------|
| **FastAPI** | 0.104.1 | Web 框架 |
| **SQLAlchemy** | 2.0.23 | ORM |
| **SQLite** | 3.x | 資料庫 |
| **python-jose** | 3.3.0 | JWT 身份驗證 |
| **passlib[bcrypt]** | 1.7.4 | 密碼加密 |
| **Pydantic** | 2.5.0 | 資料驗證 |
| **Pydantic Settings** | 2.1.0 | 配置管理 |
| **Uvicorn** | 0.24.0 | ASGI 伺服器 |
| **Alembic** | 1.12.1 | 資料庫遷移 |
| **Python** | 3.10+ | 程式語言 |
| **PyPDF2** | 3.0.1 | PDF 處理 |
| **python-multipart** | latest | 檔案上傳支援 |

### DevOps（部署與開發）

| 工具 | 說明 |
|------|------|
| **Docker** | 容器化技術 |
| **Docker Compose** | 多容器編排 |
| **Git** | 版本控制 |
| **uv** | Python 套件管理器 |
| **npm** | Node.js 套件管理器 |

## 📁 專案結構 (Project Structure)

```
ResumexLab/
├── backend/                          # FastAPI 後端應用
│   ├── alembic/                      # 資料庫遷移工具
│   │   ├── versions/                 # 遷移歷史
│   │   │   ├── d711f173f9e3_初始化資料庫表.py
│   │   │   └── ce10aaa23747_添加附件欄位.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/                          # 應用核心代碼
│   │   ├── api/                      # API 路由
│   │   │   └── endpoints/            # API 端點處理器
│   │   │       ├── auth.py           # 認證登入/登出
│   │   │       ├── personal_info.py  # 個人資訊
│   │   │       ├── work_experience.py # 工作經歷
│   │   │       ├── projects.py       # 專案經驗
│   │   │       ├── education.py      # 教育背景
│   │   │       ├── certifications.py # 證照管理
│   │   │       ├── languages.py      # 語言能力
│   │   │       ├── publications.py   # 學術著作
│   │   │       ├── github_projects.py # GitHub 專案
│   │   │       └── import_data.py    # 批量匯入
│   │   ├── core/                     # 核心配置
│   │   │   ├── config.py             # 應用設置
│   │   │   └── security.py           # 安全相關 (JWT)
│   │   ├── crud/                     # CRUD 操作
│   │   ├── db/                       # 資料庫相關
│   │   │   ├── base.py               # 資料庫基礎設置
│   │   │   └── init_db.py            # 初始化數據庫
│   │   ├── models/                   # SQLAlchemy 模型
│   │   │   ├── user.py               # 使用者模型
│   │   │   ├── personal_info.py      # 個人資訊模型
│   │   │   ├── work_experience.py    # 工作經歷模型
│   │   │   ├── project.py            # 專案模型 (含 details & attachments)
│   │   │   ├── education.py          # 教育背景模型
│   │   │   ├── certification.py      # 證照模型
│   │   │   └── publication.py        # 學術著作模型
│   │   ├── schemas/                  # Pydantic 模式
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
│   ├── data/                         # 資料庫檔案目錄
│   │   └── resume.db                 # SQLite 資料庫
│   ├── uploads/                      # 上傳檔案目錄
│   ├── requirements.txt              # Python 依賴
│   ├── alembic.ini                   # Alembic 配置
│   ├── Dockerfile                    # Docker 映像建置
│   ├── run.py                        # 啟動腳本
│   └── .env.example                  # 環境變數範例
│
├── frontend/                         # Vue 3 前端應用
│   ├── src/
│   │   ├── api/                      # API 服務
│   │   │   ├── auth.js               # 認證 API
│   │   │   └── resume.js             # 履歷資料 API
│   │   ├── assets/                   # 靜態資源
│   │   │   └── css/                  # 樣式檔案
│   │   ├── components/               # Vue 組件
│   │   │   ├── ProjectCard.vue       # 專案卡片組件
│   │   │   ├── ProjectDetails.vue    # 專案細節組件
│   │   │   └── ...
│   │   ├── locales/                  # 多語言翻譯
│   │   │   ├── en.js                 # 英文翻譯
│   │   │   └── zh.js                 # 中文翻譯
│   │   ├── router/                   # 路由配置
│   │   │   └── index.js              # 路由定義
│   │   ├── stores/                   # Pinia 狀態管理
│   │   │   ├── auth.js               # 認證狀態
│   │   │   └── resume.js             # 履歷資料狀態
│   │   ├── utils/                    # 工具函數
│   │   ├── views/                    # 頁面視圖
│   │   │   ├── ResumeView.vue        # 履歷展示頁面
│   │   │   └── admin/                # 管理後台
│   │   │       ├── AdminLayout.vue   # 管理介面佈局
│   │   │       ├── LoginView.vue     # 登入頁面
│   │   │       ├── DashboardView.vue # 儀表板
│   │   │       ├── PersonalInfoEdit.vue  # 個人資訊編輯
│   │   │       ├── WorkExperienceEdit.vue # 工作經歷編輯
│   │   │       ├── ProjectEdit.vue        # 專案編輯
│   │   │       ├── EducationEdit.vue      # 教育背景編輯
│   │   │       ├── CertificationEdit.vue  # 證照編輯
│   │   │       ├── LanguageEdit.vue       # 語言能力編輯
│   │   │       ├── PublicationEdit.vue    # 學術著作編輯
│   │   │       ├── GithubProjectEdit.vue  # GitHub 專案編輯
│   │   │       └── ImportDataView.vue     # 資料匯入
│   │   └── App.vue                   # 應用根組件
│   ├── public/                       # 公共靜態資源
│   │   └── media/                    # 媒體檔案
│   ├── package.json                  # Node.js 依賴
│   ├── vite.config.js                # Vite 配置
│   ├── Dockerfile                    # Docker 映像建置
│   └── nginx.conf                    # Nginx 配置
│
├── scripts/                          # 工具腳本
│   ├── create_database.py            # 資料庫初始化
│   ├── DEPLOYMENT_GUIDE.md           # 部署指南
│   └── ...
│
├── docs/                             # 文件目錄
│   └── DOCKER_COMPOSE_USAGE.md       # Docker 使用說明
│
├── docker-compose.yml                # 生產環境 Docker 配置
├── docker-compose.dev.yml            # 開發環境 Docker 配置
├── .gitignore                        # Git 忽略配置
├── README.md                         # 本文件
├── CLAUDE.md                         # Claude Code 專案指引
└── .env.example                      # 環境變數範例
```

### 關鍵目錄說明 (Key Directories)

| 目錄 | 說明 |
|------|------|
| `backend/app/api/endpoints/` | 所有 API 端點實作 |
| `backend/app/models/` | SQLAlchemy 資料庫模型 |
| `backend/app/schemas/` | Pydantic 資料驗證模式 |
| `backend/alembic/versions/` | 資料庫遷移歷史 |
| `frontend/src/views/` | Vue 頁面組件 |
| `frontend/src/stores/` | Pinia 狀態管理 |
| `frontend/src/locales/` | 多語言翻譯檔案 |
| `backend/data/` | SQLite 資料庫檔案 |
| `backend/uploads/` | 上傳檔案儲存目錄 |

## 🚀 快速開始 (Quick Start)

### 前置需求 (Prerequisites)

- Python 3.10+
- Node.js 20+
- npm or yarn
- Docker & Docker Compose (可選)
- uv (Python package manager)

### 方法一：Docker 部署（推薦）

我們提供兩個 Docker Compose 配置檔案：

#### 開發環境 (本地開發)

```bash
# 1. 克隆專案
git clone <repository-url>
cd ResumexLab

# 2. 啟動開發環境
docker-compose -f docker-compose.dev.yml up -d

# 3. 訪問應用
# 前端: http://localhost:8000
# 後端: http://localhost:8001
# API 文件: http://localhost:8001/docs
```

#### 生產環境 (GCP VM / 雲端主機)

```bash
# 1. 克隆專案
git clone <repository-url>
cd ResumexLab

# 2. 啟動生產環境
docker-compose up -d

# 3. 訪問應用
# 前端: http://<YOUR-IP>:58432
# 後端: http://<YOUR-IP>:58433
# API 文件: http://<YOUR-IP>:58433/docs
```

**詳細部署指南**: 請參考 [`docs/DOCKER_COMPOSE_USAGE.md`](./docs/DOCKER_COMPOSE_USAGE.md) 和 [`scripts/DEPLOYMENT_GUIDE.md`](./scripts/DEPLOYMENT_GUIDE.md)

### 方法二：手動部署（開發模式）

#### 啟動後端 (Start Backend)

```bash
# 1. 進入後端目錄
cd backend

# 2. 建立虛擬環境
uv venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 3. 安裝依賴
uv pip install -r requirements.txt

# 4. 初始化資料庫 (首次運行)
python ../scripts/create_database.py

# 5. 啟動伺服器
python run.py
# OR
uvicorn app.main:app --reload
```

後端將運行在 `http://localhost:8000`
- API 文件: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 啟動前端 (Start Frontend)

```bash
# 1. 進入前端目錄
cd frontend

# 2. 安裝依賴
npm install

# 3. 啟動開發伺服器
npm run dev
```

前端將運行在 `http://localhost:5173`

## 📡 API 端點 (API Endpoints)

### 認證 (Authentication)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/auth/login` | POST | 使用者登入 | ❌ |
| `/api/auth/logout` | POST | 使用者登出 | ✅ |
| `/api/auth/verify` | GET | 驗證 Token | ✅ |
| `/api/auth/me` | GET | 獲取當前使用者資訊 | ✅ |

### 個人資訊 (Personal Info)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/personal-info/` | GET | 取得個人資訊 | ❌ |
| `/api/personal-info/` | POST | 新增個人資訊 | ✅ |
| `/api/personal-info/` | PUT | 更新個人資訊 | ✅ |

### 工作經歷 (Work Experience)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/work-experience/` | GET | 取得所有工作經歷 | ❌ |
| `/api/work-experience/` | POST | 新增工作經歷 | ✅ |
| `/api/work-experience/{id}` | GET | 取得特定工作經歷 | ❌ |
| `/api/work-experience/{id}` | PUT | 更新工作經歷 | ✅ |
| `/api/work-experience/{id}` | DELETE | 刪除工作經歷 | ✅ |

### 專案 (Projects)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/projects/` | GET | 取得所有專案 | ❌ |
| `/api/projects/` | POST | 新增專案 | ✅ |
| `/api/projects/{id}` | GET | 取得特定專案 | ❌ |
| `/api/projects/{id}` | PUT | 更新專案 | ✅ |
| `/api/projects/{id}` | DELETE | 刪除專案 | ✅ |
| `/api/projects/{id}/attachments` | GET | 取得專案附件列表 | ❌ |
| `/api/projects/{id}/attachments` | POST | 上傳專案附件 | ✅ |
| `/api/projects/{id}/attachments/{attachment_id}` | DELETE | 刪除專案附件 | ✅ |

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

### GitHub專案 (GitHub Projects)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/github-projects/` | GET | 取得所有 GitHub 專案 | ❌ |
| `/api/github-projects/` | POST | 新增 GitHub 專案 | ✅ |
| `/api/github-projects/{id}` | GET | 取得特定 GitHub 專案 | ❌ |
| `/api/github-projects/{id}` | PUT | 更新 GitHub 專案 | ✅ |
| `/api/github-projects/{id}` | DELETE | 刪除 GitHub 專案 | ✅ |

### 資料匯入 (Data Import)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/api/import/all` | POST | 批量匯入所有履歷資料 | ✅ |
| `/api/import/personal-info` | POST | 匯入個人資訊 | ✅ |
| `/api/import/work-experience` | POST | 匯入工作經歷 | ✅ |
| `/api/import/education` | POST | 匯入教育背景 | ✅ |
| `/api/import/certifications` | POST | 匯入證照資料 | ✅ |
| `/api/import/publications` | POST | 匯入學術著作 | ✅ |

### 工具端點 (Utility Endpoints)

| 端點 | 方法 | 功能 | 認證 |
|------|------|------|------|
| `/` | GET | API 根端點 (歡迎訊息) | ❌ |
| `/health` | GET | 健康檢查 | ❌ |

## 💾 資料庫模型 (Database Models)

### 資料表總覽 (Tables Overview)

| 資料表 | 說明 | 主要欄位 |
|--------|------|----------|
| `users` | 使用者帳號 | id, username, password_hash, email |
| `personal_info` | 個人資訊 | name_zh, name_en, phone, email, address |
| `work_experience` | 工作經歷 | company_zh/en, position_zh/en, start_date, end_date |
| `projects` | 專案經驗 | title_zh/en, description, technologies, tools, environment |
| `project_details` | 專案細節 | project_id, detail_zh/en, display_order |
| `project_attachments` | 專案附件 | project_id, file_name, file_path, file_type |
| `education` | 教育背景 | school_zh/en, degree_zh/en, major_zh/en |
| `certifications` | 證照 | name_zh/en, issuer, issue_date, certificate_number |
| `languages` | 語言能力 | language_zh/en, proficiency_zh/en, test_name, score |
| `publications` | 學術著作 | title, authors, publication, year, pages |
| `github_projects` | GitHub 專案 | name_zh/en, description_zh/en, url |

### 資料表關係 (Table Relationships)

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│   users     │     │work_exp     │     │    projects      │
│             │     │             │     │                  │
│ id          │     │ id          │◄────│ work_exp_id (FK) │
│ username    │     │ company_zh  │     │ id               │
│ password... │     │ position... │     │ title_zh         │
└─────────────┘     └─────────────┘     │ description...   │
                                         └────────┬─────────┘
                                                  │
                    ┌─────────────────────────────┴──────────┐
                    │                                        │
            ┌───────▼────────┐                   ┌──────────▼────────┐
            │project_details │                   │project_attachments│
            │                │                   │                   │
            │ id             │                   │ id                │
            │ project_id(FK) │                   │ project_id(FK)    │
            │ detail_zh/en   │                   │ file_name         │
            │ display_order  │                   │ file_path...      │
            └────────────────┘                   └───────────────────┘
```

## 🔐 安全性 (Security)

### JWT 認證機制 (JWT Authentication)

- **演算法**: HS256
- **Token 有效期**: 24 小時 (可配置)
- **儲存方式**: LocalStorage (前端)
- **傳送方式**: Authorization Header (`Bearer <token>`)

```python
# Token 生成範例
SECRET_KEY = secrets.token_urlsafe(32)  # 請在生產環境使用安全的密鑰
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 小時
```

### 密碼安全 (Password Security)

- **加密方式**: bcrypt
- **Salt 輪數**: 預設 12 輪
- **不儲存明文密碼**: 只儲存 bcrypt hash

### CORS 配置 (CORS Configuration)

```python
# 生產環境 CORS 設定
BACKEND_CORS_ORIGINS = [
    "http://localhost:58432",
    "http://localhost:58433",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost",
]
```

### XSS 防護 (XSS Protection)

- 前端使用 DOMPurify 清理 HTML
- 後端驗證所有輸入資料
- 使用 Pydantic 模型驗證

### SQL Injection 防護

- 使用 SQLAlchemy ORM
- 參數化查詢
- 不允許原生 SQL 執行

## ⚙️ 環境變數 (Environment Variables)

### Backend (.env)

```env
# API 設定
PROJECT_NAME="Resume Management System"
API_V1_STR=/api
VERSION=1.0.0

# 資料庫設定
DATABASE_URL=sqlite:///./data/resume.db

# JWT 設定
# 請使用以下命令生成安全的 SECRET_KEY：
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=PLEASE-GENERATE-A-SECURE-SECRET-KEY-USING-PYTHON-SECRETS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS 設定
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","http://localhost:58432"]
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_BASE_URL_DOCKER=http://localhost:58433/api
```

## 🧪 測試 (Testing)

### 單元測試 (Unit Tests)

```bash
# 後端測試
cd backend
pytest

# 前端測試
cd frontend
npm run test
```

### 端到端測試 (E2E Tests)

```bash
# 使用 Playwright 或 Cypress 進行 E2E 測試
npm run test:e2e
```

## 📝 開發指南 (Development Guide)

### 後端開發 (Backend Development)

```bash
# 執行測試
pytest

# 程式碼格式化
black app/
isort app/

# 開發模式啟動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 資料庫遷移
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### 前端開發 (Frontend Development)

```bash
# 建置生產版本
npm run build

# 預覽生產版本
npm run preview

# 開發模式
npm run dev

# 程式碼檢查
npm run lint
```

## 🚢 部署 (Deployment)

### Docker 部署 (Production)

```bash
# 使用 Docker Compose 部署到生產環境
docker-compose up -d --build

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

### 環境變數配置

在生產環境中，請確保已正確設置所有環境變數：

1. 將 `.env.example` 複製為 `.env`
2. 更新 `SECRET_KEY` 為安全的隨機字串
3. 更新 `DATABASE_URL` 指向生產資料庫
4. 調整 CORS 設定

### 部署到雲端平台

#### 後端 (Backend)
建議使用：
- **Railway**: 一鍵部署，自動環境變數
- **Render**: 簡單部署，支援自動建置
- **PythonAnywhere**: Python 專業部署平台
- **AWS/GCP/Azure**: 進階雲端部署

#### 前端 (Frontend)
建議使用：
- **Netlify**: 簡單部署，支援自定義網域
- **Vercel**: Vue.js 優化部署
- **GitHub Pages**: 免費靜態網站托管
- **AWS S3 + CloudFront**: 高效能 CDN

## 🔍 故障排除 (Troubleshooting)

### 常見問題 (Common Issues)

1. **後端 API 無法訪問**
   - 檢查 CORS 設定
   - 確認前端 API URL 配置正確
   - 檢查防火牆規則

2. **前端無法加載圖片**
   - 檢查 `public/media` 資料夾是否包含圖片
   - 確認圖片路徑配置正確
   - 檢查 Nginx 靜態檔案配置

3. **Docker 容器啟動失敗**
   - 檢查端口是否被佔用
   - 查看容器日誌：`docker-compose logs`
   - 確認 Docker 資源是否足夠

4. **資料庫連線失敗**
   - 確認 `data/` 目錄存在且有寫入權限
   - 檢查 SQLite 檔案權限
   - 驗證 DATABASE_URL 配置

5. **JWT Token 過期**
   - 重新登入獲取新 Token
   - 調整 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置

### 建議解決步驟 (Troubleshooting Steps)

1. 檢查日誌輸出
2. 驗證環境變數
3. 確認資料庫連線
4. 檢查網路連線
5. 查看 API 文件 (`/docs`)
6. 使用瀏覽器開發者工具檢查網路請求

## 🤝 貢獻 (Contributing)

### 開發流程 (Development Workflow)

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 程式碼風格 (Code Style)

- **Python**: 使用 Black 和 isort 格式化
- **JavaScript**: 使用 ESLint 和 Prettier
- **Commit Messages**: 遵循 conventional commits

### Pull Request 檢查清單 (PR Checklist)

- [ ] 程式碼通過所有測試
- [ ] 程式碼符合專案風格指南
- [ ] 更新相關文件
- [ ] 添加必要的註釋
- [ ] 確認沒有引入安全漏洞

## 📄 授權 (License)

MIT License - 請在專案中包含著作權聲明和授權宣告。

```
MIT License

Copyright (c) 2025 Polo (林鴻全)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 作者 (Author)

**Polo (林鴻全)**

## 📞 支援 (Support)

如需技術支援或問題回報：

- **GitHub Issues**: 提交問題和功能請求
- **Email**: sprigga@gmail.com
- **文件**: 請參考 `docs/` 目錄下的詳細文件

---

## 📌 重要提示 (Important Notes)

### 端口配置 (Port Configuration)

| 環境 | 前端端口 | 後端端口 | 說明 |
|------|----------|----------|------|
| **開發環境** | 5173 | 8000 | Vite dev server & Uvicorn |
| **Docker 生產環境** | 58432 | 58433 | Nginx & Uvicorn in Docker |
| **Docker 開發環境** | 8000 | 8001 | Local Docker development |

### 資料庫位置 (Database Location)

- 資料庫檔案位於: `backend/data/resume.db`
- 首次運行需執行: `python scripts/create_database.py` 初始化資料庫
- 建議定期備份資料庫檔案

### 環境變數 (Environment Variables)

- 後端環境變數請參考 `backend/.env.example`
- **重要**: 生產環境務必更改 `SECRET_KEY`
- 使用 `python -c "import secrets; print(secrets.token_urlsafe(32))"` 生成安全密鑰

### 預設登入帳號 (Default Login)

- 使用 `create_database.py` 建立的預設帳號請查看腳本內容
- 建議首次登入後立即更改密碼
- 可透過管理後台新增更多使用者帳號

### 檔案上傳 (File Upload)

- 上傳檔案儲存於: `backend/uploads/`
- 支援的檔案類型取決於配置
- 建議定期清理不必要的附件檔案

---

**開發日期**: 2025年11月
**最後更新**: 2025年1月
**版本**: 1.0
**狀態**: Production Ready ✅

---

## 🙏 致謝 (Acknowledgments)

感謝以下開源專案：

- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Element Plus](https://element-plus.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)

特別感謝所有貢獻者的大力支持！

---

**⭐ 如果這個專案對你有幫助，請給予 Star 支援！**

如有任何問題或建議，歡迎隨時聯繫或提交 Issue。
