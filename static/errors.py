from static.constants import STANDARD_KEYS


class DeficientChainError(Exception):

    def __init__(self, msg: str = "Current chain has no blocks available to return"):

        self.msg = msg
        super(DeficientChainError, self).__init__(self.msg)


class WrongKeysError(Exception):

    def __init__(self,
                 keys: set,
                 msg: str = f"Invalid keys supplied to block instance. Expected {STANDARD_KEYS}"):

        self.msg = msg + f"\n got {keys}"
        super(WrongKeysError, self).__init__(self.msg)
