import os


def create_project_structure():
    # لیست پوشه‌هایی که باید ساخته شوند
    directories = [
        "src",
        "src/core",
        "src/ui",
        "src/database",
        "src/utils",
        "assets"
    ]

    # لیست فایل‌ها و محتوای پیش‌فرض آن‌ها
    files = {
        "requirements.txt": "PyQt6\nSpeechRecognition\nPyAudio\n",
        "README.md": "# پلتفرم تخصصی Voice to Text\n\nاین پروژه یک پلتفرم حرفه‌ای دو زبانه (فارسی و انگلیسی) برای تبدیل بلادرنگ صدا به متن است.\n",

        # فایل اصلی اجرایی برنامه
        "src/main.py": "import sys\n\ndef main():\n    print('پلتفرم با موفقیت پیکربندی شد. آماده توسعه هستیم!')\n\nif __name__ == '__main__':\n    main()\n",

        # ساخت فایل‌های __init__.py برای تبدیل پوشه‌ها به ماژول‌های پایتون
        "src/__init__.py": "",
        "src/core/__init__.py": "",
        "src/ui/__init__.py": "",
        "src/database/__init__.py": "",
        "src/utils/__init__.py": "",
    }

    # ساخت پوشه‌ها
    print("در حال ایجاد معماری پوشه‌ها...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ پوشه ایجاد شد: {directory}")

    # ساخت فایل‌ها و نوشتن محتوا داخل آن‌ها
    print("\nدر حال ایجاد فایل‌ها...")
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ فایل ایجاد شد: {file_path}")

    print("\n🚀 معماری و فایل‌های پایه پلتفرم با موفقیت و بدون نقص ایجاد شدند!")


if __name__ == "__main__":
    create_project_structure()