import sys
import os

# خاموش کردن هشدارهای مربوط به Symlink در ویندوز
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# بقیه کدهای فایل...
# این سه خط برای جلوگیری از خطای ModuleNotFound است تا پایتون پوشه src را بشناسد
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    # ساخت اپلیکیشن پایه PyQt
    app = QApplication(sys.argv)

    # اعمال یک استایل مدرن و یکپارچه برای همه سیستم‌عامل‌ها
    app.setStyle("Fusion")

    # فراخوانی و نمایش پنجره اصلی
    window = MainWindow()
    window.show()

    # اجرای حلقه اصلی برنامه (Loop) تا زمانی که کاربر آن را نبندد
    sys.exit(app.exec())


if __name__ == '__main__':
    main()