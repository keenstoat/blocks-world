from copy import deepcopy
import os

class Node:

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
    
    def __init__(self):
        self.children = []

    def get_block_value(self, stack_index, block_index, platform=None):
        if not platform: 
            platform = self.platform
        stack = platform[stack_index]
        if stack and block_index < len(stack):
            return stack[block_index]
        return None

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

    def get_eval_function(self):
        return self.cost + self.get_hamming_d()

    def add_child(self, origin_stack_index, dest_stack_index):

        child_node = Node()
        child_node.name = f"{self.name}.{len(self.children)}"
        child_node.max_stacks = self.max_stacks
        child_node.max_stack_size = self.max_stack_size
        
        cloned_platform = deepcopy(self.platform)
        cloned_platform[dest_stack_index].append(cloned_platform[origin_stack_index].pop())
        child_node.platform = cloned_platform
        child_node.goal_platform = self.goal_platform

        child_node.parent = self
        self.children.append(child_node)
        
        child_node.origin_stack_index = origin_stack_index
        child_node.dest_stack_index = dest_stack_index
        
        child_node.cost = self.cost + 1

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
    ["G", "H"],
    [],
    []
]

goal_platform = [
    ["A", "B"],
    ["D", "E", "F"],
    ["G", "H"],
    ["C"],
    []
]

root = Node()
root.max_stacks = 5
root.max_stack_size = 3
root.platform = platform
root.goal_platform = goal_platform

root.expand_children()

print("------------ ROOT ---------- ")
root.print_platform()
for child in root.children:
    print("-"*30)
    child.print_platform()


