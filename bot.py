from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TOKEN, ADMIN_IDS
from db import init_db, add_user, get_balance, get_transactions, is_admin
from wallet import get_wallet_balance, send_ltc
from mining import start_cpu_mining, stop_mining
from admin import force_withdraw, promote_user_to_admin

# Initialize the database and wallet
init_db()

# Initialize mining process
mining_process = None

# Start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    add_user(user.id)
    if user.id in ADMIN_IDS:
        promote_user_to_admin(user.id, user.id)
    update.message.reply_text(f"Welcome to LTC Mining Bot, {user.first_name}!")

# Get wallet balance command
def balance(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if is_admin(user.id):
        balance = get_wallet_balance()
        update.message.reply_text(f"Your wallet balance is {balance} LTC.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Withdraw command
def withdraw(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if is_admin(user.id):
        try:
            amount = float(context.args[0])
            to_address = context.args[1]
            txid = send_ltc(to_address, amount)
            update.message.reply_text(f"Successfully withdrew {amount} LTC! Transaction ID: {txid}")
        except (IndexError, ValueError):
            update.message.reply_text("Usage: /withdraw <amount> <address>")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Start mining command
def start_mining(update: Update, context: CallbackContext) -> None:
    global mining_process
    user = update.message.from_user
    if is_admin(user.id):
        if mining_process is None or mining_process.poll() is not None:  # Check if mining is already running
            mining_process = start_cpu_mining()
            update.message.reply_text("Started CPU mining!")
        else:
            update.message.reply_text("Mining is already running!")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Stop mining command
def stop_mining_cmd(update: Update, context: CallbackContext) -> None:
    global mining_process
    user = update.message.from_user
    if is_admin(user.id):
        if mining_process is not None and mining_process.poll() is None:  # Check if mining is running
            stop_mining(mining_process)
            mining_process = None
            update.message.reply_text("Stopped CPU mining!")
        else:
            update.message.reply_text("Mining is not currently running!")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Transaction history command
def transactions(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if is_admin(user.id):
        transactions = get_transactions(user.id)
        if transactions:
            txn_list = "\n".join([f"{txn[0]} LTC - {txn[1]} on {txn[2]}" for txn in transactions])
            update.message.reply_text(f"Transaction History:\n{txn_list}")
        else:
            update.message.reply_text("No transactions found.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Admin-only force withdraw command
def admin_withdraw(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if is_admin(user.id):
        try:
            target_id = int(context.args[0])
            amount = float(context.args[1])
            success = force_withdraw(user.id, target_id, amount)
            if success:
                update.message.reply_text(f"Successfully withdrew {amount} LTC from user {target_id}!")
            else:
                update.message.reply_text("Operation failed.")
        except (IndexError, ValueError):
            update.message.reply_text("Usage: /admin_withdraw <user_telegram_id> <amount>")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Admin-only promote to admin command
def promote(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if is_admin(user.id):
        try:
            target_id = int(context.args[0])
            success = promote_user_to_admin(user.id, target_id)
            if success:
                update.message.reply_text(f"Successfully promoted user {target_id} to admin!")
            else:
                update.message.reply_text("Operation failed.")
        except (IndexError, ValueError):
            update.message.reply_text("Usage: /promote <user_telegram_id>")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Main function to start the bot
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("withdraw", withdraw, pass_args=True))
    dispatcher.add_handler(CommandHandler("startmining", start_mining))
    dispatcher.add_handler(CommandHandler("stopmining", stop_mining_cmd))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("admin_withdraw", admin_withdraw, pass_args=True))
    dispatcher.add_handler(CommandHandler("promote", promote, pass_args=True))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
