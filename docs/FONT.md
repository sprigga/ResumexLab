# 網站字體設定文件

**專案**: ResumeXLab 個人履歷管理系統
**文件版本**: 1.0
**更新日期**: 2025-12-25
**作者**: Polo (林鴻全)

---

## 目錄

1. [字體族設定](#字體族設定)
2. [字體大小設定](#字體大小設定)
3. [字體渲染設定](#字體渲染設定)
4. [各元素字體應用](#各元素字體應用)
5. [響應式字體調整](#響應式字體調整)
6. [代碼位置參考](#代碼位置參考)

---

## 字體族設定

### 全局字體族

```css
font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
```

**定義位置**:
- `/home/ubuntu/ResumexLab/frontend/src/style.css:2`
- `/home/ubuntu/ResumexLab/frontend/src/views/ResumeView.vue:317`

### 字體堆疊說明

| 優先級 | 字體名稱 | 類型 | 平台支援 | 說明 |
|--------|---------|------|---------|------|
| 1 | **system-ui** | 系統預設 | 所有平台 | 使用作業系統預設字體 |
| 2 | **Avenir** | 無襯線 | macOS | Apple 專業字體 |
| 3 | **Helvetica** | 無襯線 | 所有平台 | 經典無襯線字體 |
| 4 | **Arial** | 無襯線 | 所有平台 | 常見通用字體 |
| 5 | **sans-serif** | 通用備選 | 所有平台 | 系統無襯線字體 |

### 各平台 system-ui 實際字體

| 作業系統 | 中文字體 | 英文字體 |
|---------|---------|---------|
| **Windows** | 微軟正黑體、微軟雅黑 | Segoe UI |
| **macOS** | 蘋方、標楷體 | San Francisco |
| **Linux** | 文泉驛、黑體 | 各發行版預設 |
| **Android** | Noto Sans CJK | Roboto |
| **iOS/iPadOS** | 蘋方 | San Francisco |

### 字體特性

✅ **自動中英文支援**: `system-ui` 自動使用系統優化的中英文字體
✅ **跨平台一致性**: 在不同作業系統上顯示該平台原生字體
✅ **快速載入**: 無需下載外部字體檔案，載入速度快
✅ **優化混排**: 系統字體已優化中英文混排顯示效果

---

## 字體大小設定

### 網站標題（姓名）

| 項目 | 數值 | 單位 | 定義位置 |
|-----|------|------|---------|
| **桌面版標題** | 3.2 | em | `style.css:74`, `ResumeView.vue:429` |
| **手機版標題** | 28 | px | `ResumeView.vue:780` (媒體查詢) |

**CSS 代碼**:
```css
/* style.css */
h1 {
  font-size: 3.2em;
  line-height: 1.1;
  color: rgba(255, 255, 255, 0.95);
  font-weight: bold;
}

/* ResumeView.vue */
.contact-info-vertical .name {
  font-size: 3.2em;
  line-height: 1.1;
  font-weight: bold;
  margin: 0;
  padding: 0;
  color: rgba(255, 255, 255, 0.95);
  text-align: left;
}
```

### 主體內容字體大小

| 元素類型 | 字體大小 | 行高 | 顏色 | 定義位置 |
|---------|---------|------|------|---------|
| **段落文字** | 16px | 1.6 | rgba(255,255,255,0.87) | ResumeView.vue:512, 605 |
| **公司名稱** | 20px | - | #8FB8ED | ResumeView.vue:543 |
| **職位名稱** | 16px | - | #F5F5F5 | ResumeView.vue:561 |
| **日期/地點** | 14px | - | - | ResumeView.vue:586, 591 |
| **區段標題** | 24px | - | - | ResumeView.vue:497 |

### 標題層級字體大小

| 標題 | 字體大小 | 行高 | 字重 | 顏色 |
|-----|---------|------|------|------|
| **h1** | 3.2em | 1.1 | bold | rgba(255,255,255,0.95) |
| **h2** | 1.5em | 1.3 | bold | rgba(255,255,255,0.95) |
| **h3** | 1.25em | 1.4 | bold | #8FB8ED |
| **h4** | 1.1em | 1.4 | 600 | #8FB8ED |

### CSS 代碼範例

```css
/* 段落文字 */
.objective p,
.summary p {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
  font-size: 16px;
  text-align: left;
}

/* 描述文字 */
.description {
  color: rgba(255, 255, 255, 0.87) !important;
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 16px;
  text-align: left;
}

/* 公司名稱 */
.company {
  font-size: 20px;
  font-weight: bold;
  color: #8FB8ED !important;
  margin-bottom: 5px;
}

/* 職位名稱 */
.position {
  font-size: 16px;
  color: #F5F5F5 !important;
  font-weight: 500;
}

/* 日期 */
.date {
  font-size: 14px;
  margin-bottom: 3px;
}

/* 地點 */
.location {
  font-size: 14px;
}
```

---

## 字體渲染設定

### 全局字體渲染優化

```css
/* style.css */
:root {
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**設定說明**:

| 屬性 | 值 | 說明 |
|-----|---|------|
| `font-synthesis` | none | 不自動合成粗體和斜體 |
| `text-rendering` | optimizeLegibility | 優化文字可讀性 |
| `-webkit-font-smoothing` | antialiased | WebKit 瀏覽器抗鋸齒 |
| `-moz-osx-font-smoothing` | grayscale | Firefox macOS 灰階平滑 |

### 基礎字體屬性

```css
:root {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
}
```

---

## 各元素字體應用

### 聯絡資訊區

```css
.contact-info-vertical .name {
  font-size: 3.2em;
  line-height: 1.1;
  font-weight: bold;
}
```

### 專業摘要

```css
.objective p,
.summary p {
  font-size: 16px;
  line-height: 1.6;
}
```

### 工作經歷

```css
.company {
  font-size: 20px;
  font-weight: bold;
  color: #8FB8ED;
}

.position {
  font-size: 16px;
  font-weight: 500;
}

.date, .location {
  font-size: 14px;
}

.description {
  font-size: 16px;
  line-height: 1.6;
}
```

### 按鈕

```css
button {
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
}
```

### 連結

```css
a {
  font-weight: 500;
  color: #A8C5F0;
}
```

---

## 響應式字體調整

### 手機版調整

**觸發條件**: 螢幕寬度 ≤ 768px

```css
/* ResumeView.vue 媒體查詢 */
@media (max-width: 768px) {
  .contact-info-vertical .name {
    font-size: 28px; /* 從 3.2em 調整為固定 28px */
  }
}
```

### 調整說明

| 元素 | 桌面版 | 手機版 | 調整原因 |
|-----|-------|-------|---------|
| 姓名 | 3.2em (~51.2px) | 28px | 避免手機版字體過大 |
| 其他元素 | 保持原設定 | 保持原設定 | 響應式流式佈局自動調整 |

---

## 代碼位置參考

### 主要檔案

| 檔案路徑 | 說明 |
|---------|------|
| `/home/ubuntu/ResumexLab/frontend/src/style.css` | 全局樣式表 |
| `/home/ubuntu/ResumexLab/frontend/src/views/ResumeView.vue` | 履歷展示頁面組件 |

### 關鍵行號

| 檔案 | 行號 | 內容 |
|-----|------|------|
| `style.css` | 1-20 | 全局字體設定 |
| `style.css` | 73-100 | 標題樣式 (h1-h4) |
| `ResumeView.vue` | 317 | 字體族設定 |
| `ResumeView.vue` | 429 | 姓名標題字體 |
| `ResumeView.vue` | 497 | 區段標題字體 |
| `ResumeView.vue` | 512, 605 | 段落字體 |
| `ResumeView.vue` | 543 | 公司名稱字體 |
| `ResumeView.vue` | 561 | 職位名稱字體 |
| `ResumeView.vue` | 586, 591 | 日期地點字體 |
| `ResumeView.vue` | 780 | 手機版響應式字體 |

---

## 未來擴展建議

### 如果需要使用特定字體

可以使用 Google Fonts 或其他 Web Font 服務：

```css
/* 引入思源黑體 (Noto Sans TC) */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');

/* 更新字體族 */
font-family: 'Noto Sans TC', system-ui, Avenir, Helvetica, Arial, sans-serif;
```

### 推薦的中英文字體組合

| 組合 | 中文字體 | 英文字體 | 適用場景 |
|-----|---------|---------|---------|
| **系統預設** | system-ui | system-ui | 目前使用，快速載入 |
| **思源黑體** | Noto Sans TC | Roboto | 專業、現代 |
| **思源宋體** | Noto Serif TC | Merriweather | 傳統、學術 |
| **苹方** | PingFang TC | SF Pro | Apple 生態系統 |

---

## 附錄

### 字體大小換算參考

| em 單位 | 約等於 px (基於 16px) |
|---------|---------------------|
| 3.2em | 51.2px |
| 1.5em | 24px |
| 1.25em | 20px |
| 1.1em | 17.6px |
| 1em | 16px |

### 字重參考

| 數值 | 說明 | 用途 |
|-----|------|------|
| 400 | Regular (常規) | 正文 |
| 500 | Medium (中等) | 強調文字 |
| 600 | Semi-Bold (半粗) | 小標題 |
| 700 | Bold (粗體) | 大標題 |

---

**文件版本歷史**

| 版本 | 日期 | 作者 | 變更說明 |
|------|------|------|----------|
| 1.0 | 2025-12-25 | Polo | 初版建立，整理網站字體設定 |

---

**參考資源**

- [MDN - font-family](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family)
- [MDN - system-ui](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family#system-ui)
- [Google Fonts - Noto Sans TC](https://fonts.google.com/noto/specimen/Noto+Sans+TC)
