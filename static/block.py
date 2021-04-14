from static.constants import STANDARD_KEYS
from static.errors import WrongKeysError

class Block(object):

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
        return set(vars(self.valuables))

