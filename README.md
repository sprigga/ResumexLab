# Resume Management System (個人履歷管理系統)

A full-stack resume management system with Vue 3 frontend and FastAPI backend, featuring bilingual support (Chinese/English).

## 專案概述 (Project Overview)

這是一個全端履歷管理系統，提供：
- 公開的履歷展示頁面
- 受保護的後台管理介面
- 中英文雙語支援
- RESTful API
- SQLite 資料庫

This is a full-stack resume management system that provides:
- Public resume display page
- Protected admin management interface
- Bilingual support (Chinese/English)
- RESTful API
- SQLite database

## 技術堆疊 (Tech Stack)

### Frontend
- **Framework**: Vue 3 (Composition API)
- **State Management**: Pinia
- **Routing**: Vue Router
- **UI Framework**: Element Plus
- **Internationalization**: Vue I18n
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Authentication**: JWT
- **Validation**: Pydantic
- **Server**: Uvicorn

## 專案結構 (Project Structure)

```
resumexlab/
├── backend/                # FastAPI 後端
│   ├── app/
│   │   ├── api/           # API 端點
│   │   ├── core/          # 核心配置
│   │   ├── crud/          # CRUD 操作
│   │   ├── db/            # 資料庫設定
│   │   ├── models/        # 資料庫模型
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # 主應用程式
│   ├── requirements.txt
│   └── README.md
│
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── api/          # API 服務
│   │   ├── components/   # 元件
│   │   ├── locales/      # 多語言
│   │   ├── router/       # 路由
│   │   ├── stores/       # 狀態管理
│   │   └── views/        # 頁面
│   ├── package.json
│   └── README.md
│
└── README.md             # 本檔案
```

## 快速開始 (Quick Start)

### 前置需求 (Prerequisites)

- Python 3.10+
- Node.js 20+
- npm or yarn
- uv (Python package manager)

### 1. 啟動後端 (Start Backend)

```bash
cd backend

# 建立虛擬環境
uv venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 安裝依賴
uv pip install -r requirements.txt

# 啟動伺服器
python run.py
# OR
uvicorn app.main:app --reload
```

後端將運行在 `http://localhost:8000`
- API 文件: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. 啟動前端 (Start Frontend)

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端將運行在 `http://localhost:5173`

## 預設登入資訊 (Default Credentials)

- **使用者名稱**: `admin`
- **密碼**: `admin123`

**重要**: 生產環境請務必更改預設密碼！
**Important**: Change default credentials in production!

## 功能特性 (Features)

### 前台功能 (Public Features)
- ✅ 履歷展示頁面
- ✅ 中英文語言切換
- ✅ 響應式設計

### 後台功能 (Admin Features)
- ✅ JWT 身份驗證
- ✅ Dashboard 儀表板
- ✅ 個人資訊管理
- ✅ 工作經歷 CRUD
- 🚧 專案經驗管理
- 🚧 教育背景管理
- 🚧 證照與語言管理

## API 端點 (API Endpoints)

### 認證 (Authentication)
- `POST /api/auth/login` - 登入
- `GET /api/auth/verify` - 驗證 Token
- `POST /api/auth/logout` - 登出

### 個人資訊 (Personal Info)
- `GET /api/personal-info` - 取得個人資訊
- `PUT /api/personal-info` - 更新個人資訊

### 工作經歷 (Work Experience)
- `GET /api/work-experience` - 取得所有工作經歷
- `GET /api/work-experience/{id}` - 取得特定工作經歷
- `POST /api/work-experience` - 新增工作經歷
- `PUT /api/work-experience/{id}` - 更新工作經歷
- `DELETE /api/work-experience/{id}` - 刪除工作經歷

## 開發指南 (Development Guide)

### 後端開發 (Backend Development)

```bash
# 執行測試
pytest

# 程式碼格式化
black app/
isort app/
```

### 前端開發 (Frontend Development)

```bash
# 建置生產版本
npm run build

# 預覽生產版本
npm run preview
```

## 環境變數 (Environment Variables)

### Backend (.env)
```env
PROJECT_NAME="Resume Management System"
DATABASE_URL="sqlite:///./resume.db"
SECRET_KEY="your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 部署 (Deployment)

### Backend
建議使用：
- Railway
- Render
- PythonAnywhere

### Frontend
建議使用：
- Netlify
- Vercel
- GitHub Pages

## 授權 (License)

MIT License

## 作者 (Author)

Polo (林鴻全)

---

**開發日期**: 2025年11月
**版本**: 1.0
