from hashlib import sha3_256

HASH = sha3_256
HASH_LEN = len(HASH().hexdigest())


class Pool:
    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError
