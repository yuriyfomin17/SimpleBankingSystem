import math


class PiggyBank:
    # create __init__ and add_money methods
    def __init__(self, deposit_dollars, deposit_cents):
        self.dollars = deposit_dollars
        self.cents = deposit_cents

    def add_money(self, deposit_dollars, deposit_cents):
        self.cents += deposit_cents
        if self.cents >= 100:
            deposit_dollars += math.floor(self.cents / 100)
            self.cents = self.cents % 100
        self.dollars += deposit_dollars
        return "" + str(self.dollars) + " " + str(self.cents)
