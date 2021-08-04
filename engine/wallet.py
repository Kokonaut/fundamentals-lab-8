class Wallet:

    def __init__(self, starting_amount):
        self.amount = int(starting_amount)

    def request_purchase(self, price):
        price = int(price)
        if price > self.amount:
            return False
        self.amount -= price
        return True

    def add_amount(self, amount):
        self.amount += int(amount)

    def get_amount(self):
        return self.amount
