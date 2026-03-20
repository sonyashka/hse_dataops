from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PredictionRequest(BaseModel):
    """Модель запроса на предсказание"""
    features: list[float]
    request_id: Optional[str] = None

class PredictionResponse(BaseModel):
    """Модель ответа с предсказанием"""
    prediction: float
    request_id: str
    processing_time_ms: float
    model_version: str

class PredictionLog(BaseModel):
    """Модель для логирования в БД"""
    id: Optional[int] = None
    request_id: str
    input_features: str
    prediction: float
    processing_time_ms: float
    model_version: str
    created_at: datetime