from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def get_ai_diet_plan(profile: dict, calorie_target: int) -> str:
    restrictions = profile.get("restrictions", "").strip()
    restrictions_text = f"Besin kısıtlamaları/alerjileri: {restrictions}" if restrictions else "Besin kısıtlaması yok."

    prompt = f"""Kullanıcı profili:
- Yaş: {profile['age']}, Cinsiyet: {profile['gender']}
- Kilo: {profile['weight']}kg, Boy: {profile['height']}cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Hedef: {profile['goal']}
- Günlük kalori hedefi: {calorie_target} kcal
- {restrictions_text}

Bu kişi için günlük 5 öğünlük kişiselleştirilmiş diyet planı oluştur.
Besin kısıtlamalarına kesinlikle uy, o besinleri kullanma.
Her öğün için: öğün adı, yemek önerisi ve tahmini kalori yaz.
Türkçe yaz, kısa ve net ol."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
    )
    return response.choices[0].message.content


def get_ai_exercise_plan(profile: dict) -> str:
    equipment = profile.get("equipment", "Spor salonu")

    prompt = f"""Kullanıcı profili:
- Yaş: {profile['age']}, Cinsiyet: {profile['gender']}
- Kilo: {profile['weight']}kg, Boy: {profile['height']}cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Hedef: {profile['goal']}
- Aktivite seviyesi: {profile['activity_level']}
- Deneyim: {profile['experience']}
- Haftada {profile['frequency']} gün antrenman
- Antrenman ortamı: {equipment}

Bu kişi için haftalık 7 günlük kişiselleştirilmiş egzersiz planı oluştur.
Antrenman ortamına uygun egzersizler seç.
Her gün için: gün adı, antrenman içeriği ve yoğunluk seviyesi yaz.
Türkçe yaz, kısa ve net ol."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
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
