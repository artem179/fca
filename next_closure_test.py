#import FCA
#import FCA.io
#import FCA.alg
from FCA import Context, Concept, Intent, Extent
from FCA.io import read_csv
from FCA.alg import all_intents, all_certain_intents, all_small_intents, all_large_intents, \
all_intents_in_reversed_order, upper_neighbors, find_index, all_max_orbit_intents, all_minimal_generating_sets_of_intents
from FCA.tools import attributes_ordered_list, objects_ordered_list
from itertools import permutations

if __name__ == '__main__':
    context = read_csv('next_closure.csv')
    print("All intents")
    for intent in all_intents(context):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))
    print("All certain intents with C = {'e'}, A = {'h', 'c'}")
    for intent in all_certain_intents(context, Intent(context, {'e'}), Intent(context, {'h', 'c'})):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))
    print("All small intents with minsupp 0.51")
    for intent in all_small_intents(context, 0.51):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))
    print("All large intents of size at least 4")
    for intent in all_large_intents(context, 4):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))
    print("All intents in reversed order (previous_closure algorithm used)")
    for intent in all_intents_in_reversed_order(context):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))
    print("Upper neighbors")
    up_n = upper_neighbors(Intent(context, {'e'}), Intent(context, context.attributes))
    print(up_n)
    A = Intent(context, {'e'})
    print("Intent, index")
    for n in up_n.get_list():
        B = (A | {n}).closure()
        print(B, find_index(B, -1, all_intents(context)), sep=', ')
    orbit = list([context.attributes, ['a', 'b', 'c', 'd', 'g', 'f', 'e', 'h']])
    print("All lectically maximal intents of it's orbit")
    for intent in all_max_orbit_intents(context, context.attributes, orbit):
        print("intent: ", attributes_ordered_list(intent),
              "extent: ", objects_ordered_list(intent.derive()))

