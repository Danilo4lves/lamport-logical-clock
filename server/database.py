import sqlite3


class Database:
    _instance = None

    # Initializes database
    def __init__(self) -> None:
        self._connection = sqlite3.connect("data.db")

        self.__migration()

    # Creates database entities
    def __migration(self):
        self.__execute("""
            CREATE TABLE IF NOT EXISTS checking_account (
                rg INTEGER PRIMARY KEY,
                client_name TEXT,
                amount_in_cents INTEGER
            )
        """)

    # Executes database query
    def __execute(self, query, params=None):
        cursor = self._connection.cursor()

        if (params):
            return cursor.execute(query, params)

        return cursor.execute(query)

    # Maintains same class instance i.e singleton pattern
    @staticmethod
    def instance():
        if Database._instance is None:
            Database._instance = Database()

        return Database._instance

    def save(self):
        self._connection.commit()

    # Creates checking account
    def create(self, rg, client_name):
        self.__execute("""
            INSERT INTO checking_account
            VALUES (?, ?, ?)
        """, (rg, client_name, 0))

        self.save()

    # Retrieves checking account
    def get_checking_account(self, rg):
        return self.__execute("""
            SELECT * FROM checking_account
            WHERE rg = ?
        """, (rg,)).fetchone()

    # Withdraws from checking account
    def withdraw(self, rg, amount_in_cents):
        self.__execute("""
            UPDATE checking_account
            SET amount_in_cents = amount_in_cents - ?
            WHERE rg = ?
        """, (amount_in_cents, rg))

    # Withdraws from checking account without confirmation
    def withdraw_atomic(self, rg, amount_in_cents):
        self.withdraw(rg, amount_in_cents)

        self.save()

    # Deposits to checking account
    def deposit(self, rg, amount_in_cents):
        self.__execute("""
            UPDATE checking_account
            SET amount_in_cents = amount_in_cents + ?
            WHERE rg = ?
        """, (amount_in_cents, rg))

    # Deposits to checking account without confirmation
    def deposit_atomic(self, rg, amount_in_cents):
        self.deposit(rg, amount_in_cents)

        self.save()
