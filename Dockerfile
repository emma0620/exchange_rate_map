FROM python:3.12

# 設定工作目錄
WORKDIR /code

# 複製 requirements.txt 文件
COPY requirements.txt .

# 安裝依賴
RUN pip install -r requirements.txt

# 複製應用程式代碼
COPY . .

# 啟動 Django 應用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]