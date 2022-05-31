from nodo import Nodo
from nodo import CHEBYSHEV, EUCLIDEAN, MANHATTAN, HAMMING

# platform = [
#     ["A", "B", "C"],
#     ["D", "E", "F"],
#     [],
#     []
# ]

# goal_platform = [
#     [],
#     [],
#     ["A", "B", "C"],
#     ["D", "E", "F"]
# ]

# goal_platform = [
#     [],
#     [],
#     ["C", "E", "A"],
#     ["F", "B", "D"]
# ]

# class AEstrella:

def get_new_root(init_platform, goal_platform, max_stack_height):
    if len(init_platform) != len(goal_platform):
        print("Initial and Goal platforms have different sizes")
        return None
    root = Nodo()
    root.max_stacks = len(init_platform)
    root.max_stack_height = max_stack_height
    root.platform = init_platform
    root.goal_platform = goal_platform
    return root


def a_estrella(root, heuristic=CHEBYSHEV, max_iterations=None):

    visitados = []
    cola = [root]
    i = 0
    while cola:
        
        i += 1
        nodo = cola.pop(0)
        nodo.iteration = i

        # if i % 500 == 0:
        #     print(f"Iteraciones: {i} - {nodo.name}")

        if nodo.is_goal():
            # nodo.print_platform()
            # print(f"Iteraciones: {i} - {nodo.name}")
            return nodo

        if max_iterations and i >= max_iterations:
            print(f"Iteraciones: {i} - {nodo.name}")
            return nodo

        visitados.append(nodo.platform)

        def insert_in_order(nodo):
            inserted = False
            for pos in range(len(cola)):
                if cola[pos].get_f(heuristic) > nodo.get_f(heuristic):
                    cola.insert(pos, nodo)
                    inserted = True
                    break
            if not inserted: cola.append(nodo)

        nodo.expand_children()
        for child in nodo.get_children():
            if child.platform not in visitados:
                insert_in_order(child)

    return None

def get_ruta_solucion(root, nodo_solucion):
    ruta = nodo_solucion.name.split(".")
    ruta.pop(0)
    nodo_actual = root
    yield nodo_actual
    for segmento in ruta:
        nodo_actual = nodo_actual.get_children()[int(segmento)]
        yield nodo_actual


# print("\nUsando Chebyshev")
# root = get_new_root()
# nodo_solucion = a_estrella(root, heuristic=CHEBYSHEV)
# print("\nUsando Manhattan")
# a_estrella(get_new_root(), heuristic=MANHATTAN)
# print("\nUsando Euclidean")
# a_estrella(get_new_root(), heuristic=EUCLIDEAN)
# print("\nUsando Hamming")
# a_estrella(get_new_root(), heuristic=HAMMING)
# print("-"*30)
# for nodo in get_solucion(root, nodo_solucion):
#     nodo.print_platform()