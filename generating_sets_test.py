from FCA import Context, Concept, Intent, Extent
from FCA.io import read_csv
from FCA.alg import all_intents, all_certain_intents, all_small_intents, all_large_intents, \
all_intents_in_reversed_order, upper_neighbors, find_index, all_max_orbit_intents, all_minimal_generating_sets_of_intents, \
    next_candidate_set
from FCA.tools import attributes_ordered_list, objects_ordered_list
from itertools import permutations

if __name__ == '__main__':
    context = read_csv('next_closure.csv')
    print("All minimal generating sets of size at most 2")
    for intent in all_minimal_generating_sets_of_intents(context, 2):
        print("generaing set:", intent, "closure:", intent.closure())
    print("Next candidate set test")
    ksubsets = [{'h', 'g'}, {'h', 'f'}, {'f', 'g'},
                {'e', 'h'}, {'g', 'e'}, {'f', 'e'}, {'c', 'h'}]
    ksubsets = [Intent(context, intent) for intent in ksubsets]
    intent = Intent(context, {'f', 'g', 'h'})
    print(next_candidate_set(intent, context.attributes, ksubsets))
