import os
from dotenv import load_dotenv

load_dotenv()

# API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Uygulama
APP_TITLE = "💪 AI Tabanlı Kişisel Diyet ve Egzersiz Uygulaması"
APP_ICON = "💪"

# Veri setleri
GYM_DATASET = "gym_members_exercise_tracking.csv"
FOOD_DATASET = "Food_Nutrition_Dataset.csv"
MODELS_PATH = "models/"

# BMI sınırları
BMI_UNDERWEIGHT = 18.5
BMI_NORMAL = 25.0
BMI_OVERWEIGHT = 30.0

# Aktivite katsayıları
ACTIVITY_MULTIPLIERS = {
    "Hareketsiz": 1.2,
    "Az aktif": 1.375,
    "Orta aktif": 1.55,
    "Çok aktif": 1.725,
}
