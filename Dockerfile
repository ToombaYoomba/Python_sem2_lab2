FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir typer

ENV PYTHONPATH=/app

ENTRYPOINT ["python3", "-m", "src.__main__"]

CMD ["--help"]