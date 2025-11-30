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

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 建立資料庫目錄
RUN mkdir -p /app/data

# 暴露 API 端口
EXPOSE 8000

# 啟動應用
# 使用 uvicorn 運行 FastAPI 應用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
