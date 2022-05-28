from copy import deepcopy
import os
from math import sqrt

class Node:
    # heuristic constants
    HAMMING = 0
    MANHATTAN = 1 
    EUCLIDEAN = 3
    CHEBYSHEV = 4
     
    
    name = "0"
    max_stacks = 5
    max_stack_size = 3
    platform = None
    goal_platform = None
    parent = None
    children = None
    origin_stack_index = None
    dest_stack_index = None
    cost = 0
    hamming_d = None
    manhattan_d = None
    euclidean_d = None
    chebyshev_d = None
    
    def __init__(self, parent=None):
        self.children = []
        if parent:
            self.name = f"{parent.name}.{len(parent.children)}"
            self.max_stacks = parent.max_stacks
            self.max_stack_size = parent.max_stack_size
            self.goal_platform = parent.goal_platform
            self.parent = parent
            self.cost = parent.cost + 1
        
    def get_block_value(self, stack_index, block_index, platform=None):
        if not platform: 
            platform = self.platform
        stack = platform[stack_index]
        if stack and block_index < len(stack):
            return stack[block_index]
        return None

    def get_chebyshev_d(self):
        if self.chebyshev_d:
            return self.chebyshev_d
        distance = 0
        for stack_index, stack in enumerate(self.platform):
            for block_index, block in enumerate(stack):
                block_test = self.get_block_value(stack_index, block_index) 
                for goal_stack_index, goal_stack in enumerate(self.goal_platform):
                    if block_test in goal_stack:
                        goal_block_index = goal_stack.index(block_test)
                        distance += max(abs(goal_block_index - block_index), abs(goal_stack_index - stack_index))
                        break
                # if block_test not in the goal_platform, should exit
        self.chebyshev_d = distance
        return self.chebyshev_d

    def get_euclidean_d(self):
        if self.euclidean_d:
            return self.euclidean_d
        distance = 0
        for stack_index, stack in enumerate(self.platform):
            for block_index, block in enumerate(stack):
                block_test = self.get_block_value(stack_index, block_index) 
                for goal_stack_index, goal_stack in enumerate(self.goal_platform):
                    if block_test in goal_stack:
                        goal_block_index = goal_stack.index(block_test)
                        distance += sqrt((goal_block_index - block_index)**2 + (goal_stack_index - stack_index)**2)
                        break
                # if block_test not in the goal_platform, should exit
        self.manhattan_d = distance
        return self.manhattan_d

    def get_manhattan_d(self):
        if self.manhattan_d:
            return self.manhattan_d
        distance = 0
        for stack_index, stack in enumerate(self.platform):
            for block_index, block in enumerate(stack):
                block_test = self.get_block_value(stack_index, block_index) 
                for goal_stack_index, goal_stack in enumerate(self.goal_platform):
                    if block_test in goal_stack:
                        goal_block_index = goal_stack.index(block_test)
                        distance += abs(goal_block_index - block_index) + abs(goal_stack_index - stack_index)
                        break
                # if block_test not in the goal_platform, should exit
        self.manhattan_d = distance
        return self.manhattan_d

    def get_hamming_d(self):

        if self.hamming_d: 
            return self.hamming_d
        distance = 0
        for stack_index in range(self.max_stacks):
            for block_index in range(self.max_stack_size):
                block_test = self.get_block_value(stack_index, block_index) 
                block_goal = self.get_block_value(stack_index, block_index, self.goal_platform)
                if block_test is not block_goal:
                    distance += 1
        self.hamming_d = distance
        return self.hamming_d

    def get_f(self, h=None):
        if h is None:
            return self.cost
        if h == Node.MANHATTAN:
            return self.cost + self.get_manhattan_d()
        if h == Node.HAMMING:
            return self.cost + self.get_hamming_d()
        if h == Node.EUCLIDEAN:
            return self.cost + self.get_euclidean_d()
        if h == Node.CHEBYSHEV:
            return self.cost + self.get_chebyshev_d()

    def add_child(self, origin_stack_index, dest_stack_index):

        child_node = Node(self)
        
        cloned_platform = deepcopy(self.platform)
        cloned_platform[dest_stack_index].append(cloned_platform[origin_stack_index].pop())
        child_node.platform = cloned_platform

        child_node.origin_stack_index = origin_stack_index
        child_node.dest_stack_index = dest_stack_index
        
        self.children.append(child_node)

    def get_children(self):
        return self.children or []

    def expand_children(self):
        for origin_index, origin_stack in enumerate(self.platform):
            if not origin_stack: continue
            for dest_index, dest_stack in enumerate(self.platform):
                if origin_index == dest_index: continue
                if len(dest_stack) == self.max_stack_size: continue
                
                self.add_child(origin_index, dest_index)

    def is_goal(self):
        return self.get_hamming_d() == 0

    def print_platform(self):
        print(f"name={self.name} | cost={self.cost} | h={self.get_hamming_d()}")
        print(f"ori={self.origin_stack_index} | dest={self.dest_stack_index}")
        for row_index in range(self.max_stack_size - 1, -1, -1):
            for stack in self.platform:
                if row_index <= len(stack) - 1:
                    print(f"[{stack[row_index]}]", end="")
                else:
                    print(f"[ ]", end="")
            print()

    def get_graphviz_label(self):
        pass
        # header = f"{{h={str(self.get_h())}| i={self.iteration} }}"
        # labelList = [header]
        # for row in self.tablero:
        #     labelList.append("{" + "|".join([str(row[0]),str(row[1]),str(row[2])]) + "}")

        # mark_solucion = ", color=green" if self.is_solucion() else ""
        # label = f'"{self.name}" [label="{{ {"|".join(labelList)} }}" {mark_solucion}];\n'
        # return label

platform = [
    ["A", "B", "C"],
    ["D", "E", "F"],
    [],
    []
]

goal_platform = [
    [],
    [],
    ["A", "B", "C"],
    ["D", "E", "F"]
]


# goal_platform = [
#     [],
#     [],
#     ["C", "E", "A"],
#     ["F", "B", "D"]
# ]

def get_new_root():
    root = Node()
    root.max_stacks = 4
    root.max_stack_size = 3
    root.platform = platform
    root.goal_platform = goal_platform
    return root


def a_estrella(root, h=None, max_iterations=None):

    visitados = []
    cola = [root]
    i = 0
    while cola:
        
        i += 1
        nodo = cola.pop(0)
        # nodo.iteration = i
        if i % 500 == 0:
            print(f"Iteraciones: {i} - {nodo.name}")

        if nodo.is_goal():
            nodo.print_platform()
            print(f"Iteraciones: {i} - {nodo.name}")
            return nodo

        if max_iterations and i >= max_iterations:
            print(f"Iteraciones: {i} - {nodo.name}")
            return nodo

        visitados.append(nodo.platform)

        def insert_in_order(nodo):
            inserted = False
            for pos in range(len(cola)):
                if cola[pos].get_f(h) > nodo.get_f(h):
                    cola.insert(pos, nodo)
                    inserted = True
                    break
            if not inserted: cola.append(nodo)

        nodo.expand_children()
        # print(f"children: {[x.name for x in nodo.children()]}")
        for child in nodo.get_children():
            if child.platform not in visitados:
                insert_in_order(child)

    return None


print("\nUsando Chebyshev")
a_estrella(get_new_root(), h=Node.CHEBYSHEV)
print("\nUsando Manhattan")
a_estrella(get_new_root(), h=Node.MANHATTAN)
print("\nUsando Euclidean")
a_estrella(get_new_root(), h=Node.EUCLIDEAN)
print("\nUsando Hamming")
a_estrella(get_new_root(), h=Node.HAMMING)


# root.expand_children()

# print("------------ ROOT ---------- ")
# root.print_platform()
# for child in root.children:
#     print("-"*30)
#     child.print_platform()


