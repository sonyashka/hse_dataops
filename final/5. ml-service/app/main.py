from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
import uuid
import json
import logging
from datetime import datetime
import os

from .models import PredictionRequest, PredictionResponse
from .ml_model import model
from .database import db
from .metrics import (
    track_predictions, http_requests_total, http_request_duration,
    db_operation_duration, db_errors_total, init_metrics
)

# Настройка логирования (как в предыдущей версии)
log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

json_logger = logging.getLogger("json_logger")
json_logger.setLevel(logging.INFO)
json_handler = logging.FileHandler(f"{log_dir}/requests.json")
json_handler.setFormatter(logging.Formatter('%(message)s'))
json_logger.addHandler(json_handler)

console_logger = logging.getLogger("console")
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_logger.addHandler(json_handler)
console_logger.addHandler(console_handler)

# Инициализируем метрики
init_metrics()

app = FastAPI(
    title="ML Service API",
    description="Simple ML service with monitoring",
    version="1.0.0"
)

@app.middleware("http")
async def log_and_metrics_middleware(request: Request, call_next):
    """Middleware для логирования и сбора метрик"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Логируем входящий запрос
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
    }
    
    try:
        response = await call_next(request)
        
        # Обновляем HTTP метрики
        duration = time.time() - start_time
        endpoint = request.url.path
        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        http_request_duration.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
        
        # Добавляем информацию о ответе
        log_entry["status_code"] = response.status_code
        log_entry["processing_time_ms"] = duration * 1000
        
        # Сохраняем JSON лог
        json_logger.info(json.dumps(log_entry))
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        console_logger.error(f"Error processing request {request_id}: {str(e)}")
        
        # Обновляем метрики ошибок
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500
        ).inc()
        
        log_entry["status_code"] = 500
        log_entry["error"] = str(e)
        json_logger.info(json.dumps(log_entry))
        
        raise

@app.get("/metrics")
async def get_metrics():
    """Endpoint для экспорта метрик Prometheus"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/")
async def root():
    """Корневой endpoint для проверки работоспособности"""
    return {
        "service": "ML Service",
        "version": "1.0.0",
        "status": "running",
        "model_version": model.get_version(),
        "monitoring": "/metrics"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "model_version": model.get_version()}

@app.get("/api/v1/stats")
async def get_stats():
    """Получение статистики из БД"""
    import time as time_module
    start_time = time_module.time()
    
    try:
        stats = db.get_stats()
        
        # Записываем метрику БД
        duration = time_module.time() - start_time
        db_operation_duration.labels(operation='get_stats').observe(duration)
        
        return {
            "status": "success",
            "stats": stats
        }
    except Exception as e:
        db_errors_total.labels(operation='get_stats').inc()
        console_logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting statistics")

@app.post("/api/v1/predict", response_model=PredictionResponse)
@track_predictions
async def predict(request: PredictionRequest):
    """Endpoint для предсказаний"""
    start_time = time.time()
    request_id = request.request_id or str(uuid.uuid4())
    
    try:
        # Валидация входных данных
        if not request.features:
            raise HTTPException(status_code=400, detail="Features list cannot be empty")
        
        # Получаем предсказание от модели
        prediction = model.predict(request.features)
        
        # Вычисляем время обработки
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Логируем в базу данных с метриками
        db_start = time.time()
        try:
            db.log_prediction(
                request_id=request_id,
                features=request.features,
                prediction=prediction,
                processing_time=processing_time_ms,
                model_version=model.get_version()
            )
            db_duration = time.time() - db_start
            db_operation_duration.labels(operation='log_prediction').observe(db_duration)
        except Exception as e:
            db_errors_total.labels(operation='log_prediction').inc()
            raise
        
        # Логируем в консоль для отладки
        console_logger.info(
            f"Prediction - Request ID: {request_id}, "
            f"Features: {request.features}, "
            f"Prediction: {prediction:.4f}, "
            f"Time: {processing_time_ms:.2f}ms, "
            f"Model Version: {model.get_version()}"
        )
        
        return PredictionResponse(
            prediction=prediction,
            request_id=request_id,
            processing_time_ms=round(processing_time_ms, 2),
            model_version=model.get_version()
        )
        
    except ValueError as e:
        console_logger.error(f"Value error for request {request_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        console_logger.error(f"Unexpected error for request {request_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")