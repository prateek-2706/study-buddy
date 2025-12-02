FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["uvicorn", "fastapi_study_buddy.main:app", "--host", "0.0.0.0", "--port", "8000"]
