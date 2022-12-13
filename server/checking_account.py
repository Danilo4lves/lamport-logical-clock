from database import Database


class CheckingAccount:
    # Initializes a checking account
    def __init__(self, database, rg, client_name):
        self._database = database
        self.rg = rg
        self.client_name = client_name

        self.__create(rg, client_name)

    # Persists a new checking account
    def __create(self, rg, client_name):
        checking_account = self._database.get_checking_account(rg)

        if (checking_account is not None):
            return

        self._database.create(rg, client_name)

    # Verifies if checking account exists
    @staticmethod
    def login(database, rg):
        checking_account = database.get_checking_account(rg)

        if (checking_account is None):
            return None

        rg, client_name, _ = checking_account

        return CheckingAccount(database, rg, client_name)

    # Get balance
    def balance(self):
        _, _, amount_in_cents = self._database.get_checking_account(self.rg)

        return amount_in_cents


    # Withdraws from current checking account
    def withdraw(self, amount_in_cents):
        _, _, ck_amount_in_cents = self._database.get_checking_account(
            self.rg)

        if (amount_in_cents <= 0):
            raise Exception("Invalid amount to be withdrawn")

        if (amount_in_cents > ck_amount_in_cents):
            raise Exception(
                "Not enough funds to be withdrawn: {}".format(ck_amount_in_cents))

        self._database.withdraw_atomic(self.rg, amount_in_cents)

    # Deposits to current checking account
    def deposit(self, amount_in_cents):
        if (amount_in_cents <= 0):
            raise Exception("Invalid amount to be deposited")

        self._database.deposit_atomic(self.rg, amount_in_cents)

    # Transfers to another checking account
    def transfer_to(self, destination_rg, amount_in_cents):
        if (amount_in_cents <= 0):
            raise Exception("Invalid amount to be transfered")

        destination_ck = self._database.get_checking_account(destination_rg)

        if (destination_ck is None):
            raise Exception("Unable to make transfer")

        _, _, origin_amount_in_cents = self._database.get_checking_account(
            self.rg)

        if (amount_in_cents > origin_amount_in_cents):
            raise Exception("Not enough funds: {}".format(
                origin_amount_in_cents))

        self._database.withdraw(self.rg, amount_in_cents)
        self._database.deposit(destination_rg, amount_in_cents)
        self._database.save()


# rg1 = 12312312
# rg2 = 12312313
#
# db = Database.instance()
# ck1 = CheckingAccount(db, rg1, "Teste 1")
# ck2 = CheckingAccount(db, rg2, "Teste 2")
#
# ck1.deposit(10)
# ck1.withdraw(5)
# ck1.transfer_to(rg2, 3)
