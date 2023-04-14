import io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re
import youtube_dl
import youtube_dl
import aiofiles
import aiohttp
from noobcoder.converter import convert
import ffmpeg
import requests
from cache.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from noobcoder.config import ASSISTANT_NAME, BOT_USERNAME
from cache.filters import command, other_filters
from cache.queues import QUEUE, add_to_queue
from cache.main import call_py, noobcoder as user
from cache.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
from Process.design.thumbnail import play_thumb, queue_thumb 
from noobcoder.inline import stream_markup, audio_markup

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []

    
@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    buttons = audio_markup(user_id)
    if m.sender_chat:
        return await m.reply_text("You're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"Error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ   ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪssɪᴏɴs**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n» ❌ __ʙᴀɴ ᴜsᴇʀs__\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴅᴀᴛᴀ ɪs **ᴜᴘᴅᴀᴛᴇᴅ** ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀғᴛᴇʀ ʏᴏᴜ **ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    if not a.can_restrict_members:
        await m.reply_text(
        "💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
        + "\n\n» ❌ __ʙᴀɴ ᴜsᴇʀs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **is banned in group** {m.chat.title}\n\n» **Unban the userbot first if you want to use this bot.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **Userbot failed to join**\n\n**reason**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **Downloading audio...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else: 
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({link}) | `music`\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {m.from_user.mention()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"🏷 **Name:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}\n📹 **Stream type:** `Music`",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_photo(
                     photo=f"{IMG_5}",
                    caption="**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**",
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("• Support", url=f"https://t.me/BotDuniyaXd"),
                            InlineKeyboardButton("• Close", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            suhu = await m.reply_text(
        f"**⚡"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("💬 **No results Found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                videoid = search[4]
                dlurl = f"https://www.youtubepp.com/watch?v={videoid}"
                info = f"https://t.me/elsaa_Ro_bot?start=info_{videoid}"
                keyboard = stream_markup(user_id, dlurl)
                playimg = await play_thumb(videoid)
                queueimg = await queue_thumb(videoid)
                await suhu.edit(
                            f"**𝙉𝙪𝙡𝙡 Downloader**\n\n**Title**: {title[:22]}\n\n100% ▓▓▓▓▓▓▓▓▓▓▓▓0%\n\n**Time Taken**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=queueimg,
                            caption=f"📡 Next Streaming 💡 at {pos}\n\n​🍄 **ɴᴀᴍᴇ :**[{title[:65]}]({url})\n\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n\n👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ​:{requester}**",
                            reply_markup=InlineKeyboardMarkup(keyboard),
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"**𝙉𝙪𝙡𝙡 Downloader**\n\n**Title**: {title[:22]}\n\n0% ████████████100%\n\n**Time Taken**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )

                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)

                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=playimg,
                                caption=f"📡 Started Streaming 💡**\n\n​🍄 **ɴᴀᴍᴇ :**[{title[:65]}]({url})\n\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n\n👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ​:{requester}**",
                                reply_markup=InlineKeyboardMarkup(keyboard),
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 error: `{ep}`")
