import pytest
import logging
import random
import time

from arbitrary_indexing.IndexedContainerSqrt import IndexedContainerSqrt

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


# def test_init_empty():
#     ics = IndexedContainerSqrt()

# def test_init_tuples():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

# def test_large_init_tuples():
#     size = int(1E7)
#     obj_array = [(i,i) for i in range(size)]
#     value_array = [i for i in range(size)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

# # @pytest.mark.skip(reason="Recreating large array can be slow")
# def test_large_init_tuples_access_random_idx():
#     size = int(1E7)
#     obj_array = [(i,i) for i in range(size)]
#     value_array = [i for i in range(size)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
#     start = time.time()
#     num_random_access = int(1E5)
#     for i in range(num_random_access):
#         random_idx = random.randint(0,size-1)
#         assert(ics[obj_array[random_idx]] == value_array[random_idx])
#     end = time.time()
#     logger.info(f"Total search time across {num_random_access} random accesses across {size} elements in test_large_init_tuples_access_random_idx: {round(end - start,5)} seconds")

# def test_large_get_contiguous_array():
#     # Converting back to contiguous array performs simiarly well a regular append-based
#     # IndexedContainer like IndexedContainerBasic. That takes ~6 seconds for 1E7 accesses over 1E7
#     # items, this is ~23 seconds for (1E7) / 2 accesses across 1E7 items
#     size = int(1E7)
#     obj_array = [(i,i) for i in range(size)]   # tuple (i,i) representing i \in \Z
#     value_array = [i for i in range(size)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
#     array, mapping = ics.get_contiguous_array()
#     shuffled_obj_array = [o for o in obj_array]
#     random.shuffle(shuffled_obj_array)
#     num_random_access = int(1E6) // 2

#     # why is this so variable? the array is already determined, so it should only be the hash map that is slow
#     start = time.time()
#     for i in range(num_random_access):
#         random_obj = shuffled_obj_array[i]
#         temp = array[mapping[random_obj]]
#     end = time.time()
#     logger.info(f"Total search time across {num_random_access} random accesses across {size} elements in test_large_get_contiguous_array: {round(end - start,5)} seconds")

# def test_access_success():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
#     for i in range(5):
#         assert(ics[obj_array[i]] == i)

# def test_access_fail():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#     # This tuple doesn't exist, should not access properly
#     with pytest.raises(LookupError):
#         ics[(1,2)]

# def test_append_success():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
#     new_obj = (1,2)
#     new_val = 3
#     ics.append(obj=new_obj, value=new_val)
#     for i in range(5):
#         assert(ics[obj_array[i]] == i)
#     assert(ics[new_obj] == new_val)

# def test_append_fail():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#     # This tuple has value already exist, should not append properly
#     with pytest.raises(AssertionError):
#         prev_obj = obj_array[0]
#         dummy_value = 0
#         ics.append(obj=prev_obj, value=dummy_value)

# def test_append_large():
#     # Create ICS
#     sample_len = 100
#     obj_array = [(i,i) for i in range(sample_len)]
#     value_array = [i for i in range(sample_len)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#     # Append elements
#     to_append = int(5E6)
#     obj_array += [None] * to_append
#     value_array += [None] * to_append
#     for i in range(to_append):
#         obj = (i + sample_len, i + sample_len)
#         value = i
#         ics.append(obj=obj, value=value)

#         obj_array[i + sample_len] = obj
#         value_array[i + sample_len] = value


# def test_insert_success():
#     sample_len = 10
#     for insert_idx in range(sample_len):
#         obj_array = [(i,i) for i in range(sample_len)]
#         value_array = [i for i in range(sample_len)]
#         ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#         # Insert new element at insert_idx
#         obj = (sample_len + 10, sample_len + 10)
#         value = -1
#         ics.insert(idx=insert_idx, obj=obj, value=value)

#         # Update obj_arrary and value_array for testing
#         obj_array.insert(insert_idx, obj)
#         value_array.insert(insert_idx, value)
#         # logger.debug(obj_array)
#         # logger.debug(value_array)

#         for i in range(len(obj_array)):
#             # logger.debug(i)
#             assert(ics[obj_array[i]] == value_array[i])

# def test_insert_fail():
#     obj_array = [(i,i) for i in range(5)]
#     value_array = [i for i in range(5)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#     # This tuple has value already exist, should not append properly
#     with pytest.raises(AssertionError):
#         prev_obj = obj_array[0]
#         dummy_value = 0
#         idx = 0
#         ics.insert(idx=idx, obj=prev_obj, value=dummy_value)

# def test_random_inserts():
#     # Create ICS
#     sample_len = 10000
#     obj_array = [(i,i) for i in range(sample_len)]
#     value_array = [i for i in range(sample_len)]

#     # Use set to ensure to not insert duplicate objects to indexing
#     used = set(obj_array)
#     used.add(None)

#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
#     getnum = lambda: random.randint(-int(1E15),int(1E15)) 

#     # Insert elements randomly
#     to_insert = int(1E5)
#     for i in range(to_insert):
#         # Get random insert idx
#         insert_idx = random.randint(0, sample_len + i)
#         # Generate random object
#         obj = None
#         while obj in used:
#             obj = (getnum(), getnum())
#         used.add(obj)         # Mark this object as used
#         value = i

#         # Insert
#         ics.insert(idx=insert_idx, obj=obj, value=value)

#         # Maintain another array to check
#         obj_array.insert(insert_idx, obj)
#         value_array.insert(insert_idx, value)

#     # Verify still correct
#     for i in range(len(obj_array)):
#         # logger.debug(i)
#         assert(ics[obj_array[i]] == value_array[i])
    
#     # Reinitialize
#     ics.reinitialize_container()

#     # Verify still correct after reinitialization
#     for i in range(len(obj_array)):
#         # logger.debug(i)
#         assert(ics[obj_array[i]] == value_array[i])

# def test_reinitialization():
#     # Create ICS
#     sample_len = 10000
#     obj_array = [(i,i) for i in range(sample_len)]
#     value_array = [i for i in range(sample_len)]
#     ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

#     # Append elements
#     to_append = 150
#     for i in range(to_append):
#         obj = (i + sample_len, i + sample_len)
#         value = i
#         ics.append(obj=obj, value=value)

#         obj_array.append(obj)
#         value_array.append(value)

#     # Verify still correct
#     for i in range(len(obj_array)):
#         # logger.debug(i)
#         assert(ics[obj_array[i]] == value_array[i])
    
#     # Reinitialize
#     ics.reinitialize_container()

#     # Verify still correct after reinitialization
#     for i in range(len(obj_array)):
#         # logger.debug(i)
#         assert(ics[obj_array[i]] == value_array[i])

def test_range_access():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
    for i in range(5):
        assert(icb[obj_array[0]:obj_array[i]] == value_array[:i])
    