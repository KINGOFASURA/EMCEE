# Copyright (C) 2021 Red-Aura & TeamDaisyX

# This file is part of Daisy (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import re

import emoji

IBM_WATSON_CRED_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/bd6b59ba-3134-4dd4-aff2-49a79641ea15"
IBM_WATSON_CRED_PASSWORD = "UQ1MtTzZhEsMGK094klnfa-7y_4MCpJY1yhd52MXOo3Y"
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
import re, os

import aiohttp
from google_trans_new import google_translator
from pyrogram import filters, Client

from MashaRoBot import BOT_ID, OWNER_ID
from typing import Callable, Coroutine, Dict, List, Tuple, Union

TOKEN = os.environ.get("TOKEN")
APP_ID = os.environ.get("APP_ID")
APP_HASH = os.environ.get("APP_HASH")
session_name = TOKEN.split(":")[0]
daisyx = Client(
    session_name,
    api_id=APP_ID,
    api_hash=APP_HASH,
    bot_token=TOKEN,
    workers=3,
    sleep_threshold=5,
)

from MashaRobot import db as db_x

lydia = db_x["CAHTBOT"]


def add_chat(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    if stark:
        return False
    else:
        lydia.insert_one({"chat_id": chat_id})
        return True


def remove_chat(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    else:
        lydia.delete_one({"chat_id": chat_id})
        return True


def get_all_chats():
    r = list(lydia.find())
    if r:
        return r
    else:
        return False


def get_session(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    else:
        return stark

def admins_only(func: Callable) -> Coroutine:
    async def wrapper(client: Client, message: Message):
        if message.from_user.id == OWNER_ID:
            return await func(client, message)
        admins = await get_administrators(message.chat)
        for admin in admins:
            if admin.id == message.from_user.id:
                return await func(client, message)

    return wrapper
async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


translator = google_translator()
import requests


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


emcee_chats = []
en_chats = []
# AI Chat (C) 2020-2021 by @Aquila_14
"""
@.on_message(
    filters.voice & filters.reply & ~filters.bot & ~filters.via_bot & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        message.continue_propagation()
    if message.reply_to_message.from_user.id != BOT_ID:
        message.continue_propagation()
    previous_message = message
    required_file_name = message.download()
    if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
        await message.reply(
            "You need to set the required ENV variables for this module. \nModule stopping"
        )
    else:
        headers = {
            "Content-Type": previous_message.voice.mime_type,
        }
        data = open(required_file_name, "rb").read()
        response = requests.post(
            IBM_WATSON_CRED_URL + "/v1/recognize",
            headers=headers,
            data=data,
            auth=("apikey", IBM_WATSON_CRED_PASSWORD),
        )
        r = response.json()
        print(r)
        await client.send_message(message, r)
"""

@Emcee_Bot.on_message(
    filters.command("chatbot") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def hmm(_, message):
    global daisy_chats
    if len(message.command) != 2:
        await message.reply_text(
            "I only recognize `/chatbot on` and /chatbot `off only`"
        )
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`Processing...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("Emcee AI Already Activated In This Chat")
            return
        await lel.edit(
            f"Emcee AI Successfully Added For Users In The Chat {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`Processing...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("Emcew AI Was Not Activated In This Chat")
            return
        await lel.edit(
            f"Emcee AI Successfully Deactivated For Users In The Chat {message.chat.id}"
        )

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text("English AI chat Enabled!")
            return
        await message.reply_text("AI Chat Is Already Disabled.")
        message.continue_propagation()
    else:
        await message.reply_text(
            "I only recognize `/chatbot on` and /chatbot `off only`"
        )


@Emcee_Bot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("emcee", "Aco")
        test = test.replace("Emcee", "Aco")
        URL = "https://api.affiliateplus.xyz/api/chatbot?message=hi&botname=@Emcee_Bot&ownername=@Aquila_14"

        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return

        pro = result["message"]
        try:
            await emcee.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, lang_tgt="en")
            except:
                return
        # test = emoji.demojize(test.strip())

        # Kang with the credits bitches @InukaASiTH
        test = test.replace("daisy", "Aco")
        test = test.replace("Daisy", "Aco")
        URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@DaisyXbot&ownername=@TeamDaisyX"
        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return
        pro = result["message"]
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, lang_tgt=lan[0])
            except:
                return
        try:
            await daisyx.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@Emcee_Bot.on_message(
    filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("daisy", "Aco")
    test = test.replace("Daisy", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@DaisyXbot&ownername=@TeamDaisyX"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return

    pro = result["message"]
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, lang_tgt=lan[0])
    try:
        await daisyx.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@Emcee_Bot.on_message(
    filters.regex("Emcee|emcee|Emceebot|emceebot|Emceebot")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("emcee", "Aco")
    test = test.replace("Emcee", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@Emcee_Bot&ownername=@Aquila_14"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return
    pro = result["message"]
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, lang_tgt=lan[0])
        except Exception:
            return
    try:
        await daisyx.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
<b> Chatbot </b>
Emcee AI 3.0 IS THE ONLY AI SYSTEM WHICH CAN DETECT & REPLY UPTO 200 LANGUAGES

 - /chatbot [ON/OFF]: Enables and disables AI Chat mode (EXCLUSIVE)
 - /chatbot EN : Enables English only chatbot
 
 
<b> Assistant </b>
 - /ask [question]: Ask question from daisy
 - /ask [reply to voice note]: Get voice reply
 
"""

__mod_name__ = "AI Assistant"