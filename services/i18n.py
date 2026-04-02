# ─────────────────────────────────────────────────────────────────
# services/i18n.py — Internationalization (Multilingual Support)
# ─────────────────────────────────────────────────────────────────

from utils.logger import get_logger

log = get_logger("services.i18n")

class I18nService:
    """Manages translations and current language state."""
    
    LANGUAGES = {
        "en": "English",
        "hi": "हिन्दी",
        "ta": "தமிழ்"
    }

    def __init__(self):
        self.current_lang = "en"
        # Translation dictionary
        self.translations = {
            "en": {
                "welcome_title": "Welcome to Smart Healthcare",
                "welcome_subtitle": "Self-Service Patient Registration Kiosk",
                "btn_start": "Start Registration  →",
                "btn_emergency": "⚠  EMERGENCY",
                "identity_title": "Identity Verification",
                "aadhaar_label": "Enter your 12-digit Aadhaar Number",
                "otp_label": "Enter 6-digit OTP",
                "btn_send_otp": "Send OTP  →",
                "btn_verify_otp": "✔  Verify OTP",
                "btn_back": "←  Back",
                "btn_next": "Next  →",
                "patient_info_title": "Patient Information",
                "name_label": "Full Name",
                "dob_label": "Date of Birth",
                "gender_label": "Gender",
                "visit_label": "Visit Type",
                "symptoms_title": "Select Symptoms",
                "health_title": "Vital Signs Monitoring",
                "temp_label": "Body Temperature",
                "hr_label": "Heart Rate",
                "spo2_label": "Oxygen Saturation (SpO2)",
                "dept_label": "Recommended Department",
                "token_title": "Registration Successful",
                "token_sub": "Please take your token and wait for your turn.",
                "print_btn": "🖨 Print & Finish",
                "male": "Male", "female": "Female", "other": "Other",
                "opd": "Outpatient (OPD)", "emergency_visit": "Emergency"
            },
            "hi": {
                "welcome_title": "स्मार्ट हेल्थकेयर में आपका स्वागत है",
                "welcome_subtitle": "स्व-सेवा रोगी पंजीकरण कियॉस्क",
                "btn_start": "पंजीकरण शुरू करें  →",
                "btn_emergency": "⚠  आपातकालीन",
                "identity_title": "पहचान सत्यापन",
                "aadhaar_label": "अपना 12-अंकीय आधार नंबर दर्ज करें",
                "otp_label": "6-अंकीय ओटीपी दर्ज करें",
                "btn_send_otp": "ओटीपी भेजें  →",
                "btn_verify_otp": "✔  ओटीपी सत्यापित करें",
                "btn_back": "←  पीछे",
                "btn_next": "आगे  →",
                "patient_info_title": "रोगी की जानकारी",
                "name_label": "पूरा नाम",
                "dob_label": "जन्म तिथि",
                "gender_label": "लिंग",
                "visit_label": "यात्रा का प्रकार",
                "symptoms_title": "लक्षणों का चयन करें",
                "health_title": "महत्वपूर्ण संकेतों की निगरानी",
                "temp_label": "शरीर का तापमान",
                "hr_label": "हृदय गति",
                "spo2_label": "ऑक्सीजन संतृप्ति (SpO2)",
                "dept_label": "अनुशंसित विभाग",
                "token_title": "पंजीकरण सफल",
                "token_sub": "कृपया अपना टोकन लें और अपनी बारी का प्रतीक्षा करें।",
                "print_btn": "🖨 प्रिंट और समाप्त करें",
                "male": "पुरुष", "female": "महिला", "other": "अन्य",
                "opd": "बाहरी रोगी (OPD)", "emergency_visit": "आपातकालीन"
            },
            "ta": {
                "welcome_title": "ஸ்மார்ட் ஹெல்த்கேருக்கு வரவேற்கிறோம்",
                "welcome_subtitle": "சுய சேவை நோயாளி பதிவு மையம்",
                "btn_start": "பதிவைத் தொடங்கவும்  →",
                "btn_emergency": "⚠  அவசரம்",
                "identity_title": "அடையாள சரிபார்ப்பு",
                "aadhaar_label": "உங்கள் 12 இலக்க ஆதார் எண்ணை உள்ளிடவும்",
                "otp_label": "6 இலக்க OTP ஐ உள்ளிடவும்",
                "btn_send_otp": "OTP ஐ அனுப்பு  →",
                "btn_verify_otp": "✔  OTP ஐச் சரிபார்",
                "btn_back": "←  பின்னால்",
                "btn_next": "அடுத்து  →",
                "patient_info_title": "நோயாளி தகவல்",
                "name_label": "முழு பெயர்",
                "dob_label": "பிறந்த தேதி",
                "gender_label": "பாலினம்",
                "visit_label": "வருகை வகை",
                "symptoms_title": "அறிகுறிகளைத் தேர்ந்தெடுக்கவும்",
                "health_title": "உயிர் அறிகுறிகள் கண்காணிப்பு",
                "temp_label": "உடல் வெப்பநிலை",
                "hr_label": "இதய துடிப்பு",
                "spo2_label": "ஆக்சிஜன் அளவு (SpO2)",
                "dept_label": "பரிந்துரைக்கப்பட்ட துறை",
                "token_title": "பதிவு வெற்றிகரமாக முடிந்தது",
                "token_sub": "தயவுசெய்து உங்கள் டோக்கனை எடுத்துக்கொண்டு உங்கள் முறைக்காக காத்திருக்கவும்.",
                "print_btn": "🖨 அச்சிட்டு முடிக்கவும்",
                "male": "ஆண்", "female": "பெண்", "other": "மற்றவை",
                "opd": "வெளிநோயாளி (OPD)", "emergency_visit": "அவசரம்"
            }
        }

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.current_lang = lang_code
            log.info(f"Language changed to: {self.LANGUAGES[lang_code]}")
        else:
            log.warning(f"Unsupported language code: {lang_code}")

    def get(self, key, default=None):
        """Get translated text for the current language."""
        return self.translations.get(self.current_lang, {}).get(key, default or key)

# Global instance for easy access
i18n = I18nService()
