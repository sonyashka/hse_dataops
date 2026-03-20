import numpy as np
from typing import List
import os

class SimpleMLModel:
    """Простая ML модель для демонстрации"""
    
    def __init__(self):
        # Простая линейная модель: y = w1*x1 + w2*x2 + ... + bias
        self.version = "1.0.0"
        self.weights = np.array([0.5, 0.3, 0.2, 0.1])
        self.bias = 0.5
        self.is_trained = True
        
    def predict(self, features: List[float]) -> float:
        """
        Предсказание на основе входных признаков
        
        Args:
            features: список числовых признаков
            
        Returns:
            предсказанное значение
        """
        # Преобразуем в numpy массив
        features_array = np.array(features[:len(self.weights)])
        
        # Линейная комбинация
        prediction = np.dot(features_array, self.weights) + self.bias
        
        # Применяем сигмоиду для ограничения выхода в диапазоне (0, 1)
        prediction = 1 / (1 + np.exp(-prediction))
        
        return float(prediction)
    
    def get_version(self) -> str:
        """Возвращает версию модели"""
        return self.version

# Создаем глобальный экземпляр модели
model = SimpleMLModel()