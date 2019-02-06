from pathlib import Path

from .base import *


class LocalPool(Pool):
    def __init__(self, path):
        super().__init__()
        self._path = Path(path)
        self._temp = self._path / 'tmp'
        self._temp.mkdir(parents=True, exist_ok=True)

    def __truediv__(self, other):
        """For internal-use only."""
        path = self._path
        for i in range(0, HASH_LEN, 2):
            if (path / other[i:]).exists():
                return path / other[i:]
            path /= other[i:i + 2]
            if not path.exists():
                count = len(list(path.parent.iterdir()))
                if count < 250:
                    return path.parent / other[i:]
                path.mkdir()
                return path / other[i + 2:]

    def __contains__(self, key):
        path = self / key
        return path.exists()

    def __getitem__(self, key):
        path = self / key
        if not path.exists():
            raise KeyError(key)
        with path.open('rb') as f:
            return f.read()

    def __setitem__(self, key, data):
        path = self / key
        if path.exists():
            return
        hash = HASH(data).hexdigest()
        if key != hash:
            raise ValueError('hash mismatch', key, hash)
        temp = self._temp / key
        with temp.open('wb') as f:
            f.write(data)
        temp.rename(path)

    def get_size(self, key):
        path = self / key
        if not path.exists():
            raise KeyError(key)
        return path.stat().st_size
