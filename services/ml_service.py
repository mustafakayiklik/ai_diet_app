import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
import pickle
import os
from config import GYM_DATASET, FOOD_DATASET, MODELS_PATH


def load_gym_data() -> pd.DataFrame:
    df = pd.read_csv(GYM_DATASET)
    df.columns = df.columns.str.strip()
    return df


def load_nutrition_data() -> pd.DataFrame:
    df = pd.read_csv(FOOD_DATASET)
    df.columns = df.columns.str.strip()
    return df


def train_calorie_model():
    df = load_gym_data()
    le_gender = LabelEncoder()
    le_workout = LabelEncoder()
    df["Gender_enc"] = le_gender.fit_transform(df["Gender"])
    df["Workout_enc"] = le_workout.fit_transform(df["Workout_Type"])

    features = ["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                "Session_Duration (hours)", "Workout_enc", "Workout_Frequency (days/week)"]
    target = "Calories_Burned"
    df = df.dropna(subset=features + [target])

    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Kalori modeli MAE: {mae:.1f} kcal")

    os.makedirs(MODELS_PATH, exist_ok=True)
    with open(MODELS_PATH + "calorie_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(MODELS_PATH + "gender_encoder.pkl", "wb") as f:
        pickle.dump(le_gender, f)
    with open(MODELS_PATH + "workout_encoder.pkl", "wb") as f:
        pickle.dump(le_workout, f)


def train_workout_type_model():
    df = load_gym_data()
    le_gender = LabelEncoder()
    le_workout = LabelEncoder()
    df["Gender_enc"] = le_gender.fit_transform(df["Gender"])
    df["Workout_enc"] = le_workout.fit_transform(df["Workout_Type"])

    features = ["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                "BMI", "Experience_Level", "Workout_Frequency (days/week)"]
    target = "Workout_enc"
    df = df.dropna(subset=features + [target])

    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Antrenman tipi modeli doğruluğu: {acc*100:.1f}%")

    with open(MODELS_PATH + "workout_type_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(MODELS_PATH + "workout_label_encoder.pkl", "wb") as f:
        pickle.dump(le_workout, f)


def predict_calories(age, weight, height_m, gender, session_hours, workout_type, frequency) -> int | None:
    try:
        with open(MODELS_PATH + "calorie_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODELS_PATH + "gender_encoder.pkl", "rb") as f:
            le_gender = pickle.load(f)
        with open(MODELS_PATH + "workout_encoder.pkl", "rb") as f:
            le_workout = pickle.load(f)

        gender_enc = le_gender.transform([gender])[0]
        workout_enc = le_workout.transform([workout_type])[0]
        X = pd.DataFrame([[age, weight, height_m, gender_enc, session_hours, workout_enc, frequency]],
                         columns=["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                                  "Session_Duration (hours)", "Workout_enc", "Workout_Frequency (days/week)"])
        return round(model.predict(X)[0])
    except Exception as e:
        print(f"Kalori tahmin hatası: {e}")
        return None


def predict_workout_type(age, weight, height_m, gender, bmi, experience, frequency) -> str | None:
    try:
        with open(MODELS_PATH + "workout_type_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODELS_PATH + "workout_label_encoder.pkl", "rb") as f:
            le_workout = pickle.load(f)
        with open(MODELS_PATH + "gender_encoder.pkl", "rb") as f:
            le_gender = pickle.load(f)

        gender_enc = le_gender.transform([gender])[0]
        X = pd.DataFrame([[age, weight, height_m, gender_enc, bmi, experience, frequency]],
                         columns=["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                                  "BMI", "Experience_Level", "Workout_Frequency (days/week)"])
        pred_enc = model.predict(X)[0]
        return le_workout.inverse_transform([pred_enc])[0]
    except Exception as e:
        print(f"Antrenman tipi tahmin hatası: {e}")
        return None


def get_food_recommendations(calorie_target: int, goal: str, top_n: int = 10) -> pd.DataFrame | None:
    try:
        df = load_nutrition_data()
        calorie_col = next((c for c in df.columns if "calori" in c.lower() or "energy" in c.lower()), None)
        protein_col = next((c for c in df.columns if "protein" in c.lower()), None)

        if not calorie_col:
            return None

        df[calorie_col] = pd.to_numeric(df[calorie_col], errors="coerce")
        df = df.dropna(subset=[calorie_col])

        if goal == "Kilo ver":
            filtered = df[df[calorie_col] < 300]
        elif goal == "Kilo al":
            filtered = df[df[calorie_col] > 200]
        else:
            filtered = df[(df[calorie_col] >= 100) & (df[calorie_col] <= 400)]

        if protein_col:
            df[protein_col] = pd.to_numeric(df[protein_col], errors="coerce")
            filtered = filtered.sort_values(protein_col, ascending=False)

        return filtered.head(top_n)
    except Exception as e:
        print(f"Besin önerisi hatası: {e}")
        return None


def train_all_models():
    print("Modeller eğitiliyor...")
    train_calorie_model()
    train_workout_type_model()
    print("Tüm modeller hazır!")


if __name__ == "__main__":
    train_all_models()
