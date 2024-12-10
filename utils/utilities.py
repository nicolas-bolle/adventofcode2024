"""Misc data structures and things"""


class BinaryList(list):
    """list() but also sort of a binary tree
    Assumes it's made up of a single type of object, with comparisons implemented
    Assumed it's ordered at all times
    The key new things are
    - push(): push to it like a binary tree
    - find(): find the index of an element in the binary tree
    """

    def push(self, obj):
        """Add obj to the list using binary tree insert
        Assumes obj has the necessary comparisons implemented
        """
        i = self._find_above(obj)
        self.insert(i, obj)

    def find(self, obj) -> int:
        """Find the index of an item in the list, using the binary tree for speed"""
        i = self._find_above(obj)
        if i < len(self) and self[i] == obj:
            return i
        return ValueError

    def _find_above(self, obj) -> int:
        """Find the smallest index i with obj <= self[i]
        If no such i, returns len(self)
        """
        # trivial case
        if len(self) == 0:
            return 0

        # binary search
        i = 0
        j = len(self)
        while j - i:
            k = i + (j - i) // 2
            _obj = self[k]
            if obj <= _obj:
                j = k
            else:
                i = k + 1

        return j

    def remove(self, obj):
        """Remove item from the list, using the binary tree for speed"""
        i = self.find(obj)
        self.pop(i)
