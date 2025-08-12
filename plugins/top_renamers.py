from config import Config
from helper.database import digital_botz
from helper.utils import humanbytes
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

THUMBNAIL_URL = "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg"

BADGES = [
    "🥇", "🥈", "🥉", "🏅", "🎖️", "🏆", "💎", "🔥", "⚡", "⭐",
    "🌟", "🎯", "🚀", "🛠️", "📦", "🧰", "🪄", "🎉", "🧨", "🔧"
]

@Client.on_message(filters.command("tops") & filters.user(Config.ADMIN))
async def top_renamers(bot, message: Message):
    users = await digital_botz.get_top_renamers(limit=20)
    if not users:
        return await message.reply("No renamer data found.")

    intro = "<b>🏆 Top 20 Renamers</b>\n\n"
    lines = [intro]

    for i, user in enumerate(users):
        badge = BADGES[i] if i < len(BADGES) else "🔰"
        username = f"@{user['username']}" if user.get("username") else "No Username"
        mention = f"<a href='tg://user?id={user['user_id']}'>Click</a>"
        rename_count = user.get("rename_count", 0)
        total_upload = user.get("total_upload_size", 0)
        human_upload = humanbytes(total_upload)

        lines.append(
            f"{badge} <b>{username}</b> ({mention})\n"
            f"🔁 Renames: <code>{rename_count}</code>\n"
            f"📦 Uploaded: <code>{human_upload}</code>\n"
        )

    await message.reply_photo(
        photo=THUMBNAIL_URL,
        caption="\n".join(lines),
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_tops")]
        ])
    )


@Client.on_callback_query(filters.regex("refresh_tops") & filters.user(Config.ADMIN))
async def refresh_tops(bot, callback_query):
    await callback_query.message.delete()
    await top_renamers(bot, callback_query.message)

