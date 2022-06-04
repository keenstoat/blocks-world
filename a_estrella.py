from nodo import Nodo
from nodo import CHEBYSHEV, EUCLIDEAN, MANHATTAN, HAMMING
from datetime import datetime

run_status = True

def set_run_status(status):
    global run_status
    run_status = status
    
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

def a_estrella(root, heuristic=CHEBYSHEV, callback=None, max_iterations=None):

    visitados = []
    cola = [root]
    i = 0
    children_expanded = 0
    t_start = datetime.now()
    def get_info_dict():
        b = children_expanded/len(visitados) if len(visitados) > 0 else -1.0
        cola_visitados = len(cola) / len(visitados) if len(visitados) > 0 else -1.0
        return {
            "Ciclos": i, 
            "Tiempo": f"{datetime.now() - t_start}",
            "Nodos en cola": len(cola), 
            "Nodos visitados": len(visitados), 
            "Visitados / En cola":  f"1 / {cola_visitados:.2f}" ,
            "Factor ramificacion": f"{b:.2f}"
        }


    while cola and run_status:
        i += 1
        nodo = cola.pop(0)
        nodo.iteration = i
        visitados.append(nodo.platform)
        
        if nodo.is_goal():
            if callback:
                info = get_info_dict()
                info["Pasos en solucion"] = len(nodo.name.split(".")) - 1
                info["Estado"] = "Terminado"
                callback(info)
            return nodo

        if max_iterations and i >= max_iterations:
            if callback:
                info = get_info_dict()
                info["Estado"] = "Ciclos agotados"
                callback(info)
            print(f"Ciclos: {i} - {nodo.name}")
            return nodo

    
        def insert_in_order(nodo):
            inserted = False
            for pos in range(len(cola)):
                if cola[pos].get_f(heuristic) > nodo.get_f(heuristic):
                    cola.insert(pos, nodo)
                    inserted = True
                    break
            if not inserted: cola.append(nodo)

        nodo.expand_children()
        children_expanded += len(nodo.children)
        for child in nodo.get_children():
            if child.platform not in visitados:
                insert_in_order(child)

        if callback:
            callback(get_info_dict())

    if callback:
        info = get_info_dict()
        info["Estado"] = "Sin solucion" if run_status else "Detenido"
        callback(info)
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