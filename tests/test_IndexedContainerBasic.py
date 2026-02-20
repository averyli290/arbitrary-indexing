import pytest
from arbitrary_indexing.IndexedContainerBasic import IndexedContainerBasic


def test_init_empty():
    icb = IndexedContainerBasic()

def test_init_tuples():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)

@pytest.mark.skip(reason="This test is currently broken due to a known bug")
def test_large_init_tuples():
    num_elts = int(1E7)
    obj_array = [(i,i) for i in range(num_elts)]
    value_array = [i for i in range(num_elts)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)
    # Verify still correct
    for i in range(num_elts):
        # logger.debug(i)
        assert(icb[obj_array[i]] == value_array[i])

def test_access_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)
    for i in range(5):
        assert(icb[obj_array[i]] == i)

def test_access_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)

    # This tuple doesn't exist, should not access properly
    with pytest.raises(AssertionError):
        icb[(1,2)]

def test_append_success():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)
    new_obj = (1,2)
    new_val = 3
    icb.append(obj=new_obj, value=new_val)
    for i in range(5):
        assert(icb[obj_array[i]] == i)
    assert(icb[new_obj] == new_val)

def test_append_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)

    # This tuple has value already exist, should not append properly
    with pytest.raises(AssertionError):
        prev_obj = obj_array[0]
        dummy_value = 0
        icb.append(obj=prev_obj, value=dummy_value)

def test_insert_fail():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)

    # Insert is not implemented for IndexedContainerBasic, should return NotImplementedError
    with pytest.raises(NotImplementedError):
        dummy_obj = obj_array[0]
        dummy_value = 0
        icb.insert(idx=0, obj=dummy_obj, value=dummy_value)

def test_range_access():
    obj_array = [(i,i) for i in range(5)]
    value_array = [i for i in range(5)]
    icb = IndexedContainerBasic(obj_array=obj_array, value_array=value_array)
    for i in range(5):
        assert(icb[obj_array[0]:obj_array[i]] == value_array[:i])

    