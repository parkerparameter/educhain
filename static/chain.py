from static.block import Block
from static.errors import DeficientChainError
from typing import List, Union
from time import time
import json
from hashlib import sha256


class BlockChain(object):

    def __init__(self) -> None:
        self.chain: List[Block] = []
        self.transactions: List[object] = []

        # seed the genesis block

        self.add_new_block(previous_hash=1, proof=100)

    def __len__(self):

        return len(self.chain)

    def add_new_block(self, previous_hash: Union[str, int], proof: int) -> Block:
        """

        :param previous_hash:
        :param proof:
        :return:
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

        :param amount:
        :param sender:
        :param recipient:
        :param payload:
        :return:
        """

        self.transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'data': payload,
                'amount': amount
            }
        )

        return self.last_block['index'] + 1

    def simple_pow(self, last_proof: int) -> int:
        this_proof = 0
        while not self.validate_proof(last_proof=last_proof, this_proof=this_proof):

            this_proof += 1
        return this_proof

    @staticmethod
    def validate_proof(last_proof: int, this_proof: int) -> bool:

        return sha256(f'{last_proof *  this_proof}'.encode()).hexdigest()[:4] == "0000"


    @staticmethod
    def hash(block: Block) -> str:
        """

        :param block:
        :return:
        """
        block_string = json.dumps(block.serialize(), sort_keys=True).encode()

        return sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        """

        :return:
        """
        if not self.chain:
            raise DeficientChainError()

        return self.chain[-1]
