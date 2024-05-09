import sys
from models import User, Payment


MAX_NO_OF_MONTHS = 12
FAIL_MSG = "An unexpected turn of events has occured. Please get help."
MONTHS = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep",
    "oct", "nov", "dec"]

class Date:
    def __init__(self, month, year):
        self.month = month
        self.year = year
    
    def __lt__(self, other):
        return self.year < other.year or (self.year == other.year and self.month < other.month)
    
    def __eq__(self, other):
        return self.year == other.year and self.month == other.month
    
    def __le__(self, other):
        return self < other or self == other
    
    def __str__(self):
        return f"{MONTHS[self.month]} in the year {self.year}"
    
    def increment_month_and_year(self):
        self.month = (1 + self.month) % MAX_NO_OF_MONTHS
        self.year += 1
    
    def next_month(self):
        month, year = self.month, self.year
        month += 1
        if month == MAX_NO_OF_MONTHS:
            month, year = 0, year + 1
        return Date(month, year)
    
    def prev_month(self):
        month, year = self.month, self.year
        month -= 1
        if month < 0:
            month, year = MAX_NO_OF_MONTHS - 1, year -1
        return Date(month, year)

def enter_loan():
    while True:
        try:
            loan = float(input("Enter loan: "))
            break
        except ValueError:
            print("Please enter a valid loan amount")
    return loan

def enter_rate():
    while True:
        try:
            rate = float(input("Enter rate in percent: "))
            break
        except ValueError:
            print("Please enter a valid rate")
    return rate / 100

def enter_month():
    print("Please enter one of", ", ".join(MONTHS), ":")
    while True:
        entered_month = input()
        if entered_month not in MONTHS:
            print("Expected one of", ", ".join(MONTHS))
        else:
            break
    return MONTHS.index(entered_month)

def enter_year():
    while True:
        try:
            entered_year = int(input("Please enter the year:"))
            break
        except ValueError:
            print("Please enter a valid integer for the year")
    return entered_year

def enter_username_and_get_user():
    def print_user_doesnt_exist_msg():
        print("The user does't exist")
        print("Please enter the name of an existing user")
    while True:
        username = input("The name of the user: ")
        try:
            user = User.get(username)
            if user is None:
                print_user_doesnt_exist_msg()
            else:
                return user
        except Exception:
            print_user_doesnt_exist_msg()

def enter_payment_amount():
    while True:
        try:
            amount = float(input("Enter payment amount: "))
            break
        except ValueError:
            print("Please enter a valid payment amount")
    return amount

def new_borrower():
    while True:
        username = input("Enter username: ")
        if User.username_exists(username):
            print("A user with this username already exists")
        else:
            break
    loan = enter_loan()
    rate = enter_rate()
    month_loaned = enter_month()
    year_loaned = enter_year()
    return User.create(username, loan, rate, month_loaned, year_loaned)

def calc_remaining_amount(user, month, year, amount):
    to_be_paid = user.loan
    curr_date = Date(user.month_loaned, user.year_loaned).prev_month()
    # All payments made by the user to the bank,
    # from the latest to the earliest
    payments = list(reversed(user.all_payments()))
    # Computing the amount owed after the last month paid
    while len(payments) > 0:
        amount_paid, payment_month, payment_year = payments[-1].amount, payments[-1].month, payments[-1].year
        if Date(month, year) <= Date(payment_month, payment_year):
            print("No going back in time.")
            print("Please input only payments for the present.")
            sys.exit(1)
        curr_date = curr_date.next_month()
        interest = user.rate * to_be_paid
        to_be_paid += interest
        # The payment is only popped when the year and month correspond
        # This is to account for the possibility in which the user doesn't pay in some months
        # The amount owed should just keep accumulating by the interest rate
        if curr_date == Date(payment_month, payment_year):
            to_be_paid -= amount_paid
            if to_be_paid <= 0:
                return 0
            payments.pop()
        elif curr_date > Date(payment_month, payment_year):
            print(FAIL_MSG)
            sys.exit(1)
    
    # Accounting for the possibility in which the user hasn't paid for some months
    # In each month of no payment, the money owed should just keep accumulating
    while curr_date != Date(month, year):
        to_be_paid += (user.rate * to_be_paid)
        curr_date = curr_date.next_month()

    return to_be_paid - amount

def input_payment():
    user = enter_username_and_get_user()
    amount = enter_payment_amount()
    month, year = enter_month(), enter_year()
    payments = user.all_payments()
    last_payment_month, last_payment_year = (payments[-1].month, payments[-1].year) if len(payments) else (-1, -1)
    if (Date(month, year) < Date(last_payment_month, last_payment_year) 
        or Date(month, year) < Date(user.month_loaned, user.year_loaned)):
            print("No going back in time.")
            print("Please input only payments for the present.")
            sys.exit(1)
    amount_left = calc_remaining_amount(user, month, year, amount)
    Payment.record(user, amount, month, year)
    if amount_left <= 0:
        print("User", user.username, "has completely paid of their loan")
    else:
        print("User", user.username, "still has", amount_left, "to pay")

def total_money_borrowed():
    print("Total money borrowed:", sum([user.loan for user in User.all()]))

def average_income_per_month():
    payments = list(Payment.all())
    if len(payments) == 0:
        print("No payments have been made")
    else:
        print("Average income per month:", sum([payment.amount for payment in payments]) / MAX_NO_OF_MONTHS)

def highest_earning_month():
    from collections import defaultdict
    earnings_by_month_and_year = defaultdict(lambda: defaultdict(int))
    for payment in Payment.all():
        earnings_by_month_and_year[payment.year][payment.month] += payment.amount
    highest_amount = -1
    highest_month, highest_year = -1, -1
    for year in earnings_by_month_and_year.keys():
        for month in earnings_by_month_and_year[year].keys():
            if earnings_by_month_and_year[year][month] > highest_amount:
                highest_amount = earnings_by_month_and_year[year][month]
                highest_month, highest_year = month, year
    if highest_amount == -1:
        print("No earnings have been made")
    else:
        print("The highest earning month:", Date(highest_month, highest_year))

def main():
    print("The Loan Calculator")
    print("What do you want to do?")
    print("Input a payment by a borrower: enter 'input-payment'")
    print("Show total money borrowed out: enter 'total-money-borrowed'")
    print("Show average income per month: enter 'average-income-per-month'")
    print("Show highest earning month: enter 'highest-earning-month'")
    print("Create a new borrower: enter 'new-borrower'")
    while True:
        entered = input()
        input_to_action = {
            "input-payment": input_payment,
            "new-borrower": new_borrower,
            "total-money-borrowed": total_money_borrowed,
            "average-income-per-month": average_income_per_month,
            "highest-earning-month": highest_earning_month
        }
        func = input_to_action.get(entered)
        if not func:
            print("Expected one of:", ", ".join(input_to_action.keys()), "as input")
            continue
        func()
        break

if __name__ == "__main__":
    main()
    """
    u = User.get("tit")
    print(u.month_loaned, u.year_loaned)
    for p in u.all_payments():
        print(p)
    """

    """
    for user in User.all():
        print(user.username, user.loan, user.month_loaned, user.year_loaned)
        for p in user.all_payments():
            print(p)
        print()
    """
