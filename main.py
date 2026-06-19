from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import (
    calculate_bmi,
    calculate_tdee,
    get_calorie_target,
    predict_calories,
    predict_workout_type,
    get_ai_diet_plan,
    get_ai_exercise_plan,
    get_ai_chat_response,
)

app = FastAPI(title="AI Diet & Exercise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    name: str = ""
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str
    frequency: int
    experience: int
    session_hours: float
    equipment: str
    restrictions: str = ""


class ChatRequest(BaseModel):
    messages: list
    profile: dict


@app.get("/")
def root():
    return {"message": "AI Diet & Exercise API çalışıyor!"}


@app.post("/generate-program")
def generate_program(user: UserProfile):
    gender_tr = "Erkek" if user.gender == "Male" else "Kadın"
    bmi, bmi_category = calculate_bmi(user.weight, user.height)
    tdee = calculate_tdee(user.weight, user.height, user.age, gender_tr, user.activity_level)
    calorie_target = get_calorie_target(tdee, user.goal)
    height_m = user.height / 100

    predicted_workout = predict_workout_type(
        user.age, user.weight, height_m, user.gender, bmi, user.experience, user.frequency
    )
    predicted_calories = predict_calories(
        user.age, user.weight, height_m, user.gender,
        user.session_hours, predicted_workout or "Cardio", user.frequency
    )

    profile = {
        "name": user.name, "age": user.age, "gender": gender_tr,
        "weight": user.weight, "height": user.height, "bmi": bmi,
        "bmi_category": bmi_category, "tdee": tdee,
        "calorie_target": calorie_target, "goal": user.goal,
        "activity_level": user.activity_level, "frequency": user.frequency,
        "experience": {1: "Başlangıç", 2: "Orta", 3: "İleri"}[user.experience],
        "equipment": user.equipment, "restrictions": user.restrictions,
    }

    ai_diet = get_ai_diet_plan(profile, calorie_target)
    ai_exercise = get_ai_exercise_plan(profile)

    return {
        "profile": profile,
        "bmi": bmi,
        "bmi_category": bmi_category,
        "tdee": tdee,
        "calorie_target": calorie_target,
        "predicted_workout": predicted_workout,
        "predicted_calories": predicted_calories,
        "ai_diet": ai_diet,
        "ai_exercise": ai_exercise,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    reply = get_ai_chat_response(request.messages, request.profile)
    return {"reply": reply}
