from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# Define data file paths (adjust these paths if necessary for your environment)
DATA_DIR = "data"
AR_FILE = "quran_ar.json"
EN_FILE = "quran_en.json"
UR_FILE = "quran_ur.json"
BN_FILE = "quran_bn.json"
FR_FILE = "quran_fr.json"
ES_FILE = "quran_es.json"
ZH_FILE = "quran_zh.json"
RU_FILE = "quran_ru.json"
ID_FILE = "quran_id.json"
NO_FILE = "quran_sv.json"
TR_FILE = "quran_tr.json"
TRQ_FILE = "quran_trq.json"

# Load the Quran data from all four JSON files at app startup
with open(AR_FILE, "r", encoding="utf-8") as f:
    arabic_data = json.load(f)
with open(EN_FILE, "r", encoding="utf-8") as f:
    english_data = json.load(f)
with open(UR_FILE, "r", encoding="utf-8") as f:
    urdu_data = json.load(f)
with open(BN_FILE, "r", encoding="utf-8") as f:
    bangla_data = json.load(f)
with open(FR_FILE, "r", encoding="utf-8") as f:
    french_data = json.load(f)
with open(ES_FILE, "r", encoding="utf-8") as f:
    spanish_data = json.load(f)
with open(ZH_FILE, "r", encoding="utf-8") as f:
    chinese_data = json.load(f)
with open(RU_FILE, "r", encoding="utf-8") as f:
    russian_data = json.load(f)
with open(ID_FILE, "r", encoding="utf-8") as f:
    indonesian_data = json.load(f)
with open(NO_FILE, "r", encoding="utf-8") as f:
    norwegian_data = json.load(f)
with open(TR_FILE, "r", encoding="utf-8") as f:
    turkish_data = json.load(f)
with open(TRQ_FILE, "r", encoding="utf-8") as f:
    transliteration_data = json.load(f)

# Combine verses from all languages into a single list for easier searching.
# Each entry in combined_ayahs will be a dictionary containing surah number, ayah number,
# and the text of that ayah in Arabic, English, Urdu, and transliteration.
combined_ayahs = []

# Create lookup dictionaries for surahs in each language (keyed by surah number)
surah_map_ar = { (s.get("number") or s.get("id")): s for s in arabic_data }
surah_map_en = { (s.get("number") or s.get("id")): s for s in english_data }
surah_map_ur = { (s.get("number") or s.get("id")): s for s in urdu_data }
surah_map_bn = { (s.get("number") or s.get("id")): s for s in bangla_data }
surah_map_fr = { (s.get("number") or s.get("id")): s for s in french_data }
surah_map_es = { (s.get("number") or s.get("id")): s for s in spanish_data }
surah_map_zh = { (s.get("number") or s.get("id")): s for s in chinese_data }
surah_map_ru = { (s.get("number") or s.get("id")): s for s in russian_data }
surah_map_id = { (s.get("number") or s.get("id")): s for s in indonesian_data }
surah_map_no = { (s.get("number") or s.get("id")): s for s in norwegian_data }
surah_map_tr = { (s.get("number") or s.get("id")): s for s in turkish_data }
surah_map_trq = { (s.get("number") or s.get("id")): s for s in transliteration_data }


# Iterate through each surah (1 to 114) and combine corresponding verses
for surah_num in range(1, 115):
    surah_ar = surah_map_ar.get(surah_num)
    surah_en = surah_map_en.get(surah_num)
    surah_ur = surah_map_ur.get(surah_num)
    surah_bn = surah_map_bn.get(surah_num)
    surah_fr = surah_map_fr.get(surah_num)
    surah_es = surah_map_es.get(surah_num)
    surah_zh = surah_map_zh.get(surah_num)
    surah_ru = surah_map_ru.get(surah_num)
    surah_id = surah_map_id.get(surah_num)
    surah_no = surah_map_no.get(surah_num)
    surah_tr = surah_map_tr.get(surah_num)
    surah_trq = surah_map_trq.get(surah_num)
    
    # Skip if any language is missing this surah (all should be present)
    if not surah_ar:
        continue

    # Get the list of verses (ayahs) for this surah in each language
    verses_ar = surah_ar.get("ayahs") or surah_ar.get("verses") or []
    verses_en = surah_en.get("ayahs") or surah_en.get("verses") or []
    verses_ur = surah_ur.get("ayahs") or surah_ur.get("verses") or []
    verses_bn = surah_bn.get("ayahs") or surah_bn.get("verses") or []
    verses_fr = surah_fr.get("ayahs") or surah_fr.get("verses") or []
    verses_es = surah_es.get("ayahs") or surah_es.get("verses") or []
    verses_zh = surah_zh.get("ayahs") or surah_zh.get("verses") or []
    verses_ru = surah_ru.get("ayahs") or surah_ru.get("verses") or []
    verses_id = surah_id.get("ayahs") or surah_id.get("verses") or []
    verses_no = surah_no.get("ayahs") or surah_no.get("verses") or []
    verses_tr = surah_tr.get("ayahs") or surah_tr.get("verses") or []
    verses_trq = surah_trq.get("ayahs") or surah_trq.get("verses") or []

    # Combine verses by index (we assume each list is ordered by ayah number)
    for i, verse_ar in enumerate(verses_ar):
        # Ayah number within the surah
        ayah_num = verse_ar.get("number") or verse_ar.get("id")
        # Get corresponding verse entries from other languages by index
        verse_en = verses_en[i] if i < len(verses_en) else None
        verse_ur = verses_ur[i] if i < len(verses_ur) else None
        verse_bn = verses_bn[i] if i < len(verses_bn) else None
        verse_fr = verses_fr[i] if i < len(verses_fr) else None
        verse_es = verses_es[i] if i < len(verses_es) else None
        verse_zh = verses_zh[i] if i < len(verses_zh) else None
        verse_ru = verses_ru[i] if i < len(verses_ru) else None
        verse_id = verses_id[i] if i < len(verses_id) else None
        verse_no = verses_no[i] if i < len(verses_no) else None
        verse_tr = verses_tr[i] if i < len(verses_tr) else None
        verse_trq = verses_trq[i] if i < len(verses_trq) else None

        # Extract the text in each language.
        # Arabic file: text is under "text"
        text_ar = verse_ar.get("text", "")

        # English/Urdu files might store the translation under "translation" if the original Arabic text is in "text"
        text_en = ""
        if verse_en:
            text_en = verse_en.get("translation") or verse_en.get("text", "")
        text_ur = ""
        if verse_ur:
            text_ur = verse_ur.get("translation") or verse_ur.get("text", "")
        text_bn = ""        
        if verse_bn:
            text_bn = verse_bn.get("translation") or verse_bn.get("text", "")
        text_fr = ""
        if verse_fr:
            text_fr = verse_fr.get("translation") or verse_fr.get("text", "")
        text_es = ""
        if verse_es:
            text_es = verse_es.get("translation") or verse_es.get("text", "")
        text_zh = ""
        if verse_zh:
            text_zh = verse_zh.get("translation") or verse_zh.get("text", "")
        text_ru = ""
        if verse_ru:
            text_ru = verse_ru.get("translation") or verse_ru.get("text", "")
        text_id = ""
        if verse_id:
            text_id = verse_id.get("translation") or verse_id.get("text", "")
        text_no = ""
        if verse_no:
            text_no = verse_no.get("translation") or verse_no.get("text", "")
        text_trq = ""
        if verse_tr:
            text_tr = verse_tr.get("translation") or verse_tr.get("text", "")
        
        text_trq = ""
        if verse_trq:
            text_trq = verse_trq.get("transliteration") or verse_trq.get("text", "")

        # Append a combined record for this verse containing all languages
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
            "text_trq":text_trq
        })

# Search endpoint: /search?word=<query>&lang=<ar|en|ur|transliteration>&page=<n>&size=<m>
@app.route("/search", methods=["GET"])

def search():
    from difflib import SequenceMatcher

    query = request.args.get("word", "").strip()
    lang = request.args.get("lang", "ar").strip().lower()
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))

    if not query:
        return jsonify(results)

    field_map = {
        "ar": "text_ar",
        "en": "text_en",
        "ur": "text_ur",
        "bn": "text_bn",
        "fr": "text_fr",
        "es": "text_es",
        "zh": "text_zh",
        "ru": "text_ru",
        "id": "text_id",
        "no": "text_no",
        "tr": "text_tr",
        "trq": "text_transliteration"
    }
    search_field = field_map.get(lang, "text_ar")

    def normalize_arabic(text):
        return text.replace(" ", "").replace("َ", "").replace("ُ", "").replace("ِ", "")\
                   .replace("ّ", "").replace("ْ", "").replace("ً", "").replace("ٌ", "").replace("ٍ", "")

    matches = []

    for verse in combined_ayahs:
        content = verse.get(search_field, "")
        if lang in ["en", "transliteration"]:
            if query.lower() in content.lower():
                matches.append(verse)
        elif lang == "ar":
            norm_query = normalize_arabic(query)
            norm_content = normalize_arabic(content)
            score = SequenceMatcher(None, norm_query, norm_content).ratio()
            if score >= 0.6:
                matches.append(verse)
        else:
            if query in content:
                matches.append(verse)

    start = (page - 1) * size
    end = start + size
    paginated_matches = matches[start:end]
    return jsonify(paginated_matches)

@app.route("/voice-search-ar", methods=["POST"])
def voice_search_ar():
    import whisper
    from difflib import SequenceMatcher
    import tempfile
    import os

    # Save uploaded audio file to a temporary location
    audio = request.files["audio"]
    temp_audio_path = tempfile.mktemp(suffix=".wav")
    audio.save(temp_audio_path)

    # Load Whisper model and transcribe
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio_path, language="ar")
    spoken_text = result["text"].strip()

    os.remove(temp_audio_path)

    # Normalize Arabic for comparison
    def normalize(text):
        return text.replace(" ", "").replace("َ", "").replace("ُ", "").replace("ِ", "")\
                   .replace("ّ", "").replace("ْ", "").replace("ً", "").replace("ٌ", "").replace("ٍ", "")

    norm_query = normalize(spoken_text)

    # Match with Arabic Ayahs using similarity score
    matches = []
    for verse in combined_ayahs:
        ar_text = normalize(verse.get("text_ar", ""))
        score = SequenceMatcher(None, norm_query, ar_text).ratio()
        if score >= 0.6:
            matches.append({
                "surah": verse["surah"],
                "ayah": verse["ayah"],
                "text_ar": verse["text_ar"],
                "text_transliteration": verse.get("text_transliteration", ""),
        "score": round(score, 2)
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(matches)

