FROM python:3.12-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH='/app'

RUN apt-get update && apt-get install -y wkhtmltopdf
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric
COPY . .
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["src.lambda_function.handle"]
