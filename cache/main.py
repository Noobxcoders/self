from pyrogram import Client
from noobcoder.config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME
from pytgcalls import PyTgCalls, idle

bot = Client(
    "noobcoder",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="noobcoder.handler"),
    )

noobcoder = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    session_name=SESSION_NAME,
    
    )

user = PyTgCalls(noobcoder,
    cache_duration=100,
    overload_quiet_mode=True,)

call_py = PyTgCalls(noobcoder, overload_quiet_mode=True)

with Client("noobcoder", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
    me_bot = app.get_me()
with noobcoder as app:
    me_noobcoder = app.get_me()
