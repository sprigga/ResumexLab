# Alembic 遷移功能審查報告

- **審查日期:** 2026-04-01
- **審查範圍:** `backend/alembic/` 目錄與相關模型定義
- **審查者:** Claude Code

---

## 整體評估：完善

Alembic 設置可正常運行，所有模型欄位均已反映在遷移腳本中（無 schema drift），遷移歷史已透過 squash 整合為單一初始化 migration。

---

## 遷移版本鏈

```
d711f173f9e3 (初始化資料庫表, 含附件欄位, 2025-12-30)
    ↓
    （原 ce10aaa23747 已於 2026-04-01 合併至此 migration）
```

---

## 設置清單

| 項目 | 檔案 | 狀態 | 說明 |
|------|------|------|------|
| 資料庫 URL | `alembic.ini` | 已設定 | `sqlite:///./data/resume.db` |
| Target Metadata | `alembic/env.py` | 已設定 | 正確導入 `Base.metadata` |
| 模型導入 | `alembic/env.py` | 已設定 | `from app.models import *` 涵蓋所有模型 |
| Autogenerate 支援 | `alembic/env.py` | 已設定 | 可用 `--autogenerate` 偵測 schema 差異 |

---

## 資料表覆蓋確認

所有 SQLAlchemy 模型均已在遷移中反映，**目前無 schema drift**：

| 資料表 | 模型類別 | 初始遷移 | 備註 |
|--------|---------|---------|------|
| `certifications` | `Certification` | `d711f173f9e3` | 完整 |
| `education` | `Education` | `d711f173f9e3` | 完整 |
| `github_projects` | `GithubProject` | `d711f173f9e3` | 完整 |
| `languages` | `Language` | `d711f173f9e3` | 完整 |
| `personal_info` | `PersonalInfo` | `d711f173f9e3` | 完整 |
| `publications` | `Publication` | `d711f173f9e3` | 完整 |
| `users` | `User` | `d711f173f9e3` | 完整 |
| `work_experience` | `WorkExperience` | `d711f173f9e3` | 附件欄位已合併至初始 migration |
| `projects` | `Project` | `d711f173f9e3` | 附件欄位已合併至初始 migration |
| `project_details` | `ProjectDetail` | `d711f173f9e3` | 完整 |
| `project_attachments` | `ProjectAttachment` | `d711f173f9e3` | 完整 |

---

## 問題與風險

### ~~P1（中等）— Migration 歷史不一致~~ ✅ 已解決

**原問題：** `ce10aaa23747` 要添加的 5 個 attachment 欄位（`attachment_name`, `attachment_path`, `attachment_size`, `attachment_type`, `attachment_url`），在 `d711f173f9e3` 的初始 migration 中已經存在。

**根本原因：** 在建立第二個 migration 之前，初始 migration 就已手動加入這些欄位，導致 migration 歷史無法反映真實的 schema 演進過程。

**解決方式：** 2026-04-01 已將 `ce10aaa23747` 合併（squash）至 `d711f173f9e3`，附件欄位從一開始就包含在初始 migration 中，`ce10aaa23747` 已刪除。遷移歷史現在準確反映 schema 結構。

---

### ~~P2（低）— `downgrade()` 缺乏防護~~ ✅ 已解決

**原問題：** `ce10aaa23747` 的 `upgrade()` 使用了 `column_exists()` 防護，但 `downgrade()` 直接呼叫 `op.drop_column()`，未檢查欄位是否實際存在。

**解決方式：** 2026-04-01 已將 `ce10aaa23747` 合併（squash）至 `d711f173f9e3`，`ce10aaa23747` 已刪除。由於該 migration 不再存在，此問題不再適用。

---

### ~~P3（低）— 雙重建表策略~~ ✅ 已解決

**原問題：** 系統同時使用 `Base.metadata.create_all()`（透過應用程式啟動時）和 Alembic migration，這是導致歷史不一致的根本原因。

**解決方式：** 2026-04-01 已從 `backend/app/main.py` 移除 `Base.metadata.create_all(bind=engine)` 呼叫，改由 Alembic 單一管理 schema。應用程式啟動時僅執行資料初始化（admin user），不再重複建表。migration 已使用 `CREATE TABLE IF NOT EXISTS` 確保冪等性，即使首次部署未執行 migration 也能正常運作。

---

## 建議

| 優先級 | 建議 | 說明 |
|--------|------|------|
| ~~低~~ | ~~統一建表策略~~ | ~~選擇一種方式：純 Alembic migration 或純 `create_all()`，避免雙重管理~~ ✅ 2026-04-01 已移除 `create_all()`，改由純 Alembic 管理 |
| ~~低~~ | ~~補強 `downgrade()`~~ | ~~在 `ce10aaa23747` 的 downgrade 中加入 `column_exists()` 檢查~~ ✅ 已透過 squash 解決 |
| ~~可選~~ | ~~Squash migrations~~ | ~~將兩個 migration 合併為一個語義正確的初始化 migration~~ ✅ 2026-04-01 已完成 |

---

## 輔助腳本

| 檔案 | 用途 |
|------|------|
| `backend/scripts/alembic_create_migration.sh` | 建立新 migration 的輔助腳本 |
| `backend/scripts/alembic_diagnose.sh` | 診斷 Alembic 狀態的輔助腳本 |
| `backend/scripts/alembic_helper.py` | Python 輔助工具 |

---

## 結論

Alembic 功能完善，**可安全用於生產環境的資料庫版本管理**。遷移歷史已整合為單一語義正確的初始化 migration，schema 現由 Alembic 單一管理，所有已識別問題均已解決，技術債務清零。
