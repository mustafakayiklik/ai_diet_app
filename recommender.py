def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Zayıf"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Fazla kilolu"
    else:
        category = "Obez"
    return round(bmi, 1), category


def calculate_tdee(weight, height_cm, age, gender, activity_level):
    if gender == "Erkek":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

    activity_multipliers = {
        "Hareketsiz": 1.2,
        "Az aktif": 1.375,
        "Orta aktif": 1.55,
        "Çok aktif": 1.725,
    }
    tdee = bmr * activity_multipliers[activity_level]
    return round(tdee)


def get_calorie_target(tdee, goal):
    if goal == "Kilo ver":
        return tdee - 500
    elif goal == "Kilo al":
        return tdee + 400
    else:
        return tdee


def get_diet_plan(calorie_target, goal):
    if goal == "Kilo ver":
        meals = [
            {"öğün": "Kahvaltı", "öneri": "2 yumurta, 1 dilim tam buğday ekmek, domates, salatalık", "kalori": 300},
            {"öğün": "Ara öğün", "öneri": "1 elma, 10 badem", "kalori": 150},
            {"öğün": "Öğle", "öneri": "Izgara tavuk göğsü, bulgur pilavı, salata", "kalori": 450},
            {"öğün": "Ara öğün", "öneri": "Yoğurt (az yağlı)", "kalori": 100},
            {"öğün": "Akşam", "öneri": "Izgara balık veya sebze yemeği, yeşil salata", "kalori": 400},
        ]
    elif goal == "Kilo al":
        meals = [
            {"öğün": "Kahvaltı", "öneri": "Yulaf ezmesi, muz, fıstık ezmesi, süt", "kalori": 500},
            {"öğün": "Ara öğün", "öneri": "Peynirli tam buğday sandviç", "kalori": 300},
            {"öğün": "Öğle", "öneri": "Pirinç pilavı, tavuk sote, mercimek çorbası", "kalori": 700},
            {"öğün": "Ara öğün", "öneri": "Muz + protein shake", "kalori": 350},
            {"öğün": "Akşam", "öneri": "Makarna, kıymalı sos, salata", "kalori": 650},
        ]
    else:
        meals = [
            {"öğün": "Kahvaltı", "öneri": "Yumurta, peynir, sebze, tam buğday ekmek", "kalori": 400},
            {"öğün": "Ara öğün", "öneri": "Meyve + ceviz", "kalori": 200},
            {"öğün": "Öğle", "öneri": "Izgara et veya tavuk, pirinç, salata", "kalori": 550},
            {"öğün": "Ara öğün", "öneri": "Yoğurt", "kalori": 150},
            {"öğün": "Akşam", "öneri": "Sebze yemeği, çorba, tam buğday ekmek", "kalori": 450},
        ]
    return meals


def get_exercise_plan(goal, activity_level, bmi_category):
    if goal == "Kilo ver":
        plan = [
            {"gün": "Pazartesi", "antrenman": "30 dk yürüyüş + 20 dk kardiyo", "yoğunluk": "Orta"},
            {"gün": "Salı", "antrenman": "Üst vücut ağırlık antrenmanı", "yoğunluk": "Orta"},
            {"gün": "Çarşamba", "antrenman": "45 dk tempolu yürüyüş", "yoğunluk": "Düşük"},
            {"gün": "Perşembe", "antrenman": "Alt vücut + core antrenmanı", "yoğunluk": "Orta"},
            {"gün": "Cuma", "antrenman": "HIIT antrenmanı (20 dk)", "yoğunluk": "Yüksek"},
            {"gün": "Cumartesi", "antrenman": "Bisiklet veya yüzme (45 dk)", "yoğunluk": "Orta"},
            {"gün": "Pazar", "antrenman": "Dinlenme veya hafif esneme", "yoğunluk": "Düşük"},
        ]
    elif goal == "Kilo al":
        plan = [
            {"gün": "Pazartesi", "antrenman": "Göğüs + triceps ağırlık antrenmanı", "yoğunluk": "Yüksek"},
            {"gün": "Salı", "antrenman": "Sırt + biceps antrenmanı", "yoğunluk": "Yüksek"},
            {"gün": "Çarşamba", "antrenman": "Dinlenme", "yoğunluk": "Düşük"},
            {"gün": "Perşembe", "antrenman": "Bacak + omuz antrenmanı", "yoğunluk": "Yüksek"},
            {"gün": "Cuma", "antrenman": "Full body compound hareketler", "yoğunluk": "Yüksek"},
            {"gün": "Cumartesi", "antrenman": "Hafif kardiyo (20 dk)", "yoğunluk": "Düşük"},
            {"gün": "Pazar", "antrenman": "Dinlenme", "yoğunluk": "Düşük"},
        ]
    else:
        plan = [
            {"gün": "Pazartesi", "antrenman": "30 dk yürüyüş + esneme", "yoğunluk": "Düşük"},
            {"gün": "Salı", "antrenman": "Vücut ağırlığı antrenmanı", "yoğunluk": "Orta"},
            {"gün": "Çarşamba", "antrenman": "Yoga veya pilates (30 dk)", "yoğunluk": "Düşük"},
            {"gün": "Perşembe", "antrenman": "Kardiyo + core", "yoğunluk": "Orta"},
            {"gün": "Cuma", "antrenman": "Ağırlık antrenmanı", "yoğunluk": "Orta"},
            {"gün": "Cumartesi", "antrenman": "Outdoor aktivite (yürüyüş, bisiklet)", "yoğunluk": "Orta"},
            {"gün": "Pazar", "antrenman": "Dinlenme", "yoğunluk": "Düşük"},
        ]
    return plan
