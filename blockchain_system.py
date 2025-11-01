import time
import hashlib
from typing import List


class Block:
    """
    Представляет отдельный блок в цепочке блокчейна.

    Атрибуты:
        index (int): Позиция блока в цепи.
        timestamp (float): Метка времени создания блока.
        data (str): Содержимое блока (например, транзакции).
        previous_hash (str): Хэш предыдущего блока.
        hash (str): Вычисленный хэш текущего блока.
    """

    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str) -> None:
        """
        Инициализирует объект блока и сразу вычисляет его хэш.

        Args:
            index (int): Позиция блока в цепи.
            timestamp (float): Время создания блока (time.time()).
            data (str): Данные, хранимые в блоке.
            previous_hash (str): Хэш предыдущего блока.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Генерирует псевдо-хэш блока на основе его данных.

        Алгоритм:
            1. Преобразует строку из всех полей блока.
            2. Заменяет буквы на их позиции в алфавите.
            3. Убирает неалфанумерные символы.
            4. Преобразует результат в HEX и троирует символы.

        Returns:
            str: Строка, представляющая “хэш” блока.
        """
        s = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        converted = ""
        for ch in s:
            if ch.isalpha():
                converted += str(ord(ch.lower()) - ord('a') + 1)
            elif ch.isdigit():
                converted += ch
            # остальные символы игнорируются

        if not converted:
            return '0' * 96

        num = int(converted)
        hex_str = hex(num)[2:]
        hex_str = hex_str.zfill(32)
        result = ''.join(ch * 3 for ch in hex_str)
        return result


class Blockchain:
    """
    Простая реализация блокчейна с возможностью добавления и проверки блоков.
    """

    def __init__(self) -> None:
        """Создаёт цепь и добавляет генезис-блок."""
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """
        Создаёт первый блок цепи (генезис-блок).

        Returns:
            Block: Начальный блок цепи.
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Получает последний блок в цепи.

        Returns:
            Block: Последний добавленный блок.
        """
        return self.chain[-1]

    def add_block(self, data: str) -> None:
        """
        Добавляет новый блок с указанными данными в цепь.

        Args:
            data (str): Информация, записываемая в блок.
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        Проверяет целостность всей цепи.

        Returns:
            bool: True, если цепь валидна, иначе False.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Проверка хэша текущего блока
            if current.hash != current.calculate_hash():
                print(f"❌ Несовпадение хэша в блоке {i}")
                return False

            # Проверка связи с предыдущим блоком
            if current.previous_hash != previous.hash:
                print(f"❌ Несовпадение ссылок между блоками {i-1} и {i}")
                return False

        return True


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("Transaction 1")
    blockchain.add_block("Transaction 2")

    for block in blockchain.chain:
        print(f"\n🧱 Block {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Previous: {block.previous_hash}")

    print("\nBlockchain valid:", blockchain.is_chain_valid())
