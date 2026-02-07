'''
Docstring for arbitrary-indexing.src.arbitrary_indexing.IndexedContainerSqrt

We want to be able to index a container with arbitrary objects.
Currently we can hash an object and map those to indices. This works
well for appending to the end just fine, but what if we want to insert in the middle?

Idea:
Store two mappings M1 (object hash to index mapping) and M2 (index to object hash mapping)
Whenever inserting an index
    - for all regions after, increase the offset by 1 (takes sqrt(n) time)
    - for region that it lands in, update all of them manually by using 

when any single region gets too big, recalculate

maintain a list of lists: sqrt(n) lists of size sqrt(n)
'''

import logging

from .IndexedContainer import IndexedContainer

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class IndexedContainerSqrt(IndexedContainer):
    '''
    # does not support removing elements
    # what if we onyl have to ever update sqrt(n) elements (offsets?)
    # insert at index i
    # for every index i ABOVE it, they must now increase by 1
    # for each of their regions as designated increase the offset by 1
    # how about within a region? 
    # if there is ever more than 1 internal within a region, recalculate the indices for that region
    # recalculating takes at most sqrt(n) time
    '''
    def __init__(self, obj_array=None, value_array=None, hash_func=hash):

        self.hash_func = hash_func
        self.hash_to_idx = {}
        self.internal_value_array = []

        self.regions = []                               # List of ~sqrt(n) regions of size ~sqrt(n) which contain the values
        self.regions_hash_values = []                   # List of ~sqrt(n) regions of size ~sqrt(n) which contain the hashes corresponding to the indices
        self.region_size = []                           # size of region i
        self.region_offset = []                         # Offset to apply to each region. If a region has an offset of 1, then every entry in it is considered
                                                        # to have an index increased by 1. This is to handle insertions at arbitrary positions and allows 
                                                        # updating up to n indices in O(sqrt(n)) time.

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

        # Get length of each region
        region_length = max(1, int(self.length ** (1/2)))


        # Construct array containing values
        for i in range(self.length):

            # Add a new region every ~sqrt(self.length) elements
            if i % region_length == 0:
                self.regions.append([])
                self.regions_hash_values.append([])
                self.region_size.append(0)
                self.region_offset.append(0)
            
            
            # Update hash value, check that it doesn't already exist
            hash_value = self.hash_func(obj_array[i])
            if hash_value in self.hash_to_idx:
                # Clear and reset class variables for memory
                self.length = 0
                self.regions.clear()
                self.region_size.clear()
                self.hash_to_idx.clear()
                raise AssertionError(f"The hash value of {obj} has already been assigned an index. The initialization has failed.")

            # Update region and region size with new element
            self.regions[-1].append(value_array[i])
            self.regions_hash_values[-1].append(hash_value)
            self.region_size[-1] += 1

            # Update hash map value
            self.hash_to_idx[hash_value] = i

    def access(self, obj):
        '''
        Returns the value at index represented by object obj.
        
        :param obj: Obj representing the index
        '''

        # Get if obj has a corresponding index
        hash_value = self.hash_func(obj)
        if hash_value not in self.hash_to_idx:
            raise LookupError(f"Hash value {hash_value} of object {obj} cannot be found in the object to index mapping.")

        # Get index corresponding to obj, check if it is within bounds
        idx = self.hash_to_idx[hash_value]
        if idx < 0 or idx >= self.length:
            raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")
        
        # Iterate through regions until in correct region to access
        # Takes O(sqrt(n))
        cur_idx = 0             # The global index of the first element in the current region(=self.region[cur_region])
        cur_region_idx = 0
        while cur_idx + self.region_size[cur_region_idx] <= idx:
            # Update current index, have to add the size of the current region and the next region's offset
            cur_idx += self.region_size[cur_region_idx]
            cur_region_idx += 1
            cur_idx += self.region_offset[cur_region_idx]       # Moves cur_idx to index of first element

        logger.debug(self.regions)
        logger.debug(self.region_offset)
        logger.debug(f"idx: {idx}")
        logger.debug(cur_region_idx)
        logger.debug(cur_idx)

        # Return value in region offset by values before it
        return self.regions[cur_region_idx][idx - cur_idx]
    
    def append(self, obj, value):
        '''
        Docstring for append
        
        :param self: Description
        :param obj: Object to index the value
        :param value: Value to append to array
        '''
        
        # Check for no duplicate hash
        hash_value = self._check_duplicate_hash(obj=obj)
        
        self.hash_to_idx[hash_value] = self.length          # Assign index to hash value of object
        self.length += 1                                    # Update length
        self.region_size[-1] += 1                           # Update region size of last region
        self.regions[-1].append(value)                      # Add value to last region
        self.regions_hash_values[-1].append(hash_value)     # Add hash value to index->hash value mapping by region

    def insert(self, idx, obj, value):
        '''
        Docstring for insert
        
        :param self: Description
        :param idx: Index to insert object at
        :param obj: Object to index the value
        :param value: Value to append to array
        '''
        
        if idx < 0 or idx > self.length:
            raise AssertionError(f"Cannot insert value at index {idx} in a container of size {self.length}.")

        # Check for no duplicate hash
        hash_value = self.hash_func(obj)
        if hash_value in self.hash_to_idx:
            raise AssertionError(f"The hash value of {obj} has already been assigned an index. The append operation has failed.")

        # Iterate through regions until in correct region to insert into
        # Takes O(sqrt(n))
        cur_idx = 0
        cur_region_idx = 0
        while cur_idx + self.region_size[cur_region_idx] <= idx:
            cur_idx += self.region_size[cur_region_idx]
            cur_region_idx += 1
        
        # O(sqrt(n)), each region is O(sqrt(n))
        insert_idx = idx - cur_idx
        self.hash_to_idx[hash_value] = idx                                      # Assign index to hash value of object
        self.length += 1                                                        # Update length
        self.region_size[cur_region_idx] += 1                                   # Update region size of target region
        self.regions[cur_region_idx].insert(insert_idx, value)    # Insert value into target region
        self.regions_hash_values[cur_region_idx].insert(insert_idx, hash_value)   # Insert hash value into backwards mapping

        logger.debug(f"Inserted into {self.regions[cur_region_idx]} at index {insert_idx}")

        # Update hash_value->index mapping for everything inside current region which is after inserted element
        for i in range(insert_idx + 1, self.region_size[cur_region_idx]):
            logger.debug(f"Updating hash value->index mapping at index {i}")
            cur_hash_value = self.regions_hash_values[cur_region_idx][i]
            self.hash_to_idx[cur_hash_value] += 1
            logger.debug(f"Update: {self.hash_to_idx[cur_hash_value] - 1} to {self.hash_to_idx[cur_hash_value]}")
        
        # For all regions after, apply an offset of +1, all indices there must be considered to be 1 index increased now
        for i in range(cur_region_idx + 1, len(self.regions)):
            self.region_offset[i] += 1

    
    def _check_duplicate_hash(self, obj):
        '''
        Raises AssertionError if hash of obj already exists, otherwise returns hashed value of obj.
        
        :param obj: Object to check duplicate hash in self.hash_to_idx
        '''

        hash_val = self.hash_func(obj)
        if hash_val in self.hash_to_idx:
            raise AssertionError(f"The hash value of {obj} has already been assigned an index.")
        
        return hash_val