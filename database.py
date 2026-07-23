import aiosqlite
from rich import print
from rich.console import Console

console = Console(highlight=False)
game_database = "game_database.db"

create_gdb_table = """CREATE TABLE IF NOT EXISTS game_database (
    appid INTEGER PRIMARY KEY,
    name TEXT,
    playtime INTEGER,
    playtime_2weeks INTEGER,
    playtime_windows INTEGER,
    playtime_linux INTEGER,
    playtime_mac INTEGER,
    last_played INTEGER,
    hltb_main REAL,
    hltb_completionist REAL,
    categories TEXT,
    is_completed INTEGER
);"""


async def database_init():
    try:
        async with aiosqlite.connect(game_database) as gdb:
            console.print("Game Database initialising...")
            await gdb.execute(create_gdb_table)
            await gdb.commit()
    except aiosqlite.OperationalError as error:
        print(error)


async def game_query(appid: int):
    async with aiosqlite.connect(game_database) as gdb:
        gdb.row_factory = aiosqlite.Row
        async with gdb.execute(
            """SELECT * FROM game_database WHERE appid = ?""", (appid,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def save_game_database(game: dict):
    async with aiosqlite.connect(game_database) as gdb:
        await gdb.execute(
            """INSERT OR REPLACE INTO game_database (
                appid, name, playtime, playtime_2weeks, playtime_windows,
                playtime_linux, playtime_mac, last_played, hltb_main,
                hltb_completionist, categories, is_completed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                game.get("appid"),
                game.get("name"),
                game.get("playtime"),
                game.get("playtime_2weeks"),
                game.get("playtime_windows"),
                game.get("playtime_linux"),
                game.get("playtime_mac"),
                game.get("last_played"),
                game.get("hltb_main", 0.0),
                game.get("hltb_completionist", 0.0),
                str(game.get("categories", "")),
                game.get("is_completed", 0),
            ),
        )
        await gdb.commit()


async def query_all_games():
    async with aiosqlite.connect(game_database) as gdb:
        gdb.row_factory = aiosqlite.Row
        async with gdb.execute("""SELECT * FROM game_database""") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
