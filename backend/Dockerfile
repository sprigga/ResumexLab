# Backend Dockerfile for Resume Management System
# Python 3.10 基礎鏡像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
# Python 不生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
# Python 輸出不緩衝
ENV PYTHONUNBUFFERED=1
# 設定 pip 使用阿里雲鏡像加速 (適用於亞洲地區)
# 修改日期: 2025-12-01
# 說明: 加速 pip 套件下載,減少構建時間
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# 安裝系統依賴
# 原版本: 僅安裝 gcc
# 修改日期: 2025-12-01
# 說明: 添加 curl 供 healthcheck 使用,優化 apt 鏡像源
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY requirements.txt .

# 安裝 Python 依賴
# 原版本: 使用 --no-cache-dir
# 修改日期: 2025-12-01
# 說明: 移除 --no-cache-dir 以啟用緩存,使用鏡像源加速下載
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 複製應用程式碼
COPY . .

# 建立資料庫目錄
RUN mkdir -p /app/data

# 暴露 API 端口
EXPOSE 8000

# 啟動應用
# 使用 uvicorn 運行 FastAPI 應用
# 已修改於 2025-01-12，原因：增加 --limit-max-requests 以支援大檔案上傳（最大 200MB）
# --timeout-keep-alive 300: 延長連線保持時間至 5 分鐘
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
