from static.constants import STANDARD_KEYS
from static.errors import WrongKeysError

class Block(object):
    """
    There are plenty of good reasons for fighting,' I said, 'but no good reason ever to hate without reservation,
    to imagine that God Almighty Himself hates with you, too. Where's evil? It's that large part of every man that wants
    to hate without limit, that wants to hate with God on its side. It's that part of every man that finds all kinds of
    ugliness so attractive
    """

    def __init__(self, valuables: dict):

        if set(valuables.keys()) - STANDARD_KEYS:
            raise WrongKeysError(keys=set(vars(valuables)))

        self.valuables = valuables

    def __getitem__(self, item):

        return self.valuables[item]

    def serialize(self) -> dict:

        return {
            'index': self.valuables['index'],
            'ts': self.valuables['ts'],
            'proof': self.valuables['proof'],
            'transactions': self.valuables['transactions'],
            'previous_hash': self.valuables['previous_hash']
        }

    @property
    def keys(self):
        return set(self.valuables.keys())

