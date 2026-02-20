

class temp:
    def __init__(self):
        self.arr = [] 
        self.internal = []
        self.is_internal = set()
        self.arr_map = {}           # obj -> array index
        self.internal_map = {}      # obj -> array index

    def access(self, obj):
        if obj in self.is_internal:
            return self.internal[self.internal_map[obj]]
        else:
            return self.arr[self.arr_map[obj]]

    def insert(self, obj, value):
        # O(n)
        pass

    def range(self, obj1, obj2):
        # return everything between
        # allows ability to return a submatrix
        pass

