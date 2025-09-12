FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
# اگر requirements.txt در ریشه‌ی ریپو است:
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
# کل پروژه را کپی می‌کنیم
COPY . /app
# نکته مهم: manage.py داخل پوشه backend است
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
