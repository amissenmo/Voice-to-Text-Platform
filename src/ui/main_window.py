from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QComboBox, QLineEdit,
                             QListWidget, QSplitter, QListWidgetItem, QDialog, QTextBrowser)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor

from src.core.speech_engine import SpeechRecognizerThread
from src.database.db_manager import DatabaseManager

# ==================== Advanced Theme Engine (7 Distinct Themes) ====================
THEMES = {
    "Light (Default)": {
        "bg": "#f3f4f6", "panel": "#ffffff", "text": "#1f2937",
        "border": "#d1d5db", "primary": "#2563eb", "primary_text": "#ffffff",
        "record_btn": "#16a34a", "stop_btn": "#dc2626", "btn_text": "#ffffff"
    },
    "Dark Modern": {
        "bg": "#111827", "panel": "#1f2937", "text": "#f9fafb",
        "border": "#374151", "primary": "#3b82f6", "primary_text": "#ffffff",
        "record_btn": "#22c55e", "stop_btn": "#ef4444", "btn_text": "#ffffff"
    },
    "Ocean Blue": {
        "bg": "#0c4a6e", "panel": "#0369a1", "text": "#e0f2fe",
        "border": "#0284c7", "primary": "#38bdf8", "primary_text": "#0c4a6e",
        "record_btn": "#10b981", "stop_btn": "#f1f5f9", "btn_text": "#0f172a"
    },
    "Warm Sunset": {
        "bg": "#fff7ed", "panel": "#ffedd5", "text": "#431407",
        "border": "#fdba74", "primary": "#ea580c", "primary_text": "#ffffff",
        "record_btn": "#16a34a", "stop_btn": "#b91c1c", "btn_text": "#ffffff"
    },
    "Neutral Mocha": {
        "bg": "#f5f5f4", "panel": "#e7e5e4", "text": "#292524",
        "border": "#d6d3d1", "primary": "#57534e", "primary_text": "#ffffff",
        "record_btn": "#65a30d", "stop_btn": "#991b1b", "btn_text": "#ffffff"
    },
    "Forest Green": {
        "bg": "#064e3b", "panel": "#065f46", "text": "#ecfdf5",
        "border": "#059669", "primary": "#10b981", "primary_text": "#064e3b",
        "record_btn": "#a3e635", "stop_btn": "#f87171", "btn_text": "#064e3b"
    },
    "High Contrast": {
        "bg": "#000000", "panel": "#000000", "text": "#ffffff",
        "border": "#ffffff", "primary": "#eab308", "primary_text": "#000000",
        "record_btn": "#22c55e", "stop_btn": "#ef4444", "btn_text": "#ffffff"
    }
}


def generate_stylesheet(theme_name: str) -> str:
    t = THEMES.get(theme_name, THEMES["Light (Default)"])
    return f"""
        QMainWindow, QDialog, QWidget#main_widget {{ background-color: {t['bg']}; }}
        QLabel {{ color: {t['text']}; font-size: 13px; }}
        QTextEdit, QListWidget, QLineEdit, QTextBrowser {{ 
            background-color: {t['panel']}; color: {t['text']}; 
            border: 1px solid {t['border']}; border-radius: 6px; padding: 8px; font-size: 14px;
        }}
        QPushButton {{ 
            background-color: {t['primary']}; color: {t['primary_text']}; 
            border: none; border-radius: 6px; padding: 8px 16px; font-weight: bold; font-size: 13px;
        }}
        QPushButton:hover {{ opacity: 0.8; border: 1px solid {t['border']}; }}
        QPushButton#record_btn_start {{ background-color: {t['record_btn']}; color: {t['btn_text']}; }}
        QPushButton#record_btn_stop {{ background-color: {t['stop_btn']}; color: {t['btn_text']}; }}
        QComboBox {{ 
            background-color: {t['panel']}; color: {t['text']}; 
            border: 1px solid {t['border']}; border-radius: 4px; padding: 5px; min-width: 120px;
        }}
        QComboBox QAbstractItemView {{ background-color: {t['panel']}; color: {t['text']}; }}
        QSplitter::handle {{ background-color: {t['border']}; width: 1px; }}
    """


# ==================== Help Center Dialog ====================
class HelpDialog(QDialog):
    def __init__(self, parent=None, current_theme="Light (Default)"):
        super().__init__(parent)
        self.setWindowTitle("Help Center")
        self.resize(650, 500)
        self.setStyleSheet(generate_stylesheet(current_theme))

        self.layout = QVBoxLayout(self)

        self.lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Guide Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "فارسی"])
        self.lang_combo.currentTextChanged.connect(self.update_content)
        self.lang_layout.addStretch()
        self.lang_layout.addWidget(self.lang_label)
        self.lang_layout.addWidget(self.lang_combo)
        self.layout.addLayout(self.lang_layout)

        self.browser = QTextBrowser()
        self.layout.addWidget(self.browser)

        self.close_btn = QPushButton("Close")
        self.close_btn.setMinimumHeight(40)
        self.close_btn.clicked.connect(self.accept)
        self.layout.addWidget(self.close_btn)

        self.update_content("English")

    def update_content(self, language: str):
        if language == "English":
            self.browser.setHtml("""
                <h2>Comprehensive User Guide</h2>
                <p><b>1. Network Prerequisites:</b> This application utilizes an isolated proxy tunnel for high-speed transcription. You must have a proxy application (e.g., v2rayN) running in the background. It is not necessary to set the system proxy.</p>
                <p><b>2. How to Record:</b> Select your desired language from the top menu. Click the <b>Start Recording</b> button and begin speaking. The system processes your voice intelligently. When you pause (approx. 1.5 seconds), the engine will extract and type the text.</p>
                <p><b>3. Smart Cursor Insertion:</b> The transcribed text is strictly inserted wherever your text cursor is currently positioned inside the editor. You can click anywhere to append or correct text.</p>
                <p><b>4. Managing History:</b> To save a document, you must enter a Subject. You can retrieve past documents from the left panel. Opening a past document allows you to edit and update it using the same save button.</p>
            """)
            self.browser.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        else:
            self.browser.setHtml("""
                <div align='right' style='direction: rtl;'>
                <h2>راهنمای جامع استفاده از پلتفرم</h2>
                <p><b>۱. پیش‌نیازهای شبکه:</b> این پلتفرم برای دستیابی به بالاترین سرعت، از یک تونل شبکه ایزوله استفاده می‌کند. نرم‌افزار عبور از تحریم شما (مانند v2rayN) حتماً باید در پس‌زمینه ویندوز در حال اجرا باشد. نیازی به تنظیم System Proxy نیست.</p>
                <p><b>۲. نحوه ضبط و تبدیل:</b> ابتدا زبان مورد نظر خود را از منوی بالا انتخاب کنید. روی دکمه <b>Start Recording</b> کلیک کرده و شروع به صحبت کنید. سیستم به صورت هوشمند منتظر می‌ماند تا شما مکث کنید و سپس متن را تولید می‌کند.</p>
                <p><b>۳. تایپ هوشمند و تعاملی:</b> متن‌های تولید شده دقیقاً در نقطه‌ای از ادیتور تایپ می‌شوند که نشانگر موس شما در آنجا قرار دارد. می‌توانید آزادانه بین کلمات کلیک کرده و متن جدید را در آنجا دیکته کنید.</p>
                <p><b>۴. مدیریت تاریخچه متون:</b> برای ذخیره هر متن، وارد کردن موضوع الزامی است. با انتخاب متن‌های قبلی از پنل سمت چپ، می‌توانید آن‌ها را مجدداً باز کرده، ویرایش کنید و تغییرات را روی همان فایل ذخیره (Update) نمایید.</p>
                </div>
            """)
            self.browser.setLayoutDirection(Qt.LayoutDirection.RightToLeft)


# ==================== Main Application Window ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V2T")
        self.resize(1150, 750)
        self.setMinimumSize(950, 600)

        self.db = DatabaseManager()
        self.speech_thread = SpeechRecognizerThread()
        self.current_record_id = None
        self.current_theme = "Light (Default)"

        self.setup_ui()
        self.connect_signals()
        self.load_history()
        self.apply_theme(self.current_theme)

    def setup_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setObjectName("main_widget")
        self.setCentralWidget(self.central_widget)

        main_font = QFont("Segoe UI", 10)
        self.setFont(main_font)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Left Panel: History ---
        self.history_panel = QWidget()
        self.history_layout = QVBoxLayout(self.history_panel)
        self.history_layout.setContentsMargins(0, 0, 10, 0)

        self.history_label = QLabel("Transcription History")
        self.history_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.history_layout.addWidget(self.history_label)

        self.history_list = QListWidget()
        self.history_layout.addWidget(self.history_list)

        self.load_btn = QPushButton("Load Selected Text")
        self.load_btn.setMinimumHeight(40)
        self.history_layout.addWidget(self.load_btn)

        # --- کدهای جدید برای دکمه حذف ---
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setMinimumHeight(40)
        # اعمال استایل اختصاصی قرمز رنگ برای دکمه حذف
        self.delete_btn.setStyleSheet("background-color: #ef4444; color: white; font-weight: bold; border-radius: 6px;")
        self.history_layout.addWidget(self.delete_btn)

        # --- Right Panel: Editor & Controls ---
        self.editor_panel = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_panel)
        self.editor_layout.setContentsMargins(10, 0, 0, 0)

        self.top_controls = QHBoxLayout()
        self.lang_label = QLabel("Recognition Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["فارسی (fa-IR)", "English (en-US)"])

        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))

        self.help_btn = QPushButton("Help Center")

        self.top_controls.addWidget(self.lang_label)
        self.top_controls.addWidget(self.lang_combo)
        self.top_controls.addStretch()
        self.top_controls.addWidget(self.theme_label)
        self.top_controls.addWidget(self.theme_combo)
        self.top_controls.addWidget(self.help_btn)
        self.editor_layout.addLayout(self.top_controls)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter the document subject here...")
        self.subject_input.setMinimumHeight(40)
        self.editor_layout.addWidget(self.subject_input)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText(
            "Click 'Start Recording' to begin speaking...\n(The transcribed text will be automatically inserted at your cursor's position)")
        self.text_editor.setStyleSheet("font-size: 15px; line-height: 1.6;")
        self.editor_layout.addWidget(self.text_editor)

        self.bottom_controls = QHBoxLayout()
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.setObjectName("record_btn_start")
        self.record_btn.setMinimumHeight(45)
        self.record_btn.setMinimumWidth(150)

        self.save_btn = QPushButton("Save to History")
        self.save_btn.setMinimumHeight(45)

        self.status_label = QLabel("Status: Ready to record")
        self.status_label.setStyleSheet("font-style: italic; font-weight: bold;")

        self.bottom_controls.addWidget(self.record_btn)
        self.bottom_controls.addWidget(self.save_btn)
        self.bottom_controls.addStretch()
        self.bottom_controls.addWidget(self.status_label)
        self.editor_layout.addLayout(self.bottom_controls)

        splitter.addWidget(self.history_panel)
        splitter.addWidget(self.editor_panel)
        splitter.setSizes([350, 800])
        self.main_layout.addWidget(splitter)

        # --- Interactive Toast Notification System (5 seconds + Close Button) ---
        self.toast_widget = QWidget(self.central_widget)
        self.toast_widget.setObjectName("toast_widget")
        self.toast_layout = QHBoxLayout(self.toast_widget)
        self.toast_layout.setContentsMargins(15, 10, 10, 10)

        self.toast_label = QLabel("")
        self.toast_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px; border: none;")

        self.toast_close_btn = QPushButton("✕")
        self.toast_close_btn.setFixedSize(26, 26)
        self.toast_close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toast_close_btn.setStyleSheet(
            "background-color: transparent; color: white; font-weight: bold; border: none; font-size: 14px;")

        self.toast_layout.addWidget(self.toast_label)
        self.toast_layout.addWidget(self.toast_close_btn)

        self.toast_widget.hide()

        self.toast_timer = QTimer()
        self.toast_timer.setSingleShot(True)
        # زمان محو شدن روی ۵ ثانیه (5000 میلی‌ثانیه) تنظیم شد
        self.toast_timer.timeout.connect(self.toast_widget.hide)

    def connect_signals(self):
        self.record_btn.clicked.connect(self.toggle_recording)
        self.save_btn.clicked.connect(self.save_current_text)
        self.lang_combo.currentTextChanged.connect(self.change_language)
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        self.help_btn.clicked.connect(self.show_help)

        self.load_btn.clicked.connect(self.load_selected_text)
        self.history_list.itemDoubleClicked.connect(self.load_selected_text)

        self.speech_thread.text_recognized.connect(self.insert_text)
        self.speech_thread.status_changed.connect(self.update_status)
        self.speech_thread.error_occurred.connect(self.show_toast)

        self.delete_btn.clicked.connect(self.delete_selected_text)

        # اتصال دکمه ضربدر برای بستن پیام به صورت دستی
        self.toast_close_btn.clicked.connect(self.toast_widget.hide)

    # ==================== Core Functions ====================
    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        stylesheet = generate_stylesheet(theme_name)
        self.setStyleSheet(stylesheet)

        # استایل‌دهی مجزای ویجت Toast برای حفظ تمایز بصری
        self.toast_widget.setStyleSheet("""
            QWidget#toast_widget {
                background-color: #ef4444; 
                border-radius: 8px;
                border: 1px solid #dc2626;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
        """)

    def show_help(self):
        dialog = HelpDialog(self, self.current_theme)
        dialog.exec()

    def toggle_recording(self):
        if not self.speech_thread.is_running:
            self.speech_thread.start()
            self.record_btn.setText("Stop Recording")
            self.record_btn.setObjectName("record_btn_stop")
            self.apply_theme(self.current_theme)
        else:
            self.speech_thread.stop_listening()
            self.record_btn.setText("Start Recording")
            self.record_btn.setObjectName("record_btn_start")
            self.apply_theme(self.current_theme)
            self.update_status("Status: Stopped")

    def insert_text(self, text):
        cursor = self.text_editor.textCursor()
        cursor.insertText(text + " ")
        self.text_editor.setTextCursor(cursor)

    def update_status(self, status_msg):
        msg_map = {
            "در حال آماده‌سازی میکروفون (تونل شبکه فعال است)...": "Status: Initializing proxy tunnel...",
            "آماده صحبت (دقت بالا + سرعت فوق‌العاده گوگل)": "Status: Ready to record",
            "در حال گوش دادن...": "Status: Listening...",
            "در حال ترجمه سریع...": "Status: Processing...",
            "خطای اتصال تونل": "Status: Proxy Connection Error",
            "میکروفون غیرفعال است": "Status: Microphone Disabled"
        }
        english_msg = msg_map.get(status_msg, f"Status: {status_msg}")
        self.status_label.setText(english_msg)

    def change_language(self, text):
        lang_code = text.split("(")[1].split(")")[0]
        self.speech_thread.set_language(lang_code)

    def show_toast(self, message):
        self.toast_label.setText(message)
        self.toast_widget.adjustSize()
        x = self.width() - self.toast_widget.width() - 30
        y = self.height() - self.toast_widget.height() - 30
        self.toast_widget.move(x, y)
        self.toast_widget.show()
        self.toast_widget.raise_()
        self.toast_timer.start(5000)

    def load_history(self):
        self.history_list.clear()
        records = self.db.get_all_history()
        for record in records:
            item = QListWidgetItem(f"{record[1]} - {record[3][:10]}")
            item.setData(Qt.ItemDataRole.UserRole, record[0])
            self.history_list.addItem(item)

    def load_selected_text(self, item=None):
        if item is None or not isinstance(item, QListWidgetItem):
            item = self.history_list.currentItem()
        if item is None:
            self.show_toast("Please select a document from the history list first.")
            return

        record_id = item.data(Qt.ItemDataRole.UserRole)
        record = self.db.get_record(record_id)
        if record:
            self.current_record_id = record_id
            self.subject_input.setText(record[0])
            self.text_editor.setPlainText(record[1])
            self.update_status(f"Status: Document '{record[0]}' loaded.")

    def delete_selected_text(self):
        item = self.history_list.currentItem()
        if item is None:
            self.show_toast("Error: Please select a document to delete.")
            return

        record_id = item.data(Qt.ItemDataRole.UserRole)

        # حذف از دیتابیس
        self.db.delete_record(record_id)

        # اگر متنی که پاک شد در حال حاضر در ادیتور باز است، ادیتور را هم پاک کن
        if self.current_record_id == record_id:
            self.current_record_id = None
            self.subject_input.clear()
            self.text_editor.clear()
            self.update_status("Status: Ready to record")

        self.load_history()
        self.show_toast("Document deleted successfully.")


    def save_current_text(self):
        subject = self.subject_input.text().strip()
        content = self.text_editor.toPlainText().strip()

        if not subject:
            self.show_toast("Error: Please provide a subject.")
            return
        if not content:
            self.show_toast("Error: There is no text to save.")
            return

        if self.current_record_id:
            self.db.update_text(self.current_record_id, content)
            self.update_status("Status: Document updated.")
        else:
            new_id = self.db.save_text(subject, content)
            self.current_record_id = new_id
            self.update_status("Status: Document saved.")
        self.load_history()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.toast_widget.isHidden():
            x = self.width() - self.toast_widget.width() - 30
            y = self.height() - self.toast_widget.height() - 30
            self.toast_widget.move(x, y)