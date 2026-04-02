# 解決 Alembic "Can't locate revision" 錯誤

## 修改日期
2026-04-02（初始）→ 2026-04-02（加入自動修復防護）

---

## 問題描述

Backend 容器啟動後不斷重啟，Docker log 顯示：

```
ERROR [alembic.util.messaging] Can't locate revision identified by 'ce10aaa23747'
FAILED: Can't locate revision identified by 'ce10aaa23747'
```

容器因 entrypoint 執行 `alembic upgrade head` 失敗而退出，形成重啟迴圈。

---

## 根本原因

Migration `ce10aaa23747`（添加附件欄位到 work_experience 和 projects 表）已被合併（squash）進 `d711f173f9e3`（初始化資料庫表），並從檔案系統中刪除。

然而資料庫中的 `alembic_version` 表仍記錄舊的 revision ID `ce10aaa23747`，導致 Alembic 找不到對應的 migration 檔案。

**這是典型的「squash 後未更新 DB 版本指標」問題**：squash migration 時必須同步更新所有現有環境的 `alembic_version`，否則下次執行 `alembic upgrade head` 就會失敗。

---

## 影響範圍

- Backend 容器無法啟動，API 完全不可用
- 因為 entrypoint 一失敗就退出，容器無法長時間運行以供 `docker exec` 進入
- **生產環境風險**：若 GCP 上的 DB `alembic_version` 仍記錄 `ce10aaa23747`，佈署時會觸發相同的重啟迴圈

---

## 解決方案

### 修正一：手動修復（已完成）

透過直接更新 DB 的 `alembic_version` 表，將版本指標從 `ce10aaa23747` 改為 `d711f173f9e3`。

#### 前提：DB 是 bind mount，可直接從 host 修改

透過 `docker inspect` 確認：

```bash
docker inspect resumexlab-backend --format '{{json .Mounts}}'
# Source: /Users/pololin/python_project/resumexlab/backend/data
# -> 容器內 /app/data
```

#### Step 1：停止容器並關閉自動重啟

```bash
docker stop resumexlab-backend
docker update --restart=no resumexlab-backend
```

#### Step 2：直接從 host 更新 DB 版本指標

```bash
# 確認當前版本（應為 ce10aaa23747）
sqlite3 /Users/pololin/python_project/resumexlab/backend/data/resume.db \
  "SELECT * FROM alembic_version;"

# 更新為現存的 head revision
sqlite3 /Users/pololin/python_project/resumexlab/backend/data/resume.db \
  "UPDATE alembic_version SET version_num = 'd711f173f9e3';"

# 驗證
sqlite3 /Users/pololin/python_project/resumexlab/backend/data/resume.db \
  "SELECT * FROM alembic_version;"
# 應輸出：d711f173f9e3
```

#### Step 3：恢復重啟策略並啟動容器

```bash
docker update --restart=unless-stopped resumexlab-backend
docker start resumexlab-backend
```

#### Step 4：確認成功

```bash
docker logs resumexlab-backend --tail 20
# 應看到：
# === Migration Complete ===
# === Starting Application ===
# INFO: Uvicorn running on http://0.0.0.0:8000
```

---

### 修正二：自動修復防護（已實作）

手動修復是一次性的，為了防止此問題在任何環境（本地、GCP 生產）再次發生，在 entrypoint 中加入 revision guard。

#### 為何不用 `alembic stamp head` 自動修復

`stamp` 內部也會從 `alembic_version` 記錄的 revision 開始解析 migration 鍊。當 revision 檔案不存在時，`stamp` 和 `upgrade` 一樣會報 "Can't locate revision" 失敗。因此必須直接用 SQL 更新 `alembic_version` 表，繞過 Alembic 自己的鏈驗證。

#### 新增檔案：`backend/alembic_guard.py`

獨立的 Python 腳本，在 `alembic upgrade head` 前執行：

1. 讀取 DB 的 `alembic_version`
2. 檢查該 revision 是否有對應的 `.py` migration 檔案
3. 若找不到 → 解析 `alembic/versions/` 目錄找出 head revision → 直接用 SQL 更新 DB
4. 若找到 → 靜默通過，不做任何事

用法：`python3 alembic_guard.py <db_path> <versions_dir>`

#### 修改檔案：`backend/entrypoint.sh`

在 `alembic upgrade head` 之前加入一行：

```bash
# --- Alembic revision guard ---
# 修改日期: 2026-04-02
python3 /app/alembic_guard.py /app/data/resume.db /app/alembic/versions
# --- End revision guard ---
```

#### 為何用獨立 Python 腳本而非 inline shell

在 shell script 中嵌入多行 Python 會遇到嚴重的引號轉義問題（shell 的 `'`、`"`、`\` 和 Python 的 regex `[]`、`\w` 互相衝突）。獨立的 `.py` 檔案避免了這個問題，同時也更容易維護。

#### 驗證結果

| 測試情境 | 結果 |
|---------|------|
| 正常路徑（revision 一致） | 靜默通過，正常啟動 |
| 壞路徑（revision 斷鏈 `ce10aaa23747`） | 自動修正為 `d711f173f9e3`，正常啟動，不重啟迴圈 |

---

## 替代方案

若資料不重要，或有完整備份，可選擇清除 volume 重建：

```bash
# ⚠️ 會清除所有資料
docker-compose down -v
docker-compose up -d --build
```

---

## 預防措施

1. **自動防護（已實作）**：`entrypoint.sh` 中的 `alembic_guard.py` 會在每次容器啟動時檢查 revision 一致性，自動修復斷鏈
2. **手動預防**：執行 migration squash 後，必須對所有現有環境的資料庫執行版本更新：

```sql
UPDATE alembic_version SET version_num = '<new_head_revision>';
```

或使用 Alembic stamp 指令（需在可進入的環境中執行）：

```bash
alembic stamp <new_head_revision>
```

---

## 相關檔案

- `backend/alembic/versions/d711f173f9e3_初始化資料庫表.py` — 現存的唯一 migration，包含原 `ce10aaa23747` 的附件欄位內容
- `backend/data/resume.db` — SQLite 資料庫（bind mount）
- `backend/entrypoint.sh` — 容器啟動腳本，包含 revision guard 呼叫
- `backend/alembic_guard.py` — Revision guard 腳本，檢查並自動修復 revision 斷鏈
- `docs/superpowers/specs/2026-04-02-alembic-revision-guard-design.md` — 自動防護的設計文件
