FROM python:3.9-slim
WORKDIR /app
COPY task_manager.py user.txt tasks.txt /app/
CMD ["python", "task_manager.py"]