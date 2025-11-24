FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN uv sync
CMD ["py", "petstore.py"]