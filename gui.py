import tkinter as tk
import time
from concurrent.futures import ThreadPoolExecutor
import a_estrella

block_border = 1
block_width = 40
block_height = 40

max_stacks = 3
max_stack_height = 3
max_blocks = 5

platform_frame = None
goal_frame = None

thread_pool = ThreadPoolExecutor(1)
thread_is_running = False

# event handlers para drag and drop
def drag_start(event):
    if thread_is_running: return
    block = event.widget
    block.start_x = event.x
    block.start_y = event.y
    block.start_column = block.grid_info()['column']
    block.start_row = block.grid_info()['row']

def drag_motion(event):
    if thread_is_running: return
    block = event.widget
    x = block.winfo_x() - block.start_x + event.x
    y = block.winfo_y() - block.start_y + event.y
    block.place(x=x, y=y)

def drag_release(event):
    if thread_is_running: return
    block = event.widget
    #get x,y of resting place
    x = block.winfo_x() - block.start_x + event.x
    y = block.winfo_y() - block.start_y + event.y
    # get col, row of resting place
    column = x // block_width 
    if column < 0:
        column = 0
    elif column > max_stacks - 1:
        column = max_stacks -1

    row = y // block_height 
    if row < 0:
        row = 0
    elif row > max_stack_height - 1:
        row = max_stack_height - 1
    
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

# init de bloques y botones
def configure_platform(max_stacks_input, max_stack_height_input, max_blocks_input):
    global max_stacks, max_stack_height, max_blocks
    max_stacks = int(max_stacks_input)
    max_stack_height = int(max_stack_height_input)
    max_blocks = int(max_blocks_input)

    global platform_frame, goal_frame

    frame_width = (block_width + block_border * 2) * (max_stacks + 1)
    frame_height = (block_height + block_border * 2) * (max_stack_height + 1)

    if platform_frame:
        platform_frame.destroy()
     
    platform_frame = tk.Frame(platform_frame_container, width=frame_width, height=frame_height,\
    highlightbackground="grey", highlightthickness=1 )
    platform_frame.grid(row=0, column=0) 
    platform_frame.grid_propagate(0)

    if goal_frame:
        goal_frame.destroy()

    goal_frame = tk.Frame(goal_frame_container, width=frame_width, height=frame_height,\
        highlightbackground="grey", highlightthickness=1 )
    goal_frame.grid(row=0, column=0) 
    goal_frame.grid_propagate(0)
    
    create_place_holders(platform_frame)
    create_platform(platform_frame)
    create_place_holders(goal_frame)
    create_platform(goal_frame)

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

    added_blocks = 0
    for stack_index in range(max_stacks):
        for block_index in range(max_stack_height - 1, -1, -1):

            if added_blocks >= max_blocks:
                return
            
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
            added_blocks += 1

def add_config_platform_buttons():
    tk.Label(top_frame, text="Ancho: ").grid(row=0, column=0)
    max_stacks_input = tk.Spinbox(top_frame, from_=3, to=6)
    max_stacks_input.grid(row=0, column=1)

    tk.Label(top_frame, text="Alto: ").grid(row=1, column=0)
    max_stack_height_input = tk.Spinbox(top_frame, from_=3, to=6)
    max_stack_height_input.grid(row=1, column=1)

    tk.Label(top_frame, text="Cajas: ").grid(row=2, column=0)
    max_blocks_input = tk.Spinbox(top_frame, from_=3, to=26)
    max_blocks_input.grid(row=2, column=1)

    set_platform_button = tk.Button(top_frame, text="Configurar\nPlataforma", font = ("Arial", 10, "bold"), padx=10, pady=10)
    set_platform_button["command"] = lambda: configure_platform(max_stacks_input.get(), max_stack_height_input.get(), max_blocks_input.get())
    set_platform_button.grid(row=0, column=2, rowspan=3)

def add_run_buttons():
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

    stop_button = tk.Button(bottom_frame, text="STOP", font=font, padx=10, pady=10)
    stop_button["command"] = lambda: a_estrella.set_run_status(False)
    stop_button['state'] = tk.DISABLED
    stop_button.grid(row=0, column=5)

# integracion con ejecucion de solucion
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
    
    delay = 50/1000
    # move block up
    for row in range(origin_row, -1, -1):
        block.grid(row=row, column=origin_column)
        window.update()
        time.sleep(delay)
    # move block side ways
    step = (dest_column - origin_column)
    step //= abs(step)
    for col in range(origin_column, dest_column + step, step):
        block.grid(row=0, column=col)
        window.update()
        time.sleep(delay)
    # move block down
    for row in range(0, dest_row+1):
        block.grid(row=row, column=dest_column)
        window.update()
        time.sleep(delay)

def set_run_buttons_state(run_button_state):
    global thread_is_running
    if run_button_state == tk.DISABLED:
        stop_button_state = tk.NORMAL
        thread_is_running = True
    else:
        run_button_state = tk.NORMAL
        stop_button_state = tk.DISABLED
        thread_is_running = False
    
    for button in bottom_frame.grid_slaves():
        if button['text'] == 'STOP':
            button['state'] = stop_button_state
        else:
            button['state'] = run_button_state

def update_run_info(run_info_dict):
    
    info_text = ""
    for key, val in run_info_dict.items():
        info_text += f"{key}: {val}\n\n"
    info_label['text'] = info_text

def solve_a_estrella(heuristic_name, heuristic_value):
    
    def run_in_thread():
        set_run_buttons_state(tk.DISABLED)
        a_estrella.set_run_status(True)
        title = f"======= Solving with {heuristic_name} =============="
        print(title)
        heuristic_label['text'] = f"f(n) = {heuristic_name}"

        init_platform = get_platform_from_frame(platform_frame)
        goal_platform = get_platform_from_frame(goal_frame)
        
        root = a_estrella.get_new_root(init_platform, goal_platform, max_stack_height)
        nodo_solucion = a_estrella.a_estrella(root, heuristic_value, callback=update_run_info)

        # nodo_solucion puede ser None si a_estrella fue detenido prematuramente
        if nodo_solucion:
            for nodo in a_estrella.get_ruta_solucion(root, nodo_solucion):
                if not nodo.parent: continue
                animate_block_move(nodo.origin_stack_index, nodo.dest_stack_index)
        
        set_run_buttons_state(tk.NORMAL)
        print("="*len(title))
    
    thread_pool.submit(run_in_thread)
    

def close_window():
    if thread_is_running:
        a_estrella.set_run_status(False)
        print("search stopped!")
    else:
        print("window destroyed!")
        window.destroy()

window = tk.Tk()
window.title("Blocks World")
window.protocol("WM_DELETE_WINDOW", close_window)

frame_max_width = 300
frame_max_height = 300

# TOP frame
top_frame = tk.Frame(window, width=frame_max_width*3, height=50)
top_frame.grid(row=0, columnspan=3) 

# Platform fixed frame
platform_frame_container = tk.Frame(window, width=frame_max_width, height=frame_max_height)
platform_frame_container.grid(row=1, column=0) 
platform_frame_container.grid_propagate(0)

# INFO fixed frame
info_frame = tk.Frame(window, width=frame_max_width, height=frame_max_height)
info_frame.grid(row=1, column=1)
info_frame.grid_propagate(0)

heuristic_label = tk.Label(info_frame, text="- No info -", font = ("Arial", 15, "bold"))
heuristic_label.grid(row=0, column=0)
info_label = tk.Label(info_frame, text="- No info -", font = ("Arial", 10, "bold"), anchor="e", justify=tk.LEFT)
info_label.grid(row=1, column=0)

# GOAL fixed frame
goal_frame_container = tk.Frame(window, width=frame_max_width, height=frame_max_height)
goal_frame_container.grid(row=1, column=2) 
goal_frame_container.grid_propagate(0)

# Buttons fixed frame
bottom_frame = tk.Frame(window, width=frame_max_width*3, height=50)
bottom_frame.grid(row=2, columnspan=3) 
bottom_frame.grid_propagate(0)

# Buttons
add_config_platform_buttons()
add_run_buttons()

window.mainloop()
