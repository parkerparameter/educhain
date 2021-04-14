import hashlib
import json
from textwrap import dedent
from time import time
from static.constants import STANDARD_TRANS_KEYS
from uuid import uuid4

from static.chain import BlockChain

from flask import Flask, jsonify, request

# rev the Node
app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')

# starting the chain

blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.simple_pow(last_proof=last_proof)

    blockchain.add_new_transaction(
        sender="0",
        recipient=node_id,
        payload={},
        amount=1
    )
    phash = blockchain.hash(last_block)
    block = blockchain.add_new_block(previous_hash=phash, proof=proof)

    resp = block.serialize()

    return jsonify(resp), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    #unpack post

    values = request.get_json()

    if not all([k in values for k in STANDARD_TRANS_KEYS]):

        return f'insufficient keys supplied. Given: {values.keys()}\n Required: {STANDARD_TRANS_KEYS}', 400

    # create the transaction

    ix = blockchain.add_new_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        payload=values['payload']
    )
    resp = {'message': f'transaction completed & will be added to block {ix}'}

    return jsonify(resp), 201

@app.route('/chain', methods=['GET'])
def full_chain():

    resp = {
        'chain': blockchain.chain,
        'chain_length': len(blockchain)
    }

    return jsonify(resp), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
