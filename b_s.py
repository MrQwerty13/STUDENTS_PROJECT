# ===== Libraries =====
import hashlib

# ===== User =====
class User:
    def __init__(self, name: str, wallet: float, global_number: int):
        self.name = name
        self.wallet = wallet
        self.global_number = global_number

    def make_transaction(self, receiver, amount: float) -> bool:
        if self.wallet >= amount:
            self.wallet -= amount
            receiver.wallet += amount
            return True
        else:
            print(f"{self.name} doesn't have enough funds!")
            return False

# ===== Block =====
class Block:
    def __init__(self, amount: float, previous_hash: str, index: int, user_1: int, user_2: int):
        self.amount = amount
        self.previous_hash = previous_hash
        self.index = index
        self.user_1 = user_1
        self.user_2 = user_2
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data_string = f"{self.index}-{self.user_1}-{self.amount}-{self.user_2}-{self.previous_hash}"
        return hashlib.sha512(data_string.encode()).hexdigest()

    def is_block_valid(self, previous_block=None) -> bool:
        if self.amount < 0 or self.user_1 == self.user_2 or self.index <= 0:
            return False
        if self.hash != self.calculate_hash():
            return False
        if previous_block and self.previous_hash != previous_block.hash:
            return False
        return True

# ===== Blockchain =====
class Blockchain:
    def __init__(self):
        genesis_block = Block(0.0, "0", 1, 0, 0)
        self.chain = [genesis_block]

    def get_previous_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block):
        self.chain.append(block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if not current_block.is_block_valid(previous_block):
                print(f"Invalid block at index {current_block.index}")
                return False
        return True

# ===== Example with Users =====
user1 = User("Alice", 5000, 1)
user2 = User("Bob", 3000, 2)
user3 = User("Charlie", 1000, 3)

my_BC = Blockchain()

# Функция для создания блока и проведения транзакции
def create_transaction_block(sender: User, receiver: User, amount: float):
    if sender.make_transaction(receiver, amount):
        block = Block(amount, my_BC.get_previous_block().hash, my_BC.get_previous_block().index + 1,
                      sender.global_number, receiver.global_number)
        my_BC.add_block(block)
        print(f"Transaction successful: {sender.name} -> {receiver.name} : {amount}")
    else:
        print(f"Transaction failed: {sender.name} -> {receiver.name} : {amount}")

# Пример транзакций
create_transaction_block(user1, user2, 1000)
create_transaction_block(user2, user3, 500)
create_transaction_block(user3, user1, 2000)  # не хватит средств

# Проверка блокчейна
print(f"\nIs blockchain valid? Answer: {my_BC.is_chain_valid()}")

# Балансы пользователей
print("\nBalances:")
print(f"{user1.name}: {user1.wallet}")
print(f"{user2.name}: {user2.wallet}")
print(f"{user3.name}: {user3.wallet}")

# Вывод блоков
for block in my_BC.chain:
    print(f"\nIndex: {block.index}")
    print(f"Hash: {block.hash}")
    print(f"Amount: {block.amount}")
    print(f"{block.user_1} -> {block.user_2}")
