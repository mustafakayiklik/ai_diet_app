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
    experience = profile.get("experience", "Baslangic")
    frequency = profile.get("frequency", 3)
    session_hours = profile.get("session_hours", 1)

    if experience == "Başlangıç" or experience == "Baslangic":
        intensity_note = "Bu kisi BASLANGIC seviyesinde. Basit, temel hareketler sec. Agir agirliklar ve karmasik hareketler KULLANMA."
        set_rep = "2-3 set, 10-12 tekrar, 60-90 sn dinlenme"
    elif experience == "Orta":
        intensity_note = "Bu kisi ORTA seviyesinde. Orta zorlukta hareketler sec."
        set_rep = "3-4 set, 8-12 tekrar, 60-90 sn dinlenme"
    else:
        intensity_note = "Bu kisi ILERI seviyesinde. Karmasik ve agir hareketler sec. Supersetler ekleyebilirsin."
        set_rep = "4-5 set, 6-12 tekrar, 45-90 sn dinlenme"

    prompt = f"""Sen bir fitness antrenoru asistanisin. Asagidaki kisiye TAMAMEN OZEL bir egzersiz plani olustur.

KISISEL BILGILER:
- Yas: {profile['age']}
- Cinsiyet: {profile['gender']}
- Kilo: {profile['weight']} kg
- Boy: {profile['height']} cm
- BMI: {profile['bmi']} ({profile['bmi_category']})
- Hedef: {profile['goal']}
- Aktivite seviyesi: {profile['activity_level']}
- Deneyim seviyesi: {experience}
- Haftada {frequency} gun antrenman
- Her antrenman suresi: {session_hours} saat
- Antrenman ortami: {equipment}

DENEYIM SEVIYESI KURALI:
{intensity_note}
Onerilecek set ve tekrar: {set_rep}

ANTRENMAN SURESI KURALI - COK ONEMLI:
- Bu kisi her antrenmanda {session_hours} saat calisacak
- Asagidaki kurallara gore egzersiz sayisi ve yuruyus suresi belirle:
- 0.5 saat: 3 egzersiz, yuruyus ekleme
- 1 saat: 4-5 egzersiz + 15 dakika yuruyus ile bitir
- 1.5 saat: 5-6 egzersiz + 20 dakika yuruyus ile bitir
- 2 saat: 6-7 egzersiz + 30 dakika yuruyus ile bitir
- 2.5 saat: 7-8 egzersiz + 45 dakika yuruyus ile bitir
- 3 saat: 8-9 egzersiz + 60 dakika yuruyus ile bitir
- Bu kisinin suresi {session_hours} saat oldugu icin buna uygun egzersiz sayisi sec ve sonu yuruyus ile tamamla
- Her gun toplam sure yaklasik {session_hours} saat olmali

HEDEF KURALLARI:
- Kilo verme: kardiyo agirlikli, yuksek tekrarli, kisa dinlenme
- Kilo alma: agirlik antrenman agirlikli, compound hareketler, uzun dinlenme
- Formu koruma: karma program, hem kardiyo hem agirlik

ORTAM KURALLARI:
- Spor salonu: barbell, dumbbell, makine egzersizleri kullan
- Ev ekipmansiz: SADECE vucut agirligi egzersizleri kullan
- Ev ekipmanli: dumbbell ve bant egzersizleri ekle
- Acik alan: kos, bisiklet, park egzersizleri oner

CESITLILIK KURALLARI:
- Her gun farkli kas grubu calis
- 7 gunun hicbirinde ayni egzersiz tekrarlanmasin
- Egzersiz isimlerini Turkce yaz
- SADECE Turkce yaz

HAFTADA {frequency} GUN ANTRENMAN YAPACAK:
- Kalan gunleri dinlenme veya hafif aktivite olarak isle
- Antrenman gunlerini dengeli dagit

FORMAT:
Pazartesi: [Antrenman adi] - [Yogunluk: Dusuk/Orta/Yuksek]
- [Egzersiz 1]: [set] x [tekrar], [dinlenme] sn dinlenme
- [Egzersiz 2]: [set] x [tekrar], [dinlenme] sn dinlenme
- [Egzersiz 3]: [set] x [tekrar], [dinlenme] sn dinlenme
Toplam sure: yaklasik {session_hours} saat

(Sali, Carsamba, Persembe, Cuma, Cumartesi, Pazar da ayni formatta devam et)
SADECE Turkce yaz."""

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
