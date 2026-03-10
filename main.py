import telebot
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from gtts import gTTS
import re
import os
import tempfile

# Bot tokenini kiriting
BOT_TOKEN = '8685110661:AAHRi4s8UoK4h2T2OokPf9LL-UFEycslNRE'
bot = telebot.TeleBot(BOT_TOKEN)

# Talaffuz lug'ati
pronunciation_dict = {
    'hello': 'həˈloʊ', 'world': 'wɜːrld', 'book': 'bʊk', 'water': 'ˈwɔːtər',
    'food': 'fuːd', 'house': 'haʊs', 'love': 'lʌv', 'thank': 'θæŋk',
    'you': 'juː', 'welcome': 'ˈwelkəm', 'goodbye': 'ɡʊdˈbaɪ', 'yes': 'jes',
    'no': 'noʊ', 'please': 'pliːz', 'sorry': 'ˈsɒri', 'friend': 'frend',
    'family': 'ˈfæməli', 'time': 'taɪm', 'day': 'deɪ', 'night': 'naɪt',
    'good': 'ɡʊd', 'bad': 'bæd', 'big': 'bɪɡ', 'small': 'smɔːl',
    'happy': 'ˈhæpi', 'sad': 'sæd', 'beautiful': 'ˈbjuːtɪfl',
    'important': 'ɪmˈpɔːrtnt', 'different': 'ˈdɪfrənt', 'possible': 'ˈpɑːsəbl',
    'necessary': 'ˈnesəseri', 'work': 'wɜːrk', 'study': 'ˈstʌdi',
    'learn': 'lɜːrn', 'teach': 'tiːtʃ', 'read': 'riːd', 'write': 'raɪt',
    'speak': 'spiːk', 'listen': 'ˈlɪsn', 'understand': 'ˌʌndərˈstænd',
    'know': 'noʊ', 'think': 'θɪŋk', 'want': 'wɑːnt', 'need': 'niːd',
    'like': 'laɪk', 'help': 'help', 'give': 'ɡɪv', 'take': 'teɪk',
    'come': 'kʌm', 'go': 'ɡoʊ', 'morning': 'ˈmɔːrnɪŋ', 'evening': 'ˈiːvnɪŋ',
    'today': 'təˈdeɪ', 'tomorrow': 'təˈmɑːroʊ', 'yesterday': 'ˈjestərdeɪ',
    'now': 'naʊ', 'later': 'ˈleɪtər', 'before': 'bɪˈfɔːr', 'after': 'ˈæftər',
    'always': 'ˈɔːlweɪz', 'never': 'ˈnevər', 'sometimes': 'ˈsʌmtaɪmz',
    'often': 'ˈɔːfn', 'many': 'ˈmeni', 'much': 'mʌtʃ', 'few': 'fjuː',
    'little': 'ˈlɪtl', 'all': 'ɔːl', 'some': 'sʌm', 'any': 'ˈeni',
    'every': 'ˈevri', 'new': 'nuː', 'old': 'oʊld', 'young': 'jʌŋ',
    'long': 'lɔːŋ', 'short': 'ʃɔːrt', 'hot': 'hɑːt', 'cold': 'koʊld',
    'easy': 'ˈiːzi', 'hard': 'hɑːrd', 'right': 'raɪt', 'wrong': 'rɔːŋ',
    'strong': 'strɔːŋ', 'weak': 'wiːk', 'fast': 'fæst', 'slow': 'sloʊ',
    'high': 'haɪ', 'low': 'loʊ', 'computer': 'kəmˈpjuːtər', 'computers': 'kəmˈpjuːtərz',
    'recognize': 'ˈrekəɡnaɪz', 'understand': 'ˌʌndərˈstænd', 'text': 'tekst',
    'stored': 'stɔːrd', 'human': 'ˈhjuːmən', 'language': 'ˈlæŋɡwɪdʒ',
    'generates': 'ˈdʒenəreɪts', 'natural': 'ˈnætʃrəl', 'allowing': 'əˈlaʊɪŋ',
    'users': 'ˈjuːzərz', 'draw': 'drɔː', 'useful': 'ˈjuːsfl', 'insights': 'ˈɪnsaɪts',
    'inferences': 'ˈɪnfərənsɪz', 'data': 'ˈdeɪtə', 'optimize': 'ˈɑːptɪmaɪz',
    'real-world': 'riːl-wɜːrld', 'decisions': 'dɪˈsɪʒnz', 'actions': 'ˈækʃnz',
    'enables': 'ɪˈneɪblz', 'also': 'ˈɔːlsoʊ', 'allows': 'əˈlaʊz',
}


def detect_language(text):
    """
    Tilni aniq aniqlash - YANGI VERSIYA
    Returns: 'uz' yoki 'en'
    """
    text_lower = text.lower().strip()

    # 1. O'zbek harflarini tekshirish (ENG MUHIM)
    uzbek_chars = set("oʻgʻʼ'ўқғҳ")
    if any(char in text_lower for char in uzbek_chars):
        print(f"O'zbek harfi topildi: {text}")
        return 'uz'

    # 2. O'zbek so'zlarini tekshirish
    uzbek_keywords = {
        'men', 'sen', 'u', 'biz', 'siz', 'ular',
        'va', 'yoki', 'lekin', 'uchun', 'bilan',
        'dan', 'ga', 'ni', 'ning', 'da', 'na',
        'bu', 'shu', 'o\'', 'qilish', 'berish',
        'olish', 'ketish', 'kelish', 'borish',
        'talaba', 'talabaman', 'o\'qiyman', 'ishlayapman',
        'salom', 'xayr', 'rahmat', 'kechirasiz'
    }

    words = text_lower.split()
    uzbek_word_count = sum(1 for word in words if word in uzbek_keywords)

    if uzbek_word_count > 0:
        print(f"O'zbek so'zi topildi: {uzbek_word_count} ta")
        return 'uz'

    # 3. langdetect kutubxonasidan foydalanish
    try:
        detected = detect(text)
        print(f"langdetect natijasi: {detected}")

        # Agar ingliz deb aniqlasa
        if detected == 'en':
            # Faqat lotin harflari borligini tekshirish
            if re.match(r'^[a-zA-Z\s\.\,\!\?\-\']+$', text):
                return 'en'

        # Agar boshqa til deb aniqlasa, o'zbek deb hisoblaymiz
        return 'uz'

    except:
        print("langdetect ishlamadi")
        pass

    # 4. Ingliz so'zlarini tekshirish (eng oxirida)
    english_common_words = {
        'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'can', 'could', 'should', 'may', 'might', 'must', 'shall',
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'my', 'your', 'his', 'her', 'its', 'our', 'their',
        'this', 'that', 'these', 'those', 'what', 'which', 'who',
        'when', 'where', 'why', 'how', 'a', 'an', 'and', 'or', 'but',
        'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
        'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under',
        'nlp', 'enables', 'computers', 'recognize', 'understand',
        'text', 'stored', 'human', 'language', 'also', 'generates',
        'natural', 'allowing', 'users', 'draw', 'useful', 'insights'
    }

    english_count = sum(1 for word in words if word in english_common_words)

    # Agar ingliz so'zlari ko'p bo'lsa
    if english_count >= len(words) * 0.3:  # 30% dan ko'p ingliz so'zlari
        print(f"Ingliz so'zlari: {english_count}/{len(words)}")
        return 'en'

    # Default: O'zbek
    print("Default: O'zbek")
    return 'uz'


def get_pronunciation(word):
    """So'z talaffuzini olish"""
    word_lower = word.lower().strip()
    word_lower = re.sub(r'[^\w\s-]', '', word_lower)

    if word_lower in pronunciation_dict:
        return pronunciation_dict[word_lower]

    return f"[{word_lower}]"


def create_audio(text, lang='en'):
    """Audio fayl yaratish"""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_filename = temp_file.name
        temp_file.close()

        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(temp_filename)

        return temp_filename
    except Exception as e:
        print(f"Audio yaratishda xatolik: {str(e)}")
        return None


def translate_text(text):
    """Matnni tarjima qilish - TO'LIQ QAYTA YOZILGAN"""
    try:
        # Tilni aniqlash
        detected_lang = detect_language(text)
        print(f"\n{'=' * 50}")
        print(f"Matn: {text}")
        print(f"Aniqlangan til: {detected_lang}")
        print(f"{'=' * 50}\n")

        # INGLIZ TILIDAN O'ZBEKCHAGA
        if detected_lang == 'en':
            print("INGLIZ → O'ZBEK tarjima boshlandi...")

            # Rus tili orqali tarjima
            try:
                translator = GoogleTranslator(source='en', target='ru')
                translation = translator.translate(text)
                print(f"Tarjima (ruscha): {translation}")
            except Exception as e:
                print(f"Tarjima xatosi: {str(e)}")
                translation = text

            # Talaffuz va audio (asl inglizcha matn uchun)
            words = text.split()
            pronunciations = []
            for word in words[:5]:
                pronunciations.append(get_pronunciation(word))
            pronunciation = " ".join(pronunciations)

            audio_file = create_audio(text, lang='en')

            return {
                'original': text,
                'translation': translation,
                'from_lang': '🇬🇧 Inglizcha',
                'to_lang': '🇺🇿 O\'zbekcha',
                'pronunciation': pronunciation,
                'audio_file': audio_file,
                'audio_lang': 'en'
            }

        # O'ZBEK TILIDAN INGLIZCHAGA
        else:
            print("O'ZBEK → INGLIZ tarjima boshlandi...")

            # Rus tili orqali tarjima
            try:
                translator_to_ru = GoogleTranslator(source='auto', target='ru')
                russian_text = translator_to_ru.translate(text)
                print(f"Oraliq tarjima (ruscha): {russian_text}")

                translator_ru_to_en = GoogleTranslator(source='ru', target='en')
                translation = translator_ru_to_en.translate(russian_text)
                print(f"Yakuniy tarjima (inglizcha): {translation}")

            except Exception as e:
                print(f"Tarjima xatosi: {str(e)}")
                try:
                    translator_direct = GoogleTranslator(source='auto', target='en')
                    translation = translator_direct.translate(text)
                except:
                    translation = text

            # Talaffuz va audio (inglizcha tarjima uchun)
            words = translation.split()
            pronunciations = []
            for word in words[:5]:
                pronunciations.append(get_pronunciation(word))
            pronunciation = " ".join(pronunciations)

            audio_file = create_audio(translation, lang='en')

            return {
                'original': text,
                'translation': translation,
                'from_lang': '🇺🇿 O\'zbekcha',
                'to_lang': '🇬🇧 Inglizcha',
                'pronunciation': pronunciation,
                'audio_file': audio_file,
                'audio_lang': 'en'
            }

    except Exception as e:
        print(f"Umumiy xato: {str(e)}")
        try:
            audio_file = create_audio(text, lang='en')
            return {
                'original': text,
                'translation': f"⚠️ Tarjima xatosi: {text}",
                'from_lang': '❓ Noma\'lum',
                'to_lang': '❓ Noma\'lum',
                'pronunciation': f"[xato]",
                'audio_file': audio_file,
                'audio_lang': 'en'
            }
        except:
            return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🌐 O'zbek-Ingliz Tarjimon Botga xush kelibsiz!

📝 Foydalanish juda oddiy:
Istalgan so'z yoki jumlani yuboring!

✨ Imkoniyatlar:
• 🔄 Avtomatik til aniqlash
• 🇺🇿 O'zbek → 🇬🇧 Ingliz tarjima
• 🇬🇧 Ingliz → 🇺🇿 O'zbek tarjima
• 📖 Inglizcha talaffuz (IPA)
• 🔊 Audio talaffuz

💡 Misol:
• "men talabaman" → "I am a student"
• "hello" → "привет" (ruscha)
• "NLP enables computers..." → ruscha tarjima

🎯 Faqat matn yuboring - bot avtomatik aniqlaydi!
    """
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
❓ Yordam:

1️⃣ Istalgan so'z yoki jumlani yozing
2️⃣ Bot avtomatik tilni aniqlaydi
3️⃣ Tarjima, talaffuz va audio ko'rsatiladi

📌 Buyruqlar:
/start - Botni qayta boshlash
/help - Yordam

🌟 Test uchun:
• "salom" (o'zbek → ingliz)
• "hello" (ingliz → o'zbek)
• "men talabaman" (o'zbek → ingliz)
• "good morning" (ingliz → o'zbek)
    """
    bot.reply_to(message, help_text)


@bot.message_handler(func=lambda message: True)
def handle_translation(message):
    text = message.text.strip()

    if not text:
        bot.reply_to(message, "❌ Iltimos, so'z yoki jumla kiriting")
        return

    waiting_msg = bot.reply_to(message, "⏳ Tarjima qilinmoqda...")

    try:
        result = translate_text(text)

        if result:
            response = f"""
{result['from_lang']} ➡️ {result['to_lang']}

📝 Asl matn:
{result['original']}

✅ Tarjima:
{result['translation']}

🔊 Talaffuz:
{result['pronunciation']}
            """
            bot.edit_message_text(response, waiting_msg.chat.id, waiting_msg.message_id)

            if result.get('audio_file') and os.path.exists(result['audio_file']):
                try:
                    with open(result['audio_file'], 'rb') as audio:
                        audio_text = result['original'] if result['from_lang'] == '🇬🇧 Inglizcha' else result[
                            'translation']
                        bot.send_voice(
                            message.chat.id,
                            audio,
                            caption=f"🔊 Audio: {audio_text}"
                        )
                    os.remove(result['audio_file'])
                except Exception as e:
                    print(f"Audio yuborishda xatolik: {str(e)}")
        else:
            bot.edit_message_text(
                "❌ Tarjima qilishda xatolik. Qaytadan urinib ko'ring.",
                waiting_msg.chat.id,
                waiting_msg.message_id
            )
    except Exception as e:
        bot.edit_message_text(
            f"❌ Xatolik yuz berdi. Internet aloqasini tekshiring.",
            waiting_msg.chat.id,
            waiting_msg.message_id
        )
        print(f"Xatolik: {str(e)}")


if __name__ == '__main__':
    print("🤖 Tarjimon bot ishga tushdi...")
    print("📡 Xabarlarni kutmoqda...")
    print("🔊 Audio yoqilgan!")
    print("=" * 50)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot xatosi: {str(e)}")