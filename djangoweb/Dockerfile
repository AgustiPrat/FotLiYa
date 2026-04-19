FROM astral/uv:python3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

EXPOSE 8080

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]