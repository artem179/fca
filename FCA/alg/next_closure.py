from FCA import Context, Concept, Intent, Extent

def _next_certain_closure(A_set, order, func=(lambda x: True)):
    A_set = A_set.copy()
    for m in order[::-1]:
        if m in A_set:
            A_set.remove(m)
        else:
            B_set = (A_set | {m}).closure()
            if not func(B_set):
                continue
            for b in order:
                if b == m:
                    return B_set
                if b not in A_set and b in B_set:
                    break
    return None


def next_intent(intent):
    return _next_certain_closure(intent, intent.context.attributes)


def next_extent(extent):
    return _next_certain_closure(extent, extent.context.objects)


def first_intent(context):
    return Intent(context, set()).closure()


def first_extent(context):
    return Extent(context, set()).closure()


def all_intents(context):
    intents = []
    intent = first_intent(context)
    while intent is not None:
        intents.append(intent)
        intent = next_intent(intent)
    return intents


def all_extents(context):
    extents = []
    extent = first_extent(context)
    while extent is not None:
        extents.append(extent)
        extent = next_extent(extent)
    return extents


def all_certain_closures(full_set, contained, avoided):
    closures = []
    order = avoided.get_list() + contained.get_list() + (full_set - contained - avoided).get_list()
    closure = contained.closure()
    if len(closure & avoided):
        return closures
    while (closure is not None and (closure & contained) == contained and
        (closure & avoided) == set()):
        closures.append(closure)
        closure = _next_certain_closure(closure, order)
    return closures


def all_certain_intents(context, contained, avoided):
    return all_certain_closures(Intent(context, context.attributes), contained, avoided)


def all_certain_extents(context, contained, avoided):
    return all_certain_closures(Extent(context, context.objects), contained, avoided)


def next_small_closure(context, intent, order, small):
    return _next_certain_closure(intent, order, small)


def all_small_intents(context, minsupp):    
    intents = []
    small = lambda x: len(x.derive()) / x.context.shape[0] >= minsupp
    intent = first_intent(context)
    if not small(intent):
        return intents
    while intent is not None:
        intents.append(intent)
        intent = next_small_closure(context, intent, context.attributes, small)
    return intents

def all_small_extents(context, minsupp):
    extents = []
    small = lambda x: len(x.derive()) / x.context.shape[1] >= minsupp
    extent = first_extent(context)
    if not small(extent):
        return extents
    while extent is not None:
        extents.append(extent)
        extent = next_small_closure(context, intent, context.objects, small)
    return extents


def next_large_closure(closure, order, large):
    closure = _next_certain_closure(closure.derive(), order, large)
    if closure is not None:
        return closure.derive()
    return None


def all_large_intents(context, minsize):
    intents = []
    large = lambda x: len(x.derive()) >= minsize
    intent = first_extent(context).derive()
    if len(intent) < minsize:
        intent = next_large_closure(intent, context.objects, large)
    while intent is not None:
        intents.append(intent)
        intent = next_large_closure(intent, context.objects, large)
    return intents


def all_large_extents(context, minsize):
    extents = []
    large = lambda x : len(x.derive()) >= minsize
    extent = first_intent(context).derive()
    if len(extent) < minsize:
        extent = next_large_closure(extent, context.attributes, large)
    while extent is not None:
        extents.append(extent)
        extent = next_large_closure(extent, context.attribites, large)
    return extents


def next_minimal_generating_set(A_set, order, k):
    A_set = A_set.copy()
    for m in order[::-1]:
        if m in A_set:
            A_set.remove(m)
        elif len(A_set) < k:
            B_set = A_set | {m}
            flag = True
            for b in B_set.get_list():
                if (B_set - {b}).closure() == B_set:
                    flag = False
                    break
            if flag:
                return B_set
    return None


def find_index(C_set, m, list_of_sets):
    left = m + 1
    right = len(list_of_sets)
    while right - left > 1:
        middle = (left + right) // 2
        if C_set < list_of_sets[middle]:
            right = middle
        else:
            left = middle
    return left


def _next_in(S, sets_list):
    index = find_index(S, -1, sets_list)
    if index + 1 >= len(sets_list):
        return None
    return sets_list[index + 1]


def _is_in_list(x, lst):
    index = find_index(x, -1, lst)
    if lst[index] == x:
        return True
    return False


def _find_in(S, sets_list):
    index = find_index(S, -1, sets_list)
    if sets_list[index] == S:
        return sets_list[index]
    return None


def next_candidate_set(C_set, order, ksubsets):
    B_set = C_set - {C_set.max()}
    A_set = C_set - {B_set.max()}
    A_set = _next_in(A_set, ksubsets)
    if A_set is None:
        return None
    while True:
        D_set = B_set - {B_set.max()}
        while A_set & B_set == D_set:
            flag = True
            result = A_set | B_set
            for x in D_set.get_list():
                if not _is_in_list(result - {x}, ksubsets):
                    flag = False
                    break
            if flag:
                return result
            A_set = _next_in(A_set, ksubsets)
        if A_set == B_set:
            for m in order[::-1]:
                if _is_in_list(D_set | {m}, ksubsets):
                    A_set = D_set | {m}
                    break
        else:
            A_set = B_set
        B_set = _next_in(B_set, ksubsets)
        if B_set is None:
            return None


'''
def titanic(context, minsupp, kmax, custom_support=False):
    current_k = {Intent(context, set())}
    C = [Intent(context, {x}) for x in context.attributes]
    result = []
    for X in C:
        X.predsupp = 1
    for k in range(1, kmax + 1):
        total_support = 0
        for X in C:
            X.support = 0
        for obj in context.objects:
            derived = derive(Intent(context, {x}))
            for X in C:
                if X & derived == X:
                    delta = 1
                    if custom_support:
                        delta += x.support
                    total_support += delta
                    X.support += delta
        for X in C:
            X.support /= total_support
        current_k = []
        for X in C:
            if X.predsupp > X.support and X.support >= minsupp:
                current_k.append(X)
        if len(current_k) == 0:
            break
'''

def _make_permutation(A_set, initial_order, permutation):
    B_set = A_set & set() #empty_set
    for a, b in zip(initial_order, permutation):
        if a in A_set:
            B_set.add(b)
    return B_set


def next_orbit_optimal(A_set, initial_order, permutations_list):
    orbit_maximal = (lambda x: max([_make_permutation(x, initial_order, permutation) for permutation in permutations_list]) ==
                     x)
    return _next_certain_closure(A_set, initial_order, orbit_maximal)


def upper_neighbors(C_set, M_set):
    N_set = M_set - C_set
    lst = N_set.get_list()
    for m in lst:
        if ((C_set | {m}).closure() & N_set) != {m}:
            N_set = N_set - {m}
    return N_set


def previous_closure(B_set, order):
    for index, m in enumerate(order[::-1]):
        if m not in B_set:
            continue
        B_set = B_set - {m}
        if m not in B_set.closure():
            for n in order[len(order) - index:]:
                if n not in B_set:
                    C_set = (B_set | {n}).closure()
                    flag = True
                    for g in order[:len(order) - index]:
                        if g in C_set and g not in B_set:
                            flag = False
                            break
                    if flag:
                        B_set = C_set
            return B_set
    return None


def all_intents_in_reversed_order(context):
    intent = Extent(context, {}).derive()
    intents = []
    while intent is not None:
        intents.append(intent)
        intent = previous_closure(intent, intent.context.attributes)
    return intents


def all_max_orbit_intents(context, initial_order, orbit):
    intent = first_intent(context)
    intents = []
    while intent is not None:
        intents.append(intent)
        intent = next_orbit_optimal(intent, initial_order, orbit)
    return intents


def all_minimal_generating_sets_of_intents(context, k):
    intent = Intent(context, {})
    intents = []
    while intent is not None:
        intents.append(intent)
        intent = next_minimal_generating_set(intent, context.attributes, k)
    return intents