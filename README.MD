Код представляет собой асинхронный веб-сервер на базе aiohttp, который запускается на порту 8080 и обрабатывает GET запросы (например, к /test), генерируя JSON с данными о запросе(время, метод, endpoint, user-agent) Каждый запрос логируется в Elasticsearch (для ELK стека, индекс app_logs, просмотр в Kibana), сохраняется как JSON файл в AWS S3-бакет (путь logs/дата.json), а метрики (количество запросов, время обработки) экспортируются в Prometheus через /metrics и порт 8000 для визуализации в Grafana. 
Ошибки обрабатываются с логированием, сервер использует асинхронные клиенты для ES и S3

Установите зависимости через pip install aiohttp==3.9.1 elasticsearch==8.11.0 boto3==1.34.0 prometheus_client==0.20.0 на Windows может потребоваться Microsoft C++ Build Tools, настройте env-переменные: ES_HOST, S3_BUCKET, S3_REGION, AWS-ключи, запустите внешние сервисы (Elasticsearch, S3, Prometheus/Grafana), затем python main.py протестируйте curl http://localhost:8080/test, метрики на http://localhost:8000/metrics

git clone https://github.com/Keveray/asynchronous-web-server.git
Установите зависимости pip install -r requirements.txt с фиксом для Windows, если надо
Настройте env-переменные, запустите сервисы
Запустике python main.py

The code is an asynchronous web server based on aiohttp, which runs on port 8080 and handles GET requests (e.g., to /test), generating JSON with request data (time, method, endpoint, user-agent). Each request is logged to Elasticsearch (for the ELK stack, index 'app_logs', viewable in Kibana), saved as a JSON file in an AWS S3 bucket (path logs/date.json), and metrics (number of requests, processing time) are exported to Prometheus via /metrics and port 8000 for visualization in Grafana. Errors are handled with logging, and the server uses asynchronous clients for ES and S3.
Install dependencies via pip install aiohttp==3.9.1 elasticsearch==8.11.0 boto3==1.34.0 prometheus_client==0.20.0 (on Windows, Microsoft C++ Build Tools may be required), set env variables: ES_HOST, S3_BUCKET, S3_REGION, AWS keys, start external services (Elasticsearch, S3, Prometheus/Grafana), then run python main.py and test with curl http://localhost:8080/test, metrics at http://localhost:8000/metrics.
git clone https://github.com/Keveray/asynchronous-web-server.git
Install dependencies: pip install -r requirements.txt (with Windows fix if needed)
Set env variables, start services
Run: python main.py