from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# Allow all origins while testing on Replit; tighten later if needed
CORS(app)

# ---- Data files (yours are in the project root on Replit now) ----
AR_FILE  = "quran_ar.json"
EN_FILE  = "quran_en.json"
UR_FILE  = "quran_ur.json"
BN_FILE  = "quran_bn.json"
FR_FILE  = "quran_fr.json"
ES_FILE  = "quran_es.json"
ZH_FILE  = "quran_zh.json"
RU_FILE  = "quran_ru.json"
ID_FILE  = "quran_id.json"
NO_FILE  = "quran_sv.json"   # your “no” language uses the sv file
TR_FILE  = "quran_tr.json"
TRQ_FILE = "quran_trq.json"

# ---- Load all languages once at startup ----
with open(AR_FILE, "r", encoding="utf-8") as f: arabic_data = json.load(f)
with open(EN_FILE, "r", encoding="utf-8") as f: english_data = json.load(f)
with open(UR_FILE, "r", encoding="utf-8") as f: urdu_data = json.load(f)
with open(BN_FILE, "r", encoding="utf-8") as f: bangla_data = json.load(f)
with open(FR_FILE, "r", encoding="utf-8") as f: french_data = json.load(f)
with open(ES_FILE, "r", encoding="utf-8") as f: spanish_data = json.load(f)
with open(ZH_FILE, "r", encoding="utf-8") as f: chinese_data = json.load(f)
with open(RU_FILE, "r", encoding="utf-8") as f: russian_data = json.load(f)
with open(ID_FILE, "r", encoding="utf-8") as f: indonesian_data = json.load(f)
with open(NO_FILE, "r", encoding="utf-8") as f: norwegian_data = json.load(f)
with open(TR_FILE, "r", encoding="utf-8") as f: turkish_data = json.load(f)
with open(TRQ_FILE, "r", encoding="utf-8") as f: transliteration_data = json.load(f)

# ---- Build combined ayah list ----
combined_ayahs = []

surah_map_ar  = {(s.get("number") or s.get("id")): s for s in arabic_data}
surah_map_en  = {(s.get("number") or s.get("id")): s for s in english_data}
surah_map_ur  = {(s.get("number") or s.get("id")): s for s in urdu_data}
surah_map_bn  = {(s.get("number") or s.get("id")): s for s in bangla_data}
surah_map_fr  = {(s.get("number") or s.get("id")): s for s in french_data}
surah_map_es  = {(s.get("number") or s.get("id")): s for s in spanish_data}
surah_map_zh  = {(s.get("number") or s.get("id")): s for s in chinese_data}
surah_map_ru  = {(s.get("number") or s.get("id")): s for s in russian_data}
surah_map_id  = {(s.get("number") or s.get("id")): s for s in indonesian_data}
surah_map_no  = {(s.get("number") or s.get("id")): s for s in norwegian_data}
surah_map_tr  = {(s.get("number") or s.get("id")): s for s in turkish_data}
surah_map_trq = {(s.get("number") or s.get("id")): s for s in transliteration_data}

for surah_num in range(1, 115):
    surah_ar  = surah_map_ar.get(surah_num)
    if not surah_ar:
        continue
    surah_en  = surah_map_en.get(surah_num)
    surah_ur  = surah_map_ur.get(surah_num)
    surah_bn  = surah_map_bn.get(surah_num)
    surah_fr  = surah_map_fr.get(surah_num)
    surah_es  = surah_map_es.get(surah_num)
    surah_zh  = surah_map_zh.get(surah_num)
    surah_ru  = surah_map_ru.get(surah_num)
    surah_id  = surah_map_id.get(surah_num)
    surah_no  = surah_map_no.get(surah_num)
    surah_tr  = surah_map_tr.get(surah_num)
    surah_trq = surah_map_trq.get(surah_num)

    verses_ar  = surah_ar.get("ayahs") or surah_ar.get("verses") or []
    verses_en  = surah_en.get("ayahs") or surah_en.get("verses") or [] if surah_en else []
    verses_ur  = surah_ur.get("ayahs") or surah_ur.get("verses") or [] if surah_ur else []
    verses_bn  = surah_bn.get("ayahs") or surah_bn.get("verses") or [] if surah_bn else []
    verses_fr  = surah_fr.get("ayahs") or surah_fr.get("verses") or [] if surah_fr else []
    verses_es  = surah_es.get("ayahs") or surah_es.get("verses") or [] if surah_es else []
    verses_zh  = surah_zh.get("ayahs") or surah_zh.get("verses") or [] if surah_zh else []
    verses_ru  = surah_ru.get("ayahs") or surah_ru.get("verses") or [] if surah_ru else []
    verses_id  = surah_id.get("ayahs") or surah_id.get("verses") or [] if surah_id else []
    verses_no  = surah_no.get("ayahs") or surah_no.get("verses") or [] if surah_no else []
    verses_tr  = surah_tr.get("ayahs") or surah_tr.get("verses") or [] if surah_tr else []
    verses_trq = surah_trq.get("ayahs") or surah_trq.get("verses") or [] if surah_trq else []

    for i, verse_ar in enumerate(verses_ar):
        ayah_num = verse_ar.get("number") or verse_ar.get("id")

        verse_en  = verses_en[i]  if i < len(verses_en)  else {}
        verse_ur  = verses_ur[i]  if i < len(verses_ur)  else {}
        verse_bn  = verses_bn[i]  if i < len(verses_bn)  else {}
        verse_fr  = verses_fr[i]  if i < len(verses_fr)  else {}
        verse_es  = verses_es[i]  if i < len(verses_es)  else {}
        verse_zh  = verses_zh[i]  if i < len(verses_zh)  else {}
        verse_ru  = verses_ru[i]  if i < len(verses_ru)  else {}
        verse_id  = verses_id[i]  if i < len(verses_id)  else {}
        verse_no  = verses_no[i]  if i < len(verses_no)  else {}
        verse_tr  = verses_tr[i]  if i < len(verses_tr)  else {}
        verse_trq = verses_trq[i] if i < len(verses_trq) else {}

        text_ar = verse_ar.get("text", "")

        text_en = verse_en.get("translation") or verse_en.get("text", "")
        text_ur = verse_ur.get("translation") or verse_ur.get("text", "")
        text_bn = verse_bn.get("translation") or verse_bn.get("text", "")
        text_fr = verse_fr.get("translation") or verse_fr.get("text", "")
        text_es = verse_es.get("translation") or verse_es.get("text", "")
        text_zh = verse_zh.get("translation") or verse_zh.get("text", "")
        text_ru = verse_ru.get("translation") or verse_ru.get("text", "")
        text_id = verse_id.get("translation") or verse_id.get("text", "")
        text_no = verse_no.get("translation") or verse_no.get("text", "")
        text_tr = ""  # ensure defined even if verse_tr missing
        if verse_tr:
            text_tr = verse_tr.get("translation") or verse_tr.get("text", "")
        text_trq = verse_trq.get("transliteration") or verse_trq.get("text", "")

        combined_ayahs.append({
            "surah": surah_num,
            "ayah": ayah_num,
            "text_ar": text_ar,
            "text_en": text_en,
            "text_ur": text_ur,
            "text_bn": text_bn,
            "text_fr": text_fr,
            "text_es": text_es,
            "text_zh": text_zh,
            "text_ru": text_ru,
            "text_id": text_id,
            "text_no": text_no,
            "text_tr": text_tr,
            "text_trq": text_trq
        })

# ---- Search endpoint ----
@app.route("/search", methods=["GET"])
def search():
    from difflib import SequenceMatcher

    # Accept both ?word= and ?q= for compatibility
    query = (request.args.get("word") or request.args.get("q") or "").strip()
    lang  = (request.args.get("lang") or "ar").strip().lower()
    page  = int(request.args.get("page", 1))
    size  = int(request.args.get("size", 5))

    results = []  # important: avoid NameError

    if not query:
        return jsonify(results)

    field_map = {
        "ar":  "text_ar",
        "en":  "text_en",
        "ur":  "text_ur",
        "bn":  "text_bn",
        "fr":  "text_fr",
        "es":  "text_es",
        "zh":  "text_zh",
        "ru":  "text_ru",
        "id":  "text_id",
        "no":  "text_no",
        "tr":  "text_tr",
        "trq": "text_trq",  # <-- correct key matches combined_ayahs
    }
    search_field = field_map.get(lang, "text_ar")

    def normalize_arabic(text: str) -> str:
        return (text.replace(" ", "")
                    .replace("َ", "").replace("ُ", "").replace("ِ", "")
                    .replace("ّ", "").replace("ْ", "")
                    .replace("ً", "").replace("ٌ", "").replace("ٍ", ""))

    for verse in combined_ayahs:
        content = verse.get(search_field, "")
        if lang in ["en", "trq"]:
            if query.lower() in content.lower():
                results.append(verse)
        elif lang == "ar":
            norm_q = normalize_arabic(query)
            norm_c = normalize_arabic(content)
            score = SequenceMatcher(None, norm_q, norm_c).ratio()
            if score >= 0.6:
                results.append(verse)
        else:
            if query in content:
                results.append(verse)

    start = (page - 1) * size
    end   = start + size
    return jsonify(results[start:end])

# Ensure Arabic renders properly
app.config['JSON_AS_ASCII'] = False

if __name__ == "__main__":
    # Replit: bind 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
