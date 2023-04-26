

class Variable:

    def __init__(self, data, short_name, long_name=None, units=None):
        
        if long_name is None: long_name = short_name

        self._data = data
        self._short_name = short_name
        self._long_name = long_name
        self._units = units

    def create_metadata_copy(self, data):
        return Variable(data, self.short_name, self.long_name, self.units)

    def is_same_metadata(self, var):

        if not self.short_name == var.short_name: return False
        if not self.long_name == var.long_name: return False
        if not self.units == var.units: return False

        return True


    @property
    def data(self): return self._data

    @property
    def short_name(self): return self._short_name

    @property
    def long_name(self): return self._long_name

    @property
    def units(self): return self._units

    @property
    def shape(self): return self._data.shape

    def is_same_size(self, var):
        if not type(var) is Variable: return False
        return self.data.shape == var.data.shape

    def filter(self, filt):
        sub_data = filt.filter(self.data)
        return Variable(sub_data, self._short_name, self._long_name, self._units)
