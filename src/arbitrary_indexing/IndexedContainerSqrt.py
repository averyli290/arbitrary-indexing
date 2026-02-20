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
    # what if we only have to ever update sqrt(n) elements (offsets?)
    # insert at index i
    # for every index i ABOVE it, they must now increase by 1
    # for each of their regions as designated increase the offset by 1
    # how about within a region? 
    # if there is ever more than 1 internal within a region, recalculate the indices for that region
    # recalculating takes at most sqrt(n) time
    '''
    def __init__(self, obj_array=None, value_array=None):

        self.length = 0
        self.sqrtval = 0

        '''
        TODO:
        Work on figuring on what gives the best reinitialization_ratio or if
        there is a better heuristic for when to reinitialize. (repeated in comment below)
        Setting reinitialize_ratio to be equal to the sqrtval makes the most sense, why?
        there are sqrtval lists of length sqrtval, if there is one of length sqrtval ^ 2=self.length,
        then how does worst case search look?
        '''
        self.reinitialize_ratio = 10

        self.obj_to_repr_obj = {}                      # Maps from obj value of object->representative obj value of object of region containing both objects
        self.repr_obj_to_region_start_idx = {}         # Maps from representative hash value->the index of the start of the region which contains it

        self.regions = []                               # List of ~sqrt(n) regions of size ~sqrt(n) which contain the values
        self.regions_obj_values = []                    # List of ~sqrt(n) regions of size ~sqrt(n) which contain the objects corresponding to the indices
        self.region_size = []                           # size of region i
        self.num_regions = 0                            # Number of total regions

        super().__init__(
            obj_array=obj_array,
            value_array=value_array,
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
        region_length = max(10, int(self.length ** (1/2)))
        self.sqrtval = region_length
        self.reinitialize_ratio = region_length


        # Construct array containing values
        for i in range(self.length):

            # Check object to add doesn't already exist
            obj = obj_array[i]
            if obj in self.obj_to_repr_obj:
                # Clear and reset class variables for memory
                self.length = 0
                self.sqrtval = 0
                self.num_regions = 0
                self.regions.clear()
                self.region_size.clear()
                self.regions_obj_values.clear()
                self.obj_to_repr_obj.clear()
                self.repr_obj_to_region_start_idx.clear()
                raise AssertionError(f"The object {obj} has already been assigned an index. The initialization has failed.")

            # Add a new region every ~sqrt(self.length) elements
            if i % region_length == 0:
                self.regions.append([None] * region_length)
                self.regions_obj_values.append([None] * region_length)
                self.region_size.append(0)
                self.num_regions += 1

                # If first element then the obj is the representative obj
                self.obj_to_repr_obj[obj] = obj # Self mapping
                self.repr_obj_to_region_start_idx[obj] = i          # representative obj to index of start of region
            else:
                # Otherwise map hash to representative obj of current region
                self.obj_to_repr_obj[obj] = self.regions_obj_values[-1][0]

            # Update region and region size with new element
            self.regions[-1][i % region_length] = value_array[i]
            self.regions_obj_values[-1][i % region_length] = obj
            self.region_size[-1] += 1
        
        # Remove excess None values at the end of both self.regions and self.regions_obj_values
        if self.region_size[-1] < region_length:
            self.regions[-1] = self.regions[-1][:self.region_size[-1]]
            self.regions_obj_values[-1] = self.regions_obj_values[-1][:self.region_size[-1]]
    
    def get_contiguous_array(self):
        '''
        Docstring for get_contiguous_array
        
        :param self: Description
        '''
        mapping = {}
        array = [None] * self.length
        idx = 0
        for i in range(self.num_regions):
            for j in range(self.region_size[i]):
                mapping[self.regions_obj_values[i][j]] = idx
                array[idx] = self.regions[i][j]
                idx += 1

        # reference Family data structure defined in SageMath
        # inverted indexing, this might be more useful to return BECAUSE 
        # we are more concerned about the elements
        
        return array, mapping

    
    def reinitialize_container(self):
        '''
        Takes the current object and value array mappings and reruns initialization
        O(n)
        '''

        # Set object array to be the raw obj values to preserve mapping when reinitializing
        obj_array = [0] * self.length
        value_array = [None] * self.length

        idx = 0
        for i in range(self.num_regions):
            for j in range(self.region_size[i]):
                obj_array[idx] = self.regions_obj_values[i][j]
                value_array[idx] = self.regions[i][j]
                idx += 1
        
        # Reset variables, arrays, and dicitonaries before initialization to avoid hashing errors
        self.length = 0
        self.sqrtval = 0
        self.num_regions = 0
        self.regions.clear()
        self.region_size.clear()
        self.regions_obj_values.clear()
        self.obj_to_repr_obj.clear()
        self.repr_obj_to_region_start_idx.clear()
        
        # Reiniatialize container
        self._initialize_container(obj_array, value_array)
    
    def index(self, obj):
        '''
        Returns the index represented by object obj.
        
        :param obj: Obj representing the index
        '''

        # Get if obj has a corresponding representative object
        if obj not in self.obj_to_repr_obj:
            raise LookupError(f"Representative object of object {obj} cannot be found.")

        # Get index corresponding to repr obj, check if it is within bounds
        repr_obj = self.obj_to_repr_obj[obj]
        idx = self.repr_obj_to_region_start_idx[repr_obj]
        if idx < 0 or idx >= self.length:
            raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")
        
        # Iterate through regions until in correct region to access
        # Takes O(sqrt(n))
        repr_obj = self.obj_to_repr_obj[obj]
        region_start = self.repr_obj_to_region_start_idx[repr_obj]

        # find region index once
        for i in range(self.num_regions):
            # Get if idx is contained within current region
            if self.repr_obj_to_region_start_idx[self.obj_to_repr_obj[self.regions_obj_values[i][0]]] == region_start:
                # Return index of matching obj
                return self.regions_obj_values[i].index(obj)
        
        raise LookupError

    def __getitem__(self, key):
        '''
        Returns the value at index represented by object obj.
        
        :param obj: Obj representing the index
        '''

        if isinstance(key, slice):
            # Get objects from slice
            start_obj = key.start
            stop_obj  = key.stop

            # We do NOT support stepped slicing
            if key.step is not None:
                raise TypeError("Stepped slicing is not supported for IndexedContainerSqrt.")

            # Convert start and stop objects to internal index
            start_idx = 0 if start_obj is None else self.index(start_obj)
            stop_idx = 0 if stop_obj is None else self.index(stop_obj)

            # Collect everything in index range [start_idx, stop_idx)
            result = []

            idx = start_idx
            cur_region_idx = 0
            while idx + self.region_size[cur_region_idx] < stop_idx:
                result.extend(self.regions[cur_region_idx])
                idx += self.region_size[cur_region_idx]
                cur_region_idx += 1
            
            if idx < stop_idx:
                num_remaining_elements = stop_idx - idx
                result.extend(self.regions[cur_region_idx][:num_remaining_elements])
                idx += num_remaining_elements

            return result

        else:
            obj = key

            # Get if obj has a corresponding representative object
            if obj not in self.obj_to_repr_obj:
                raise LookupError(f"Representative object of object {obj} cannot be found.")

            # Get index corresponding to repr obj, check if it is within bounds
            repr_obj = self.obj_to_repr_obj[obj]
            idx = self.repr_obj_to_region_start_idx[repr_obj]
            if idx < 0 or idx >= self.length:
                raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")
            
            # Iterate through regions until in correct region to access
            # Takes O(sqrt(n))
            repr_obj = self.obj_to_repr_obj[obj]
            region_start = self.repr_obj_to_region_start_idx[repr_obj]

            # find region index once
            for i in range(self.num_regions):
                # Get if idx is contained within current region
                if self.repr_obj_to_region_start_idx[self.obj_to_repr_obj[self.regions_obj_values[i][0]]] == region_start:
                    # Iterate over region until hash value found
                    for j in range(self.region_size[i]):
                        object_hash_value = self.regions_obj_values[i][j]
                        if object_hash_value == obj:
                            return self.regions[i][j]
            
            raise LookupError
    
    def append(self, obj, value):
        '''
        Appends value to the end of the container indexed by obj.

        Note that append performs poorly for large amounts of data, probably due to
        dynamic arrays in Python.
        
        :param self: Description
        :param obj: Object to index the value
        :param value: Value to append to array
        '''
        
        # Check for no duplicate obj
        self._check_duplicate_obj(obj)

        # Assign representative obj to representative obj of last region
        self.obj_to_repr_obj[obj] = self.obj_to_repr_obj[self.regions_obj_values[-1][0]]

        self.length += 1                                    # Update length
        self.region_size[-1] += 1                           # Update region size of last region
        self.regions[-1].append(value)                      # Add value to last region
        self.regions_obj_values[-1].append(obj)             # Add obj value to index->obj mapping by region

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
            return

        # Check for no duplicate obj
        self._check_duplicate_obj(obj)

        # Iterate through regions until in correct region to insert into
        # Takes O(sqrt(n))
        region_idx = 0
        while region_idx < self.num_regions:
            # Get if index to insert at is contained in current region
            region_start_idx = self.repr_obj_to_region_start_idx[self.obj_to_repr_obj[self.regions_obj_values[region_idx][0]]]
            if region_start_idx <= idx and idx < region_start_idx + self.region_size[region_idx]:
                # If contained, insert at the current region
                
                insert_idx = idx - region_start_idx

                # Assign representative obj to newly inserted object
                self.obj_to_repr_obj[obj] = self.obj_to_repr_obj[self.regions_obj_values[region_idx][0]]

                self.length += 1                                                        # Update length
                self.region_size[region_idx] += 1                                       # Update region size
                self.regions[region_idx].insert(insert_idx, value)                      # Insert value into region
                self.regions_obj_values[region_idx].insert(insert_idx, obj)             # Insert obj value into region
                break

            region_idx += 1

        target_region_idx = region_idx      # size of this region is used to check integrity later
        if target_region_idx >= self.num_regions:
            raise IndexError(f"Could not insert value {value} at index {idx} represented by object {obj}.")
        
        # For all regions after the one inserted into, update the starting index to be += 1
        region_idx += 1         # Shift to the region after inserted to region
        while region_idx < self.num_regions:
            repr_obj = self.obj_to_repr_obj[self.regions_obj_values[region_idx][0]]
            self.repr_obj_to_region_start_idx[repr_obj] += 1
            region_idx += 1

        # Check if integrity has degraded, reinitialize if so
        if self.region_size[target_region_idx] > self.reinitialize_ratio * self.sqrtval:
            self.reinitialize_container()

    
    def _check_duplicate_obj(self, obj):
        '''
        Raises AssertionError if obj already exists in self.obj_to_repr_obj, otherwise return nothing.
        
        :param obj: Object to check duplicate.
        '''

        if obj in self.obj_to_repr_obj:
            raise AssertionError(f"The object {obj} has already been assigned a mapping for a representative.")
