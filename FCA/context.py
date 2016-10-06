import numpy
from .concept import Concept

class Context(object):
    '''Formal context class'''
    
    def __init__(self, cross_table, objects, attributes):
        if len(cross_table) != len(objects):
            raise ValueError("The number of cross_table's rows and objects's length don't agree")
        for row in cross_table:
            if len(row) != len(attributes):
                raise ValueError("The number of cross_table's columns and attributes's length don't agree")
        self._cross_table = numpy.array(cross_table, dtype=bool)
        self._objects = objects
        self._attributes = attributes

    def __str__(self):
        return ('attributes: ' + ' '.join(self._attributes) + '\n' +
                '\n'.join((self._objects[i]) + ': ' +
                          ''.join(('1' if self._cross_table[i][j] else '0' for j in range(len(self._attributes))))
                          for i in range(len(self._objects))))
    
    def get_objects(self):
        return self._objects

    def get_attributes(self):
        return self._attributes

    def get_cross_table(self):
        return self._cross_table

    def get_shape(self):
        return self._cross_table.shape

    objects = property(get_objects)
    attributes = property(get_attributes)
    cross_table = property(get_cross_table)
    shape = property(get_shape)
    
    def drop_object_by_index(self, index):
        self._objects.pop(index)
        self._cross_table = numpy.delete(self._cross_table, index, axis=0)
    
    def drop_object_by_name(self, name):
        index = self._objects.index(name)
        self.drop_object_by_index(index)

    def drop_attribute_by_index(self, index):
        self._attributes.pop(index)
        self._cross_table = numpy.delete(self._cross_table, index, axis=1)

    def drop_attribute_by_name(self, name):
        index = self._attributes.index(name)
        self.drop_object_by_index(index)
    
    def insert_object(self, name, pos=None, bool_array=None):
        if pos == None:
            pos = len(self._objects)
        if bool_array == None:
            bool_array = numpy.zeros(len(self._attributes), dtype=bool)
        self._objects.insert(name, pos)
        self._cross_table = numpy.insert(self._cross_table, pos, bool_array, axis = 0)
    
    def insert_attribute(self, name, pos=None, bool_array=None):
        if pos == None:
            pos = len(self._attributes)
        if bool_array == None:
            bool_array = np.zeros(len(self._objects), dtype=bool)
        self._attributes.insert(name, pos)
        self._cross_table = numpy.insert(self._cross_table, pos, bool_array, axis = 1)
        
    def set_cell_by_index(self, value, row, column):
        self._cross_table[row][column] = value

    def set_cell_by_name(self, value, object_name, attribute_name):
        self._cross_table[self._objects.index(object_name)][self._objects.index(attribute_name)] = value

    def set_row(self, row, bool_array):
        self._cross_table[row] = numpy.copy(bool_array)

    def set_column(self, column, bool_array):
        self._cross_table[:,column] = numpy.copy(bool_array)

    def _check_attributes(self, attributes_list):
        attr_set = set(self._attributes)
        for attr in attributes_list:
            if attr not in attr_set:
                raise ValueError('The attribute {0} doesn\'t exist'.format(attr))
            

    def _check_objects(self, objects_list):
        obj_set = set(self._objects)
        for obj in objects_list:
            if obj not in obj_set:
                raise ValueError('The object {0} doesn\'t exist'.format(object))

            
    def _attr_mask_to_list(self, bool_array):
        answer = []
        for i in range(self.shape[1]):
            if bool_array[i]:
                answer.append(self._attributes[i])
        return answer

    def _obj_mask_to_list(self, bool_array):
        answer = []
        for i in range(self.shape[0]):
            if bool_array[i]:
                answer.append(self._objects[i])
        return answer

    def _attr_list_to_mask(self, attributes_list):
        attr_set = set(attributes_list)
        return numpy.array([True if self._attributes[i] in attr_set
                            else False for i in range(self.shape[1])], dtype=bool)

    def _obj_list_to_mask(self, objects_list):
        obj_set = set(objects_list)
        return numpy.array([True if self._objects[i] in obj_set
                            else False for i in range(self.shape[0])], dtype=bool)
    
    
    def attributes_derive(self, attributes_list):
        self._check_attributes(attributes_list)
        intersection = numpy.ones(self.shape[0], dtype=bool)
        attr_set = set(attributes_list)
        for column, attr in enumerate(self._attributes):
            if attr in attr_set:
                intersection &= self._cross_table[:,column]
        return self._obj_mask_to_list(intersection)

    def objects_derive(self, objects_list):
        self._check_objects(objects_list)
        intersection = numpy.ones(self.shape[1], dtype=bool)
        obj_set = set(objects_list)
        for row, obj in enumerate(self._objects):
            if obj in obj_set:
                intersection &= self._cross_table[row]
        return self._attr_mask_to_list(intersection)

    def attributes_closure(self, attributes_list):
        self._check_attributes(attributes_list)
        attr_mask = self._attr_list_to_mask(attributes_list)
        intersection = numpy.ones(self.shape[1], dtype=bool)
        for i in range(self.shape[0]):
            if numpy.array_equal(attr_mask, attr_mask & self._cross_table[i]):
                intersection &= self._cross_table[i]
        return self._attr_mask_to_list(intersection)        

    def objects_closure(self, objects_list):
        self._check_objects(objects_list)
        obj_mask = self._obj_list_to_mask(objects_list)
        intersection = numpy.ones(self.shape[0], dtype=bool)
        for i in range(self.shape[1]):
            if (numpy.array_equal(obj_mask, obj_mask & self._cross_table[:,i])):
                intersection &= self._cross_table[:,i]
        return self._obj_mask_to_list(intersection)
'''    
    def infimum(self, concepts_list):
        obj_intersection = set(self._objects)
        attr_union = set()

        for concept in concepts_list:
            obj_intersection &= concept.extent
            attr_union |= concept.intent

        self._check_objects(list(obj_intersection))

        attr_union = self.attributes_closure(list(attr_union)) 
        
        return Concept(obj_intersection, attr_union)

    def supremum(self, concepts_list):
        obj_union = set()
        attr_intersection = set(self._attributes)

        for concept in concepts_list:
            obj_union |= concept.extent
            attr_intersection &= concept.intent

        self._check_attributes(list(attr_intersection))

        obj_union = self.objects_closure(list(obj_union))

        return Concept(obj_union, attr_intersection)
'''
    
