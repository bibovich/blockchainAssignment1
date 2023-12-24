import random
import hashlib


# Assymetric encryption implementation:
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_keys():
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = pow(e, -1, phi)

    return (e, n), (d, n)


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def generate_prime():
    while True:
        num = random.randrange(100, 1000)
        if is_prime(num):
            return num


# Digital Signature implementation:
def sign(private_key, message):
    # Hash the message
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    # Encrypt the hash with the private key
    signature = encrypt(private_key, hashed_message)
    return signature


def verify(public_key, message, signature):
    # Hash the message
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    # Decrypt the signature with the public key
    decrypted_signature = decrypt(public_key, signature)
    # Compare the decrypted signature with the hash
    return decrypted_signature == hashed_message


# Merkle Tree implementation:
class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = self.build_tree()

    def build_tree(self):
        tree = [hashlib.sha256(str(transaction).encode()).hexdigest() for transaction in self.transactions]
        while len(tree) > 1:
            tree = [hashlib.sha256((tree[i] + tree[i + 1]).encode()).hexdigest() for i in range(0, len(tree), 2)]
        return tree

    def get_merkle_root(self):
        return self.tree[0] if self.tree else None


class Blockchain:
    def __init__(self):
        self.chain = []
        self.participants = set()

    def add_participant(self, participant):
        self.participants.add(participant)

    def generate_genesis_block(self):
        if len(self.participants) < 2:
            raise Exception("Need at least two participants to start the blockchain")

        client1, client2 = list(self.participants)[:2]

        # Generate keys for clients
        keys1 = generate_keys()
        keys2 = generate_keys()

        # Create the genesis block
        genesis_block = Block(transactions=[], previous_hash="0")
        genesis_block.add_transaction(
            Transaction(sender=client1, recipient=client2, amount=100, keys=keys1, role="client"))
        genesis_block.add_transaction(
            Transaction(sender=client2, recipient=client1, amount=50, keys=keys2, role="client"))

        # Mine the genesis block
        genesis_block.mine_block()

        # Add genesis block to the chain
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        if not transactions:
            return

        # Error handling
        if not all(participant in self.participants for transaction in transactions for participant in
                   transaction.participants):
            raise Exception("Invalid participant in the transaction")

        # Create a new block
        block = Block(transactions=transactions, previous_hash=self.chain[-1].hash)

        # Mine the block
        block.mine_block()

        # Add the block to the chain
        self.chain.append(block)

    def print_chain(self):
        for block in self.chain:
            print(f"Block Hash: {block.hash}")
            print("Transactions:")
            for transaction in block.transactions:
                print(f"\t{transaction}")
            print("\n")


class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_tree = MerkleTree(transactions)
        self.nonce = None
        self.hash = None

    def mine_block(self):
        # Proof of Work using Merkle Tree
        while True:
            self.nonce = random.getrandbits(32)
            block_data = f"{self.merkle_tree.get_merkle_root()}{self.previous_hash}{self.nonce}"
            self.hash = hashlib.sha256(block_data.encode()).hexdigest()
            if self.hash.startswith("0000"):  # Criteria for mining the block
                break

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return f"Block - Hash: {self.hash}, Previous Hash: {self.previous_hash}"


class Transaction:
    def __init__(self, sender, recipient, amount, keys, role):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.keys = keys
        self.role = role
        self.participants = {self.sender, self.recipient}

    def __str__(self):
        return f"{self.sender} ({self.role}) sent {self.amount} to {self.recipient} ({self.role})"


class Miner:
    def __init__(self, name):
        self.name = name

    def mine_block(self, blockchain):
        # Create a mining transaction (reward) to the miner
        mining_reward = 10
        mining_keys = generate_keys()
        mining_transaction = Transaction(sender="System", recipient=self.name, amount=mining_reward, keys=mining_keys,
                                         role="miner")

        # Add the mining transaction to a new block
        new_block = Block(transactions=[mining_transaction], previous_hash=blockchain.chain[-1].hash)
        new_block.mine_block()

        # Add the new block to the blockchain
        blockchain.chain.append(new_block)
        print(f"{self.name} mined a new block! Reward: {mining_reward}")


def runEncryption():
    public_key, private_key = generate_keys()
    message = input("Enter a message: ")

    # Digital Signature
    signature = sign(private_key, message)
    print("Digital Signature:", signature)

    # Encryption
    encrypted_message = encrypt(public_key, message)
    print("Encrypted message:", encrypted_message)

    # Decryption
    decrypted_message = decrypt(private_key, encrypted_message)
    print("Decrypted message:", decrypted_message)

    # Verification
    if verify(public_key, decrypted_message, signature):
        print("Digital Signature Verification: Successful")
    else:
        print("Digital Signature Verification: Failed")


def runBlockchain():
    blockchain = Blockchain()
    blockchain.add_participant("Ali")
    blockchain.add_participant("Serzhan")
    blockchain.add_participant("Nurislam")

    # Start the blockchain with the genesis block
    blockchain.generate_genesis_block()

    # Create transactions
    transaction1 = Transaction(sender="Ali", recipient="Serzhan", amount=10, keys=generate_keys(), role="client")
    transaction2 = Transaction(sender="Serzhan", recipient="Nurislam", amount=5, keys=generate_keys(), role="client")

    # Add transactions to the blockchain
    blockchain.add_block([transaction1, transaction2])

    # Print the blockchain
    blockchain.print_chain()

    # Add a miner
    miner1 = Miner("Miner1")
    blockchain.add_participant(miner1.name)

    # Miner mines a new block
    miner1.mine_block(blockchain)

    blockchain.print_chain()


# Main:
if __name__ == '__main__':
    choice = input("Press 1 to go to String Encryption\nPress 2 to create a Blockchain: ")
    if (choice == "1"):
        runEncryption()
    elif (choice == "2"):
        runBlockchain()
    else:
        print("Invalid argument")
