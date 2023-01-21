import os
import logging
import random
import asyncio
import time
import datetime
import pytz
import shutil
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, BOT_START_TIME
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp, humanbytes 
from database.connections_mdb import active_connection
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^rekast'))
async def request_files(bot, query):
    _, athul, lst_msg_id, from_user = query.data.split("#") 
    if athul = "unupload":
        await query.message.delete() 
        await bot.send_message(int(from_user), 
                               "Sorry..Your request for movie is declined by admin, because it is already in the bot. Check with correct spelling", 
                               reply_to_message_id=int(lst_msg_id))
        return
    if athul = "notfound":
        await query.message.delete() 
        await bot.send_message(int(from_user), 
                               "Regret to inform you that your requested movie file is not available in telegram right now😞", 
                               reply_to_message_id=int(lst_msg_id))
        return
        
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user), 
                               "Your requested file is successfully uploaded. Thank you for using this feature. Stay in touch with us🥰", 
                               reply_to_message_id=int(lst_msg_id))
        

@Client.on_message(filters.command("request"))
async def request_moviez(bot, message):   
    if len(message.command) < 2:
        return await message.reply("No Movie name entered. Pls request your movies on format => MOVIE-LANGUAGE-YEAR") 
    rqst=message.text.split(' ', 1)[1]
    buttons = [
        [
            InlineKeyboardButton('UPLOADED',
                                 callback_data=f'rekast#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('ALREADY UPLOADED',
                                 callback_data=f'rekast#unupload#{chat_id}#{message.id}#{message.from_user.id}'),
        ], 
        [
            InlineKeyboardButton('FILES NOT FOUND',
                                 callback_data=f'rekast#notfound#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#movierequested\n\nBy : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/ Username - <code> {chat_id}</code> MOVIE NAME: {rqst}',
                           reply_markup=reply_markup)
    await message.reply("Thanks for using this feature. You will be notified once your requested file is uploaded☺🥰") 
