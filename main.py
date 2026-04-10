
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from helper import get_drm_keys
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
from config import *
import sys
import os
import random
import re
import tempfile
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import datetime
import aiohttp

bot = Client("bot",
             bot_token=os.environ.get("BOT_TOKEN", "8659589420:AAG5yM6ZQKxZzVLvGe1NQSF0_EogMtZpjQw"),
             api_id=int(os.environ.get("API_ID", "25531611")),
             api_hash=os.environ.get("API_HASH", "2f63a48be678dfea4ad03e495377403f"))
auth_users = [8553304761, 8564849592]

owner_id = [8553304761,8564849592]
failed_links = []
fail_cap = f"**➜ This file Contain Failed Downloads while Downloding \n You Can Retry them one more time **"

global videocount, pdfcount

pwdl = os.environ.get("api")

processing_request = False


keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨🏻‍💻 Devloper", url="https://t.me/EX_DOLPHIN"),
            InlineKeyboardButton(text="❣️ GITHUB", url="https://t.me/EX_DOLPHIN"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/EX_DOLPHIN"),
        ],
    ]
)

Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨🏻‍💻 Devloper", url="https://t.me/EX_DOLPHIN"),
            InlineKeyboardButton(text="❣️ GITHUB", url="https://t.me/EX_DOLPHIN"),
        ],
        [
            InlineKeyboardButton(text="Join to Check My Status", url="https://t.me/EX_DOLPHIN"),
        ],
    ]
)


@bot.on_message(filters.command(["logs"]))
async def send_logs(bot: Client, m: Message):
    try:
        with open("Assist.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")


image_urls = [
    "https://graph.org/file/9dbe3901f43b11e98e6f0.jpg",
    "https://graph.org/file/c5ec0a02be408b354d3fc.jpg",
    "https://graph.org/file/c186818a566c501f14abf.jpg",
    "https://graph.org/file/850ef256ede1370257b5d.jpg",
    "https://graph.org/file/40700542e58889b5c42fe.jpg",
    "https://graph.org/file/94a7875bb51006e7bd528.jpg",
]


@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = f"**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫  👋!\n\n➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️\n➠ Can Extract Videos & Pdf Form Your Text File and Upload to Telegram\n\n➠ 𝐔𝐬𝐞 /drm 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐅𝐫𝐨𝐦 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞\n\n➠𝐌𝐚𝐝𝐞 𝐁𝐲: @EX_DOLPHIN **\n"
    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)


@bot.on_message(filters.command('h2t'))
async def run_bot(bot: Client, m: Message):
    user_id = m.from_user.id
    if user_id not in auth_users:
        await m.reply_text("**HEY BUDDY THIS IS ONLY FOR MY ADMINS**")
    else:
        editable = await m.reply_text("Send Your HTML file\n")
        input: Message = await bot.listen(editable.chat.id)
        html_file = await input.download()
        await input.delete(True)
        await editable.delete()
        with open(html_file, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.find_all('table')
            videos = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    name = cols[0].get_text().strip()
                    link = cols[1].find('a')['href']
                    videos.append(f'{name}:{link}')
        txt_file = os.path.splitext(html_file)[0] + '.txt'
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))
        await m.reply_document(document=txt_file, caption="Here is your txt file.")
        os.remove(txt_file)


def is_subscription_expired(user_id):
    with open("Subscription_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(", ")
            if int(data[0]) == user_id:
                end_date = datetime.datetime.strptime(data[2], "%d-%m-%Y")
                today = datetime.datetime.today()
                return end_date < today
    return True


@bot.on_message(filters.command("myplan"))
async def myplan_command_handler(bot, message):
    user_id = message.from_user.id
    with open("Subscription_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(", ")
            if int(data[0]) == user_id:
                subscription_start = data[1]
                expiration_date = data[2]
                today = datetime.datetime.today()
                if today > datetime.datetime.strptime(expiration_date, "%d-%m-%Y"):
                    plan = "EXPIRED"
                    response_text = f"**✨ User ID: {user_id}\n📊 PLAN STAT : {plan}\n\n🔰 Activated on : {subscription_start}\n🧨 Expiration Date: {expiration_date}\n\n🫰🏼 ACTIVATE YOUR PLAN NOW!\n⚡️ TO ACTIVATE MESSAGE : @ITS_NOT_ROMEO**"
                else:
                    plan = "ALIVE!"
                    response_text = f"**✨ User ID: {user_id}\n📊 PLAN STAT : {plan}\n🔰 Activated on : {subscription_start}\n🧨 Expiration Date: {expiration_date}**"
                await message.reply(response_text)
                return
    if user_id in auth_users:
        await message.reply("YOU HAVE LIFE TIME ACCESS :)")
    else:
        await message.reply("No subscription data found for you.")


@bot.on_message(filters.command("stop"))
async def stop_handler(_, m):
    global processing_request
    if failed_links:
        error_file_send = await m.reply_text("**📤 Sending Failed Downloads List Before Stopping**")
        with open("failed_downloads.txt", "w") as f:
            for link in failed_links:
                f.write(link + "\n")
        await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
        await error_file_send.delete()
        os.remove('failed_downloads.txt')
        failed_links.clear()
    processing_request = False
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    global processing_request
    processing_request = False
    await m.reply_text("🤖**Restarting Bot**🤖", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["drm"]))
async def account_login(bot: Client, m: Message):
    global processing_request
    if m.from_user.id not in auth_users:
        await m.reply_text("** YOU ARE NOT IN ADMIN LIST **", reply_markup=keyboard)
        return

    if processing_request:
        await m.reply_text("**🫨 I'm currently processing another request.\nPlease try again later.**", reply_markup=Busy)
        return
    else:
        editable = await m.reply_text(f"**➠ Send Me Your TXT File\n\n➠ TXT FORMAT : LINK : URL\n➠ Modified By: @EX_DOLPHIN **")
        input: Message = await bot.listen(editable.chat.id)
        editable = await editable.edit(f"**⚙️PROCESSING INPUT.......**")

        if input.document:
            processing_request = True
            x = await input.download()
            await input.delete(True)
            file_name, ext = os.path.splitext(os.path.basename(x))

            try:
                links = []
                videocount = 0
                pdfcount = 0
                with open(x, "r", encoding="utf-8") as f:
                    for line in f:
                        link = line.strip().split("://", 1)
                        links.append(link)
                        if ".pdf" in link[1]:
                            pdfcount += 1
                        else:
                            videocount += 1
            except Exception as e:
                await m.reply_text("Error occurred while processing the file.")
                os.remove(x)
                processing_request = False
                return
        else:
            content = input.text.split("\n")
            links = []
            videocount = 0
            pdfcount = 0
            for i in content:
                link = i.split("://", 1)
                links.append(link)
                if ".pdf" in link[1]:
                    pdfcount += 1
                else:
                    videocount += 1

    await editable.edit(f"**Total links: {len(links)}\n┃\n┠ Videos: {videocount}\n┠ PDFs: {pdfcount}\n┠ Start from (default 1):\n┖ Send `stop` to cancel**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    if raw_text.lower() == "stop":
        await editable.edit("**Task Stopped!**")
        processing_request = False
        return

    await editable.edit(f"**ENTER TILL WHERE YOU WANT TO DOWNLOAD\n┠ Start: `{raw_text}`\n┖ Last index: `{len(links)}`**")
    input9: Message = await bot.listen(editable.chat.id)
    if int(input9.text) > len(links):
        await editable.edit("**PLZ ENTER NUMBER IN RANGE**")
        processing_request = False
        await m.reply_text("**Exiting Task...**")
        return
    else:
        await input9.delete(True)

    await editable.edit("**Enter Batch Name or send `d` for filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    b_name = file_name if raw_text0 == 'd' else raw_text0

    await editable.edit("**Enter resolution\n1 = 720p\n2 = 480p\n3 = 360p\n4 = 240p**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    quality = input2.text
    await input2.delete(True)

    await editable.edit("**Enter Your Name or send `de` for default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    CR = "@ITS_NOT_ROMEO" if raw_text3 == 'de' else raw_text3

    await editable.edit("**🖼 Thumbnail\n• Custom: use @vtelegraphbot and send link\n• No thumbnail: send `no`**")
    input6 = message = await bot.listen(editable.chat.id)
    await input6.delete(True)
    thumb = input6.text
    thumb2 = input6.text

    await editable.edit("**⚡️ Thumbnail in PDF too?\n• Same as video: `yes`\n• No: `no`\n• Different: `custom`**")
    input7 = message = await bot.listen(editable.chat.id)
    raw_text7 = input7.text.lower()
    await input7.delete(True)

    thumb3 = ""
    if raw_text7 == "custom":
        await editable.edit("**Send URL of PDF Thumbnail**")
        input8 = message = await bot.listen(editable.chat.id)
        await input8.delete(True)
        await editable.delete()
        thumb3 = input8.text
    else:
        await editable.delete()

    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget {thumb} -O thumb1.jpg")
        thumb = "thumb1.jpg"
    else:
        thumb = "no"

    count = 1 if len(links) == 1 else int(raw_text)

    try:
        for i in range(count - 1, int(input9.text)):
            key = ""
            V = links[i][1].replace("file/d/", "uc?export=download&id=") \
                .replace("www.youtube-nocookie.com/embed", "youtu.be") \
                .replace("?modestbranding=1", "") \
                .replace("/view?usp=sharing", "") \
                .replace("youtube.com/embed/", "youtube.com/watch?v=")

            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                    }) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or 'media-cdn.classplusapp' in url:
                try:
                    url = requests.get(
                        f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                        headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}
                    ).json()['url']
                except:
                    pass

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'

            if "/master.mpd" in url:
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/", "https://d1d34p8vz63oiq.cloudfront.net/")

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best"

            try:
                cc = f'**➭ Index » {str(count).zfill(3)}**\n**➭ Title » {name1}.mkv**\n**➭ Batch » {b_name}**\n**➭ Quality » {raw_text2}**\n\n✨ **Downloaded By : {CR}**\n**━━━━━━━✦✗✦━━━━━━━**'
                cc1 = f'**➭ Index » {str(count).zfill(3)}**\n**➭ Title » {name1}.pdf**\n**➭ Batch » {b_name}**\n\n✨ **Downloaded By : {CR}**\n**━━━━━━━✦✗✦━━━━━━━**'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        time.sleep(1)
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        time.sleep(1)
                        start_time = time.time()
                        reply = await m.reply_text(f"**⚡️ Uploading...** - `{name}`")
                        time.sleep(1)
                        if raw_text7 == "custom":
                            subprocess.run(['wget', thumb3, '-O', 'pdfthumb.jpg'], check=True)
                            thumbnail = "pdfthumb.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                            os.remove(thumbnail)
                        elif thumb == "no" and raw_text7 == "no":
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, progress=progress_bar, progress_args=(reply, start_time))
                        elif raw_text7 == "yes" and thumb != "no":
                            subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)
                            thumbnail = "thumb1.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                        else:
                            subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)
                            thumbnail = "thumb1.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                        await reply.delete(True)
                        os.remove(f'{name}.pdf')
                        count += 1
                        time.sleep(2)
                    except FloodWait as e:
                        time.sleep(e.x)
                        continue

                else:
                    prog = await m.reply_text(f"📥 **Downloading**\n\n**➭ Count » {str(count).zfill(3)}**\n**➭ Video Name »** `{name}`\n**➭ Quality »** `{raw_text2}`\n**➭ URL »** `{url}`\n\n✨ **Bot By @EX_DOLPHIN**\n**━━━━━━━✦✗✦━━━━━━━**")
                    time.sleep(2)
                    try:
                        key = await helper.get_drm_keys(url)
                    except:
                        key = ""
                    if ".mpd" in url:
                        res_file = await helper.drm_download_video(url, quality, name, key)
                    else:
                        cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.mkv"'
                        os.system(cmd)
                        res_file = f"{name}.mkv"
                    filename = res_file
                    await prog.delete(True)
                    time.sleep(1)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, thumb2)
                    count += 1

            except Exception as e:
                await m.reply_text(f"**Failed**\n**Name** =>> `{name1}`\n**Link** =>> `{url}`\n**Reason »** {e}")
                failed_links.append(f"{name1} : {url}")
                count += 1
                continue

    except Exception as e:
        await m.reply_text(str(e))
    time.sleep(2)

    if failed_links:
        error_file_send = await m.reply_text("**📤 Sending Failed Downloads List**")
        with open("failed_downloads.txt", "w") as f:
            for link in failed_links:
                f.write(link + "\n")
        await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
        await error_file_send.delete()
        failed_links.clear()
        os.remove('failed_downloads.txt')
    await m.reply_text("🔰Done🔰")
    await m.reply_text("**✨Thanks for Choosing**")
    processing_request = False


processing_request = False
bot.run()
