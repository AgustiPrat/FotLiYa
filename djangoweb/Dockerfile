FROM astral/uv:python3.12-alpine

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml

RUN uv sync

COPY . .

EXPOSE 8080

CMD ["uv", "run", "python3", "manage.py", "runserver", "0.0.0.0:8080"]