from db import update_balance, record_transaction, is_admin, make_admin

# Force withdrawal for a specific user (admin only)
def force_withdraw(admin_id, target_telegram_id, amount):
    if is_admin(admin_id):
        balance = get_balance(target_telegram_id)
        if amount <= balance:
            update_balance(target_telegram_id, -amount)
            record_transaction(target_telegram_id, amount, 'force_withdraw')
            return True
    return False

# Promote a user to admin (admin only)
def promote_user_to_admin(admin_id, target_telegram_id):
    if is_admin(admin_id):
        make_admin(target_telegram_id)
        return True
    return False
