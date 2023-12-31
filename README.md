# Blockchain Assignment

## Project Overview
This is the first assignment of Blockhain Technologies 1
### Focus: 
Develop a command-line blockchain application, by using skills in asymmetric encryption, digital signatures, and understanding the intricate architecture of blockchain systems. 

## Import necessary modules
'random' module provides an access to the random numbers.
'hashlib' module provides an access to the hashing algorithms, in project we use sha-256
```python
import random
import hashlib
```


# Project Explanation

## Functions

## Assymetric Functions

### gcd(a,b)
This function calculates the greatest common divisor (GCD) of two integers, a and b, using the Euclidean algorithm to implement assymetric encryption
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

### is_prime(num)
Determines whether a given integer, num, is a prime number.
```python
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
```

### generate_keys()
Generates a pair of public and private keys for asymmetric encryption using the RSA algorithm.
```python
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
```

### encrypt(pk, plaintext)
Encrypts a plaintext using the public key (pk) with the RSA algorithm.
```python
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher
```

### decrypt(pk, ciphertext)
Decrypts a ciphertext using the private key (pk) with the RSA algorithm.
```python
def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)
```

### generate_prime()
Generates a random prime number in the range from 100 to 1000.
```python
def generate_prime():
    while True:
        num = random.randrange(100, 1000)
        if is_prime(num):
            return num
```

## Digital Signature

### sign(private_key, message)
Generates a digital signature for a given message using the SHA-256 hash function and encrypts the hash with the private key.
```python
def sign(private_key, message):
    # Hash the message
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    # Encrypt the hash with the private key
    signature = encrypt(private_key, hashed_message)
    return signature
```

### verify(public_key, message, signature)
Verifies the authenticity of a message by comparing the decrypted signature with the hash of the original message, using the public key.
```python
def verify(public_key, message, signature):
    # Hash the message
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    # Decrypt the signature with the public key
    decrypted_signature = decrypt(public_key, signature)
    # Compare the decrypted signature with the hash
    return decrypted_signature == hashed_message
```

## Encryption and Digital Signature in Action

### runEncryption()
Function demonstrates the use of the implemented encryption and digital signature functions in a practical scenario.
```python
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
```

### runBlockchain()
This function showcases the integration of the implemented blockchain-related classes (Blockchain, Transaction, Miner) in a simple blockchain application. 
```python
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
```

# Classes

## MerkleTree
A class representing a Merkle Tree. It takes a list of transactions as input during initialization.

### build_tree() 
Builds the Merkle Tree using SHA-256 hash functions.
```python
def build_tree(self):
    tree = [hashlib.sha256(str(transaction).encode()).hexdigest() for transaction in self.transactions]
    while len(tree) > 1:
        tree = [hashlib.sha256((tree[i] + tree[i + 1]).encode()).hexdigest() for i in range(0, len(tree), 2)]
    return tree
```
### get_merkle_root()
Returns the root of the Merkle Tree.
```python
def get_merkle_root(self):
    return self.tree[0] if self.tree else None
```

## Blockchain
A class representing a simple blockchain.

### add_participant(participant) 
Adds a participant to the set of participants.
```python
def add_participant(self, participant):
    self.participants.add(participant)
```

### generate_genesis_block() 
Generates the genesis block with predefined transactions and miners' keys.
```python
def generate_genesis_block(self):
    if len(self.participants) < 2:
        raise Exception("Need at least two participants to start the blockchain")
```

### add_block(transactions) 
Adds a new block to the blockchain with the provided transactions.
```python
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
```
### print_chain() 
Prints the entire blockchain.
```python
def print_chain(self):
    for block in self.chain:
        print(f"Block Hash: {block.hash}")
        print("Transactions:")
        for transaction in block.transactions:
            print(f"\t{transaction}")
        print("\n")
```

## Block
A class representing a block in the blockchain.

### mine_block() 
Mines the block using proof of work with a Merkle Tree.
```python
def mine_block(self):
    # Proof of Work using Merkle Tree
    while True:
        self.nonce = random.getrandbits(32)
        block_data = f"{self.merkle_tree.get_merkle_root()}{self.previous_hash}{self.nonce}"
        self.hash = hashlib.sha256(block_data.encode()).hexdigest()
        if self.hash.startswith("0000"):  # Criteria for mining the block
            break
```
### add_transaction(transaction) 
Adds a transaction to the block.
```python
def add_transaction(self, transaction):
    self.transactions.append(transaction)
```
### __str__() 
Returns a string representation of the block.
```python
def __str__(self):
    return f"Block - Hash: {self.hash}, Previous Hash: {self.previous_hash}"
```

## Transactions
A class representing a transaction in the blockchain.

### __str__()
Returns a string representation of the transaction.
```python
def __str__(self):
    return f"{self.sender} ({self.role}) sent {self.amount} to {self.recipient} ({self.role})"
```

## Miner
A class representing a miner in the blockchain.

### mine_block(blockchain)
Mines a new block and adds it to the blockchain with a mining reward.
```python
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
```


# User Interaction
The user is prompted to enter either "1" to go to String Encryption or "2" to create a Blockchain. The program then checks the user's choice and executes the corresponding functionality:

If the user enters "1", the runEncryption() function is called to demonstrate string encryption, digital signature, and verification.
If the user enters "2", the runBlockchain() function is called to showcase the implementation of a simple blockchain with participants, transactions, blocks, and mining.
If the user enters any other value, an "Invalid argument" message is displayed.
```python
if __name__ == '__main__':
    choice = input("Press 1 to go to String Encryption\nPress 2 to create a Blockchain: ")
    if (choice == "1"):
        runEncryption()
    elif (choice == "2"):
        runBlockchain()
    else:
        print("Invalid argument")
```





