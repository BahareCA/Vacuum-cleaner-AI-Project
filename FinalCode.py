def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        task_type = lines[0].strip()
        if task_type == "CHECK PLAN":
            plan = lines[1].strip()
            cave_map = [list(line.strip()) for line in lines[2:]]
            cave_map=correct_cave_map(cave_map)
            return task_type, plan, cave_map
        elif task_type == "FIND PLAN":
            cave_map = [list(line.strip()) for line in lines[1:]]
            cave_map=correct_cave_map(cave_map)
            return task_type, None, cave_map
        else:
            raise ValueError("Invalid task type")
def correct_cave_map(cave_map):
     height = 12#len(cave_map)
     width = 18#len(cave_map[0])
     s= [[' '] * width for _ in range(height)]
     for i, row in enumerate(cave_map):
        for j, square in enumerate(row):      
               s[i][j] =square
     return s



def find_starting_position(cave_map):
    for y, row in enumerate(cave_map):
        for x, square in enumerate(row):
            if square == 'S':
                return x, y
    return None  # Starting position not specified


def simulate_movement(plan, cave_map, start_x, start_y):
    height = len(cave_map)
    width = len(cave_map[0])
    cleaned_squares = set()
    
    x, y = start_x, start_y
    
    for move in plan:
        init_x, init_y=x, y
        if move == 'N':
            y = (y - 1) % height
        elif move == 'E':
            x = (x + 1) % width
        elif move == 'S':
            y = (y + 1) % height
        elif move == 'W':
            x = (x - 1) % width
        
        if cave_map[y][x] != 'X':
            cleaned_squares.add((x, y))
        else :
            cleaned_squares.add((init_x, init_y))
            
    return cleaned_squares

def simulate_movement_2(plan, cave_map, start_x, start_y):
    height = len(cave_map)
    width = len(cave_map[0])
    cleaned_squares = set()
    
    x, y = start_x, start_y
    
    for move in plan:
        
        if move == 'N':
            y2 = (y - 1) % height

            if cave_map[y2][x] != 'X':
                y=y2
                cleaned_squares.add((x, y2))
            else :
                cleaned_squares.add((x, y))

        elif move == 'E':
            x2 = (x + 1) % width
            if cave_map[y][x2] != 'X':
                x=x2
                cleaned_squares.add((x2, y))
            else :
                cleaned_squares.add((x, y))
        elif move == 'S':
            y2 = (y + 1) % height
            if cave_map[y2][x] != 'X':
                y=y2
                cleaned_squares.add((x, y2))
            else :
                cleaned_squares.add((x, y))
        elif move == 'W':
            x2 = (x - 1) % width
            if cave_map[y][x2] != 'X':
                 x=x2
                 cleaned_squares.add((x2, y))
            else :
                cleaned_squares.add((x, y))

            
    return cleaned_squares

def find_missed_squares(cleaned_squares, cave_map):
    missed_squares = []
    for y, row in enumerate(cave_map):
        for x, square in enumerate(row):
            if square == ' ' and (x, y) not in cleaned_squares:
                missed_squares.append((x, y))
    return missed_squares

#Check plan starts_Return string:GOOD PLAN, BAD PLAN

def check_plan(plan, cave_map, start_x, start_y):
    cleaned_squares = simulate_movement(plan, cave_map, start_x, start_y)
    missed_squares = find_missed_squares(cleaned_squares, cave_map)
    
    if not missed_squares:
        msg="GOOD PLAN"
        missed_points=""
        return msg,missed_points
    else:
        msg="BAD PLAN"
        missed_points=""
        for x, y in missed_squares:
          missed_points+= "\n"+f"{x}, {y}"
        return msg,missed_points

def check_plan_with_unknown_start(plan, cave_map):
    height = len(cave_map)
    width = len(cave_map[0])
    all_cleaned_squares = set()
    t_missed_squares=set()
    
    # Simulate movement from all possible starting positions
    for y in range(height):
        for x in range(width):
            if cave_map[y][x] == ' ':
                cleaned_squares = simulate_movement_2(plan, cave_map, x, y)
                #all_cleaned_squares.update(cleaned_squares)
                t_missed_squares.update(find_missed_squares(cleaned_squares, cave_map))
                
    #missed_squares = find_missed_squares(all_cleaned_squares, cave_map)
    missed_squares=t_missed_squares;
    if not missed_squares:
        msg="GOOD PLAN"
        missed_points=""
        return msg,missed_points
    else:
        msg="BAD PLAN"
        missed_points=""
        for x, y in missed_squares:
          missed_points+= "\n"+f"{x}, {y}"
        return msg,missed_points
            
#Check plan Ends
 
#Find plan starts_Return string of a plan


def find_plan_for_known_start(cave_map, start_x, start_y):
    height = len(cave_map)
    width = len(cave_map[0])
    visited = [[False] * width for _ in range(height)]
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    
    def is_cleanable(x, y):
        return 0 <= x < width and 0 <= y < height and cave_map[y][x] != "X"
    def is_last_square(visited,cave_map):
        
        for y, row in enumerate(cave_map):
            for x, square in enumerate(row):
                if square == ' ' and visited[y][x]!=True:
                    return False
        return True

    def dfs(x, y, plan, last_move):
        if not is_cleanable(x, y) or visited[y][x]:
            return plan
        visited[y][x] = True
        for direction, (dx, dy) in directions.items():
            new_x, new_y = (x + dx) % width, (y + dy) % height
            if is_cleanable(new_x, new_y) and not visited[new_y][new_x]:
                plan = dfs(new_x, new_y, plan + direction,direction)
            
        if   last_move!="" and not is_last_square(visited,cave_map):
            if last_move=="N":
                plan+="S"
            elif last_move=="S":
                plan+="N"
            elif last_move=="E":
                plan+="W"
            elif last_move=="W":
                plan+="E"

        return plan

    cleaning_plan = dfs(start_x, start_y, "","")
    #cleaned_squares = [(x, y) for y in range(height) for x in range(width) if visited[y][x]]
    return  cleaning_plan

 

def find_plan_for_unknown_start(cave_map):
    height = len(cave_map)
    width = len(cave_map[0])
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    plan = ""
    
    def dfs(x, y, visited):
        nonlocal plan
        if visited[y][x]:
            return
        visited[y][x] = True
        for direction, (dx, dy) in directions.items():
            new_x, new_y = (x + dx) % width, (y + dy) % height
            if cave_map[new_y][new_x] != "X" and not visited[new_y][new_x]:
                plan += direction
                dfs(new_x, new_y, visited)
                # Move back to the previous position
                plan += opposite_direction(direction)
                
    def opposite_direction(direction):
        return {"N": "S", "E": "W", "S": "N", "W": "E"}[direction]

    # Initialize visited matrix
    visited = [[False] * width for _ in range(height)]
    
    # Start DFS from the first empty cell
    t=[]
    for y in range(height):
        for x in range(width):
            if cave_map[y][x] == ' ':
                dfs(x, y, visited)
                 

    return plan


#Find plan Ends

def check_alg(file_detail,final_result,missed_points):
    #My solution
    print(final_result)
    print(missed_points)
    #Expected solution
    file_path = "example-solutions\\solution_"+file_detail+".txt"
    expected_final_result=None
    expected_missed_points=None
    t=""
    with open(file_path, 'r') as f:
        lines = f.readlines()
        expected_final_result = lines[0].strip()
        if expected_final_result == "BAD PLAN":            
            expected_missed_points = [list(line.strip()) for line in lines[1:]]

            for y, row in enumerate(expected_missed_points):
                t+="\n"
                for x, square in enumerate(row):
                    if square != ' ':
                        t+=square

            
        elif expected_final_result == "GOOD PLAN":
            expected_missed_points=""
    
    print(expected_final_result)
    print(t)
         
def print_cave_map(cave_map):
    for y, row in enumerate(cave_map):
        print(row)
    missed_squares = []
    for y, row in enumerate(cave_map):
        for x, square in enumerate(row):
            if square == ' ':
                missed_squares.append((x, y))
                print(str(x)+","+str(y))



def create_solution_file(task_type,final_result,missed_points,file_detail):
    final_msg=""
    if task_type == "CHECK PLAN":  
        final_msg=final_result+missed_points;
    elif task_type == "FIND PLAN":
        final_msg=final_result;
    file_path="solutions"+"\\solution_"+file_detail+".txt"
    with open(file_path, 'w') as f:
        f.write(final_msg)
    
 
import os

if __name__ == "__main__":

    directory = os.fsencode("problems")
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): 
            file_root="problems"
            file_detail=filename[8:12]
            
            file_path = file_root+"\\"+filename
            task_type, plan, cave_map = read_input(file_path)
            #print_cave_map(cave_map)
        
            start_position = find_starting_position(cave_map)
            missed_points=""
            if task_type == "CHECK PLAN":  
                if start_position:
                        start_x, start_y = start_position
                        final_result,missed_points=check_plan(plan, cave_map, start_x, start_y)
                else:
                        final_result,missed_points=check_plan_with_unknown_start(plan, cave_map)
            elif task_type == "FIND PLAN":
                if start_position:
                    start_x, start_y = start_position
                    final_result  = find_plan_for_known_start(cave_map, start_x, start_y)
                else:
                    final_result = find_plan_for_unknown_start(cave_map)
        
            #check_alg(file_detail,final_result,missed_points)
            create_solution_file(task_type,final_result,missed_points,file_detail)
      
    
     
