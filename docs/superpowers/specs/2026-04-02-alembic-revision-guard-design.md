# Alembic Revision Guard — Entrypoint 預檢 + 容錯

## 修改日期
2026-04-02

---

## 問題描述

當 migration 被 squash 並刪除舊檔案後，DB 的 `alembic_version` 表仍指向舊 revision ID。
容器啟動時 `entrypoint.sh` 執行 `alembic upgrade head` 失敗，導致重啟迴圈。

## 解決方案

在 `backend/entrypoint.sh` 中，`alembic upgrade head` 之前加入預檢：
讀取 DB 的 `alembic_version`，檢查該 revision 是否存在於 `alembic/versions/` 目錄。
若不存在，自動執行 `alembic stamp head` 修正版本指標，再繼續 migration。

## 修改範圍

僅修改 `backend/entrypoint.sh`。

## 設計

### 流程

```
容器啟動
  → sleep 1（等待檔案系統就緒）
  → 讀取 DB 的 alembic_version
  → 檢查該 revision 是否有對應的 .py 檔案
  → 如果找不到：
      → 印出警告 log（revision ID、版本將被 stamp 到的 head）
      → alembic stamp head
  → alembic upgrade head
  → 啟動應用
```

### 實作細節

1. 用 Python one-liner 讀取 `alembic_version`（不額外依賴 sqlite3 CLI）
2. 用 `ls alembic/versions/<revision>*.py` 確認檔案存在
3. 只處理 revision 找不到的情況，其他錯誤正常失敗
4. 所有動作印出明確 log 方便運維追蹤

### 不做的事

- 不修改 migration 檔案
- 不改 docker-compose.yml volume 設計
- 不加 CI/CD 檢查腳本
