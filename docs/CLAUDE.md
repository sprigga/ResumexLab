# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ResumeXLab is a Python-based project for resume processing and experimentation.

## Development Environment

### Python Environment Setup

This project uses `uv` for Python environment management:

```bash
# Create/activate virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows

# Install dependencies (when available)
uv pip install -r requirements.txt
```

### Running Code

Always ensure you're in the correct Python environment before executing or testing:

```bash
# Switch to project environment
uv venv
source .venv/bin/activate

# Run Python scripts
python <script_name>.py
```

## Code Modification Guidelines

When modifying existing code:
1. **Comment out old code** instead of deleting it
2. **Add explanatory comments** about what changed and why
3. This allows easy tracking and rollback if needed

Example:
```python
# Original implementation - commented out on 2025-11-29
# Reason: Optimizing performance by using pandas instead of manual iteration
# def process_resume(file_path):
#     with open(file_path) as f:
#         return f.read()

# New implementation
import pandas as pd
def process_resume(file_path):
    return pd.read_csv(file_path)
```

## Project Structure

```
resumexlab/
├── script/          # Utility scripts and tools
├── .venv/          # Virtual environment (not committed)
└── CLAUDE.md       # This file
```

Place any utility or helper scripts in the `script/` directory for organization.

## Testing and Development

- Keep testing steps simple and efficient to minimize token usage
- Delete test programs after completion
- Think through implementation before executing to reduce iterations

## Version Control

This project is not yet initialized as a git repository. To set up version control:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repository-url>
git push -u origin main
```

For pushing to GitHub and resolving conflicts, standard git workflows apply.

## Notes for Claude Code

- Always use `uv` commands for Python environment management
- Do not create documentation files unless specifically requested
- Simplify testing procedures when possible
- Place scripts in the `script/` directory
- Preserve original code as comments when making modifications


# 個人履歷網站系統需求規格書 (SRS)
## Software Requirements Specification

**專案名稱**: 個人履歷管理系統  
**版本**: 1.0  
**日期**: 2025年11月  
**作者**: Polo (林鴻全)

---

## 1. 專案概述 (Project Overview)

### 1.1 專案目標
建立一個全端 (Full-Stack) 個人履歷管理系統，提供線上履歷展示與後台編輯功能，支援中英文雙語切換，並能即時更新履歷內容。

### 1.2 專案範圍
- 前端使用 Vue 3 開發響應式網頁介面
- 後端使用 FastAPI 提供 RESTful API
- 使用 SQLite 資料庫儲存履歷資料
- 支援中文/英文雙語切換
- 提供履歷資料的 CRUD (新增、讀取、更新、刪除) 功能

---

## 2. 系統架構 (System Architecture)

### 2.1 技術堆疊

#### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **狀態管理**: Pinia
- **路由**: Vue Router
- **UI 框架**: Element Plus / Vuetify / Tailwind CSS
- **HTTP 客戶端**: Axios
- **國際化**: Vue I18n

#### 後端 (Backend)
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **資料驗證**: Pydantic
- **認證**: JWT (JSON Web Token)
- **CORS**: FastAPI CORS Middleware

#### 資料庫 (Database)
- **類型**: SQLite
- **版本控制**: Alembic (資料庫遷移工具)

#### 開發工具
- **前端**: Vite
- **後端**: Uvicorn (ASGI 伺服器)
- **API 文件**: FastAPI 自動生成 (Swagger UI / ReDoc)

### 2.2 系統架構圖

```
┌─────────────────────────────────────────┐
│          使用者瀏覽器 (Browser)          │
└────────────────┬────────────────────────┘
                 │
                 │ HTTP/HTTPS
                 ▼
┌─────────────────────────────────────────┐
│       前端 (Vue 3 Application)          │
│  - 履歷展示頁面                          │
│  - 管理後台                              │
│  - 多語言切換                            │
└────────────────┬────────────────────────┘
                 │
                 │ RESTful API
                 ▼
┌─────────────────────────────────────────┐
│       後端 (FastAPI Server)             │
│  - API 路由                              │
│  - 業務邏輯                              │
│  - 資料驗證                              │
│  - 認證授權                              │
└────────────────┬────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 ▼
┌─────────────────────────────────────────┐
│       資料庫 (SQLite Database)          │
│  - 個人資訊                              │
│  - 工作經歷                              │
│  - 教育背景                              │
│  - 專案經驗                              │
│  - 技能證照                              │
└─────────────────────────────────────────┘
```

---

## 3. 功能需求 (Functional Requirements)

### 3.1 前台功能 (Public Features)

#### F1: 履歷展示頁面
- **描述**: 以專業格式展示個人履歷
- **優先級**: 高
- **需求細項**:
  - F1.1: 顯示個人基本資訊 (姓名、聯絡方式、目標)
  - F1.2: 顯示個性特質與摘要
  - F1.3: 顯示工作經歷列表（包含公司、職位、時間、專案描述）
  - F1.4: 顯示教育背景
  - F1.5: 顯示證照與語言能力
  - F1.6: 顯示學術著作
  - F1.7: 顯示 GitHub 專案連結
  - F1.8: 響應式設計 (支援手機、平板、桌面)

#### F2: 多語言切換
- **描述**: 支援中文/英文語言切換
- **優先級**: 高
- **需求細項**:
  - F2.1: 語言切換按鈕（旗幟圖示或下拉選單）
  - F2.2: 切換後即時更新頁面內容
  - F2.3: 記憶使用者語言偏好 (LocalStorage)

#### F3: PDF 匯出功能
- **描述**: 將履歷匯出為 PDF 格式
- **優先級**: 中
- **需求細項**:
  - F3.1: 點擊按鈕下載 PDF
  - F3.2: PDF 格式與網頁呈現一致

### 3.2 後台管理功能 (Admin Features)

#### F4: 使用者認證
- **描述**: 管理者登入系統
- **優先級**: 高
- **需求細項**:
  - F4.1: 登入頁面（帳號、密碼）
  - F4.2: JWT Token 認證
  - F4.3: 登出功能
  - F4.4: Session 過期處理

#### F5: 個人資訊管理
- **描述**: 編輯基本個人資訊
- **優先級**: 高
- **需求細項**:
  - F5.1: 編輯姓名（中英文）
  - F5.2: 編輯聯絡資訊（電話、Email、地址）
  - F5.3: 編輯職涯目標（中英文）
  - F5.4: 編輯個性描述（中英文）
  - F5.5: 編輯專業摘要（中英文）

#### F6: 工作經歷管理
- **描述**: 管理工作經驗資料
- **優先級**: 高
- **需求細項**:
  - F6.1: 新增工作經歷
  - F6.2: 編輯工作經歷（公司名稱、職位、時間、地點、描述）
  - F6.3: 刪除工作經歷
  - F6.4: 調整工作經歷順序
  - F6.5: 支援中英文內容

#### F7: 專案經驗管理
- **描述**: 管理專案經驗資料
- **優先級**: 高
- **需求細項**:
  - F7.1: 新增專案
  - F7.2: 編輯專案（名稱、描述、技術堆疊、時間）
  - F7.3: 刪除專案
  - F7.4: 支援子項目列表（bullet points）
  - F7.5: 支援中英文內容

#### F8: 教育背景管理
- **描述**: 管理學歷資料
- **優先級**: 高
- **需求細項**:
  - F8.1: 新增學歷
  - F8.2: 編輯學歷（學校、科系、學位、時間、專案）
  - F8.3: 刪除學歷
  - F8.4: 支援中英文內容

#### F9: 證照與技能管理
- **描述**: 管理證照與語言能力
- **優先級**: 中
- **需求細項**:
  - F9.1: 新增證照
  - F9.2: 編輯證照資訊
  - F9.3: 刪除證照
  - F9.4: 管理語言能力（語言、級別、分數）

#### F10: 著作與專案連結管理
- **描述**: 管理學術著作與 GitHub 專案
- **優先級**: 中
- **需求細項**:
  - F10.1: 新增學術著作
  - F10.2: 編輯著作資訊
  - F10.3: 刪除著作
  - F10.4: 管理 GitHub 專案連結

---

## 4. 非功能需求 (Non-Functional Requirements)

### 4.1 效能需求 (Performance)
- NFR1: 頁面載入時間應小於 3 秒
- NFR2: API 回應時間應小於 500ms
- NFR3: 支援至少 100 個並發使用者

### 4.2 安全性需求 (Security)
- NFR4: 使用 HTTPS 加密通訊
- NFR5: 密碼需使用 bcrypt 雜湊儲存
- NFR6: JWT Token 有效期限為 24 小時
- NFR7: 實施 CORS 政策防止跨站請求
- NFR8: SQL Injection 防護 (使用 ORM)

### 4.3 可用性需求 (Usability)
- NFR9: 介面需直覺易用
- NFR10: 支援常見瀏覽器（Chrome, Firefox, Safari, Edge）
- NFR11: 響應式設計 (Mobile-first)

### 4.4 可維護性需求 (Maintainability)
- NFR12: 程式碼需符合 PEP 8 (Python) 和 ESLint (JavaScript) 規範
- NFR13: 關鍵功能需有單元測試覆蓋率 > 70%
- NFR14: API 需有完整文件 (Swagger/ReDoc)

### 4.5 可擴展性需求 (Scalability)
- NFR15: 資料庫設計需支援未來擴展其他語言
- NFR16: 模組化設計，便於新增功能

---

## 5. 資料庫設計 (Database Design)

### 5.1 資料表結構

#### 5.1.1 使用者表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.2 個人資訊表 (personal_info)
```sql
CREATE TABLE personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_zh VARCHAR(100),
    name_en VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address_zh TEXT,
    address_en TEXT,
    objective_zh TEXT,
    objective_en TEXT,
    personality_zh TEXT,
    personality_en TEXT,
    summary_zh TEXT,
    summary_en TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.3 工作經歷表 (work_experience)
```sql
CREATE TABLE work_experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_zh VARCHAR(200),
    company_en VARCHAR(200),
    position_zh VARCHAR(100),
    position_en VARCHAR(100),
    location_zh VARCHAR(100),
    location_en VARCHAR(100),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    description_zh TEXT,
    description_en TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.4 專案經驗表 (projects)
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_experience_id INTEGER,
    title_zh VARCHAR(200),
    title_en VARCHAR(200),
    description_zh TEXT,
    description_en TEXT,
    technologies TEXT,  -- JSON 格式儲存技術堆疊
    tools TEXT,  -- JSON 格式儲存工具
    environment TEXT,  -- JSON 格式儲存環境
    start_date DATE,
    end_date DATE,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (work_experience_id) REFERENCES work_experience(id)
);
```

#### 5.1.5 專案細節表 (project_details)
```sql
CREATE TABLE project_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    detail_zh TEXT,
    detail_en TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

#### 5.1.6 教育背景表 (education)
```sql
CREATE TABLE education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_zh VARCHAR(200),
    school_en VARCHAR(200),
    degree_zh VARCHAR(100),
    degree_en VARCHAR(100),
    major_zh VARCHAR(100),
    major_en VARCHAR(100),
    start_date DATE,
    end_date DATE,
    description_zh TEXT,
    description_en TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.7 證照表 (certifications)
```sql
CREATE TABLE certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_zh VARCHAR(200),
    name_en VARCHAR(200),
    issuer VARCHAR(200),
    issue_date DATE,
    certificate_number VARCHAR(100),
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.8 語言能力表 (languages)
```sql
CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language_zh VARCHAR(50),
    language_en VARCHAR(50),
    proficiency_zh VARCHAR(50),
    proficiency_en VARCHAR(50),
    test_name VARCHAR(100),
    score VARCHAR(50),
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.9 學術著作表 (publications)
```sql
CREATE TABLE publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    authors TEXT,
    publication TEXT,
    year INTEGER,
    pages VARCHAR(50),
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.1.10 GitHub 專案表 (github_projects)
```sql
CREATE TABLE github_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_zh VARCHAR(200),
    name_en VARCHAR(200),
    description_zh TEXT,
    description_en TEXT,
    url TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. API 設計 (API Design)

### 6.1 認證相關 API

| 方法 | 端點 | 描述 |
|------|------|------|
| POST | /api/auth/login | 使用者登入 |
| POST | /api/auth/logout | 使用者登出 |
| GET | /api/auth/verify | 驗證 Token |

### 6.2 個人資訊 API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/personal-info | 獲取個人資訊 |
| PUT | /api/personal-info | 更新個人資訊 |

### 6.3 工作經歷 API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/work-experience | 獲取所有工作經歷 |
| GET | /api/work-experience/{id} | 獲取特定工作經歷 |
| POST | /api/work-experience | 新增工作經歷 |
| PUT | /api/work-experience/{id} | 更新工作經歷 |
| DELETE | /api/work-experience/{id} | 刪除工作經歷 |

### 6.4 專案經驗 API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/projects | 獲取所有專案 |
| GET | /api/projects/{id} | 獲取特定專案 |
| POST | /api/projects | 新增專案 |
| PUT | /api/projects/{id} | 更新專案 |
| DELETE | /api/projects/{id} | 刪除專案 |

### 6.5 教育背景 API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/education | 獲取所有教育背景 |
| POST | /api/education | 新增教育背景 |
| PUT | /api/education/{id} | 更新教育背景 |
| DELETE | /api/education/{id} | 刪除教育背景 |

### 6.6 證照與語言 API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/certifications | 獲取所有證照 |
| POST | /api/certifications | 新增證照 |
| PUT | /api/certifications/{id} | 更新證照 |
| DELETE | /api/certifications/{id} | 刪除證照 |
| GET | /api/languages | 獲取所有語言能力 |
| POST | /api/languages | 新增語言能力 |
| PUT | /api/languages/{id} | 更新語言能力 |
| DELETE | /api/languages/{id} | 刪除語言能力 |

### 6.7 著作與 GitHub API

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | /api/publications | 獲取所有著作 |
| POST | /api/publications | 新增著作 |
| PUT | /api/publications/{id} | 更新著作 |
| DELETE | /api/publications/{id} | 刪除著作 |
| GET | /api/github-projects | 獲取所有 GitHub 專案 |
| POST | /api/github-projects | 新增 GitHub 專案 |
| PUT | /api/github-projects/{id} | 更新 GitHub 專案 |
| DELETE | /api/github-projects/{id} | 刪除 GitHub 專案 |

---

## 7. 前端路由設計 (Frontend Routes)

| 路徑 | 組件 | 描述 | 權限 |
|------|------|------|------|
| / | ResumeView | 履歷展示頁面 | 公開 |
| /admin/login | LoginView | 登入頁面 | 公開 |
| /admin/dashboard | DashboardView | 管理後台首頁 | 需認證 |
| /admin/personal | PersonalInfoEdit | 個人資訊編輯 | 需認證 |
| /admin/work-experience | WorkExperienceEdit | 工作經歷管理 | 需認證 |
| /admin/projects | ProjectsEdit | 專案經驗管理 | 需認證 |
| /admin/education | EducationEdit | 教育背景管理 | 需認證 |
| /admin/certifications | CertificationsEdit | 證照管理 | 需認證 |
| /admin/publications | PublicationsEdit | 著作管理 | 需認證 |

---

## 8. 使用者介面設計 (UI Design)

### 8.1 前台設計要點
- 採用專業履歷樣式，參照 PDF 格式
- 使用清晰的版面配置與適當的留白
- 字體：標題使用較大字體，內文使用易讀字體
- 配色：專業色系（如深藍、灰色、白色）
- 響應式設計：
  - 桌面版：雙欄或單欄佈局
  - 平板版：單欄佈局
  - 手機版：堆疊式佈局

### 8.2 後台設計要點
- 使用管理後台模板（如 Element Plus Admin）
- 側邊導航選單
- 表單驗證與錯誤提示
- 確認對話框（刪除操作）
- 載入狀態提示

---

## 9. 開發階段規劃 (Development Phases)

### Phase 1: 基礎架構建置（第 1-2 週）
- 專案初始化（Vue 3 + FastAPI）
- 資料庫設計與建立
- 基本 API 框架
- 認證系統實作

### Phase 2: 核心功能開發（第 3-5 週）
- 個人資訊 CRUD
- 工作經歷 CRUD
- 專案經驗 CRUD
- 教育背景 CRUD

### Phase 3: 進階功能開發（第 6-7 週）
- 證照與語言管理
- 著作與 GitHub 專案管理
- 多語言系統整合
- PDF 匯出功能

### Phase 4: 前端介面優化（第 8-9 週）
- 履歷展示頁面設計
- 管理後台介面優化
- 響應式設計調整
- 使用者體驗優化

### Phase 5: 測試與部署（第 10 週）
- 單元測試
- 整合測試
- 效能測試
- 部署至正式環境

---

## 10. 測試計畫 (Testing Plan)

### 10.1 單元測試
- 後端 API 邏輯測試（使用 pytest）
- 前端組件測試（使用 Vitest）

### 10.2 整合測試
- API 端點測試
- 前後端整合測試

### 10.3 使用者測試
- 功能測試
- 跨瀏覽器測試
- 響應式設計測試

---

## 11. 部署規劃 (Deployment Plan)

### 11.1 開發環境
- 本地開發伺服器
- SQLite 資料庫

### 11.2 正式環境
- **前端**: Netlify / Vercel / GitHub Pages
- **後端**: Railway / Render / PythonAnywhere
- **資料庫**: SQLite（小型專案）或遷移至 PostgreSQL（擴展需求）

### 11.3 CI/CD
- GitHub Actions 自動化測試與部署
- 版本控制：Git

---

## 12. 風險評估 (Risk Assessment)

| 風險 | 影響 | 可能性 | 應對策略 |
|------|------|--------|----------|
| 資料庫效能不足 | 高 | 低 | 監控效能，必要時遷移至 PostgreSQL |
| 安全性漏洞 | 高 | 中 | 定期安全審查，使用最佳實踐 |
| 開發時程延遲 | 中 | 中 | 敏捷開發，逐步交付功能 |
| 跨瀏覽器兼容性問題 | 中 | 低 | 早期進行跨瀏覽器測試 |

---

## 13. 維護計畫 (Maintenance Plan)

### 13.1 日常維護
- 定期備份資料庫
- 監控系統效能
- 安全性更新

### 13.2 功能擴展
- 新增更多語言支援
- 整合社群媒體連結
- 訪客留言功能
- 履歷分析統計

---

## 14. 參考文件 (References)

- [Vue 3 官方文件](https://vuejs.org/)
- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文件](https://www.sqlalchemy.org/)
- [Element Plus 官方文件](https://element-plus.org/)
- [JWT 認證最佳實踐](https://jwt.io/introduction)

---

## 15. 附錄 (Appendix)

### 15.1 資料模型範例 (JSON)

#### 個人資訊
```json
{
  "name_zh": "林鴻全",
  "name_en": "Hung Chuan Lin",
  "phone": "0926-593-172",
  "email": "sprigga@gmail.com",
  "address_zh": "台南市安南區北安路三段305巷3號4樓之1",
  "address_en": "4F.-1, No. 3, Ln. 305, Pei'an Rd., Annan Dist., Tainan City 709004",
  "objective_zh": "尋求資訊工程師或測試工程師職位...",
  "objective_en": "Seeking a position as an IT Customer Engineer..."
}
```

#### 工作經歷
```json
{
  "company_zh": "鴻海科技集團",
  "company_en": "Hon Hai Technology Group",
  "position_zh": "專案工程師",
  "position_en": "Project Engineer",
  "location_zh": "台灣新竹",
  "location_en": "Hsinchu, Taiwan",
  "start_date": "2017-11-01",
  "end_date": null,
  "is_current": true,
  "description_zh": "負責印表機、醫療設備、EV車載系統等專案...",
  "description_en": "Spearheaded software development and system testing..."
}
```

---

**文件版本歷史**

| 版本 | 日期 | 作者 | 變更說明 |
|------|------|------|----------|
| 1.0 | 2025-11-29 | Polo | 初版建立 |

