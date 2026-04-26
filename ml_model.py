import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
import pickle
import os

MODEL_PATH = "models/"

def load_gym_data():
    df = pd.read_csv("gym_members_exercise_tracking.csv")
    df.columns = df.columns.str.strip()
    return df

def load_nutrition_data():
    df = pd.read_csv("Food_Nutrition_Dataset.csv")
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
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Kalori modeli MAE: {mae:.1f} kcal")

    os.makedirs(MODEL_PATH, exist_ok=True)
    with open(MODEL_PATH + "calorie_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(MODEL_PATH + "gender_encoder.pkl", "wb") as f:
        pickle.dump(le_gender, f)
    with open(MODEL_PATH + "workout_encoder.pkl", "wb") as f:
        pickle.dump(le_workout, f)

    print("Kalori modeli kaydedildi.")
    return model, le_gender, le_workout

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
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Antrenman tipi modeli doğruluğu: {acc*100:.1f}%")

    with open(MODEL_PATH + "workout_type_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(MODEL_PATH + "workout_label_encoder.pkl", "wb") as f:
        pickle.dump(le_workout, f)

    print("Antrenman tipi modeli kaydedildi.")
    return model, le_workout

def predict_calories(age, weight, height_m, gender, session_hours, workout_type, frequency):
    try:
        with open(MODEL_PATH + "calorie_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODEL_PATH + "gender_encoder.pkl", "rb") as f:
            le_gender = pickle.load(f)
        with open(MODEL_PATH + "workout_encoder.pkl", "rb") as f:
            le_workout = pickle.load(f)

        gender_enc = le_gender.transform([gender])[0]
        workout_enc = le_workout.transform([workout_type])[0]

        X = pd.DataFrame([[age, weight, height_m, gender_enc,
                           session_hours, workout_enc, frequency]],
                         columns=["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                                  "Session_Duration (hours)", "Workout_enc",
                                  "Workout_Frequency (days/week)"])
        prediction = model.predict(X)[0]
        return round(prediction)
    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return None

def predict_workout_type(age, weight, height_m, gender, bmi, experience, frequency):
    try:
        with open(MODEL_PATH + "workout_type_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODEL_PATH + "workout_label_encoder.pkl", "rb") as f:
            le_workout = pickle.load(f)
        with open(MODEL_PATH + "gender_encoder.pkl", "rb") as f:
            le_gender = pickle.load(f)

        gender_enc = le_gender.transform([gender])[0]

        X = pd.DataFrame([[age, weight, height_m, gender_enc,
                           bmi, experience, frequency]],
                         columns=["Age", "Weight (kg)", "Height (m)", "Gender_enc",
                                  "BMI", "Experience_Level",
                                  "Workout_Frequency (days/week)"])
        pred_enc = model.predict(X)[0]
        workout_type = le_workout.inverse_transform([pred_enc])[0]
        return workout_type
    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return None

def get_food_recommendations(calorie_target, goal, top_n=10):
    try:
        df = load_nutrition_data()

        calorie_col = None
        protein_col = None
        for col in df.columns:
            if "calori" in col.lower() or "energy" in col.lower():
                calorie_col = col
            if "protein" in col.lower():
                protein_col = col

        if calorie_col is None:
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
