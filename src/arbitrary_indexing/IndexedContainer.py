'''
Docstring for arbitrary-indexing.src.arbitrary_indexing.IndexedContainer

We want to be able to index a container with arbitrary objects.
Currently we can hash an object and map those to indices.

This implementation does not support removing elements or inserting into the middle
'''


class IndexedContainer:
    def __init__(self, obj_array=None, value_array=None, hash_func=hash):
        self.value_array = []
        self.length = 0
        self.hash_func = hash_func

        self._initialize_container(obj_array=obj_array, value_array=value_array)

    def _initialize_container(self, obj_array, value_array):
        if (obj_array is None) != (value_array is None):
            raise AssertionError(f"Either obj_array and value_array must both not be None, or they must both be None,"
                                 f"but obj_array has type {type(obj_array)} and value_array has type {type(value_array)}")

        if len(obj_array) != len(value_array):
            raise AssertionError(f"Length of obj_array to index value_array must be the same length"
                                 f"as value_array, but len(obj_array)={len(obj_array)} and"
                                 f"len(value_array)={len(value_array)}.")
        if obj_array is None or len(obj_array) == 0:
            self.array = []
            return
        raise NotImplementedError("Initialization function _initialize_container has not been implemented for a non-empty array.")
    
    def access(self, idx):
        raise NotImplementedError("Access function access(idx) has not been implemented.")

    def append(self, value):
        raise NotImplementedError("Append function append(value) has not been implemented.")

    def insert(self, idx, value):
        raise NotImplementedError("Insert function insert(idx, value) has not been implemented.")