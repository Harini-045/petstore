FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["py", "petstore.py"]