'''
Docstring for arbitrary-indexing.src.arbitrary_indexing.IndexedContainer

We want to be able to index a container with arbitrary objects.
Currently we can hash an object and map those to indices. This works
well for appending to the end just fine, but what if we want to insert in the middle?

Idea:
Store two mappings M1 (object hash to index mapping) and M2 (index to object hash mapping)
Whenever inserting an index
    - for all regions after, increase the offset by 1 (takes sqrt(n) time)
    - for region that it lands in, update all of them manually by using 


'''

# if (i >= j or i < 0 or i > len(B) or j < 0 or j > len(B)):
#     raise AssertionError(f"Attemping to access subarray starting at {i} and ending at {j} (B[{i}:{j}]), but block {B} is of length {len(B)}.")
from BitVector import BitVector




class IndexedContainer:
    # does not support removing elements
    # what if we onyl have to ever update sqrt(n) elements (offsets?)
    # insert at index i
    # for every index i ABOVE it, they must now increase by 1
    # for each of their regions as designated increase the offset by 1
    # how about within a region? 
    # if there is ever more than 1 internal within a region, recalculate the indices for that region
    # recalculating takes at most sqrt(n) time
    def __init__(self):
        self.array = []
        self.internal_array = []
        self.hash_to_index = {}           # hash to index mapping
        self.index_to_hash = {}           # index to hash mapping
        self.is_internal = BitVector(size=0)
        self.length = 0
    
    def __getitem__(self, idx):
        if (idx < 0 or idx >= self.length):
            raise AssertionError(f"Attemped to access index {idx} of a collection of size {self.length}.")

        
        r = self.is_internal.rank_of_bit_set_at_index(idx)
        if (self.is_internal[idx]):
            return self.internal_array[r]
        else:
            return self.internal_array[idx - r]
    
    def append(self, value):
        self.length += 1
        if (len(self.is_internal) < self.length):
            self.is_internal += BitVector(size=max(1, self.is_internal.length()))
        self.array.append(value)

    def insert(self, value):
        # keep track of offsets in powers of 2
        # Sqrt decomp? for each region/breakpoint, store the number
        # of 1's before that index. updating takes sqrt(n) time
        # redo the sqrt decomp when there are too many regions (do math to figure out how many,
        # for now, when region_size < sqrt(n) recalculate)
        raise NotImplementedError("Insert not yet implemented for IndexedContainer")