import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict
import aiohttp
from aiohttp import web
from elasticsearch import AsyncElasticsearch
import boto3
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_client import start_http_server
from config import ES_HOST, ES_INDEX, S3_BUCKET, S3_REGION, PROMETHEUS_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
REQUEST_COUNT = Counter('http_requests_total', 'Общее количество HTTP-запросов', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Длительность времени HTTP-запроса')
es_client = None
s3_client = None

async def init_clients(app):
    global es_client, s3_client
    es_client = AsyncElasticsearch([ES_HOST])
    s3_client = boto3.client('s3', region_name=S3_REGION)

async def cleanup_clients(app):
    if es_client:
        await es_client.close()
@REQUEST_DURATION.time()

async def handle_index(request):
    start_time = time.time()
    method = request.method
    endpoint = request.match_info.get('name', 'index') if request.match_info else 'index'
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    data = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'endpoint': endpoint,
        'user_agent': request.headers.get('User-Agent', 'неизвестно')
    }
    log_doc = {
        'timestamp': data['timestamp'],
        'level': 'INFO',
        'message': f'Запрос к {endpoint}',
        **data
    }
    try:
        await es_client.index(index=ES_INDEX, body=log_doc)
        logger.info(f"Лог отправлен в Elasticsearch: {log_doc}")
    except Exception as e:
        logger.error(f"Ошибка отправки в ES: {e}")
    s3_key = f"logs/{data['timestamp'].replace(':', '-')}.json"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        logger.info(f"Данные загружены в S3: {s3_key}")
    except Exception as e:
        logger.error(f"Ошибка загрузки в S3: {e}")
    duration = time.time() - start_time
    REQUEST_DURATION.observe(duration)
    return web.json_response(data)

async def handle_metrics(request):
    return web.Response(body=generate_latest(REGISTRY), content_type='text/plain')

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/{name}', handle_index)
    app.router.add_get('/metrics', handle_metrics)
    app.on_startup.append(init_clients)
    app.on_cleanup.append(cleanup_clients)
    return app

if __name__ == '__main__':
    start_http_server(PROMETHEUS_PORT)
    logger.info(f"Сервер метрик Prometheus запущен на порте {PROMETHEUS_PORT}")
    app = asyncio.run(init_app())
    web.run_app(app, host='localhost', port=8080)