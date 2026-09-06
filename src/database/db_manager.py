import sqlite3
import os
import sys


class DatabaseManager:
    def __init__(self, db_name="platform_data.db"):
        # بررسی اینکه آیا برنامه در حالت فایل exe در حال اجراست یا پایتون خام
        if getattr(sys, 'frozen', False):
            # مسیر اجرایی فایل نهایی (exe)
            application_path = os.path.dirname(sys.executable)
        else:
            # مسیر اجرایی در حالت توسعه (PyCharm)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            application_path = os.path.dirname(os.path.dirname(current_dir))

        # ساخت پوشه assets در کنار فایل اجرایی در صورت عدم وجود
        assets_dir = os.path.join(application_path, "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        self.db_path = os.path.join(assets_dir, db_name)
        self._create_tables()

    # ... (بقیه توابع مثل _get_connection و ... دقیقاً مانند قبل باقی بمانند)

    def _get_connection(self):
        """ایجاد و بازگرداندن کانکشن به دیتابیس"""
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """ساخت جدول تاریخچه متون در صورت عدم وجود"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS text_history
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               subject
                               TEXT
                               NOT
                               NULL,
                               content
                               TEXT
                               NOT
                               NULL,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               updated_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )
                           ''')
            conn.commit()

    def save_text(self, subject: str, content: str):
        """ذخیره یک متن جدید به همراه موضوع"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO text_history (subject, content)
                           VALUES (?, ?)
                           ''', (subject, content))
            conn.commit()
            return cursor.lastrowid

    def update_text(self, record_id: int, new_content: str):
        """آپدیت کردن متن یک رکورد خاص (زمانی که کاربر دوباره حرف می‌زند یا ادیت می‌کند)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           UPDATE text_history
                           SET content    = ?,
                               updated_at = CURRENT_TIMESTAMP
                           WHERE id = ?
                           ''', (new_content, record_id))
            conn.commit()

    def get_all_history(self):
        """دریافت تمام تاریخچه برای نمایش در منوی کناری نرم‌افزار"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id, subject, content, created_at, updated_at
                           FROM text_history
                           ORDER BY updated_at DESC
                           ''')
            return cursor.fetchall()

    def delete_record(self, record_id: int):
        """حذف یک رکورد از تاریخچه"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM text_history WHERE id = ?', (record_id,))
            conn.commit()

    def get_record(self, record_id: int):
        """دریافت یک رکورد خاص به همراه موضوع و محتوا بر اساس آیدی"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT subject, content FROM text_history WHERE id = ?', (record_id,))
            return cursor.fetchone()