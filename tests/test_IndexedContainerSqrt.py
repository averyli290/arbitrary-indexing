import pytest
import logging
import random

from arbitrary_indexing.IndexedContainerSqrt import IndexedContainerSqrt

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)



def test_init_empty():
    ics = IndexedContainerSqrt()

def test_init_tuples():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

def test_large_init_tuples():
    size = 10000000
    obj_array = [(i,i) for i in range(size)]
    value_array = [i for i in range(size)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

def test_access_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
    for i in range(5):
        assert(ics.access(obj_array[i]) == i)

def test_access_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # This tuple doesn't exist, should not access properly
    with pytest.raises(LookupError):
        ics.access((1,2))

def test_append_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)
    new_obj = (1,2)
    new_val = 3
    ics.append(obj=new_obj, value=new_val)
    for i in range(5):
        assert(ics.access(obj_array[i]) == i)
    assert(ics.access(new_obj) == new_val)

def test_append_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # This tuple has value already exist, should not append properly
    with pytest.raises(AssertionError):
        prev_obj = obj_array[0]
        dummy_value = 0
        ics.append(obj=prev_obj, value=dummy_value)

def test_append_large():
    # Create ICS
    sample_len = 100
    obj_array = [(i,i) for i in range(sample_len)]
    value_array = [i for i in range(sample_len)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # Append elements
    to_append = 200000
    for i in range(to_append):
        obj = (i + sample_len, i + sample_len)
        value = i
        ics.append(obj=obj, value=value)

        obj_array.append(obj)
        value_array.append(value)

    # Verify still correct
    for i in range(len(obj_array)):
        # logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])

def test_insert_success():
    sample_len = 10
    for insert_idx in range(sample_len):
        obj_array = [(i,i) for i in range(sample_len)]
        value_array = [i for i in range(sample_len)]
        ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

        # Insert new element at insert_idx
        obj = (sample_len + 10, sample_len + 10)
        value = -1
        ics.insert(idx=insert_idx, obj=obj, value=value)

        # Update obj_arrary and value_array for testing
        obj_array.insert(insert_idx, obj)
        value_array.insert(insert_idx, value)
        # logger.debug(obj_array)
        # logger.debug(value_array)

        for i in range(len(obj_array)):
            # logger.debug(i)
            assert(ics.access(obj_array[i]) == value_array[i])

def test_insert_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # This tuple has value already exist, should not append properly
    with pytest.raises(AssertionError):
        prev_obj = obj_array[0]
        dummy_value = 0
        idx = 0
        ics.insert(idx=idx, obj=prev_obj, value=dummy_value)

def test_random_inserts():
    # Create ICS
    sample_len = 10000
    obj_array = [(i,i) for i in range(sample_len)]
    value_array = [i for i in range(sample_len)]

    # Use set to ensure to not insert duplicate objects to indexing
    used = set(obj_array)
    used.add(None)

    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # Insert elements randomly
    to_insert = 1000
    for i in range(to_insert):
        # Get random insert idx
        insert_idx = random.randint(0, sample_len + i)
        # Generate random object
        obj = None
        while obj in used:
            random_int = random.randint(-1000000,1000000)
            obj = (random_int, random_int)
        used.add(obj)         # Mark this object as used
        value = i

        # Insert
        ics.insert(idx=insert_idx, obj=obj, value=value)

        # Maintain another array to check
        obj_array.insert(insert_idx, obj)
        value_array.insert(insert_idx, value)

    # Verify still correct
    for i in range(len(obj_array)):
        # logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])
    
    # Reinitialize
    ics.reinitialize_container()

    # Verify still correct after reinitialization
    for i in range(len(obj_array)):
        # logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])

def test_reinitialization():
    # Create ICS
    sample_len = 10000
    obj_array = [(i,i) for i in range(sample_len)]
    value_array = [i for i in range(sample_len)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array)

    # Append elements
    to_append = 10000
    for i in range(to_append):
        obj = (i + sample_len, i + sample_len)
        value = i
        ics.append(obj=obj, value=value)

        obj_array.append(obj)
        value_array.append(value)

    # Verify still correct
    for i in range(len(obj_array)):
        # logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])
    
    # Reinitialize
    ics.reinitialize_container()

    # Verify still correct after reinitialization
    for i in range(len(obj_array)):
        # logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])