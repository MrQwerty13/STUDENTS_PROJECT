// MARK: - Libraries
import SwiftUI
import CryptoKit

// MARK: - User
class User {
    var name: String
    var wallet: Double
    var globalNumber: Int
    
    init(name: String, wallet: Double, globalNumber: Int) {
        self.name = name
        self.wallet = wallet
        self.globalNumber = globalNumber
    }
    
    func makeTransaction(to user_2: User, amount: Double) -> Bool {
        if self.wallet >= amount {
            self.wallet -= amount
            user_2.wallet += amount
            return true
        } else {
            print("\(name) doesn't have enough funds!")
            return false
        }
    }
}

// MARK: - Block
class Block {
    var amount: Double
    var previousHash: String
    var index: Int
    var user_1: Int
    var user_2: Int
    var hash: String = ""
    
    init(_ amount: Double, _ previousHash: String, _ index: Int, _ user_1: Int, _ user_2: Int) {
        self.amount = amount
        self.previousHash = previousHash
        self.index = index
        self.user_1 = user_1
        self.user_2 = user_2
        self.hash = self.calculateHash()
    }
    
    func calculateHash() -> String {
        let dataString = "\(index)-\(user_1)-\(amount)-\(user_2)-\(previousHash)"
        let data = Data(dataString.utf8)
        let digest = SHA512.hash(data: data)
        return digest.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    func isBlockValid(previousBlock: Block?) -> Bool {
        if amount < 0 || user_1 == user_2 || index <= 0 {
            return false
        }
        if self.hash != calculateHash() {
            return false
        }
        if let prev = previousBlock, previousHash != prev.hash {
            return false
        }
        return true
    }
}

// MARK: - Blockchain
class Blockchain {
    var chain: [Block] = []
    
    init() {
        let gen_block = Block(0.0, "0", 1, 0, 0)
        chain.append(gen_block)
    }
    
    func getPreviousBlock() -> Block {
        return chain.last!
    }
    
    func addBlock(_ block: Block) {
        chain.append(block)
    }
    
    func isChainValid() -> Bool {
        for i in 1..<chain.count {
            let currentBlock = chain[i]
            let previousBlock = chain[i - 1]
            if !currentBlock.isBlockValid(previousBlock: previousBlock) {
                print("Invalid block at index \(currentBlock.index)")
                return false
            }
        }
        return true
    }
}

// MARK: - Example with Users
let user1 = User(name: "Alice", wallet: 5000, globalNumber: 1)
let user2 = User(name: "Bob", wallet: 3000, globalNumber: 2)
let user3 = User(name: "Charlie", wallet: 1000, globalNumber: 3)

var my_BC = Blockchain()

// Функция для создания блока и проведения транзакции
@MainActor func createTransactionBlock(sender: User, receiver: User, amount: Double) {
    if sender.makeTransaction(to: receiver, amount: amount) {
        let block = Block(amount, my_BC.getPreviousBlock().hash, my_BC.getPreviousBlock().index+1, sender.globalNumber, receiver.globalNumber)
        my_BC.addBlock(block)
        print("Transaction successful: \(sender.name) -> \(receiver.name) : \(amount)")
    } else {
        print("Transaction failed: \(sender.name) -> \(receiver.name) : \(amount)")
    }
}

// Пример транзакций
createTransactionBlock(sender: user1, receiver: user2, amount: 1000)
createTransactionBlock(sender: user2, receiver: user3, amount: 500)
createTransactionBlock(sender: user3, receiver: user1, amount: 2000) // не хватит средств

// Проверка блокчейна
print("Is blockchain valid?\nAnswer: \(my_BC.isChainValid())")

// Балансы пользователей
print("Balances:")
print("\(user1.name): \(user1.wallet)")
print("\(user2.name): \(user2.wallet)")
print("\(user3.name): \(user3.wallet)")

for block in my_BC.chain {
    print("\(block.index) -> \(block.hash)")
    print("Amount: \(block.amount)")
    print("\(block.user_1) -> \(block.user_2)")
}
