'''
Docstring for arbitrary-indexing.src.arbitrary_indexing.IndexedContainer

We want to be able to index a container with arbitrary objects.
Currently we can hash an object and map those to indices.

This implementation does not support removing elements or inserting into the middle
'''

from .IndexedContainer import IndexedContainer


class IndexedContainerBasic(IndexedContainer):
    def __init__(self, obj_array=None, value_array=None, hash_func=hash):

        self.hash_to_idx = {}

        super().__init__(
            obj_array=obj_array,
            value_array=value_array,
            hash_func=hash_func
        )


    def _initialize_container(self, obj_array, value_array):
        '''
        Initializes class variables based on input array.
        '''
        if (obj_array is None) != (value_array is None):
            raise AssertionError(f"Either obj_array and value_array must both not be None, or they must both be None,"
                                 f"but obj_array has type {type(obj_array)} and value_array has type {type(value_array)}")

        if obj_array is None or len(obj_array) == 0:
            self.array = []
            return

        if len(obj_array) != len(value_array):
            raise AssertionError(f"Length of obj_array to index value_array must be the same length"
                                 f"as value_array, but len(obj_array)={len(obj_array)} and"
                                 f"len(value_array)={len(value_array)}.")

        # Initialize length
        self.length = len(obj_array)

        # Hash each object i and assign object to have index i
        for i in range(self.length):
            self.hash_to_idx[self.hash_func(obj_array[i])] = i
        
        # Assign value_array
        self.value_array = value_array

    
    def access(self, obj):
        '''
        Docstring for access
        
        :param self: Description
        :param obj: Description
        '''

        # Get if obj has a corresponding index
        hash_value = self.hash_func(obj)
        if hash_value not in self.hash_to_idx:
            raise AssertionError(f"Could not find an index corresponding to object {obj}.")

        # Get index corresponding to obj, check if it is within bounds
        idx = self.hash_to_idx[hash_value]
        if idx < 0 or idx >= self.length:
            raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")

        return self.value_array[idx]
    
    def append(self, obj, value):
        '''
        Docstring for append
        
        :param self: Description
        :param obj: Object to index the value
        :param value: Value to append to array
        '''
        
        # Check for no duplicate hash
        hash_val = self.hash_func(obj)
        if hash_val in self.hash_to_idx:
            raise AssertionError(f"The hash value of {obj} has already been assigned an index. The append operation has failed.")
        
        self.hash_to_idx[hash_val] = self.length
        self.length += 1
        self.value_array.append(value)

    def insert(self, idx, obj, value):
        raise NotImplementedError("Insert not implemented for IndexedContainerBasic")