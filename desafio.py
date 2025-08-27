menu = """
[u] Create User
[c] Create Bank Account
[d] Deposit
[w] Withdraw
[s] Account Statement
[l] List Users
[a] List Accounts
[q] Exit

=> """

users = []
accounts = []

WITHDRAW_LIMIT = 3
limit = 500

def create_user(name, birth_date, cpf, address):
    if not cpf.strip() or not name.strip():
        print("Invalid input! CPF and/or Name cannot be empty.")
        return None

    if not validate_cpf(cpf):
        print("Invalid CPF! Please enter a valid CPF number.")
        return None

    cpf_numbers = "".join(filter(str.isdigit, cpf))
    for user in users:
        if user["cpf"] == cpf_numbers:
            print("User with this CPF already exists.")
            return None

    user = {
        "name": name,
        "birth_date": birth_date,
        "cpf": cpf_numbers,
        "address": address
    }
    users.append(user)
    print(f"User {name} created successfully!")
    return user

def validate_cpf(cpf):
    cpf_numbers = "".join(filter(str.isdigit, cpf))
    
    if len(cpf_numbers) != 11:
        return False

    if cpf_numbers == cpf_numbers[0] * 11:
        return False

    sum1 = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
    digit1 = (sum1 * 10 % 11) % 10

    sum2 = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
    digit2 = (sum2 * 10 % 11) % 10

    return digit1 == int(cpf_numbers[9]) and digit2 == int(cpf_numbers[10])


def create_account(user):
    account_number = len(accounts) + 1
    account = {
        "agency": "0001",
        "number": account_number,
        "user": user,
        "balance": 0,
        "account_statement": "",
        "withdraw_attempts": 0
    }
    accounts.append(account)
    print(f"Account {account_number} created successfully for user {user['name']}!")
    return account

def deposit(value, /, account):
    if value > 0:
        account["balance"] += value
        account["account_statement"] += f"Deposit: R$ {value:.2f}\n"
        print(f"You have successfully deposited an amount of: R$ {value:.2f}")
    else:
        print("Invalid Operation! Invalid input value.")

def withdraw(*, value, account):
    if account["withdraw_attempts"] >= WITHDRAW_LIMIT:
        print("Invalid Operation! Daily withdrawal attempts exceeded.")
        return

    if value > account["balance"]:
        print("Invalid Operation! Insufficient balance.")
    elif value > limit:
        print("Invalid Operation! Input value exceed withdraw limit.")
    elif value > 0:
        account["balance"] -= value
        account["account_statement"] += f"Withdraw: R$ {value:.2f}\n"
        account["withdraw_attempts"] += 1
        print(f"Withdrawal made successfully, in the amount of: R$ {value:.2f}")
        print(f"{WITHDRAW_LIMIT - account['withdraw_attempts']} withdraw attempts left today.")
    else:
        print("Invalid Operation! Invalid input value.")

def show_account_statement(account):
    print("\n================ Account Statement ================")
    print("No movements were made." if not account["account_statement"] else account["account_statement"])
    print(f"\nbalance: R$ {account['balance']:.2f}")
    print("==========================================")

def select_account():
    if not accounts:
        print("No accounts registered yet.")
        return None
    print("\nList of Accounts:")
    for acc in accounts:
        print(f"Account {acc['number']} - User: {acc['user']['name']} - Agency: {acc['agency']}")
    try:
        acc_num = int(input("Enter the account number you want to access: "))
        for acc in accounts:
            if acc["number"] == acc_num:
                return acc
        print("Invalid account number.")
    except ValueError:
        print("Invalid input! Enter numeric digits only.")
    return None

def list_users():
    if not users:
        print("No users registered.")
    else:
        print("\n=== Users ===")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user['name']} | CPF: {user['cpf']} | Birth: {user['birth_date']} | Address: {user['address']}")

def list_accounts():
    if not accounts:
        print("\nNo accounts registered.")
    else:
        print("\n=== Accounts ===")
        for acc in accounts:
            print(f"Account {acc['number']} | Agency: {acc['agency']} | User: {acc['user']['name']} | Balance: R$ {acc['balance']:.2f}")

def main():
    while True:
        option = input(menu)

        if option == "u":
            name = input("Enter full name: ")
            birth_date = input("Enter birth date (dd/mm/yyyy): ")
            cpf = input("Enter CPF: ")
            address = input("Enter address (logradouro, numero - bairro - cidade/UF): ")
            create_user(name, birth_date, cpf, address)

        elif option == "c":
            if not users:
                print("No users registered yet. Create a user first.")
                continue
            print("Select the user for the new account:")
            for i, user in enumerate(users, start=1):
                print(f"{i} - {user['name']} (CPF: {user['cpf']})")
            try:
                user_choice = int(input("Enter user number: "))
                if 1 <= user_choice <= len(users):
                    create_account(users[user_choice - 1])
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input! Enter numeric digits only.")

        elif option == "d":
            account = select_account()
            if account:
                try:
                    value = float(input("How much will you deposit? "))
                    deposit(value, account)
                except ValueError:
                    print("Invalid input value! Only numerical digits.")

        elif option == "w":
            account = select_account()
            if account:
                if account["withdraw_attempts"] >= WITHDRAW_LIMIT:
                    print("Invalid Operation! Daily withdrawal attempts exceeded.")
                    continue
                try:
                    value = float(input("How much will you withdraw? "))
                    withdraw(value=value, account=account)
                except ValueError:
                    print("Invalid input value! Only numerical digits.")

        elif option == "s":
            account = select_account()
            if account:
                show_account_statement(account)

        elif option == "l":
            list_users()

        elif option == "a":
            list_accounts()

        elif option == "q":
            confirm = input("Are you sure you want to exit? Type 'Y' to confirm: ").strip().upper()
            if confirm == "Y":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Exit canceled. Returning to menu...")

        else:
            print("Invalid operation, please reselect the desired operation.")

if __name__ == "__main__":
    main()
