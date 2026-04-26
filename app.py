import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import pandas as pd
from config import APP_TITLE, APP_ICON
from services import (
    calculate_bmi, calculate_tdee, get_calorie_target,
    predict_calories, predict_workout_type, get_food_recommendations,
    get_ai_diet_plan, get_ai_exercise_plan, get_ai_chat_response,
)

st.set_page_config(page_title="AI Diyet & Egzersiz", page_icon=APP_ICON, layout="wide")
st.title(APP_TITLE)
st.markdown("Bilgilerini gir, sana özel program oluşturalım.")

with st.sidebar:
    st.header("👤 Kişisel Bilgiler")
    name = st.text_input("Adın", placeholder="Ad")
    age = st.number_input("Yaş", min_value=10, max_value=100, value=22)
    gender = st.selectbox("Cinsiyet", ["Male", "Female"])
    weight = st.number_input("Kilo (kg)", min_value=30, max_value=250, value=75)
    height = st.number_input("Boy (cm)", min_value=100, max_value=250, value=175)
    activity_level = st.selectbox("Aktivite seviyesi", ["Hareketsiz", "Az aktif", "Orta aktif", "Çok aktif"])
    goal = st.selectbox("Hedefin", ["Kilo ver", "Formu koru", "Kilo al"])
    frequency = st.slider("Haftada kaç gün antrenman yapıyorsun?", 1, 7, 3)
    experience = st.selectbox("Deneyim seviyesi", [1, 2, 3],
                               format_func=lambda x: {1: "Başlangıç", 2: "Orta", 3: "İleri"}[x])
    session_hours = st.slider("Antrenman süresi (saat)", 0.5, 3.0, 1.0, step=0.5)
    st.divider()
    st.header("⚙️ Tercihler")
    equipment = st.selectbox("Antrenman ortamı", ["Spor salonu", "Ev (ekipmansız)", "Ev (ekipmanlı)", "Açık alan"])
    restrictions = st.text_area("Besin kısıtlamaları / alerjiler",
                                 placeholder="Örnek: gluten yiyemiyorum, muz alerjim var...",
                                 height=80)
    submitted = st.button("🚀 Program Oluştur", use_container_width=True)

if submitted:
    gender_tr = "Erkek" if gender == "Male" else "Kadın"
    bmi, bmi_category = calculate_bmi(weight, height)
    tdee = calculate_tdee(weight, height, age, gender_tr, activity_level)
    calorie_target = get_calorie_target(tdee, goal)
    height_m = height / 100
    predicted_workout = predict_workout_type(age, weight, height_m, gender, bmi, experience, frequency)
    predicted_calories = predict_calories(age, weight, height_m, gender,
                                          session_hours, predicted_workout or "Cardio", frequency)

    profile = {
        "name": name, "age": age, "gender": gender_tr,
        "weight": weight, "height": height, "bmi": bmi,
        "bmi_category": bmi_category, "tdee": tdee,
        "calorie_target": calorie_target, "goal": goal,
        "activity_level": activity_level, "frequency": frequency,
        "experience": {1: "Başlangıç", 2: "Orta", 3: "İleri"}[experience],
        "equipment": equipment, "restrictions": restrictions,
    }

    with st.spinner("🤖 AI programın hazırlanıyor..."):
        ai_diet = get_ai_diet_plan(profile, calorie_target)
        ai_exercise = get_ai_exercise_plan(profile)

    st.session_state.update({
        "program_ready": True,
        "user_profile": profile,
        "ai_diet": ai_diet,
        "ai_exercise": ai_exercise,
        "predicted_workout": predicted_workout,
        "predicted_calories": predicted_calories,
        "bmi": bmi, "bmi_category": bmi_category,
        "tdee": tdee, "calorie_target": calorie_target,
        "goal": goal, "messages": [],
    })

if st.session_state.get("program_ready"):
    profile       = st.session_state["user_profile"]
    bmi           = st.session_state["bmi"]
    bmi_category  = st.session_state["bmi_category"]
    tdee          = st.session_state["tdee"]
    calorie_target = st.session_state["calorie_target"]
    goal          = st.session_state["goal"]
    p_workout     = st.session_state["predicted_workout"]
    p_calories    = st.session_state["predicted_calories"]

    greeting = f"### Merhaba {profile['name']}! 👋" if profile["name"] else "### Programın Hazır! 👋"
    st.markdown(greeting)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("BMI", bmi, bmi_category)
    c2.metric("Günlük kalori ihtiyacı", f"{tdee} kcal")
    c3.metric("Hedef kalori", f"{calorie_target} kcal")
    c4.metric("Hedef", goal)

    if p_calories:
        m1, m2 = st.columns(2)
        m1.metric("🤖 ML: Antrenman tipi", p_workout or "Cardio")
        m2.metric("🤖 ML: Tahmini kalori yakımı", f"{p_calories} kcal")

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🥗 AI Diyet Planı", "🏋️ AI Egzersiz Planı",
        "🍎 Besin Veritabanı", "📊 Grafikler", "💬 AI Asistan"
    ])

    with tab1:
        st.subheader("🥗 AI Tarafından Oluşturulan Diyet Planın")
        if profile.get("restrictions"):
            st.info(f"✅ Kısıtlamalar dikkate alındı: {profile['restrictions']}")
        st.markdown(st.session_state["ai_diet"])

    with tab2:
        st.subheader("🏋️ AI Tarafından Oluşturulan Egzersiz Planın")
        st.info(f"✅ Antrenman ortamı: {profile.get('equipment','Spor salonu')}")
        st.markdown(st.session_state["ai_exercise"])

    with tab3:
        st.subheader("🍎 Besin Veritabanından Öneriler")
        food_df = get_food_recommendations(calorie_target, goal)
        if food_df is not None:
            st.dataframe(food_df.head(10), use_container_width=True, hide_index=True)
        else:
            st.warning("Besin verisi yüklenemedi.")

    with tab4:
        st.subheader("BMI Göstergesi")
        fig, ax = plt.subplots(figsize=(8, 1.5))
        bmi_ranges = [0, 18.5, 25, 30, 40]
        bmi_colors = ["#64B5F6", "#81C784", "#FFB74D", "#E57373"]
        bmi_labels = ["Zayıf", "Normal", "Fazla kilolu", "Obez"]
        for i in range(len(bmi_colors)):
            ax.barh(0, bmi_ranges[i+1] - bmi_ranges[i], left=bmi_ranges[i],
                    color=bmi_colors[i], height=0.5)
            ax.text(bmi_ranges[i] + (bmi_ranges[i+1]-bmi_ranges[i])/2, 0,
                    bmi_labels[i], ha="center", va="center", fontsize=9, color="white", fontweight="bold")
        ax.axvline(bmi, color="black", linewidth=3, label=f"Senin BMI'n: {bmi}")
        ax.set_xlim(10, 40)
        ax.set_yticks([])
        ax.set_xlabel("BMI")
        ax.legend(loc="upper right")
        ax.set_title("BMI skalası")
        st.pyplot(fig)

    with tab5:
        st.subheader("💬 AI Sağlık Asistanı")
        st.markdown("Diyet, egzersiz ve sağlık hakkındaki sorularını sorabilirsin.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Sorunuzu yazın..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Düşünüyor..."):
                    reply = get_ai_chat_response(st.session_state.messages, profile)
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("👈 Sol taraftaki formu doldurup **Program Oluştur** butonuna tıkla.")
    st.image("https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=60",
             caption="Sağlıklı yaşam için kişisel program", use_container_width=True)
