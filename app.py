from uuid import uuid4

from flask import Flask, jsonify, request

from static.chain import BlockChain
from static.constants import STANDARD_TRANS_KEYS

# rev the Node
app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')

# starting the chain

blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    interface for forging new blocks into the chain
    :return: jsonified response
    """

    last_block = blockchain.last_block  # need this previous hash to store on the upcoming block
    last_proof = last_block['proof']  # where the last pow alg halted

    proof = blockchain.simple_pow(last_proof=last_proof)  # generate pow for current block

    # add the mining transaction
    blockchain.add_new_transaction(
        sender="0",
        recipient=node_id,
        payload={},
        amount=1
    )

    phash = blockchain.hash(last_block)  # previous hash we were just chatting about
    block = blockchain.add_new_block(previous_hash=phash, proof=proof)  # finally get to add the block to the chain

    resp = block.serialize()

    return jsonify(resp), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # unpack post

    values = request.get_json(force=True)

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
        'chain': [block.serialize() for block in blockchain],
        'chain_length': len(blockchain)
    }

    return jsonify(resp), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
