from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def get_ai_diet_plan(profile: dict, calorie_target: int) -> str:
    restrictions = profile.get("restrictions", "").strip()
    restrictions_text = f"Besin kısıtlamaları/alerjileri: {restrictions}" if restrictions else "Besin kısıtlaması yok."

    prompt = f"""Sen bir diyetisyen asistanisin. Asagidaki kisiye TAMAMEN OZEL ve OZGUN bir diyet plani olustur.

UYARI: Bu plani baska hic kimseye verme. Sadece bu kisinin ozelliklerine gore yaz.
Bu kisinin BMI degeri {profile['bmi']}, kilosu {profile['weight']} kg, cinsiyeti {profile['gender']}.
Bu degerlere gore yemek secimleri ve porsiyonlar degismeli.

KISISEL BILGILER:
- Yas: {profile['age']}
- Cinsiyet: {profile['gender']}
- Kilo: {profile['weight']} kg
- Boy: {profile['height']} cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Hedef: {profile['goal']}
- Gunluk kalori hedefi: {calorie_target} kcal
- Kisitlamalar: {restrictions_text}

CESITLILIK KURALLARI:
- Protein kaynaklari cesitli olsun: tavuk, balik, kirmizi et, yumurta, baklagiller
- Karbonhidrat cesitli olsun: bulgur, pirinc, makarna, ekmek, yulaf
- Her gun farkli bir protein kaynagi kullan
- Yumurtayi haftada 2-3 kez kullanabilirsin ama her gun olmasin
- Sebze ve meyveleri cesitli sec
- Geleneksel Turk mutfagindan yemekler ekle

HEDEF KURALLARI:
- Kilo verme hedefi: hafif, dusuk kalorili, bol sebzeli yemekler
- Kilo alma hedefi: yuksek proteinli, kalorili, doyurucu yemekler
- Formu koruma hedefi: dengeli, cesitli yemekler

ZORUNLU KURALLAR:
- 7 gunluk plan yaz
- Her gun 5 ogun: Kahvalti, Ara ogun, Ogle, Ara ogun, Aksam
- 7 gunun hicbirinde ayni yemek tekrarlanmasin
- Her ogunde 2-3 yiyecek, gram veya adet olarak porsiyon belirt
- Her ogun icin kalori yaz
- SADECE Turkce yaz

FORMAT:
Pazartesi:
- Kahvalti: [yiyecekler ve porsiyonlar] - [kalori] kcal
- Ara ogun: [yiyecekler] - [kalori] kcal
- Ogle: [yiyecekler] - [kalori] kcal
- Ara ogun: [yiyecekler] - [kalori] kcal
- Aksam: [yiyecekler] - [kalori] kcal

(Sali, Carsamba, Persembe, Cuma, Cumartesi, Pazar da ayni formatta devam et)"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    return response.choices[0].message.content


def get_ai_exercise_plan(profile: dict) -> str:
    equipment = profile.get("equipment", "Spor salonu")
    prompt = f"""User profile:
- Age: {profile['age']}, Gender: {profile['gender']}
- Weight: {profile['weight']}kg, Height: {profile['height']}cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Goal: {profile['goal']}
- Activity level: {profile['activity_level']}
- Experience: {profile['experience']}
- Training {profile['frequency']} days per week
- Training environment: {equipment}

Create a 7-day personalized exercise plan for this person.
Each day must have different exercises.
For each day write: day name, workout content and intensity level.
Choose exercises suitable for the training environment.
Write in Turkish, keep it short and clear."""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )
    return response.choices[0].message.content

def get_ai_chat_response(messages: list, profile: dict) -> str:
    sys_prompt = f"""Sen yalnızca diyet, beslenme, egzersiz ve sağlıkla ilgili sorulara cevap veren bir fitness asistanısın.
Kullanıcının profili: Yaş: {profile.get('age','?')}, Kilo: {profile.get('weight','?')}kg,
Boy: {profile.get('height','?')}cm, BMI: {profile.get('bmi','?')} ({profile.get('bmi_category','?')}),
Hedef: {profile.get('goal','?')}, Günlük kalori hedefi: {profile.get('calorie_target','?')} kcal,
Besin kısıtlamaları: {profile.get('restrictions','yok')},
Antrenman ortamı: {profile.get('equipment','Spor salonu')}.
Eğer kullanıcı sağlık, beslenme veya egzersiz dışında bir konu sorarsa kibarca 'Bu konuda yardımcı olamam, yalnızca diyet ve fitness sorularınızda buradayım.' de.
Türkçe cevap ver, samimi ve motive edici ol."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": sys_prompt},
            *[{"role": m["role"], "content": m["content"]} for m in messages],
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content
