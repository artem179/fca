import copy
import functools

class Concept(object):
    def __init__(self, context, extent, intent):
        self.context = context
        self.extent = extent
        self.intent = intent

    def __str__(self):
        return '{obj:' + ', '.map(str, list(self.extent)) + '; attr:' + ', '.map(str, list(self.intent)) + '}'

    def __repr__(self):
        return self.__str__()

    
class Intent(object):
    def __init__(self, context, intent):
        self.context = context
        self.intent = set(intent)
        self._int_value = None
        
    def __str__(self):
        return str(self.intent)

    def __int__(self):
        if self._int_value is not None:
            return self._int_value
        result = 0
        current_power = 1
        for attr in self.context.attributes:
            if attr in self.intent:
                result += current_power
            current_power *= 2
        self._int_value = result
        return result

    def __cmp__(self, other):
        if int(self) < int(other):
            return -1
        elif int(self) == int(other):
            return 0
        else:
            return 1

    def __lt__(self, other):
        for attr in self.context.attributes:
            if attr in self and attr not in other:
                return False
            if attr not in self and attr in other:
                return True
        return False


    def __repr__(self):
        return self.str()

    def _cast_to_set(self, other):
        if type(other) == Intent:
            return other.intent
        return other
    
    def __and__(self, other):
        return Intent(self.context, self.intent & self._cast_to_set(other))
    
    def __or__(self, other):
        return Intent(self.context, self.intent | self._cast_to_set(other))
    
    def __sub__(self, other):
        return Intent(self.context, self.intent - self._cast_to_set(other))

    def __eq__(self, other):
        return self.intent == self._cast_to_set(other)

    def max(self):
        for attr in self.context.attributes[::-1]:
            if attr in self.intent:
                return attr
        return None

    def add(self, a):
        self._int_value = None
        self.intent.add(a)
    
    def remove(self, a):
        self._int_value = None
        self.intent.remove(a)

    def get_list(self):
        return list(self.intent)
    
    def copy(self):
        return Intent(self.context, copy.copy(self.intent))
    
    def __contains__(self, a):
        return a in self.intent

    def __len__(self):
        return len(self.intent)
    
    def add_and_return(self, a):
        return Intent(self.context, self.intent | {a})
    
    def derive(self):
        return Extent(self.context, set(self.context.attributes_derive(self.intent)))
    
    def closure(self):
        return Intent(self.context, set(self.context.attributes_closure(self.intent)))

    def make_object_from_set(self, intent):
        return Intent(self.context, intent)

    
class Extent(object):
    def __init__(self, context, extent):
        self.context = context
        self.extent = set(extent)
        
    def __str__(self):
        return str(self.extent)

    def __int__(self):
        if self._int_value is not None:
            return self._int_value
        result = 0
        current_power = 1
        for obj in self.context.objects:
            if obj in self.extent:
                result += current_power
            current_power *= 2
        self._int_value = result
        return result

    def __lt__(self, other):
        for obj in self.context.objects:
            if obj in self and obj not in other:
                return False
            if obj not in self and obj in other:
                return True
        return False

    def __repr__(self):
        return self.str()

    def _cast_to_set(self, other):
        if type(other) == Extent:
            return other.extent
        return other
    
    def __and__(self, other):
        return Extent(self.context, self.extent & self._cast_to_set(other))
    
    def __or__(self, other):
        return Extent(self.context, self.extent | self._cast_to_set(other))
    
    def __sub__(self, other):
        return Extent(self.context, self.extent - self._cast_to_set(other))

    def copy(self):
        return Extent(self.context, copy.copy(self.extent))

    def __eq__(self, other):
        return self.extent == self._cast_to_set(other)

    def __len__(self):
        return len(self.extent)

    def get_list(self):
        return list(self.extent)

    def max(self):
        for obj in self.context.objects:
            if obj in self.extent:
                return obj
        return None

    def add(self, a):
        self.extent.add(a)
    
    def remove(self, a):
        self._int_value = None
        self.extent.remove(a)

    def add_and_return(self, a):
        return Extent(self.context, self.extent | {a})

    def __contains__(self, a):
        return a in self.extent
    
    def derive(self):
        return Intent(self.context, set(self.context.objects_derive(self.extent)))
    
    def closure(self):
        return Extent(self.context, set(self.context.objects_closure(self.extent)))

    def make_object_from_set(self, extent):
        return Extent(self.context, extent)

