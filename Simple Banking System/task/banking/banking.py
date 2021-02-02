# Write your code here
import random
import sqlite3


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
        current_account = "" + str(iin) + str(account_identifier)
        check_sum = luhn(current_account)
        current_account += str(check_sum)
        self.pin = random.randrange(1000, 9999)
        while len(db_manager.get_account(current_account, self.pin)) != 0:
            iin = 400000
            account_identifier = random.randrange(100000000, 999999999)
            check_sum = luhn(current_account)
            current_account = "" + str(iin) + str(account_identifier) + str(check_sum)
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
        curr_check_sum = acc[len(acc) - 1]
        curr_luhn_acc = acc[0:len(acc) - 2]
        if luhn(int(curr_luhn_acc)) == int(curr_check_sum):
            print("Enter your PIN:")
            pin = int(input())
            curr_arr = database_manager.get_account(acc, pin)
            if len(curr_arr) == 0:
                print("Wrong card number or PIN!")
            else:
                print("You have successfully logged in!")
                curr_balance = curr_arr[0][2]
                curr_pin = curr_arr[0][1]
                curr_account = curr_arr[0][0]
                menu = login_menu
        else:
            print("Probably you made a mistake in the card number.")
    elif menu[option] == "1. Balance":
        curr_arr = database_manager.get_account(curr_account, curr_pin)
        curr_balance = curr_arr[0][2]
        print("Balance:", curr_balance)
    elif menu[option] == "2. Add income":
        print("Enter income:")
        income = int(input())

        b.add_income(database_manager, curr_account, income, curr_balance)
    elif menu[option] == "3. Do transfer":
        print("Enter your card number:")
        transfer_acc = input()
        print("Enter your PIN:")
        transfer_pin = int(input())
        curr_arr = database_manager.get_account(transfer_acc, transfer_pin)
        if len(curr_arr) == 0:
            print("Wrong card number or PIN!")
        else:
            transfer_balance = curr_arr[0][2]
            transfer_acc = curr_arr[0][1]
            if transfer_acc != curr_account:
                print("Enter how much money you want to transfer:")
                diff = int(input())
                if diff <= curr_balance:
                    b.add_income(database_manager, transfer_acc, diff, transfer_balance)
                    b.add_income(database_manager, curr_account, -diff, curr_balance)
                else:
                    print("Not enough money!")
            else:
                print("You can't transfer money to the same account!")
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
print('Bye!')
