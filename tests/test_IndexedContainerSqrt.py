import pytest
import logging

from arbitrary_indexing.IndexedContainerSqrt import IndexedContainerSqrt

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)



def test_init_empty():
    ics = IndexedContainerSqrt()

def test_init_tuples():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)

def test_access_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)
    for i in range(5):
        assert(ics.access(obj_array[i]) == i)

def test_access_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)

    # This tuple doesn't exist, should not access properly
    with pytest.raises(LookupError):
        ics.access((1,2))

def test_append_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)
    new_obj = (1,2)
    new_val = 3
    ics.append(obj=new_obj, value=new_val)
    for i in range(5):
        assert(ics.access(obj_array[i]) == i)
    assert(ics.access(new_obj) == new_val)

def test_append_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)

    # This tuple has value already exist, should not append properly
    with pytest.raises(AssertionError):
        prev_obj = obj_array[0]
        dummy_value = 0
        ics.append(obj=prev_obj, value=dummy_value)

def test_insert_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    ics = IndexedContainerSqrt(obj_array=obj_array, value_array=value_array, hash_func=hash)

    # Insert new element at index 0
    idx = 0
    obj = (10,10)
    value = -1
    ics.insert(idx=idx, obj=obj, value=value)

    # Update obj_arrary and value_array for testing
    obj_array.insert(0, obj)
    value_array.insert(0, value)
    logger.debug(obj_array)
    logger.debug(value_array)

    for i in range(len(obj_array)):
        logger.debug(i)
        assert(ics.access(obj_array[i]) == value_array[i])

