from config import BMI_UNDERWEIGHT, BMI_NORMAL, BMI_OVERWEIGHT, ACTIVITY_MULTIPLIERS


def calculate_bmi(weight: float, height_cm: float) -> tuple[float, str]:
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < BMI_UNDERWEIGHT:
        category = "Zayıf"
    elif bmi < BMI_NORMAL:
        category = "Normal"
    elif bmi < BMI_OVERWEIGHT:
        category = "Fazla kilolu"
    else:
        category = "Obez"
    return round(bmi, 1), category


def calculate_tdee(weight: float, height_cm: float, age: int, gender: str, activity_level: str) -> int:
    if gender == "Erkek":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return round(bmr * multiplier)


def get_calorie_target(tdee: int, goal: str) -> int:
    if goal == "Kilo ver":
        return tdee - 500
    elif goal == "Kilo al":
        return tdee + 400
    return tdee
