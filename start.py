# === Importing necessary modules for blockchain interaction ===
import hashlib as h_lib


# === Blockchain Implementation ===
class Block():
    
    def __init__(self, index, timestamp, data, previous_hash, hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash
    
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
            return '0' * 96  # return a string of 96 zeros if no valid characters

        num = int(converted)
        hex_str = hex(num)[2:]  # delete '0x' prefix
        hex_str = hex_str.zfill(32)  # fill to ensure at least 32 characters
        result = ''.join(ch * 3 for ch in hex_str)
        return result

class Blockchain():
    def __init__(self):
        self.chain = [self.add_block()]

    def add_block(self):
        # Logic to add a new block to the blockchain
        new_block = Block(...)
        if new_block.previous_hash == self.chain[-1].hash:
            self.chain.append(new_block)
        else:
            del new_block

    def is_chain_valid(self) -> bool:
        # Logic to validate the blockchain
        for _ in range(len(self.chain)):
            if self.chain[_].hash == self.chain[_ + 1].previous_hash:
                continue
            else:
                return False
        return True
