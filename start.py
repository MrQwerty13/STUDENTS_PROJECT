# === Importing necessary modules for blockchain interaction ===
import hashlib
import time


# === Blockchain Implementation ===
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        s = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        converted = ""
        for ch in s:
            if ch.isalpha():
                converted += str(ord(ch.lower()) - ord('a') + 1)
            elif ch.isdigit():
                converted += ch
            else:
                continue  # ignore non-alphanumeric characters

        if not converted:
            return '0' * 96

        num = int(converted)
        hex_str = hex(num)[2:]
        hex_str = hex_str.zfill(32)
        result = ''.join(ch * 3 for ch in hex_str)
        return result


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                print(f"❌ Hash mismatch at block {i}")
                return False
            if current.previous_hash != previous.hash:
                print(f"❌ Previous hash mismatch between blocks {i-1} and {i}")
                return False
        return True


# === Example usage of the Blockchain ===
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("Transaction 1")
    blockchain.add_block("Transaction 2")
    blockchain.add_block("Transaction 3")

    for block in blockchain.chain:
        print(f"\n🧱 Block {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Prev Hash: {block.previous_hash}")

    print("\nBlockchain valid:", blockchain.is_chain_valid())
