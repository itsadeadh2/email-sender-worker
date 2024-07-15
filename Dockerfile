FROM python:3.12-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH='/app'

RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["src.lambda_function.handle"]
