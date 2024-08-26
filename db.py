import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 telegram_id INTEGER UNIQUE,
                 balance REAL DEFAULT 0.0,
                 is_admin INTEGER DEFAULT 0)''')
    
    # Create transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 amount REAL,
                 type TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# Add a new user to the database
def add_user(telegram_id):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    conn.commit()
    conn.close()

# Retrieve user's balance
def get_balance(telegram_id):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE telegram_id=?", (telegram_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

# Update user's balance
def update_balance(telegram_id, amount):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()
    conn.close()

# Record a transaction
def record_transaction(telegram_id, amount, txn_type):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute('''INSERT INTO transactions (user_id, amount, type) 
                 SELECT id, ?, ? FROM users WHERE telegram_id=?''', 
              (amount, txn_type, telegram_id))
    conn.commit()
    conn.close()

# Retrieve all transactions of a user
def get_transactions(telegram_id):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute('''SELECT amount, type, timestamp 
                 FROM transactions 
                 WHERE user_id = (SELECT id FROM users WHERE telegram_id=?) 
                 ORDER BY timestamp DESC''', (telegram_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions

# Check if the user is an admin
def is_admin(telegram_id):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE telegram_id=?", (telegram_id,))
    is_admin = c.fetchone()[0]
    conn.close()
    return bool(is_admin)

# Make a user an admin
def make_admin(telegram_id):
    conn = sqlite3.connect('ltc_mining_bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET is_admin = 1 WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
