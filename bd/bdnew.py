import os.path
import aiosqlite

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "botBD.db")


async def rec(about, login, passw):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT INTO passw (about,login,pass) VALUES (?,?,?)", (about,login,passw,))
        await db.commit()


async def showpassw ():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT * FROM passw')
        rows = await cursor.fetchall()
        return rows

