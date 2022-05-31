import tkinter as tk
import time
import os
import platform

import a_estrella

block_pad = 0
block_border = 1
block_width = 40
block_height = 40

max_stacks = 5
max_stack_height = 5


def drag_start(event):
    block = event.widget
    block.start_x = event.x
    block.start_y = event.y
    block.start_column = block.grid_info()['column']
    block.start_row = block.grid_info()['row']

def drag_motion(event):
    block = event.widget
    x = block.winfo_x() - block.start_x + event.x
    y = block.winfo_y() - block.start_y + event.y
    block.place(x=x, y=y)

def drag_release(event):
    block = event.widget
    #get x,y of resting place
    x = block.winfo_x() - block.start_x + event.x
    y = block.winfo_y() - block.start_y + event.y
    # get col, row of resting place
    column = x // block_width if x >= 0 else 0
    row = y // block_height if y >= 0 else 0
    
    parent_frame = block.master
    # check if blocks can be shifted up to make room for new block
    space_is_occupied = list(filter(lambda element: not element.is_placeholder, parent_frame.grid_slaves(row=row, column=column)))
    can_shift_up = len(parent_frame.grid_slaves(row=0, column=column)) == 1
    if space_is_occupied and not can_shift_up:
        column = block.start_column
        row = block.start_row
    elif space_is_occupied and can_shift_up:
        for i in range(1, row+1):
            block_to_shift = list(filter(lambda element: not element.is_placeholder, parent_frame.grid_slaves(row=i, column=column)))
            if block_to_shift:
                block_to_shift[0].grid(row=i - 1, column=column)
    # place the block
    block.grid(row=row, column=column)

    # collapse destination column
    if row < max_stack_height - 1:
        collapse_down = len(parent_frame.grid_slaves(row=row+1, column=column)) == 1
        if collapse_down:
            for i in range(row + 1, max_stack_height):
                collapse_down = len(parent_frame.grid_slaves(row=i, column=column)) == 1
                if not collapse_down:
                    break
                block.grid(row=i, column=column)

    # collapse origin column 
    if block.start_row > 0:
        collapse_down = len(parent_frame.grid_slaves(row=block.start_row-1, column=block.start_column)) == 2
        if collapse_down:
            for i in range(block.start_row - 1, -1, -1):
                block_to_collapse = list(filter(lambda element: not element.is_placeholder, parent_frame.grid_slaves(row=i, column=block.start_column)))
                if block_to_collapse:
                    block_to_collapse[0].grid(row=i + 1, column=block.start_column)

def create_place_holders(frame):
    empty_img = tk.PhotoImage()
    for stack_index in range(max_stacks):
        for block_index in range(max_stack_height - 1, -1, -1):
            block = tk.Label(frame, image=empty_img, compound=tk.CENTER, \
                width=block_width, height=block_height, \
                highlightthickness=block_border
            )
            block.is_placeholder = True
            block.grid(row=block_index, column=stack_index)

def create_platform(frame):
    block_char_int = ord("A")
    from PIL import Image,ImageTk
    box_image = Image.open("block.png").resize((block_width+10, block_height+10))
    box_image = ImageTk.PhotoImage(box_image)

    for stack_index in range(max_stacks):
        for block_index in range(max_stack_height - 1, -1, -1):

            if block_index < max_stack_height - 2 : continue # only to limit blocks
            
            block = tk.Label(frame, text=chr(block_char_int), font=("Arial", 15, "bold"), \
                image=box_image, compound=tk.CENTER, \
                width=block_width, height=block_height, \
                highlightbackground="#654A33", highlightthickness=block_border
            )
        
            block_char_int += 1
            block.is_placeholder = False
            block.box_image = box_image # anchoring image so it shows 
            block.grid(row=block_index, column=stack_index)
            block.bind("<Button-1>", drag_start)
            block.bind("<B1-Motion>", drag_motion)
            block.bind("<ButtonRelease-1>", drag_release)

def add_solve_buttons():
    font = ("Arial", 10, "bold")

    hamming_button = tk.Button(bottom_frame, text="Hamming", font=font, padx=10, pady=10)
    hamming_button["command"] = lambda: solve_a_estrella(hamming_button.cget('text'), a_estrella.HAMMING)
    hamming_button.grid(row=0, column=0)

    manhattan_button = tk.Button(bottom_frame, text="Manhattan", font=font, padx=10, pady=10)
    manhattan_button["command"] = lambda: solve_a_estrella(manhattan_button.cget('text'), a_estrella.MANHATTAN)
    manhattan_button.grid(row=0, column=1)

    euclidean_button = tk.Button(bottom_frame, text="Euclidean", font=font, padx=10, pady=10)
    euclidean_button["command"] = lambda: solve_a_estrella(euclidean_button.cget('text'), a_estrella.EUCLIDEAN)
    euclidean_button.grid(row=0, column=2)

    chebyshev_button = tk.Button(bottom_frame, text="Chebyshev", font=font, padx=10, pady=10)
    chebyshev_button["command"] = lambda: solve_a_estrella(chebyshev_button.cget('text'), a_estrella.CHEBYSHEV)
    chebyshev_button.grid(row=0, column=3)

def get_platform_from_frame(frame):
    platform = []
    for column in range(max_stacks):
        stack = []
        for row in range(max_stack_height):
            blocks = frame.grid_slaves(row=row, column=column)
            if len(blocks) == 2:
                stack.insert(0, blocks[1].cget("text") if blocks[0].is_placeholder else blocks[0].cget("text"))
        platform.append(stack)
    return platform

def animate_block_move(origin_column, dest_column):
    print(f"{origin_column} => {dest_column}")
    block = None
    origin_row = None
    for row in range(max_stack_height):
        blocks = platform_frame.grid_slaves(row=row, column=origin_column)
        if len(blocks) == 2:
            block = blocks[1] if blocks[0].is_placeholder else blocks[0]
            origin_row = row
            break
    
    dest_row = None
    for row in range(max_stack_height-1, -1, -1):
        blocks = platform_frame.grid_slaves(row=row, column=dest_column)
        if len(blocks) == 1:
            dest_row = row
            break
    
    steps = 20
    x_step = (dest_column - origin_column) * block_width // steps
    y_step = (dest_row - origin_row) * block_height // steps
    
    while steps >= 0:
        x = block.winfo_x() + x_step
        y = block.winfo_y() + y_step
        block.place(x=x, y=y)
        window.update()
        time.sleep(10/1000)
        steps -= 1
    block.grid(row=dest_row, column=dest_column)
    

def solve_a_estrella(heuristic_name, heuristic_value):
 
    title = f"======= Solving with {heuristic_name} =============="
    print(title)
    init_platform = get_platform_from_frame(platform_frame)
    goal_platform = get_platform_from_frame(goal_frame)
    root = a_estrella.get_new_root(init_platform, goal_platform, max_stack_height)
    nodo_solucion = a_estrella.a_estrella(root, heuristic_value)

    for nodo_transicion in a_estrella.get_ruta_solucion(root, nodo_solucion):
        if not nodo_transicion.parent: continue
        animate_block_move(nodo_transicion.origin_stack_index, nodo_transicion.dest_stack_index)

    print("="*len(title))


window = tk.Tk()
window.title("Blocks World")

frame_width = (block_width + block_border * 2) * (max_stacks + 1)
frame_height = (block_height + block_border * 2) * (max_stack_height + 1)

# TOP frame
top_frame = tk.Frame(window, width=frame_width*3, height=50, highlightbackground="blue", highlightthickness=2)
top_frame.grid(row=0, columnspan=3) 

# Platform frame
platform_frame = tk.Frame(window, width=frame_width, height=frame_height, \
    highlightbackground="blue", highlightthickness=2)
platform_frame.grid(row=1, column=0) 
platform_frame.grid_propagate(0)

# middle frame
blocks_frame = tk.Frame(window, width=frame_width, height=frame_height, \
    highlightbackground="blue", highlightthickness=2)
blocks_frame.grid(row=1, column=1)

# GOAL frame
goal_frame = tk.Frame(window, width=frame_width, height=frame_height, \
    highlightbackground="blue", highlightthickness=2)
goal_frame.grid(row=1, column=2) 
goal_frame.grid_propagate(0)

# Buttons frame
bottom_frame = tk.Frame(window, width=frame_width*3, height=50, highlightbackground="blue", highlightthickness=2)
bottom_frame.grid(row=2, columnspan=3) 
bottom_frame.grid_propagate(0)

# Buttons
add_solve_buttons()

create_place_holders(platform_frame)
create_platform(platform_frame)

create_place_holders(goal_frame)
create_platform(goal_frame)


window.mainloop()


