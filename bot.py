import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Tokenی بۆتەکەت لە BotFather لێرە دابنێ
TOKEN = "YOUR_BOT_TOKEN_HERE"

# بنکەی زانیاری سادە بۆ هێشتنەوەی داتای یاریزانان
players = {}

# نوێکردنەوە یان دروستکردنی کارەکتەر
def get_player(user_id, name):
    if user_id not in players:
        players[user_id] = {
            "name": name,
            "hp": 100,
            "gold": 20,
            "weapon": "Wooden Sword",
            "attack": 10
        }
    return players[user_id]

# فەرمانی دەستپێک /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = get_player(user.id, user.first_name)
    
    caption = (
        f"⚔️ Welcome to Hero Quest, {player['name']}! ⚔️\n\n"
        f"❤️ HP: {player['hp']}/100\n"
        f"💰 Gold: {player['gold']}\n"
        f"🗡️ Weapon: {player['weapon']} (+{player['attack']} ATK)\n\n"
        f"Choose an action below to start your adventure:"
    )
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Hunt Monsters", callback_data="hunt")],
        [InlineKeyboardButton("🛒 Item Shop", callback_data="shop")],
        [InlineKeyboardButton("📊 My Stats", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

# بەڕێوەبردنی کلیکەکان
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    player = get_player(user_id, query.from_user.first_name)
    
    data = query.data

    if data == "stats":
        await start(update, context)

    elif data == "hunt":
        earned_gold = 15
        player["gold"] += earned_gold
        
        text = (
            f"🌲 You ventured into the dark forest and defeated a Goblin! 👺\n\n"
            f"🎉 Reward: +{earned_gold} Gold\n"
            f"💰 Total Gold: {player['gold']}"
        )
        keyboard = [[InlineKeyboardButton("⚔️ Hunt Again", callback_data="hunt"), InlineKeyboardButton("🔙 Main Menu", callback_data="stats")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "shop":
        text = (
            f"🛒 Welcome to the Armory Shop!\n"
            f"Your Gold: 💰 {player['gold']}\n\n"
            f"1. 🗡️ Iron Sword (+25 ATK) - Cost: 50 Gold\n"
            f"2. 🪓 Battle Axe (+50 ATK) - Cost: 100 Gold"
        )
        keyboard = [
            [InlineKeyboardButton("Buy Iron Sword (50G)", callback_data="buy_iron")],
            [InlineKeyboardButton("Buy Battle Axe (100G)", callback_data="buy_axe")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="stats")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "buy_iron":
        if player["gold"] >= 50:
            player["gold"] -= 50
            player["weapon"] = "Iron Sword"
            player["attack"] = 25
            msg = "✅ You bought the Iron Sword!"
        else:
            msg = "❌ Not enough gold!"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Shop", callback_data="shop")]]
        await query.message.edit_text(f"{msg}\n💰 Gold left: {player['gold']}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "buy_axe":
        if player["gold"] >= 100:
player["weapon"] = "Battle Axe"
            player["attack"] = 50
            msg = "✅ You bought the Battle Axe!"
        else:
            msg = "❌ Not enough gold!"
            
        keyboard = [[InlineKeyboardButton("🔙 Back to Shop", callback_data="shop")]]
        await query.message.edit_text(f"{msg}\n💰 Gold left: {player['gold']}", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot is running...")
    app.run_polling()

  if name == "main":
    main()
            player["gold"] -= 100
