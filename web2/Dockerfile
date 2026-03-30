FROM python:3.9-slim
WORKDIR /app
RUN pip install flask
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py"]