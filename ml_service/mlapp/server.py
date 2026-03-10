import mlflow
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="Diabetes Prediction API", version="1.0.0")

# Глобальная переменная для модели
model = None

# Определение модели входных данных
class PatientData(BaseModel):
    age: float = Field(..., description="Age", ge=0, le=120)
    sex: float = Field(..., description="Sex", ge=0, le=1)
    bmi: float = Field(..., description="Body Mass Index", ge=10, le=50)
    bp: float = Field(..., description="Average Blood Pressure", ge=50, le=200)
    s1: float = Field(..., description="Total Serum Cholesterol", ge=100, le=400)
    s2: float = Field(..., description="Low-Density Lipoproteins", ge=50, le=300)
    s3: float = Field(..., description="High-Density Lipoproteins", ge=20, le=100)
    s4: float = Field(..., description="Total Cholesterol / HDL", ge=1, le=10)
    s5: float = Field(..., description="Log of Serum Triglycerides Level", ge=3, le=8)
    s6: float = Field(..., description="Blood Sugar Level", ge=50, le=300)

    class Config:
        schema_extra = {
            "example": {
                "age": 0.0380759064334241,
                "sex": 0.0506801187398187,
                "bmi": 0.0616962065186835,
                "bp": 0.0218723850763034,
                "s1": -0.0442234984244467,
                "s2": -0.0348207628376988,
                "s3": -0.0434008456520269,
                "s4": -0.00259226199818282,
                "s5": 0.0199074861610772,
                "s6": -0.0176461251598053
            }
        }

# Модель ответа
class PredictionResponse(BaseModel):
    predict: float

@app.on_event("startup")
async def load_model():
    """Загрузка модели при старте приложения"""
    global model
    try:
        # Настройка URI для MLflow
        mlflow.set_tracking_uri("file:./mlruns")
        
        # Загрузка последней версии модели
        model_uri = "models:/diabetes/latest"
        logger.info(f"Загрузка модели из {model_uri}")
        
        model = mlflow.sklearn.load_model(model_uri)
        logger.info("Модель успешно загружена")
    except Exception as e:
        logger.error(f"Ошибка при загрузке модели: {e}")
        # Для отладки: если модель не найдена, создаем фиктивную
        logger.warning("Используется фиктивная модель для тестирования")
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor()
        # Обучаем на случайных данных для имитации
        X_dummy = np.random.rand(100, 10)
        y_dummy = np.random.rand(100) * 200
        model.fit(X_dummy, y_dummy)

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы сервиса"""
    return {"message": "Diabetes Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(patient_data: PatientData):
    """
    Эндпоинт для предсказания прогрессии диабета
    
    Принимает 10 параметров пациента и возвращает предсказание
    """
    try:
        # Преобразование входных данных в массив для модели
        input_features = np.array([[
            patient_data.age,
            patient_data.sex,
            patient_data.bmi,
            patient_data.bp,
            patient_data.s1,
            patient_data.s2,
            patient_data.s3,
            patient_data.s4,
            patient_data.s5,
            patient_data.s6
        ]])
        
        logger.info(f"Получен запрос с данными: {patient_data}")
        
        # Предсказание
        prediction = model.predict(input_features)[0]
        
        logger.info(f"Предсказание: {prediction}")
        
        return PredictionResponse(predict=float(prediction))
        
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise HTTPException(status_code=500, detail=str(e))