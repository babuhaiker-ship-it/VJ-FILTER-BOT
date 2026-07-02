# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, LOG_CHANNEL, CHANNELS, ARIA2_HOST, ARIA2_PORT, ARIA2_SECRET
from database.ia_filterdb import save_file
from Script import script
import math
import aria2p

# Configuration for Downloads
DOWNLOAD_PATH = "downloads/"
if not os.path.isdir(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Initialize aria2
try:
    aria2 = aria2p.API(
        aria2p.Client(
            host=ARIA2_HOST,
            port=ARIA2_PORT,
            secret=ARIA2_SECRET
        )
    )
except Exception as e:
    print(f"Aria2 error: {e}")
    aria2 = None

async def progress_bar(current, total, status_msg, start_time, file_name):
    now = time.time()
    diff = now - start_time
    if diff < 1:
        return

    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion

    progress = "[{0}{1}]".format(
        ''.join(["●" for i in range(math.floor(percentage / 5))]),
        ''.join(["○" for i in range(20 - math.floor(percentage / 5))])
    )

    tmp = script.PROGRESS_BAR.format(
        round(percentage, 2),
        humanbytes(current),
        humanbytes(total),
        humanbytes(speed),
        time_formatter(estimated_total_time)
    )

    try:
        await status_msg.edit(f"<b><blockquote>🚀 ᴜᴘʟᴏᴀᴅɪɴɢ: {file_name}</blockquote></b>\n{tmp}")
    except:
        pass

def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(size) < 1024.0:
            return "%3.1f %sB" % (size, unit)
        size /= 1024.0
    return "%.1f %sB" % (size, 'Yi')

def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

@Client.on_message(filters.command("torrent") & filters.user(ADMINS))
async def torrent_handler(client, message):
    if not aria2:
        return await message.reply_text("<b>❌ ᴀʀɪᴀ2 ɪꜱ ɴᴏᴛ ʀᴜɴɴɪɴɢ! ᴘʟᴇᴀꜱᴇ ᴄᴏɴꜰɪɢᴜʀᴇ ɪᴛ ᴏɴ ʏᴏᴜʀ ꜱᴇʀᴠᴇʀ.</b>")

    link = None
    if len(message.command) > 1:
        link = message.command[1]
    elif message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.file_name.endswith(".torrent"):
            sts = await message.reply_text("<b>📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴏʀʀᴇɴᴛ ꜰɪʟᴇ...</b>")
            link = await message.reply_to_message.download(DOWNLOAD_PATH)
            await sts.delete()

    if not link:
        return await message.reply_text("<b><blockquote>⚠️ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴀɢɴᴇᴛ ʟɪɴᴋ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ .ᴛᴏʀʀᴇɴᴛ ꜰɪʟᴇ!</blockquote></b>")

    status = await message.reply_text("<b><blockquote>🔄 ɪɴɪᴛɪᴀᴛɪɴɢ ᴛᴏʀʀᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ...</blockquote></b>")

    try:
        if link.startswith("magnet:"):
            download = aria2.add_magnet(link, options={"dir": DOWNLOAD_PATH})
        else:
            download = aria2.add_torrent(link, options={"dir": DOWNLOAD_PATH})
            os.remove(link)
    except Exception as e:
        return await status.edit(f"<b>❌ ᴇʀʀᴏʀ: {e}</b>")

    gid = download.gid
    while not download.is_complete:
        download.update()
        if download.has_failed:
            return await status.edit("<b>❌ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ!</b>")

        percentage = download.progress
        speed = download.download_speed_string
        eta = download.eta_string()

        await status.edit(f"<b><blockquote>📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴏʀʀᴇɴᴛ...</blockquote>\n◈ ᴘʀᴏɢʀᴇꜱꜱ: <code>{percentage:.2f}%</code>\n◈ ꜱᴘᴇᴇᴅ: <code>{speed}</code>\n◈ ᴇᴛᴀ: <code>{eta}</code></b>")
        await asyncio.sleep(5)

    await status.edit("<b><blockquote>✅ ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ! ᴘʀᴇᴘᴀʀɪɴɢ ꜰᴏʀ ᴜᴘʟᴏᴀᴅ...</blockquote></b>")

    # Uploading logic
    files = download.files
    for file in files:
        file_path = str(file.path)
        if not os.path.exists(file_path):
            continue

        file_name = os.path.basename(file_path)
        start_time = time.time()

        try:
            # Upload to primary storage channel
            target_channel = CHANNELS[0] if CHANNELS else LOG_CHANNEL
            uploaded_msg = await client.send_document(
                chat_id=target_channel,
                document=file_path,
                caption=f"<b><blockquote>📂 ꜰɪʟᴇ: {file_name}</blockquote>\n\n◈ ꜱᴏᴜʀᴄᴇ: ᴛᴏʀʀᴇɴᴛ\n◈ ᴘᴏᴡᴇʀᴇᴅ ʙʏ: <a href='https://t.me/vj_bots'>ᴠᴊ ʙᴏᴛꜱ</a></b>",
                progress=progress_bar,
                progress_args=(status, start_time, file_name)
            )

            # Index in DB
            await save_file(uploaded_msg.document)
            await status.edit(f"<b><blockquote>✨ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ & ɪɴᴅᴇxᴇᴅ!</blockquote>\n◈ ꜰɪʟᴇ: <code>{file_name}</code></b>")
        except Exception as e:
            await message.reply_text(f"<b>❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ {file_name}: {e}</b>")

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

    # Remove from aria2 queue
    aria2.remove([download], force=True, files=True)
