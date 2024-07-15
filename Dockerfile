FROM 3.12-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH='/app'

RUN apt-get update && apt-get install -y wkhtmltopdf
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["src.lambda_function.handle"]
