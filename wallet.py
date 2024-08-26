from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

# Initialize the Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Get wallet balance
def get_wallet_balance():
    account = client.get_account()
    for balance in account['balances']:
        if balance['asset'] == 'LTC':
            return float(balance['free'])
    return 0.0

# Send Litecoin to a specified address
def send_ltc(to_address, amount):
    try:
        transaction = client.withdraw(
            asset='LTC',
            address=to_address,
            amount=amount,
        )
        return transaction['id']
    except Exception as e:
        raise Exception(f"Failed to send Litecoin: {e}")
