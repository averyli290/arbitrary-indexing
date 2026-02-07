'''
Docstring for arbitrary-indexing.src.arbitrary_indexing.IndexedContainer

We want to be able to index a container with arbitrary objects.
Currently we can hash an object and map those to indices.

This implementation does not support removing elements or inserting into the middle
'''

from .IndexedContainer import IndexedContainer


class IndexedContainerBasic(IndexedContainer):
    def __init__(self, obj_array=None, value_array=None):

        self.obj_to_idx = {}

        super().__init__(
            obj_array=obj_array,
            value_array=value_array,
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

        # Assign each object i to have index i
        for i in range(self.length):
            self.obj_to_idx[obj_array[i]] = i
        
        # Assign value_array
        self.value_array = value_array

    
    def access(self, obj):
        '''
        Docstring for access
        
        :param self: Description
        :param obj: Description
        '''

        # Get if obj has a corresponding index
        if obj not in self.obj_to_idx:
            raise AssertionError(f"Could not find an index corresponding to object {obj}.")

        # Get index corresponding to obj, check if it is within bounds
        idx = self.obj_to_idx[obj]
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
        
        # Check for no duplicate object
        if obj in self.obj_to_idx:
            raise AssertionError(f"The object {obj} has already been assigned an index. The append operation has failed.")
        
        self.obj_to_idx[obj] = self.length
        self.length += 1
        self.value_array.append(value)

    def insert(self, idx, obj, value):
        raise NotImplementedError("Insert not implemented for IndexedContainerBasic")