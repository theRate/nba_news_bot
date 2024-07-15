import sqlite3


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('bot_db.sqlite3')
        self.curs = self.conn.cursor()

    def create_table(self):
        """Создает таблицу subscriptions с полями user_id и tag."""
        self.curs.execute("CREATE TABLE IF NOT EXISTS subscriptions (user_id INTEGER, tag TEXT)")
        self.conn.commit()

    def add_user_tag(self, user_id, tag):
        """Добавляет пару user_id - tag в таблицу subscriptions."""
        self.curs.execute("INSERT INTO subscriptions VALUES (?, ?)", (user_id, tag))
        self.conn.commit()

    def delete_user_tag(self, user_id, tag):
        """Удаляет пару user_id - tag из таблицы subscriptions."""
        self.curs.execute("DELETE FROM subscriptions WHERE user_id = ? AND tag = ?", (user_id, tag))
        self.conn.commit()

    def check_exist_user_tag(self, user_id, tag):
        """Проверяет наличие записи в таблице subscriptions."""
        self.curs.execute("SELECT EXISTS (SELECT 1 FROM subscriptions WHERE user_id = ? AND tag = ?)", (user_id, tag))
        return self.curs.fetchone()

    def get_user_tags(self, user_id):
        """Возвращает все теги пользователя из таблицы subscriptions."""
        self.curs.execute("SELECT tag FROM subscriptions WHERE user_id = ?", (user_id,))
        return self.curs.fetchall()

    def get_tag_users(self, tag):
        """Возвращает всех пользователей тега из таблицы subscriptions."""
        self.curs.execute("SELECT user_id FROM subscriptions WHERE tag = ?", (tag,))
        return self.curs.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.curs.close()
        self.conn.close()


# создание базы данных
if __name__ == '__main__':
    dbm = DatabaseManager()
    dbm.create_table()
    dbm.close()
