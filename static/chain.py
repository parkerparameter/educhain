from static.block import Block
from static.errors import DeficientChainError
from typing import List, Union
from time import time
import json
from hashlib import sha256


class BlockChain(object):
    """
    we are what we pretend to be, so we must be careful what we pretend to be
    """

    def __init__(self) -> None:
        """
        initialize the block chain. set the block list to empty as well as transactions for the current block

        we must also seed a genesis block, so that the blockchain will function properly on the first POST
        request to transactions/new
        """
        self.chain: List[Block] = []
        self.transactions: List[object] = []

        # seed the genesis block

        self.add_new_block(previous_hash=1, proof=100)

    def __len__(self):

        return len(self.chain)

    def __iter__(self):

        yield from self.chain

    def add_new_block(self, previous_hash: Union[str, int], proof: int) -> Block:
        """
        forges a new block in the chain

        :param previous_hash: previous hash of the block. required for pow for the new block
                              also safeguards against altering of previously mined blocks
        :param proof: integer proof used to decrypt the block
        :return: Block object
        """
        valuables = {
            'index': len(self.chain) + 1,
            'ts': time(),
            'proof': proof,
            'transactions': self.transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        block = Block(valuables=valuables)

        # wipe transactions for next block

        self.transactions = []

        # append to the chain
        self.chain.append(block)

        return block

    def add_new_transaction(self, sender: str, recipient: str, payload: object, amount: int = 0) -> int:
        """
        appends a transaction to the current block to be mined
        :param amount: int amount of coin to be sent to in the transaction
        :param sender: network address of node sending blocks
        :param recipient: network address of data recipient
        :param payload: payload of data to be sent
        :return: int index of block the transaction will be appending to
        """

        self.transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'payload': payload,
                'amount': amount
            }
        )

        return self.last_block['index'] + 1

    def simple_pow(self, last_proof: int) -> int:
        """
        simple guess and check method for generating pow
        :param last_proof: integer last proof guess
        :return: int of sucessful proof
        """
        this_proof = 0
        while not self.validate_proof(last_proof=last_proof, this_proof=this_proof):

            this_proof += 1
        return this_proof

    @staticmethod
    def validate_proof(last_proof: int, this_proof: int) -> bool:
        """
        validates a proof against sha256 encryption
        :param last_proof: int of last proof
        :param this_proof: int of current proof
        :return: bool, True if sufficiently decrypted False else
        """

        return sha256(f'{last_proof *  this_proof}'.encode()).hexdigest()[:4] == "0000"


    @staticmethod
    def hash(block: Block) -> str:
        """
        hashes a block
        :param block: Block object to be hashed
        :return: str hash of current block
        """

        # have to write serialize method here so that we can jsonify custom Block object

        block_string = json.dumps(block.serialize(), sort_keys=True).encode()

        return sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        """
        fetch the last block of the chain, if there is atleast one block, if not raise DeficientChainError
        :return: Block last Block in chain
        """
        if not self.chain:
            raise DeficientChainError()

        return self.chain[-1]
