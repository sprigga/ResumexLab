# GitHub MCP Server 設定與疑難排解

本文檔記錄 GitHub MCP Server 的設定過程、遇到的問題及解決方案。

---

## 目錄

1. [問題描述](#問題描述)
2. [解決方案](#解決方案)
3. [驗證步驟](#驗證步驟)
4. [常見問題](#常見問題)

---

## 問題描述

### 錯誤訊息

```
Failed to reconnect to plugin:github:github.
```

### 問題原因

GitHub MCP Server 連線失敗，通常是因為：
1. GitHub Token 未設置或過期
2. Token 權限不足
3. 環境變數未正確載入

---

## 解決方案

### 方法 1: 使用 GitHub CLI 獲取 Token (推薦)

如果系統已安裝 GitHub CLI (`gh`)，可以使用現有的登入 token：

#### 步驟 1: 檢查 GitHub CLI 登入狀態

```bash
gh auth status
```

預期輸出：
```
github.com
  ✓ Logged in to github.com account <username> (/home/ubuntu/.config/gh/hosts.yml)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'admin:ssh_signing_key', 'gist', 'read:org', 'repo', 'workflow'
```

#### 步驟 2: 獲取 Token

```bash
gh auth token
```

輸出範例：
```
gho_youractualtokenhere1234567890abcdef
```

#### 步驟 3: 設置環境變數

**臨時設置（當前 session 有效）：**
```bash
export GITHUB_TOKEN="gho_youractualtokenhere1234567890abcdef"
```

**永久設置（推薦）：**

編輯 `~/.bashrc`：
```bash
nano ~/.bashrc
```

在檔案末尾添加：
```bash
# GitHub MCP Server Token
export GITHUB_TOKEN="gho_youractualtokenhere1234567890abcdef"
```

儲存後重新載入：
```bash
source ~/.bashrc
```

#### 步驟 4: 驗證設置

```bash
echo $GITHUB_TOKEN
```

應該顯示您的 token。

---

### 方法 2: 手動生成 GitHub Personal Access Token

如果未安裝 GitHub CLI，需要手動生成 token：

#### 步驟 1: 生成 Token

1. 前往 https://github.com/settings/tokens
2. 點擊 "Generate new token" → "Generate new token (classic)"
3. 設置名稱，例如 "Claude Code MCP"
4. 設置過期時間（建議選擇 "No expiration" 或較長時間）
5. 勾選權限：
   - `repo` - 完整儲存庫存取權限
   - `user` - 用戶資訊存取
   - `workflow` - 工作流程存取
6. 點擊 "Generate token"
7. **複製 token**（只顯示一次）

#### 步驟 2: 設置環境變數

參考 [方法 1 的步驟 3](#步驟-3-設置環境變數)

---

### 方法 3: 安裝 GitHub CLI (如果未安裝)

#### Linux (Ubuntu/Debian)

```bash
# 下載並安裝
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

#### macOS

```bash
brew install gh
```

#### Windows

```bash
winget install --id GitHub.cli
```

#### 登入 GitHub CLI

```bash
gh auth login
```

按照提示操作：
1. 選擇 `GitHub.com`
2. 選擇 `HTTPS` 協議
3. 選擇 `Login with a web browser`

---

## 驗證步驟

### 1. 驗證環境變數

```bash
echo $GITHUB_TOKEN
```

應該顯示您的 token。

### 2. 驗證 GitHub CLI

```bash
gh auth status
```

應該顯示已登入狀態。

### 3. 測試 MCP 連線

在 Claude Code 中執行：

```
/mcp
```

檢查 GitHub MCP Server 是否成功連線。

### 4. 測試 GitHub 操作

使用 MCP 工具測試：

```
# 列出儲存庫
# 查看分支
# 推送變更
```

---

## 常見問題

### Q1: Token 過期怎麼辦？

**解決方案：**

1. 重新生成 token（參考 [方法 2](#方法-2-手動生成-github-personal-access-token)）
2. 更新 `~/.bashrc` 中的 token
3. 執行 `source ~/.bashrc` 重新載入

### Q2: Token 權限不足

**症狀：**
- 無法推送變更
- 無法建立 Pull Request
- 權限錯誤訊息

**解決方案：**

檢查 token scopes：
```bash
gh auth token
# 然後前往 https://github.com/settings/tokens 驗證權限
```

必要權限：
- `repo` - 完整儲存庫存取
- `user` - 用戶資訊
- `workflow` - 工作流程

### Q3: 環境變數未生效

**症狀：**
- `echo $GITHUB_TOKEN` 顯示空白

**解決方案：**

1. 確認已編輯 `~/.bashrc`
2. 執行 `source ~/.bashrc`
3. 重新啟動終端機或 Claude Code

### Q4: MCP Server 仍然連線失敗

**解決方案：**

1. 確認 token 格式正確（以 `gho_` 或 `ghp_` 開頭）
2. 檢查網路連線
3. 重新啟動 Claude Code
4. 檢查 Claude Code 設定：
   ```json
   {
     "enabledPlugins": {
       "github@claude-plugins-official": true
     }
   }
   ```

### Q5: 多個 GitHub 帳號

**症狀：**
- GitHub CLI 顯示多個帳號
- MCP Server 使用錯誤的帳號

**解決方案：**

切換預設帳號：
```bash
gh auth switch -u <username>
```

或手動設置指定帳號的 token：
```bash
gh auth login
# 選擇要使用的帳號
```

---

## 安全建議

1. **不要將 token 提交到版本控制系統**
   - 將 `~/.bashrc` 加入 `.gitignore`
   - 使用環境變數而非硬編碼

2. **定期更新 token**
   - 建議每 6 個月更新一次
   - 如果懷疑洩漏，立即撤銷並重新生成

3. **使用最小權限原則**
   - 只授予必要的權限
   - 避免使用過度權限的 token

4. **監控 token 使用情況**
   - 定期檢查 https://github.com/settings/tokens
   - 撤銷不使用的 token

---

## 參考資源

- [GitHub CLI 官方文檔](https://cli.github.com/manual/)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [Claude Code MCP Server 文檔](https://docs.anthropic.com/claude-code/mcp-servers)
- [GitHub Authentication Best Practices](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)

---

**更新日期**: 2025-01-05
**作者**: Polo (林鴻全)
