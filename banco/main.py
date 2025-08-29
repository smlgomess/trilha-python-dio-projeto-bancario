from datetime import datetime, date
from abc import abstractmethod

# ========== Classes ==========

class Transacao:
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if self._valor > 0:
            conta._saldo += self._valor
            conta.historico.adicionar_transacao("Deposit", self._valor)
            print(f"Deposit of {self._valor} successfully made!")
        else:
            print("Invalid deposit amount.")

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if self._valor > 0 and self._valor <= conta._saldo:
            conta._saldo -= self._valor
            conta.historico.adicionar_transacao("Withdraw", self._valor)
            print(f"Withdraw of {self._valor} successfully made!")
        else:
            print("Insufficient balance or invalid amount.")

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, tipo, valor):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "data": data_hora
        })

    @property
    def transacoes(self):
        return self._transacoes

    def mostrar(self, saldo):
        print("\n========== Account Statement ==========")
        if not self._transacoes:
            print("Nenhuma movimentação realizada.")
        else:
            for t in self._transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("=======================================")

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._cliente = cliente
        self._numero = numero
        self._saldo = 0.0
        self._historico = Historico()
        self._limite_saques = 3
        self._saques_realizados = 0
        self._data_ultimo_saque = None
        self._agencia = agencia
        self._limite_valor_saque = 500

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print(f"You have successfully deposited R$ {valor:.2f}")
            return True

        print("Invalid deposit value!")
        return False

    def sacar(self, valor: float) -> bool:
        hoje = date.today()

        # reseta contador se o último saque não foi hoje
        if self._data_ultimo_saque != hoje:
            self._saques_realizados = 0
            self._data_ultimo_saque = hoje

        if self._saques_realizados >= self._limite_saques:
            print("Daily withdrawal limit (3) reached.")
            return False

        if valor <= 0:
            print("Invalid withdrawal value.")
            return False
        
        if valor > self._limite_valor_saque:
            print(f"Withdrawal limit per operation is R$ {self._limite_valor_saque:.2f}.")
            return False

        if valor > self._saldo:
            print("Insufficient balance.")
            return False

        self._saldo -= valor
        self._saques_realizados += 1
        print(f"Withdrawal of R$ {valor:.2f} successful!")
        return True

    @classmethod
    def nova_conta(cls, cliente, numero, agencia="0001"):
        """Factory method to create a new account"""
        return cls(cliente, numero, agencia)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)  # chama o init da classe Cliente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# ========== Funções auxiliares ==========
def validate_cpf(cpf: str) -> bool:
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

def select_account(accounts):
    if not accounts:
        print("No accounts registered yet.")
        return None
    print("\nList of Accounts:")
    for acc in accounts:
        print(f"Account {acc.numero} - User: {acc.cliente.nome} - Agency: {acc.agencia}")
    try:
        acc_num = int(input("Enter the account number you want to access: "))
        for acc in accounts:
            if acc.numero == acc_num:
                return acc
        print("Invalid account number.")
    except ValueError:
        print("Invalid input! Enter numeric digits only.")
    return None

def create_user(users: list) -> None:
    cpf = input("Enter CPF (numbers only): ").strip()

    if not cpf or not validate_cpf(cpf):
        print("\n@@@ Invalid CPF! @@@")
        return

    if any(user.cpf == cpf for user in users):
        print("\n@@@ User with this CPF already exists! @@@")
        return

    name = input("Enter full name: ").strip()
    if not name:
        print("\n@@@ Name cannot be empty! @@@")
        return

    birth_date = input("Enter birth date (dd-mm-yyyy): ").strip()
    address = input("Enter address (street, number - neighborhood - city/state): ").strip()

    user = PessoaFisica(nome=name, data_nascimento=birth_date, cpf=cpf, endereco=address)
    users.append(user)

    print("\n=== User successfully created! ===")



# ========== Menu principal ==========
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

users = []     # Lista de objetos Cliente
accounts = []  # Lista de objetos ContaCorrente

def main():
    while True:
        option = input(menu)

        if option == "u":
           create_user(users)

        elif option == "c":
            if not users:
                print("No users registered yet. Create a user first.")
                continue
            print("Select the user for the new account:")
            for i, user in enumerate(users, start=1):
                print(f"{i} - {user.nome} (CPF: {user.cpf})")
            try:
                user_choice = int(input("Enter user number: "))
                if 1 <= user_choice <= len(users):
                    numero_conta = len(accounts) + 1
                    conta = ContaCorrente.nova_conta(users[user_choice - 1], numero_conta)
                    users[user_choice - 1].adicionar_conta(conta)
                    accounts.append(conta)
                    print(f"Account {numero_conta} created successfully for user {users[user_choice - 1].nome}!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input! Enter numeric digits only.")


        elif option == "d":  # Deposit
            account = select_account(accounts)
            if not account:
                continue

            try:
                value = float(input("How much will you deposit? "))
                if account.depositar(value):
                    account.historico.adicionar_transacao("Deposit", value)
            except ValueError:
                print("Invalid value! Please enter a number.")

        elif option == "w":  # Withdraw
            account = select_account(accounts)
            if not account:
                continue

            try:
                value = float(input("How much will you withdraw? "))
                if account.sacar(value):
                    account.historico.adicionar_transacao("Withdraw", value)
            except ValueError:
                print("Invalid value! Please enter a number.")

        elif option == "s":
            account = select_account(accounts)
            if account:
                account.historico.mostrar(account.saldo)

        elif option == "l":
            if not users:
                print("No users registered.")
            else:
                print("\n=== Users ===")
                for i, user in enumerate(users, start=1):
                    print(f"{i}. {user.nome} | CPF: {user.cpf} | Birth: {user.data_nascimento} | Address: {user.endereco}")

        elif option == "a":
            if not accounts:
                print("\nNo accounts registered.")
            else:
                print("\n=== Accounts ===")
                for acc in accounts:
                    print(f"Account {acc.numero} | Agency: {acc.agencia} | User: {acc.cliente.nome} | Balance: R$ {acc.saldo:.2f}")

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
