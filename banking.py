# Write your code here

import random
import sqlite3

status = True

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()

active_user = int  # active user from login function
login_order = int  # order after login
login_pass = bool  # check if log in pass


def create_account():
    print('Your card has been created')
    new_account = str(400000000000000 + random.randint(0, 999999999))
    new_account += get_luhn(new_account)
    pin = str(random.randint(1000, 9999))
    cur.execute("SELECT * FROM card;")
    no_user = len(cur.fetchall())
    if no_user == 0:
        new_id = 1
    else:
        new_id = no_user + 1
    cur.execute('INSERT INTO card (id, number, pin) VALUES ({}, {}, {});'.format(new_id, new_account, pin))
    conn.commit()
    print('Your card number:\n{}'.format(new_account))
    print('Your card pin:\n{}\n'.format(pin))


def login():
    global active_user
    global login_pass

    user = input('Enter your card number:\n')
    user_pin = str(input('Enter your PIN:\n'))

    cur.execute("SELECT * FROM card WHERE number = {};".format(user))
    account_all = len(cur.fetchall())
    cur.execute("SELECT pin FROM card WHERE number = {};".format(user))

    if account_all == 1:
        if user_pin == cur.fetchone()[0]:
            active_user = user
            login_pass = True
            print("You have successfully logged in!")
        else:
            print('Wrong card number or PIN!\n')
            login_pass = False
    else:
        print('Wrong card number or PIN!\n')
        login_pass = False


def get_luhn(user):
    last_digit = int
    check_last = [int(i) for i in user]
    for i in range(0, 15, 2):
        test_value = check_last[i] * 2
        if test_value > 9:
            check_last[i] = test_value - 9
        else:
            check_last[i] = test_value
        sum_value = sum(check_last[0:15])
        if 10 - (sum_value % 10) == 10:
            last_digit = 0
        else:
            last_digit = 10 - (sum_value % 10)
    return str(last_digit)


def balance(user):
    print('Balance: {}'.format(
        cur.execute("SELECT balance FROM card WHERE number = {};".format(user))
    ))


def add_income():
    income = input("Enter income:\n")
    cur.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(income, active_user))
    conn.commit()
    print("Income was added!\n")


def transfer():
    receiver = input("Enter card number:\n")
    cur.execute("SELECT * FROM card WHERE number = {};".format(receiver))
    check_receiver = len(cur.fetchall())
    print(receiver[15], "and", get_luhn(receiver))
    if receiver[0] != '4':
        print("Such a card does not exist.\n")
    elif receiver[15] != get_luhn(receiver):
        print("Probably you made a mistake in the card number. Please try again!\n")
    elif receiver == active_user:
        print("You can't transfer money to the same account!\n")
    elif check_receiver != 1:
        print("Such a card does not exist.\n")
    else:
        amount = int(input("Enter how much money you want to transfer"))
        cur.execute("SELECT balance FROM card WHERE number = {}".format(active_user))
        user_balance = cur.fetchone()[0]
        if user_balance < amount:
            print("Not enough money!")
        else:
            cur.execute("UPDATE card SET balance = balance - {} WHERE number = {};".format(amount, active_user))
            cur.execute("UPDATE card SET balance = balance + {} WHERE number = {};".format(amount, receiver))
            conn.commit()
            print("Success!")


def close_account():
    cur.execute("DELETE FROM card WHERE number = {};".format(active_user))
    conn.commit()
    print("The account has been closed!\n")


while status is True:
    print('''1. Create an account
2. Log into account
0. Exit''')
    order = input()
    if order == '1':
        create_account()
    elif order == '2':
        login()
        while login_pass is True:
            login_order = input('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Logout
0. Exit
''')
            if login_order == '1':
                balance(active_user)
                continue
            elif login_order == '2':
                add_income()
                continue
            elif login_order == '3':
                transfer()
                continue
            elif login_order == '4':
                close_account()
                continue
            elif login_order == '5':
                print('You have successfully logged out!')
                login_pass = False
            elif login_order == '0':
                print('Bye!')
                status = False
                break
    else:
        print('Bye!')
        status = False
