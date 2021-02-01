# Write your code here
import random


class Bank:
    cards = {}

    def __init__(self):
        self.account = None
        self.pin = None
        self.balance = 0

    def generate_account(self):
        def luhn(number):
            luhn_num = []
            number = str(number)
            for index in range(len(number)):
                if (index + 1) % 2 != 0:
                    luhn_num.append(int(number[index]) * 2)
            for index in range(len(luhn_num)):
                if int(luhn_num[index]) > 9:
                    luhn_num[index] += luhn_num[index] - 9
            sum_luhn = 0
            for index in range(len(luhn_num)):
                sum_luhn += int(luhn_num[index])
            count = 0
            while sum_luhn % 10 != 0:
                sum_luhn += 1
                count += 1
            return count

        iin = 400000
        account_identifier = random.randrange(100000000, 999999999)
        curr_acc = "" + str(iin) + str(account_identifier)
        check_sum = luhn(curr_acc)
        curr_acc += str(check_sum)
        while Bank.cards.get(curr_acc) is not None:
            iin = 400000
            account_identifier = random.randrange(100000000, 999999999)
            check_sum = luhn(curr_acc)
            curr_acc = "" + str(iin) + str(account_identifier) + str(check_sum)
        self.account = curr_acc
        self.pin = random.randrange(1000, 9999)
        Bank.cards[self.account] = [self.pin, self.balance]
        return [self.account, self.pin]


b = Bank()
logout_menu = ["0. Exit", "1. Create an account", "2. Log into account"]
menu = logout_menu
for i in range(1, len(menu)):
    print(menu[i])
print(menu[0])
option = int(input())
login_menu = ["0. Exit", "1. Balance", "2. Log out"]
acc = ''
while option != 0:
    if option == 1 and menu[2] == "2. Log into account":
        [acc, pin] = b.generate_account()
        print("Your card has been created\nYour card number:\n{0}\nYour card PIN:\n{1}".format(acc, pin))
    elif option == 2 and menu[2] == "2. Log into account":
        print("Enter your card number:")
        acc = input()
        print("Enter your PIN:")
        pin = int(input())
        if Bank.cards.get(acc) is None or Bank.cards.get(acc)[0] != pin:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")

            menu = login_menu
    elif option == 1 and menu[2] == "2. Log out":
        print("Balance: ", Bank.cards.get(acc)[1])
    elif option == 2 and menu[menu[2] == "2. Log out"]:
        menu = logout_menu
    for i in range(1, len(menu)):
        print(menu[i])
    print(menu[0])
    option = int(input())
print('Bye!')
