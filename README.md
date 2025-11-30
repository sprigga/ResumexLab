# Resume Management System (個人履歷管理系統)

A full-stack resume management system with Vue 3 frontend and FastAPI backend, featuring bilingual support (Chinese/English), advanced resume management capabilities, and Docker containerization.

## 專案概述 (Project Overview)

這是一個全端履歷管理系統，提供：
- 公開的履歷展示頁面
- 受保護的後台管理介面
- 中英文雙語支援
- RESTful API
- SQLite 資料庫
- Docker 容器化部署
- 完整的履歷內容管理 (工作經歷、專案、教育背景、證照、語言能力、學術著作、GitHub專案)

This is a full-stack resume management system that provides:
- Public resume display page
- Protected admin management interface
- Bilingual support (Chinese/English)
- RESTful API
- SQLite database
- Docker containerization
- Complete resume content management (work experience, projects, education, certifications, languages, publications, GitHub projects)

## 系統架構 (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    Resume Management System                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue 3)              │  Backend (FastAPI)         │
│                                │                            │
│  ┌─────────────────────────┐   │   ┌─────────────────────┐  │
│  │ Vue Components          │   │   │ API Endpoints       │  │
│  │ ─────────────────────   │   │   │ ─────────────────   │  │
│  │ - ResumeView           │   │   │ - /api/auth         │  │
│  │ - AdminView            │   │   │ - /api/personal-info│  │
│  │ - Dashboard            │   │   │ - /api/work-exp     │  │
│  │ - ProjectView          │   │   │ - /api/education    │  │
│  │                        │   │   │ - /api/projects     │  │
│  │ - CertificationView    │   │   │ - /api/languages    │  │
│  │ - EducationView        │   │   │ - /api/publications │  │
│  │ - LanguageView         │   │   │ - /api/github-projects││
│  └─────────────────────────┘   │   └─────────────────────┘  │
│                                │                            │
│  State: Pinia                  │   Database: SQLite         │
│  UI: Element Plus              │   Auth: JWT                │
│  I18n: Vue I18n               │   Validation: Pydantic     │
└─────────────────────────────────────────────────────────────┘
│                            Docker                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Frontend (Nginx)│  │ Backend (Uvicorn)│ │ Database    │ │
│  │  Port: 58432    │  │   Port: 58433   │ │ (SQLite)    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 技術堆疊 (Tech Stack)

### Frontend
| 技術 | 版本 | 說明 |
|------|------|------|
| Vue 3 | 3.5.24 | 前端框架 (Composition API) |
| Pinia | 3.0.4 | 狀態管理 |
| Vue Router | 4.6.3 | 路由管理 |
| Element Plus | 2.11.9 | UI 元件庫 |
| Vue I18n | 9.14.5 | 多語言支援 |
| Axios | 1.13.2 | HTTP 客戶端 |
| Vite | 7.2.4 | 建置工具 |

### Backend
| 技術 | 版本 | 說明 |
|------|------|------|
| FastAPI | 0.104.1 | Web 框架 |
| SQLAlchemy | 2.0.23 | ORM |
| SQLite | 3.x | 資料庫 |
| JWT | python-jose | 身份驗證 |
| Pydantic | 2.5.0 | 資料驗證 |
| Uvicorn | 0.24.0 | ASGI 伺服器 |
| Alembic | 1.12.1 | 資料庫遷移 |
| Python | 3.10+ | 程式語言 |

## 專案結構 (Project Structure)

```
resumexlab/
├── backend/                    # FastAPI 後端
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/      # API 端點
│   │   │       ├── auth.py     # 認證
│   │   │       ├── personal_info.py  # 個人資訊
│   │   │       ├── work_experience.py  # 工作經驗
│   │   │       ├── projects.py   # 專案
│   │   │       ├── education.py  # 教育背景
│   │   │       ├── certifications.py  # 證照
│   │   │       ├── languages.py  # 語言能力
│   │   │       ├── publications.py # 學術著作
│   │   │       └── github_projects.py # GitHub專案
│   │   ├── core/               # 核心配置
│   │   ├── crud/               # CRUD 操作
│   │   ├── db/                 # 資料庫設定
│   │   ├── models/             # 資料庫模型
│   │   ├── schemas/            # Pydantic schemas
│   │   └── main.py             # 主應用程式
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── run.py
│   └── README.md
│
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── api/               # API 服務
│   │   ├── assets/            # 靜態資源
│   │   ├── components/        # 元件
│   │   ├── css/               # 樣式
│   │   ├── locales/           # 多語言
│   │   ├── router/            # 路由
│   │   ├── stores/            # 狀態管理
│   │   ├── utils/             # 工具函數
│   │   └── views/             # 頁面
│   ├── public/                # 靜態資源
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml         # Docker 容器化配置
├── README.md                  # 本檔案
└── .env.example              # 環境變數範例
```

## 功能特性 (Features)

### 前台功能 (Public Features)
| 功能 | 狀態 | 說明 |
|------|------|------|
| 履歷展示頁面 | ✅ 完成 | 完整的履歷內容展示 |
| 中英文語言切換 | ✅ 完成 | 支援繁體中文/英文切換 |
| 響應式設計 | ✅ 完成 | 支援行動裝置顯示 |
| 優雅的載入動畫 | ✅ 完成 | 使用 Element Plus Loading |
| 專案折叠/展開 | ✅ 完成 | 顯示前5個專案，其餘可展開 |

### 後台功能 (Admin Features)
| 功能 | 狀態 | 說明 |
|------|------|------|
| JWT 身份驗證 | ✅ 完成 | 基於 JWT 的安全驗證 |
| Dashboard 儀表板 | ✅ 完成 | 管理介面 |
| 個人資訊管理 | ✅ 完成 | 姓名、聯絡方式、履歷摘要 |
| 工作經歷 CRUD | ✅ 完成 | 公司、職位、描述、日期 |
| 專案經驗管理 | ✅ 完成 | 關聯工作經歷的專案 |
| 教育背景管理 | ✅ 完成 | 學校、學位、科系、日期 |
| 證照管理 | ✅ 完成 | 證照名稱、發證機關、日期 |
| 語言能力管理 | ✅ 完成 | 語言、熟練度、測驗成績 |
| 學術著作管理 | ✅ 完成 | 論文、出版品、作者 |
| GitHub專案管理 | ✅ 完成 | GitHub項目展示 |
| 圖片上傳 | 🚧 開發中 | 履歷用圖片上傳功能 |

## 快速開始 (Quick Start)

### 前置需求 (Prerequisites)

- Python 3.10+
- Node.js 20+
- npm or yarn
- Docker & Docker Compose
- uv (Python package manager)

### 方法一：Docker 部署 (推薦)

```bash
# 1. 克隆專案
git clone <repository-url>
cd resumexlab

# 2. 啟動服務 (使用 Docker Compose)
docker-compose up -d

# 3. 訪問應用
# 前端: http://localhost:58432
# 後端: http://localhost:58433
# API 文件: http://localhost:58433/docs
```

### 方法二：手動部署

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

# 4. 啟動伺服器
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

## API 端點 (API Endpoints)

### 認證 (Authentication)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/auth/login` | POST | 登入 |
| `/api/v1/auth/logout` | POST | 登出 |
| `/api/v1/auth/verify` | GET | 驗證 Token |
| `/api/v1/auth/me` | GET | 獲取當前使用者資訊 |

### 個人資訊 (Personal Info)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/personal-info/` | GET | 取得個人資訊 |
| `/api/v1/personal-info/` | POST | 新增個人資訊 |
| `/api/v1/personal-info/` | PUT | 更新個人資訊 |

### 工作經歷 (Work Experience)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/work-experience/` | GET | 取得所有工作經歷 |
| `/api/v1/work-experience/` | POST | 新增工作經歷 |
| `/api/v1/work-experience/{id}` | GET | 取得特定工作經歷 |
| `/api/v1/work-experience/{id}` | PUT | 更新工作經歷 |
| `/api/v1/work-experience/{id}` | DELETE | 刪除工作經歷 |

### 專案 (Projects)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/projects/` | GET | 取得所有專案 |
| `/api/v1/projects/` | POST | 新增專案 |
| `/api/v1/projects/{id}` | GET | 取得特定專案 |
| `/api/v1/projects/{id}` | PUT | 更新專案 |
| `/api/v1/projects/{id}` | DELETE | 刪除專案 |

### 教育背景 (Education)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/education/` | GET | 取得所有教育背景 |
| `/api/v1/education/` | POST | 新增教育背景 |
| `/api/v1/education/{id}` | GET | 取得特定教育背景 |
| `/api/v1/education/{id}` | PUT | 更新教育背景 |
| `/api/v1/education/{id}` | DELETE | 刪除教育背景 |

### 證照 (Certifications)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/certifications/` | GET | 取得所有證照 |
| `/api/v1/certifications/` | POST | 新增證照 |
| `/api/v1/certifications/{id}` | GET | 取得特定證照 |
| `/api/v1/certifications/{id}` | PUT | 更新證照 |
| `/api/v1/certifications/{id}` | DELETE | 刪除證照 |

### 語言能力 (Languages)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/languages/` | GET | 取得所有語言能力 |
| `/api/v1/languages/` | POST | 新增語言能力 |
| `/api/v1/languages/{id}` | GET | 取得特定語言能力 |
| `/api/v1/languages/{id}` | PUT | 更新語言能力 |
| `/api/v1/languages/{id}` | DELETE | 刪除語言能力 |

### 學術著作 (Publications)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/publications/` | GET | 取得所有學術著作 |
| `/api/v1/publications/` | POST | 新增學術著作 |
| `/api/v1/publications/{id}` | GET | 取得特定學術著作 |
| `/api/v1/publications/{id}` | PUT | 更新學術著作 |
| `/api/v1/publications/{id}` | DELETE | 刪除學術著作 |

### GitHub專案 (GitHub Projects)
| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/v1/github-projects/` | GET | 取得所有 GitHub 專案 |
| `/api/v1/github-projects/` | POST | 新增 GitHub 專案 |
| `/api/v1/github-projects/{id}` | GET | 取得特定 GitHub 專案 |
| `/api/v1/github-projects/{id}` | PUT | 更新 GitHub 專案 |
| `/api/v1/github-projects/{id}` | DELETE | 刪除 GitHub 專案 |

## 開發指南 (Development Guide)

### 後端開發 (Backend Development)

```bash
# 執行測試
pytest

# 程式碼格式化
black app/
isort app/

# 開發模式啟動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端開發 (Frontend Development)

```bash
# 建置生產版本
npm run build

# 預覽生產版本
npm run preview

# 開發模式
npm run dev
```

## 環境變數 (Environment Variables)

### Backend (.env)
```env
# API 設定
PROJECT_NAME="Resume Management System"
API_V1_STR=/api/v1
VERSION=1.0.0

# 資料庫設定
DATABASE_URL=sqlite:///./data/resume.db

# JWT 設定
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS 設定
BACKEND_CORS_ORIGINS=["http://localhost:58432","http://localhost:3000","http://localhost:8080","http://localhost"]
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_API_BASE_URL_DOCKER=http://localhost:58433/api/v1
```

## 部署 (Deployment)

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

## 安全性 (Security)

### JWT 認證
- 使用 HS256 演算法進行簽名
- Token 有效期：24 小時 (可配置)
- 支援刷新 Token 機制

### 資料庫安全
- 使用 SQLAlchemy ORM 防止 SQL 注入
- 參數化查詢確保資料安全
- SQLite 資料庫使用 WAL 模式確保一致性

### API 防護
- CORS 設定限制來源
- 請求驗證使用 Pydantic 模型
- 路徑參數類型安全檢查

## 資料庫模型 (Database Models)

### 用戶 (User)
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- hashed_password: String
- is_active: Boolean

### 個人資訊 (PersonalInfo)
- id: Integer (Primary Key)
- name_en: String
- name_zh: String
- email: String
- phone: String
- address_en: String
- address_zh: String
- summary_en: String
- summary_zh: String
- objective_en: String
- objective_zh: String
- photo_url: String

### 工作經歷 (WorkExperience)
- id: Integer (Primary Key)
- company_en: String
- company_zh: String
- position_en: String
- position_zh: String
- location_en: String
- location_zh: String
- start_date: Date
- end_date: Date
- description_en: String
- description_zh: String
- is_current: Boolean

### 專案 (Project)
- id: Integer (Primary Key)
- work_experience_id: Integer (Foreign Key)
- title_en: String
- title_zh: String
- description_en: String
- description_zh: String
- start_date: Date
- end_date: Date
- technologies: String
- tools: String

### 教育背景 (Education)
- id: Integer (Primary Key)
- school_en: String
- school_zh: String
- degree_en: String
- degree_zh: String
- major_en: String
- major_zh: String
- start_date: Date
- end_date: Date
- description_en: String
- description_zh: String

## 環境配置 (Environment Setup)

### 開發環境 (Development)

#### 準備工作
1. 克隆專案
```bash
git clone <repository-url>
cd resumexlab
```

2. 安裝 Python 依賴 (使用 uv)
```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

3. 安裝 Node.js 依賴
```bash
cd frontend
npm install
```

#### 啟動服務
1. 啟動後端
```bash
cd backend
python run.py
```

2. 啟動前端
```bash
cd frontend
npm run dev
```

### 生產環境 (Production)

#### Docker 部署
```bash
# 建置並啟動服務
docker-compose up -d --build

# 驗證服務
curl http://localhost:58433/health
curl http://localhost:58432
```

#### 環境變數設定
```bash
# 確保在 .env 中設定生產環境變數
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="sqlite:///./data/resume.db"
export ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 測試 (Testing)

### 單元測試
```bash
# 後端測試
cd backend
pytest

# 前端測試
cd frontend
npm run test
```

### 端到端測試
```bash
# 使用 Playwright 或 Cypress 進行 E2E 測試
npm run test:e2e
```

## 故障排除 (Troubleshooting)

### 常見問題
1. **後端 API 無法訪問**
   - 檢查 CORS 設定
   - 確認前端 API URL 配置正確

2. **前端無法加載圖片**
   - 檢查 `public/media` 資料夾是否包含圖片
   - 確認圖片路徑配置正確

3. **Docker 容器啟動失敗**
   - 檢查端口是否被佔用
   - 查看容器日誌：`docker-compose logs`

### 建議解決步驟
1. 檢查日誌輸出
2. 驗證環境變數
3. 確認資料庫連線
4. 檢查網路連線

## 貢獻 (Contributing)

### 開發流程
1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 程式碼風格
- Python: 使用 Black 和 isort 格式化
- JavaScript: 使用 ESLint 和 Prettier
- Commit messages: 遵循 conventional commits

## 授權 (License)

MIT License - 請在專案中包含著作權聲明和授權宣告。

## 作者 (Author)

Polo (林鴻全)

## 支援 (Support)

如需技術支援或問題回報：
- GitHub Issues: 提交問題和功能請求
- Email: [your-email@example.com]

---

**開發日期**: 2025年11月
**版本**: 1.0
**狀態**: Production Ready