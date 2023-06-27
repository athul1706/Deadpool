import asyncio
import re
import ast
import math
import time
import datetime
import pytz
import shutil 
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, BOT_START_TIME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, file_caption, temp, get_settings, save_group_settings, humanbytes
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_pmsearch_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}








@Client.on_message(filters.text & filters.private)
async def privat_in(client, message):
    
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:
        
        search = message.text
        files, offset, total_results = await get_pmsearch_results(search.lower(), offset=0)
        if not files:
            return
        btn = [
            [
                InlineKeyboardButton(
                text=f"📂[{get_size(file.file_size)}]📂 {file.file_name}", callback_data=f'mypmfile#{file.file_id}'
            ),
            ]
            for file in files
        ]

        if offset != "":
            key = f"{message.chat.id}-{message.id}"
            BUTTONS[key] = search
            req = message.from_user.id if message.from_user else 0
            mention = message.from_user.mention
            btn.append(
                [InlineKeyboardButton(text=f"🗓 1/{round(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="NEXT ⏩",callback_data=f"ynext_{req}_{key}_{offset}")]
            )
        else:
            btn.append(
                [InlineKeyboardButton(text="🗓 1/1",callback_data="pages")]
            )
        imdb = await get_poster(search) 
      #  if imdb and imdb.get('poster'):
      #      await message.reply_photo(photo=imdb.get('poster'), caption=f"Requested By: {mention}\n🏷 Title: <a href={imdb['url']}>{imdb.get('title')}</a>\n🎭 Genres: {imdb.get('genres')}\n📆 Year: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n🌟 Rating: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10", reply_markup=InlineKeyboardMarkup(btn))
      #  elif imdb:
      #      await message.reply_text(f"Requested By: {mention}\n🏷 Title: <a href={imdb['url']}>{imdb.get('title')}</a>\n🎭 Genres: {imdb.get('genres')}\n📆 Year: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n🌟 Rating: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10", reply_markup=InlineKeyboardMarkup(btn))
      #  else:
        await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ </b>", reply_markup=InlineKeyboardMarkup(btn))
        

