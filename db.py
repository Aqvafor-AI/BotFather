import aiosqlite
from config import DB_NAME

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу, если не существует
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER
            )
        ''')
        await db.commit()

        # Проверяем, есть ли колонка score
        async with db.execute("PRAGMA table_info(quiz_state)") as cursor:
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]

        # Если score нет — добавляем
        if "score" not in column_names:
            await db.execute("ALTER TABLE quiz_state ADD COLUMN score INTEGER DEFAULT 0")
            await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO quiz_state (user_id, question_index, score)
            VALUES (?, ?, COALESCE((SELECT score FROM quiz_state WHERE user_id = ?), 0))
            ON CONFLICT(user_id) DO UPDATE SET question_index = ?
        ''', (user_id, index, user_id, index))
        await db.commit()

async def increment_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            UPDATE quiz_state
            SET score = COALESCE(score, 0) + 1
            WHERE user_id = ?
        ''', (user_id,))
        await db.commit()

async def get_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
