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

recalculating the array:
    - This can take up to O(n) time
    - we can also consider merging existing regions in place, possibly reducing the time
        - is there a size where if we merge existing regions, it will take possible O(sqrt(n)) time?
          to recalculate the regions
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

        self.length = 0
        self.sqrtval = 0

        '''
        TODO:
        Work on figuring on what gives the best reinitialization_ratio or if
        there is a better heuristic for when to reinitialize. (repeated in comment below)
        '''
        self.reinitialize_ratio = 10

        self.hash_func = hash_func
        self.hash_to_repr_hash = {}                     # Maps from hash value of object->representative hash value of object of region containing both objects
        self.repr_hash_to_region_start_idx = {}         # Maps from representative hash value->the index of the start of the region which contains it

        self.regions = []                               # List of ~sqrt(n) regions of size ~sqrt(n) which contain the values
        self.regions_hash_values = []                   # List of ~sqrt(n) regions of size ~sqrt(n) which contain the hashes corresponding to the indices
        self.region_size = []                           # size of region i
        self.num_regions = 0                            # Number of total regions

        super().__init__(
            obj_array=obj_array,
            value_array=value_array,
            hash_func=hash_func
        )


    def _initialize_container(self, obj_array, value_array):
        '''
        Initializes class variables based on input array.
        O(n)
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
        self.sqrtval = region_length


        # Construct array containing values
        for i in range(self.length):

            # Check that hash value of object to add doesn't already exist
            hash_value = self.hash_func(obj_array[i])
            if hash_value in self.hash_to_repr_hash:
                # Clear and reset class variables for memory
                self.length = 0
                self.sqrtval = 0
                self.num_regions = 0
                self.regions.clear()
                self.region_size.clear()
                self.regions_hash_values.clear()
                self.hash_to_repr_hash.clear()
                self.repr_hash_to_region_start_idx.clear()
                raise AssertionError(f"The hash value of {obj} has already been assigned an index. The initialization has failed.")

            # Add a new region every ~sqrt(self.length) elements
            if i % region_length == 0:
                self.regions.append([])
                self.regions_hash_values.append([])
                self.region_size.append(0)
                self.num_regions += 1

                # If first element then the hash is the representative hash
                self.hash_to_repr_hash[hash_value] = hash_value             # Self mapping
                self.repr_hash_to_region_start_idx[hash_value] = i          # representative hash to index of start of region
            else:
                # Otherwise map hash to representative hash of current region
                self.hash_to_repr_hash[hash_value] = self.regions_hash_values[-1][0]

            # Update region and region size with new element
            # (can make more effecient by allocating region_length immediately)
            self.regions[-1].append(value_array[i])
            self.regions_hash_values[-1].append(hash_value)
            self.region_size[-1] += 1
    
    def reinitialize_container(self):
        '''
        Takes the current object and value array mappings and reruns initialization
        O(n)
        '''

        # Temporarily store old hash function and make new temp hash func for just numbers
        hash_func_copy = self.hash_func

        # Set object array to be the raw hash values to preserve mapping when reinitializing
        self.hash_func = lambda x: x
        obj_array = [0] * self.length
        obj_array_set = set()
        value_array = [None] * self.length

        idx = 0
        for i in range(self.num_regions):
            for j in range(self.region_size[i]):
                obj_array[idx] = self.regions_hash_values[i][j]
                assert(obj_array[idx] not in obj_array_set)
                obj_array_set.add(obj_array[idx])
                value_array[idx] = self.regions[i][j]
                idx += 1
        
        # Reset variables, arrays, and dicitonaries before initialization to avoid hashing errors
        self.length = 0
        self.sqrtval = 0
        self.num_regions = 0
        self.regions.clear()
        self.region_size.clear()
        self.regions_hash_values.clear()
        self.hash_to_repr_hash.clear()
        self.repr_hash_to_region_start_idx.clear()
        
        # Reiniatialize container
        self._initialize_container(obj_array, value_array)

        # Reset hash function
        self.hash_func = hash_func_copy


    def access(self, obj):
        '''
        Returns the value at index represented by object obj.
        
        :param obj: Obj representing the index
        '''

        # Get if obj has a corresponding representative hash
        hash_value = self.hash_func(obj)
        if hash_value not in self.hash_to_repr_hash:
            raise LookupError(f"Hash value {hash_value} of object {obj} cannot be found in the object to representative object mapping.")

        # Get index corresponding to obj, check if it is within bounds
        repr_hash = self.hash_to_repr_hash[hash_value]
        idx = self.repr_hash_to_region_start_idx[repr_hash]
        if idx < 0 or idx >= self.length:
            raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")
        
        # Iterate through regions until in correct region to access
        # Takes O(sqrt(n))
        for i in range(self.num_regions):
            # Get if idx is contained within current region
            region_start_idx = self.repr_hash_to_region_start_idx[self.hash_to_repr_hash[self.regions_hash_values[i][0]]]
            if idx == region_start_idx:
                # Iterate over region until hash value found
                for j in range(self.region_size[i]):
                    object_hash_value = self.regions_hash_values[i][j]
                    if object_hash_value == hash_value:
                        return self.regions[i][j]
        
        raise LookupError
    
    def append(self, obj, value):
        '''
        Docstring for append
        
        :param self: Description
        :param obj: Object to index the value
        :param value: Value to append to array
        '''
        
        # Check for no duplicate hash
        hash_value = self._check_duplicate_hash(obj)

        # Assign representative hash to representative hash of last region
        self.hash_to_repr_hash[hash_value] = self.hash_to_repr_hash[self.regions_hash_values[-1][0]]

        self.length += 1                                    # Update length
        self.region_size[-1] += 1                           # Update region size of last region
        self.regions[-1].append(value)                      # Add value to last region
        self.regions_hash_values[-1].append(hash_value)     # Add hash value to index->hash value mapping by region

        '''
        Check if integrity has degraded, reinitialize if so.
        Without reinitializing, appending 100000 elements can take up to 180 seconds,
        with reinializing it can take as low at 4-5 (for a ratio of 10 on 10000 intial elements)
        The ratio can clearly be fine tuned, perhaps it should be a function of the length, or
        when the median/average of the region sizes are too imbalanced.
        TODO: Work on figuring on what gives the best reinitialization_ratio or if there is a better heuristic for when to reinitialize.
        '''
        if self.region_size[-1] > self.reinitialize_ratio * self.sqrtval:
            self.reinitialize_container()

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
        
        # Append if insert is at end
        if idx == self.length:
            self.append(obj, value)

        # Check for no duplicate hash
        hash_value = self._check_duplicate_hash(obj)

        # Iterate through regions until in correct region to insert into
        # Takes O(sqrt(n))
        region_idx = 0
        while region_idx < self.num_regions:
            # Get if index to insert at is contained in current region
            region_start_idx = self.repr_hash_to_region_start_idx[self.hash_to_repr_hash[self.regions_hash_values[region_idx][0]]]
            if region_start_idx <= idx and idx < region_start_idx + self.region_size[region_idx]:
                # If contained, insert at the current region
                
                insert_idx = idx - region_start_idx

                # Assign representative hash to newly inserted object/hash
                self.hash_to_repr_hash[hash_value] = self.hash_to_repr_hash[self.regions_hash_values[region_idx][0]]

                self.length += 1                                                        # Update length
                self.region_size[region_idx] += 1                                       # Update region size
                self.regions[region_idx].insert(insert_idx, value)                      # Insert value into region
                self.regions_hash_values[region_idx].insert(insert_idx, hash_value)     # Insert hash value into region
                break

            region_idx += 1

        target_region_idx = region_idx      # used to check integrity later
        if target_region_idx >= self.num_regions:
            raise IndexError(f"Could not insert value {value} at index {idx} represented by object {obj}.")
        
        # For all regions after the one inserted into, update the starting index to be += 1
        region_idx += 1         # Shift to the region after inserted to region
        while region_idx < self.num_regions:
            repr_hash = self.hash_to_repr_hash[self.regions_hash_values[region_idx][0]]
            self.repr_hash_to_region_start_idx[repr_hash] += 1
            region_idx += 1

        # Check if integrity has degraded, reinitialize if so
        if self.region_size[target_region_idx] > self.reinitialize_ratio * self.sqrtval:
            self.reinitialize_container()

    
    def _check_duplicate_hash(self, obj):
        '''
        Raises AssertionError if hash of obj already exists, otherwise returns hashed value of obj.
        
        :param obj: Object to check duplicate hash in self.hash_to_idx
        '''

        # logger.debug(obj)
        hash_val = self.hash_func(obj)
        # logger.debug(hash_val)
        if hash_val in self.hash_to_repr_hash:
            raise AssertionError(f"The hash value {hash_val} of object {obj} has already been assigned a mapping.")
        
        return hash_val