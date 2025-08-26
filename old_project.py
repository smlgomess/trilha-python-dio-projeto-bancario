menu = """

[d] Deposit
[w] Withdraw
[s] Account Statement
[q] Exit

=> """

balance = 0
limit = 500
account_statement = ""
withdraw_attempts = 0
WITHDRAW_LIMIT = 3

while True:

    option = input(menu)

    if option == "d":
        try:
            value = float(input("How much will you deposit? "))

            if value > 0:
                balance += value
                account_statement += f"Deposit: R$ {value:.2f}\n"
                print(f"You have successfully deposited an amount of: R$ {value:.2f}")

            else:
                print("Invalid Operation! Invalid input value.")
        except ValueError:
            print("Invalid input value! Only numerical digits.")

    elif option == "w":
        exceeded_withdraws = withdraw_attempts >= WITHDRAW_LIMIT

        if exceeded_withdraws:
            print("Invalid Operation! Daily withdrawal attemps exceeded.")
        else:
            try:
                value = float(input("How much will you withdraw? "))

                exceeded_balance = value > balance

                exceeded_limit = value > limit

                if exceeded_balance:
                    print("Invalid Operation! Insufficient balance.")

                elif exceeded_limit:
                    print("Invalid Operation! Input value exceed withdraw limit.")

                elif value > 0:
                    balance -= value
                    account_statement += f"Withdraw: R$ {value:.2f}\n"
                    withdraw_attempts += 1
                    print(f"Withdrawal made successfully, in the amount of: R$ {value:.2f}")
                    print(f"{WITHDRAW_LIMIT - withdraw_attempts} withdraw attemps left today.")

                else:
                    print("Invalid Operation! Invalid input value.")
            except ValueError:
                print("Invalid input value! Only numerical digits.")

    elif option == "s":
        print("\n================ Account Statement ================")
        print("No movements were made." if not account_statement else account_statement)
        print(f"\nbalance: R$ {balance:.2f}")
        print("==========================================")

    elif option == "q":
        break

    else:
        print("Invalid operation, please reselect the desired operation.")