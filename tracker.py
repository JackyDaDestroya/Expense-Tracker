import csv
import sys
import os
import json
from datetime import datetime


# Globals
path = "expenses.csv"
    
categoryMapping = {
    'R': 'Restaurants & Takeaway',
    'E': 'Entertainment & Recreation',
    'C': 'Clothing & Accessories',
    'F': 'Fitness & Health',
    'B': 'Beauty & Hair',
    'G': 'Groceries',
    'T': 'Transportation',
    'S': 'Shopping',
    'L': 'Life Admin',
    'O': 'Other'
}

categoryTotal = {
    'Restaurants & Takeaway': 0,
    'Entertainment & Recreation': 0,
    'Clothing & Accessories': 0,
    'Fitness & Health': 0,
    'Beauty & Hair': 0,
    'Groceries': 0,
    'Transportation': 0,
    'Shopping': 0,
    'Life Admin': 0,
    'Other': 0
}

budget = {
    'Restaurants & Takeaway': 0,
    'Entertainment & Recreation': 0,
    'Clothing & Accessories': 0,
    'Fitness & Health': 0,
    'Beauty & Hair': 0,
    'Groceries': 0,
    'Transportation': 0,
    'Shopping': 0,
    'Life Admin': 0,
    'Other': 0
}


monthMapping = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

monthTotal = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0
}

actionPrompt = """Please pick an action:
[A]dd expense
[M]onthly total 
[C]ategory total for the month 
[Y]early Breakdown
[B]udget
[E]xit
Input: """

categoryPrompt = """Enter category: 
[R]estaurants & Takeaway
[E]ntertainment & Recreation
[C]lothing & Accessories
[F]itness & Health
[B]eauty & Hair
[G]roceries
[T]ransportation
[S]hopping
[L]ife Admin
[O]ther

Input: """

monthPrompt = """Enter a month: 
[1] January
[2] February
[3] March
[4] April
[5] May
[6] June
[7] July
[8] August
[9] September
[10] October
[11] November
[12] December 
Input: """
            
budgetPrompt = """Please pick an option:
[A]ssign a monthly budget 
[C]heck monthly budget          
Input: """

def main ():
    while True:
        answer = input(actionPrompt)
        if answer == 'A':
            os.system('cls' if os.name == 'nt' else 'clear')
            addExpense()
            print("Expense successfully added! \n")
        elif answer == 'R':
            os.system('cls' if os.name == 'nt' else 'clear')
            removeExpense()
        elif answer == 'M':
            os.system('cls' if os.name == 'nt' else 'clear')
            monthlySpending()
        elif answer == 'C':
            os.system('cls' if os.name == 'nt' else 'clear')
            categoryBreakdown()
        elif answer == 'Y':
            os.system('cls' if os.name == 'nt' else 'clear')
            yearlyBreakdown()
        elif answer == 'B':
            os.system('cls' if os.name == 'nt' else 'clear')
            monthlyBudget()
        elif answer == 'E':
            sys.exit()
        else:
            print("\nInvalid input. Please select a valid option")

def addExpense():
    # Prompt user for name of expense
    expense = input("Enter name of expense: ")

    # Prompt user for amount
    total = input("Enter total amount in dollars: ")

    while True:
        try:
            total = round(float(total), 2)
            break
        except ValueError:
            total = input("Invalid amount. Please enter a valid dollar amount: ")

    # Prompting user input for date
    date = input("Enter date of expense in the format DD-MM-YYYY or [T]oday's date: ")
    while True: 
        try:
            if date == "T":
                date = datetime.today().date()
                date = date.strftime("%d-%m-%Y")
            else:
                date = datetime.strptime(date, "%d-%m-%Y")
                date = date.strftime("%d-%m-%Y")
            break
        except ValueError:
            date = input("Invalid date format. Please enter the date in the format DD-MM-YYYY: ")
        
    # Prompt user for category of expense
    category = input(categoryPrompt)
    category = categoryMapping.get(category.upper())

    data = [expense, total, date, category]

    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    os.system('cls' if os.name == 'nt' else 'clear')

def monthlySpending():
    spending = []

    while True:
        try:
            targetMonth = int(input(monthPrompt))
            if 1 <= targetMonth <= 12:
                break
            else: 
                print("\nInvalid input. Please enter a valid month")
        except ValueError:
            print("\nInvalid input. Please enter a valid month")

    while True: 
        try:
            targetYear = int(input("Select a year: "))
            if targetYear >= 2000:
                os.system('cls' if os.name == 'nt' else 'clear')
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid year")

    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames

        for row in reader:
            date = row['date']
            date = datetime.strptime(date, "%d-%m-%Y")
            if date.month == targetMonth and date.year == targetYear:
                spending.append(row)

    spending = sorted(spending, key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"))
    total = 0

    print(f"\nYour total monthly spending in {monthMapping.get(targetMonth)} is:\n")
    print("{:<30} | {:<7} | {:<10} | {:<10}".format("Expense", "Amount", "Date", "Category"))
    print("------------------------------------------------------------------------------")

    for expense in spending: 
        amount = "{:.2f}".format(float(expense['amount']))
        total = total + float(expense['amount'])
        print(f"{expense['Expense']:<30} | ${amount:<6} | {expense['date']:<6} | {expense['category']:<10}")

    print(f"\nTotal spending for the month: ${round(total, 2)}\n")

    while True:
        userInput = input("Press 'E' to exit: ")
        if userInput.lower() == 'e':
            os.system('cls' if os.name == 'nt' else 'clear')
            break

def categoriseExpenses(spending, targetMonth, targetYear):
    with open(path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            date = row['date']
            date = datetime.strptime(date, "%d-%m-%Y")
            if date.month == targetMonth and date.year == targetYear:
                spending.append(row)

    for expense in spending: 
        categoryTotal[expense['category']] = categoryTotal[expense['category']] + float(expense['amount'])

def categoryBreakdown():
    total = 0
    spending = []
        
    while True:
        try:
            targetMonth = int(input(monthPrompt))
            if 1 <= targetMonth <= 12:
                break
            else: 
                print("\nInvalid input. Please enter a valid month")
        except ValueError:
            print("\nInvalid input. Please enter a valid month")

    while True: 
        try:
            targetYear = int(input("Select a year: "))
            if targetYear >= 2000:
                os.system('cls' if os.name == 'nt' else 'clear')
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid year")

    categoriseExpenses(spending, targetMonth, targetYear)

    print(f"\nYour category breakdown for the month of {monthMapping.get(targetMonth)} {targetYear} is: ")
    print("\n{:<30} | {:<10}".format("Category", "Amount"))
    print("------------------------------------------")
    for key, value in categoryTotal.items(): 
        amount = "{:.2f}".format(float(value))
        total = total + float(amount)
        print(f"{key:<30} | ${amount:<5}")
    
    for key in categoryTotal:
        categoryTotal[key] = 0
    
    print(f"\nTotal spending for the month: ${round(total,2)}\n")

    while True:
        userInput = input("Press 'E' to exit: ")
        if userInput.lower() == 'e':
            os.system('cls' if os.name == 'nt' else 'clear')
            break

def yearlyBreakdown():
    spending = []
    total = 0.0
    
    # Prompting user for year input
    while True: 
        try:
            targetYear = int(input("Select a year: "))
            if targetYear >= 2000:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid year")

    # opening up CSV file with all expenses
    with open(path, 'r') as file:
        reader = csv.DictReader(file)

        # adding expense to spending list if within target year
        for row in reader:
            date = row['date']
            date = datetime.strptime(date, "%d-%m-%Y")
            if date.year == targetYear:
                spending.append(row)
    
    # sort expenses for the year in chronological order
    spending = sorted(spending, key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"))
    
    # adding monthly total into dictionary
    for expense in spending:
        date = expense['date']
        date = datetime.strptime(date, "%d-%m-%Y")
        monthTotal[date.month] = monthTotal[date.month] + float(expense['amount'])
    
    # printing table format
    print(f"\nYour monthly breakdown for {targetYear} is: ")
    print("\n{:<20} | {:<10}".format("Month", "Total"))
    print("-----------------------------------")

    # printing out monthly totals
    for key, value in monthTotal.items():
        amount = "{:.2f}".format(float(value))
        total += float(value)
        print(f"{monthMapping.get(key):<20} | ${amount}")
        # reset mapping back to 0
        monthTotal[key] = 0

    # printing out yearly total
    print(f"\nTotal yearly spending: ${round(total, 2)}\n")
    
    while True:
        userInput = input("Press 'E' to exit: ")
        if userInput.lower() == 'e':
            os.system('cls' if os.name == 'nt' else 'clear')
            break

def monthlyBudget():
    budgetTotal = 0
    filename = 'budget.json'

    while True:
        try:
            option = input(budgetPrompt)
            if option.upper() == "A" or option.upper() == "C":
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else: 
                print("\nInvalid input. Please enter a valid option")
        except ValueError:
            print("\nInvalid input. Please enter a valid option")
    
    if option == "A":
        for key in budget:
            while True:
                target = input(f"Set your budget for {key}: ")
                if target.isdigit() and int(target) >= 0:
                    break
                else: 
                    print("Invalid input. Ensure the budget you enter is a whole number greater than or equal to zero.")
            budget[key] = int(target)
            budgetTotal += int(target)
        
        saveDict(budget, filename)

        print(f"\nYou have successfully setup a monthly budget for ${budgetTotal}.")

        while True:
            userInput = input("\nPress 'E' to exit: ")
            if userInput.lower() == 'e':
                os.system('cls' if os.name == 'nt' else 'clear')
                break
    
    elif option == "C":
        spendingTotal = 0
        spending = []
        
        while True:
            try:
                targetMonth = int(input(monthPrompt))
                if 1 <= targetMonth <= 12:
                    break
                else: 
                    print("\nInvalid input. Please enter a valid month")
            except ValueError:
                print("\nInvalid input. Please enter a valid month")

        while True: 
            try:
                targetYear = int(input("Select a year: "))
                if targetYear >= 2000:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
            except ValueError:
                print("\nInvalid input. Please enter a valid year")

        categoriseExpenses(spending, targetMonth, targetYear)
        budgetLoaded = loadDict(filename)

        print(f"Your budget breakdown for the month of {monthMapping.get(targetMonth)} {targetYear} is:\n")
        print("{:<30} | {:<11} | {:<11} | {:<10} | {:<30}".format("Category", "Tracked", "Budget", "% Complete", "Remaining"))
        print("-----------------------------------------------------------------------------------------------------")

        for key, value in budgetLoaded.items():
            space = " "
            remaining = value - categoryTotal[key]
            spendingTotal += categoryTotal[key]
            budgetTotal += value

            if value != 0:
                percentage = f"{round(categoryTotal[key] / value * 100)}%"
            else:
                percentage = "-"
            if remaining < 0:
                display = f"${abs(round(remaining, 2))} over budget"
            elif remaining >= 0:
                display = f"${round(remaining, 2)} left to spend"

            print(f"{key:<30} | ${round(categoryTotal[key], 2):<10} | ${value:<10} | {percentage:<10} | {display:<30}")

        print(f"\nYou have spent ${round(spendingTotal,2)} on a budget of ${budgetTotal} for the month of {monthMapping.get(targetMonth)} {targetYear}")
        
        for key in categoryTotal:
            categoryTotal[key] = 0
            
        while True:
            userInput = input("\nPress 'E' to exit: ")
            if userInput.lower() == 'e':
                os.system('cls' if os.name == 'nt' else 'clear')
                break

def saveDict(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def loadDict(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
main()