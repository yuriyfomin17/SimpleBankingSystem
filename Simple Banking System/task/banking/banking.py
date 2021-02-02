# Write your code here
import random
import sqlite3


class DBMS:
    create_table = """CREATE TABLE IF NOT EXISTS card(
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            )"""

    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute(DBMS.create_table)
        self.conn.commit()

    def create_account(self, acc_number, acc_pin, balance):
        insert_acc_command = """INSERT INTO card (id, number,pin,balance) VALUES ({0}, {1},{2},{3})""".format(
            acc_number,
            acc_number,
            acc_pin,
            balance)
        self.cur.execute(insert_acc_command)
        # After doing some changes in DB don't forget to commit them!
        self.conn.commit()

    def get_account(self, current_acc, current_pin):
        find_acc_command = """SELECT 
            number,
            pin,
            balance
        FROM
            card
        WHERE 
            id = {0}
            AND number = {0}
            AND pin = {1}
        """.format(current_acc, current_pin)
        self.cur.execute(find_acc_command)
        # Returns all rows from the response
        arr = self.cur.fetchall()
        return arr


class Bank:
    cards = {}

    def __init__(self):
        self.account = None
        self.pin = None
        self.balance = 0

    def generate_account(self, db_manager):
        def luhn(number):
            luhn_num = []
            number = str(number)
            for index in range(len(number)):
                if (index + 1) % 2 != 0:
                    luhn_num.append(int(number[index]) * 2)
                else:
                    luhn_num.append(int(number[index]))
            for index in range(len(luhn_num)):
                if int(luhn_num[index]) > 9:
                    luhn_num[index] = luhn_num[index] - 9
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
        curr_account = "" + str(iin) + str(account_identifier)
        check_sum = luhn(curr_account)
        curr_account += str(check_sum)
        self.pin = random.randrange(1000, 9999)
        while len(db_manager.get_account(curr_account, self.pin)) != 0:
            iin = 400000
            account_identifier = random.randrange(100000000, 999999999)
            check_sum = luhn(curr_account)
            curr_account = "" + str(iin) + str(account_identifier) + str(check_sum)
        self.account = curr_account
        db_manager.create_account(self.account, self.pin, 0)
        return [self.account, self.pin]


b = Bank()
database_manager = DBMS()
logout_menu = ["0. Exit", "1. Create an account", "2. Log into account"]
menu = logout_menu
for i in range(1, len(menu)):
    print(menu[i])
print(menu[0])
option = int(input())
login_menu = ["0. Exit", "1. Balance", "2. Log out"]
acc = ''
curr_balance = None
while option != 0:
    if option == 1 and menu[2] == "2. Log into account":
        [acc, pin] = b.generate_account(database_manager)
        print("Your card has been created\nYour card number:\n{0}\nYour card PIN:\n{1}".format(acc, pin))
    elif option == 2 and menu[2] == "2. Log into account":
        print("Enter your card number:")
        acc = input()
        print("Enter your PIN:")
        pin = int(input())
        curr_arr = database_manager.get_account(acc, pin)
        if len(curr_arr) == 0:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            curr_balance = curr_arr[0][2]
            menu = login_menu
    elif option == 1 and menu[2] == "2. Log out":
        print("Balance:", curr_balance)
    elif option == 2 and menu[menu[2] == "2. Log out"]:
        menu = logout_menu
    for i in range(1, len(menu)):
        print(menu[i])
    print(menu[0])
    option = int(input())
print('Bye!')
