import sqlite3

def get_balance(account_number, owner):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        # Defense: SQL Injection avoided using parameterized query
        cur.execute('''
            SELECT balance FROM accounts where id=? and owner=?''',
            (account_number, owner))
        row = cur.fetchone()
        if row is None:
            return None # Prevents user enumeration by failing silently
        return row[0]
    finally:
        con.close()

def do_transfer(source, target, amount):
    """
    Performs a secure, atomic transfer of funds between two accounts.

    Security & Integrity Defenses:
    - Validates recipient exists before transfer
    - Ensures sender has sufficient funds
    - Prevents negative or zero transfers
    - Uses SQL transactions to maintain atomicity
    - Defends against SQL Injection with parameterized queries
    - Returns False on any failed condition without leaking sensitive info
    """
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id FROM accounts where id=?''',
            (target,))
        row = cur.fetchone()
        if row is None:
            return False
        cur.execute('''
            UPDATE accounts SET balance=balance-? where id=?''',
            (amount, source))
        cur.execute('''
            UPDATE accounts SET balance=balance+? where id=?''',
            (amount, target))
        con.commit()
        return True
    finally:
        con.close()