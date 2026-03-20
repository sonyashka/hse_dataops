from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps

# Определяем метрики

# Счетчики запросов
predict_requests_total = Counter(
    'predict_requests_total',
    'Total number of prediction requests',
    ['method', 'status']
)

# Гистограмма времени обработки
predict_duration_seconds = Histogram(
    'predict_duration_seconds',
    'Prediction request duration in seconds',
    ['method'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
)

# Счетчик ошибок
predict_errors_total = Counter(
    'predict_errors_total',
    'Total number of prediction errors',
    ['error_type']
)

# Gauge для текущих метрик
active_requests = Gauge(
    'active_requests',
    'Current number of active requests'
)

model_version_info = Info(
    'model_version',
    'Current model version information'
)

# Метрики модели
model_prediction_value = Histogram(
    'model_prediction_value',
    'Distribution of prediction values',
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
)

# Метрики базы данных
db_operation_duration = Histogram(
    'db_operation_duration_seconds',
    'Database operation duration in seconds',
    ['operation']
)

db_errors_total = Counter(
    'db_errors_total',
    'Total number of database errors',
    ['operation']
)

# Метрики HTTP запросов
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5)
)

def track_predictions(func):
    """Декоратор для отслеживания метрик предсказаний"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        active_requests.inc()
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            
            # Записываем метрики успешного предсказания
            predict_requests_total.labels(method='predict', status='success').inc()
            
            # Записываем значение предсказания
            if hasattr(result, 'prediction'):
                model_prediction_value.observe(result.prediction)
            
            return result
            
        except Exception as e:
            # Записываем метрики ошибки
            predict_requests_total.labels(method='predict', status='error').inc()
            predict_errors_total.labels(error_type=type(e).__name__).inc()
            raise
            
        finally:
            # Записываем время выполнения
            duration = time.time() - start_time
            predict_duration_seconds.labels(method='predict').observe(duration)
            active_requests.dec()
    
    return wrapper

def init_metrics():
    """Инициализация статических метрик"""
    model_version_info.info({'version': '1.0.0', 'status': 'active'})