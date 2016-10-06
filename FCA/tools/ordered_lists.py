def attributes_ordered_list(attributes_set):
    attributes_list = []
    for attr in attributes_set.context.attributes:
        if attr in attributes_set:
            attributes_list.append(attr)
    return attributes_list


def objects_ordered_list(objects_set):
    objects_list = []
    for obj in objects_set.context.objects:
        if obj in objects_set:
            objects_list.append(obj)
    return objects_list
