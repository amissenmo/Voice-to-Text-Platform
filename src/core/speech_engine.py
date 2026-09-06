import os
import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal


class SpeechRecognizerThread(QThread):
    text_recognized = pyqtSignal(str)
    # این سیگنال را نگه می‌داریم تا UI قبلی که برای نمایش زنده نوشتیم کرش نکند
    partial_recognized = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, language="fa-IR"):
        super().__init__()
        self.language = language
        self.is_running = False

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        # مکث کوتاه ۰.۶ ثانیه‌ای برای اینکه استخراج متن سریع و نزدیک به Real-time انجام شود
        # افزایش زمان مکث به ۱.۵ ثانیه تا بتوانید وسط جملات طولانی نفس بگیرید
        self.recognizer.pause_threshold = 1.5

        # ==========================================
        # بخش مهندسی شبکه: تونل داخلی نرم‌افزار
        # ==========================================
        # پورت نرم‌افزار دور زدن تحریم خود را اینجا وارد کنید:
        # معمولاً در V2ray پورت 10809 یا 10808 است.
        # در Clash پورت 7890 است.
        # پورت نرم‌افزار دور زدن تحریم خود را اینجا وارد کنید:
        proxy_port = "10808"

        os.environ["http_proxy"] = f"http://127.0.0.1:{proxy_port}"
        os.environ["https_proxy"] = f"http://127.0.0.1:{proxy_port}"
    def set_language(self, language_code: str):
        self.language = language_code

    def stop_listening(self):
        self.is_running = False
        self.wait()

    def run(self):
        self.is_running = True
        self.status_changed.emit("در حال آماده‌سازی میکروفون (تونل شبکه فعال است)...")

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.status_changed.emit("آماده صحبت (دقت بالا + سرعت فوق‌العاده گوگل)")

                while self.is_running:
                    self.status_changed.emit("در حال گوش دادن...")
                    try:
                        # ضبط صدا در قطعات کوتاه (حداکثر ۸ ثانیه) تا حس Real-time حفظ شود
                        # برداشتن محدودیت زمانی تا هر چقدر خواستید پیوسته صحبت کنید
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=None)

                        if not self.is_running:
                            break

                        self.status_changed.emit("در حال ترجمه سریع...")

                        # درخواست از موتور گوگل که از تونل پروکسی پایتون عبور می‌کند
                        text = self.recognizer.recognize_google(audio, language=self.language)

                        if text and self.is_running:
                            self.text_recognized.emit(text)

                    except sr.UnknownValueError:
                        # وقتی سکوت بوده یا صدا نامفهوم است
                        continue
                    except sr.RequestError as e:
                        self.error_occurred.emit(f"خطا در شبکه: آیا نرم‌افزار پروکسی در پس‌زمینه باز است؟")
                        self.status_changed.emit("خطای اتصال تونل")
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        print(f"پردازش متوقف شد: {e}")

        except Exception as e:
            self.error_occurred.emit("میکروفون یافت نشد. لطفاً اتصالات ویندوز را بررسی کنید.")
            self.status_changed.emit("میکروفون غیرفعال است")