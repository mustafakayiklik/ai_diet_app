from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def get_ai_diet_plan(profile: dict, calorie_target: int) -> str:
    restrictions = profile.get("restrictions", "").strip()
    restrictions_text = f"Besin kısıtlamaları/alerjileri: {restrictions}" if restrictions else "Besin kısıtlaması yok."

    prompt = f"""User profile:
- Age: {profile['age']}, Gender: {profile['gender']}
- Weight: {profile['weight']}kg, Height: {profile['height']}cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Goal: {profile['goal']}
- Daily calorie target: {calorie_target} kcal
- Dietary restrictions: {restrictions_text}

Create a detailed 7-day personalized meal plan in Turkish.
Rules:
- Each day must have 5 meals: Sabah kahvaltisi, Ara ogun, Ogle yemegi, Ara ogun, Aksam yemegi
- Every day must be completely different, no repeated meals across the week
- Each meal must include 2-3 specific food items with portions
- Write estimated calories for each meal
- Daily total must be close to {calorie_target} kcal
- Each meal must be detailed and satisfying, not just one food item
- Breakfast should include protein, carbs and healthy fats (e.g. eggs, cheese, vegetables, bread, olive oil)
- Main meals should include a protein source, carbohydrate, vegetables and a side dish
- Snacks should be more than just one fruit, combine 2-3 items (e.g. fruit + nuts + yogurt)
- Use variety: chicken, fish, red meat, legumes, eggs across different days
- Include traditional Turkish meals like mercimek corbasi, kuru fasulye, izgaraetler, etc.
- Be creative and varied, do not give the same meals to every user
- Adapt meals to the user's goal: if losing weight prefer lighter meals, if gaining weight prefer calorie-dense meals
- Consider the user's BMI category when suggesting portion sizes
- Mix different cuisines and cooking methods: grilled, boiled, baked, raw
- Do not repeat the same protein source more than twice in a week
- Strictly avoid any foods mentioned in dietary restrictions
- Make it realistic and practical for a Turkish person

Format each day like:
Pazartesi:
- Sabah: [foods] - [calories] kcal
- Ara ogun: [foods] - [calories] kcal
- Ogle: [foods] - [calories] kcal
- Ara ogun: [foods] - [calories] kcal
- Aksam: [foods] - [calories] kcal"""

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
