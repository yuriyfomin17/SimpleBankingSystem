# Write your code here
import random
import sqlite3


def luhn_checksum_calc(part_code):
    part_code = part_code + "0"

    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(part_code)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    count = 0
    while checksum % 10 != 0:
        count += 1
        checksum += 1
    result = part_code[0:len(part_code) - 1] + str(count)
    return result


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0


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

    def get_account(self, current_acc):
        find_acc_command = """SELECT 
            number,
            pin,
            balance
        FROM
            card
        WHERE 
            id = {0}
            AND number = {0}
        """.format(current_acc)
        self.cur.execute(find_acc_command)
        # Returns all rows from the response
        arr = self.cur.fetchall()
        return arr

    def add_money(self, current_acc, difference, balance):
        add_income_command = """UPDATE card 
        SET balance={0}
        WHERE id={1} AND number={1}
        """.format(
            (difference + balance), current_acc)
        self.cur.execute(add_income_command)
        self.conn.commit()

    def delete_account(self, current_acc):
        delete_command = """DELETE FROM card WHERE 
        id ={0} AND number={0}""".format(current_acc)
        self.cur.execute(delete_command)
        self.conn.commit()


class Bank:
    cards = {}

    def __init__(self):
        self.account = None
        self.pin = None
        self.balance = 0

    def generate_account(self, db_manager):
        iin = 400000
        account_identifier = random.randrange(100000000, 999999999)
        part_code = "" + str(iin) + str(account_identifier)
        current_account = int(luhn_checksum_calc(part_code))
        self.pin = random.randrange(1000, 9999)
        while len(db_manager.get_account(current_account)) != 0:
            iin = 400000
            account_identifier = random.randrange(100000000, 999999999)
            part_code = "" + str(iin) + str(account_identifier)
            current_account = int(luhn_checksum_calc(part_code))
        self.account = current_account
        db_manager.create_account(self.account, self.pin, 0)
        return [self.account, self.pin]

    def add_income(self, db_manager, transfer_account, difference, account_balance):
        db_manager.add_money(transfer_account, difference, account_balance)
        print("Success!")

    def delete_acc(self, db_manager, acc_number):
        db_manager.delete_account(acc_number)
        print("The account has been closed!")


b = Bank()
database_manager = DBMS()
logout_menu = ["0. Exit", "1. Create an account", "2. Log into account"]
menu = logout_menu
for i in range(1, len(menu)):
    print(menu[i])
print(menu[0])
option = int(input())
if option > 2 or option < 0:
    option = 0
login_menu = ["0. Exit", "1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out"]
acc = ''
curr_balance = None
curr_account = None
curr_pin = None
while menu[option] != "0. Exit":
    if menu[option] == "1. Create an account":
        [acc, pin] = b.generate_account(database_manager)
        print("Your card has been created\nYour card number:\n{0}\nYour card PIN:\n{1}".format(acc, pin))
    elif menu[option] == "2. Log into account":
        print("Enter your card number:")
        acc = input()
        print("Enter your PIN:")
        pin = int(input())
        curr_arr = database_manager.get_account(acc)
        if len(curr_arr) == 0 or pin != int(curr_arr[0][1]):
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            curr_balance = curr_arr[0][2]
            curr_pin = curr_arr[0][1]
            curr_account = curr_arr[0][0]
            menu = login_menu

    elif menu[option] == "1. Balance":
        curr_arr = database_manager.get_account(curr_account)
        curr_balance = curr_arr[0][2]
        print("Balance:", curr_balance)
    elif menu[option] == "2. Add income":
        print("Enter income:")
        income = int(input())
        b.add_income(database_manager, curr_account, income, curr_balance)
        curr_arr = database_manager.get_account(curr_account)
        curr_balance = curr_arr[0][2]
        curr_pin = curr_arr[0][1]
        curr_account = curr_arr[0][0]
    elif menu[option] == "3. Do transfer":
        print("Enter card number:")
        transfer_acc = input()
        if is_luhn_valid(transfer_acc):
            transfer_arr = database_manager.get_account(transfer_acc)
            if len(transfer_arr) == 0:
                print("Such a card does not exist.")
            else:
                transfer_balance = transfer_arr[0][2]
                transfer_acc = transfer_arr[0][0]
                if transfer_acc != curr_account:
                    print("Enter how much money you want to transfer:")
                    curr_arr = database_manager.get_account(curr_account)
                    curr_balance = curr_arr[0][2]
                    curr_pin = curr_arr[0][1]
                    curr_account = curr_arr[0][0]
                    diff = int(input())
                    if diff <= curr_balance:
                        print("Transfer account", transfer_acc)
                        b.add_income(database_manager, transfer_acc, diff, transfer_balance)
                        b.add_income(database_manager, curr_account, -diff, curr_balance)
                    else:
                        print("Not enough money!")
                else:
                    print("You can't transfer money to the same account!")
        else:
            print("Probably you made a mistake in the card number. Please try again!")
    elif menu[option] == "4. Close account":
        b.delete_acc(database_manager, curr_account)
    elif menu[option] == "5. Log out":
        curr_account = None
        curr_balance = None
        menu = logout_menu
    for i in range(1, len(menu)):
        print(menu[i])
    print(menu[0])
    option = int(input())
    if option < 0 or (option > 5 and len(menu) == 6) or (option > 2 and len(menu) == 3):
        option = 0
print('Bye!')
