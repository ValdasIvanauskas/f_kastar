import random
import numpy as np
import u_lists
import math


def gen_symmetric_grid(n):
    """
    ===========================================================================
     Description: Return Serialized Symmetric Grid in shape of NxN.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. n : int (Shape of the Grid NxN).
    ===========================================================================
     Return: Serialized Symmetric Grid.
    ===========================================================================
    """
    grid = np.ones([n,n], dtype=int)
    return serialize(grid)   


def gen_obstacles_grid(n,p):
    """
    ===========================================================================
     Description:
    ---------------------------------------------------------------------------
        Return Symmetric Grid in Shape of NxN with p percent of obstacles.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. n : int (Shape of the Grid NxN).
        2. p : int (Percent of Obstacles in the Grid, from 0 to 100).
    ===========================================================================
     Return: Serialized Symmetric Grid.
    ===========================================================================
    """
    grid = gen_symmetric_grid(n)
    grid = serialize(grid)
    if (p == 0): return grid
    amount_idds = n*n
    amount_obstacles = int(amount_idds // (100 / p))
    idds = list(range(amount_idds))
    random.shuffle(idds)
    obstacles = idds[:amount_obstacles]
    for obstacle in obstacles:
        row, col = to_row_col(grid, obstacle)
        grid[row][col] = -1
    return grid
    

def gen_dict_weights(n):
    """
    ===========================================================================
     Description: Return Dictionary of Weights.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. n : int (Size of the Dict and Maximum Range of Weight).
    ===========================================================================
    """
    dict_w = dict()
    for i in range(n):
        dict_w[i] = random.randint(1,n)
    return dict_w
    

def get_center(grid):
    """
    ===========================================================================
     Description: Return Idd of Grid's Center.
    ===========================================================================
     Arguments: 
    ---------------------------------------------------------------------------
        1. grid : Serialized Grid.
    ===========================================================================
     Return: Idd : int (Center Node's Id).
    ===========================================================================
    """
    row = math.floor(grid.shape[0] / 2)
    col = math.floor(grid.shape[1] / 2)
    idd = to_idd(grid, row, col)
    x = 0
    while (idd == -1):
        x += 1
        idd = to_idd(grid, row-x, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row-x, col)
        if (idd >= 0): break
        idd = to_idd(grid, row-x, col+x)
        if (idd >= 0): break
        idd = to_idd(grid, row, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row, col+x)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col+x)           
    return idd
    
    
def lists_to_grid(lists):
    """
    ===========================================================================
     Description: Convert List of Lists to Binary Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. lists : List of Lists
    ===========================================================================
     Return: Binary Grid - 2D Arranged Numpy Array of [0,-1] 
    ===========================================================================
    """
    rows, cols = u_lists.count_rows_cols(lists)    
    
    grid = np.full(shape=[rows,cols], fill_value=-1, dtype=int)

    for row in range(rows):
        for col in range(len(lists[row])):
            grid[row][col] = lists[row][col]
        
    return grid


def to_row_col(grid, idd):
    """
    ===========================================================================
     Description: Return Row and Col indexes of the Idd.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : 2D Serialized Numpy Array.
        2. idd : int (Node's Id).
    ===========================================================================
     Return: row, col : int, int
    ===========================================================================
    """
    row = idd // grid.shape[1]
    col = idd % grid.shape[1]
    return row, col


def to_idd(grid, row, col):
    """
    ===========================================================================
     Description: Return Node's Id by Row and Col combination.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : 2D Serialized Numpy Array.
        2. row : int
        3. col : int
    ===========================================================================
     Return: idd : int (Node's Id).
    ===========================================================================
    """
    if is_valid_row_col(grid, row, col):
        return row*grid.shape[1] + col
    else:
        return -1


def is_valid_row_col(grid, row, col, by_idd=True):
    """
    ===========================================================================
     Description: Return True if Row and Col are in the Shapes of Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. row : int
        3. col : int
        4. by_idd : bool 
    ===========================================================================
     Return: True if Row and Col are in the Shapes of Grid.
    ===========================================================================
    """
    if (row<0) or (col<0) or (row>=grid.shape[0]) or (col>=grid.shape[1]):
        return False
    if (by_idd and (grid[row][col] == -1)):
        return False
    return True


def is_valid_idd(grid, idd):
    """
    ===========================================================================
     Description: Return True if Idd is valid.
    ---------------------------------------------------------------------------
     Validation is by:
         1. Location in the Shapes of the Grid.
         2. Positive Idd in the Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. idd : int (Node's Id)
    ===========================================================================
     Return: True if Idd is valid.
    ===========================================================================
    """
    row, col = to_row_col(grid, idd)
    return is_valid_row_col(grid, row, col)


def get_valid_idds(grid):
    """
    ===========================================================================
     Description: Return List of Valid Idd in the Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
    ===========================================================================
     Return: List of Valid Idd (int).
    ===========================================================================
    """
    valid_idds = []
    for idd in np.nditer(grid):
        if is_valid_idd(grid, idd):
            valid_idds.append(int(idd))
    return valid_idds            
    
    
def get_neighbors(grid, row, col):
    """
    ===========================================================================
     Description: Return List of Valid Neighbors (int).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Numpy 2D Array.
        2. row : int
        3. col : int
    ===========================================================================
     Return: List of Valid Neighbors (list of int).
    ===========================================================================
    """
    def add_neighbor(row, col):
        idd = to_idd(grid, row, col)
        if grid[row][col] >= 0:
            neighbors.append(idd)
        
    neighbors = list()
    
    if (row > 0):
        add_neighbor(row-1, col)
    if (col < grid.shape[1]-1):
        add_neighbor(row, col+1)
    if (row < grid.shape[0]-1):
        add_neighbor(row+1, col)
    if (col > 0):
        add_neighbor(row, col-1)
    
    return neighbors        


def to_course(grid, idd_1, idd_2):
    """
    ===========================================================================
     Description: Return the course from Idd_1 to Idd_2.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Canonized Grid.
        2. idd_1 : int (Node's Id).
        3. idd_2 : int (Node's Id).
    ===========================================================================
     Return: str (Course) {'UP','RIGHT','DOWN','LEFT'}
    ===========================================================================
    """
    row_1, col_1 = to_row_col(grid, idd_1)
    row_2, col_2 = to_row_col(grid, idd_2)
        
    if (col_1 == col_2):
        if (row_1 == row_2+1):
            return 'UP'
        if (row_1 == row_2-1):
            return 'DOWN'
    elif (row_1 == row_2):
        if (col_1 == col_2+1):
            return 'LEFT'
        if (col_1 == col_2-1):
            return 'RIGHT'        
    return 'ERROR'
        

def to_next_idd(grid, idd, course):
    """
    ===========================================================================
     Description: Return the Idd of the Next Node (by Course).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idd : int (Node's Id).
        3. course : str {'UP','RIGHT','DOWN','LEFT'}.
    ===========================================================================
     Return: int (Next Node's Id).
    ===========================================================================
    """
    row, col = to_row_col(grid, idd)
    if course == 'UP':
        row -= 1
    elif course == 'DOWN':
        row += 1
    elif course == 'LEFT':
        col -= 1
    elif course == 'RIGHT':
        col += 1
    else:
        return -1
    return to_idd(grid, row, col)    
        

def remove_deadlocks(grid):
    """
    ===========================================================================
     Description: Remove Deadlocks from the Grid (Nodes without Neighbors).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid with [-1] as Block.
    ===========================================================================
     Return: 2D Binary Numpy Array without Deadlocks.
    ===========================================================================
    """
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] >= 0:
                if not get_neighbors(grid, row, col):
                    grid[row][col] = -1
    return grid
    

def remove_empty_rows(grid):
    """
    ===========================================================================
     Desription: Remove Empty Rows from Grid (Empty = -1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid to be changed.
    ===========================================================================
    """
    return grid[~np.all(grid == -1, axis=1)]   
    
    
def remove_empty_cols(grid):
    """
    ===========================================================================
     Desription: Remove Empty Cols from Grid (Empty = -1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid to be changed.
    ===========================================================================
    """
    grid = grid.transpose()
    grid = remove_empty_rows(grid)
    return grid.transpose()
    
    
def serialize(grid):
    """
    ===========================================================================
     Description: Convert Grid [with -1] to Serialized Grid [0,1,-1,3].
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid with [-1] as Block.
    ===========================================================================
     Return: Serialized Numpy 2D Array.
    ===========================================================================
    """
    counter = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] >= 0:
                grid[row][col] = counter
            else:
                grid[row][col] = -1
            counter += 1
    return grid


def canonize(grid):
    """
    ===========================================================================
     Description: Canonize Binary Grid [0,1] to Serialized [0,1,2,-1,4].
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Binary Grid [0,1].
    ===========================================================================
     Return: Canonized 2D Grid.
    ===========================================================================
    """
    grid = remove_deadlocks(grid)
    grid = remove_empty_rows(grid)
    grid = remove_empty_cols(grid)
    return serialize(grid)


def xor(grid_1, grid_2):
    """
    ===========================================================================
     Description: Return Grid with differences (represented by 1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid_1 : Grid.
        2. grid_2 : Grid.
    ===========================================================================
     Return: Grid.
    ===========================================================================
    """
    return np.array(~(grid_1 == grid_2), dtype=int)


def manhattan_distance(grid, idd_1, idd_2):
    """
    ===========================================================================
     Description: Return Manhattan Distance between 2 Nodes.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. idd_1 : int (Node's Id)
        3. idd_2 : int (Node's Id)
    ===========================================================================
    """
    row_1, col_1 = to_row_col(grid, idd_1)
    row_2, col_2 = to_row_col(grid, idd_2)
    
    return abs(row_1 - row_2) + abs(col_1 - col_2)


def get_dic_h(grid, goal, lookup=dict(), with_pathmax=False):
    """
    ===========================================================================
     Description: Return a Dictionary of Nodes of the Grid with their
                     Manhattan Distance to the Goal.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. goal : Node 
        3. lookup : dict int:int (Node.idd : accurate distance).
    ===========================================================================
     Return: dict int:(int,bool) (Node.idd : (h,is_lookup).
    ===========================================================================
    """        
    row_goal, col_goal = to_row_col(grid, goal)
    dic = dict()
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            idd = to_idd(grid,row,col)
            if not is_valid_idd(grid, idd): continue
            if (idd in lookup):
                dic[idd] = (lookup[idd],True)
            else:
                h = abs(row_goal - row) + abs(col_goal - col)
                dic[idd] = (h,False)
                
    if not with_pathmax: return dic
    
    """
    rebels = set()
    for idd in lookup:
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
    pathmaxed_nodes = len(lookup)
    while rebels:
        idd = rebels.pop()
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:           
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
        pathmaxed_nodes += 1                                
    """
    
    rebels = set()
    for idd in lookup:
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
    pathmaxed_nodes = len(lookup)
    for i in range(19):
        rebels_temp = rebels.copy()
        rebels.clear()
        for idd in rebels_temp:
            row, col = to_row_col(grid, idd)
            neighbors = get_neighbors(grid, row, col)
            for neighbor in neighbors:
                if dic[neighbor][0] < dic[idd][0]-1:
                    dic[neighbor] = (dic[idd][0]-1,False)
                    rebels.add(neighbor)
        pathmaxed_nodes += len(rebels_temp)   
        
    return dic, pathmaxed_nodes               


def to_csv(grid, fr, lr, fc, lc, path):
    """
    ===========================================================================
     Description: Write Sub-Grid to CSV File.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. fr : int (First Row)
        3. lr : int (Last Row)
        4. fc : int (First Column)
        5. lc : int (Last Column)
        6. path : str (Path of CSV File)
    ===========================================================================
    """
    file = open(path, 'w')
    file.write(',')
    for col in range(fc,lc+1):
        file.write('{0},'.format(col))
    file.write('\n')
    for row in range(fr,lr+1):
        file.write('{0},'.format(row))
        for col in range(fc,lc+1):
            file.write('{0},'.format(grid[row][col]))
        file.write('\n')
    file.close()
        


"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    
    def tester_gen_symmetric_grid():
        grid = gen_symmetric_grid(2)        
        grid_true = np.array([[0,1],[2,3]])
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_gen_obstacles_grid():
        n = 10
        p = 1
        grid = gen_obstacles_grid(n,p)
        len_obstacles_true = n*n // (100/p)
        p1 = n*n - len(get_valid_idds(grid)) == len_obstacles_true
          
        fname = sys._getframe().f_code.co_name[7:]
        if (p1):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
    
    def tester_gen_dict_weights():
        n = 4
        dict_w = gen_dict_weights(n)
        
        p1 = len(dict_w) == n
        
        p2 = True
        for w in dict_w.values():
            if (w < 1) or (w > n):
                p2 = False
                
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))         
            
            
    def tester_get_center():
        grid = gen_symmetric_grid(4)
        center = get_center(grid)               
        p1 = center == 10
        
        grid = gen_symmetric_grid(3)
        center = get_center(grid)   
        p2 = center == 4  

        grid = gen_symmetric_grid(5)
        grid[2][2] = -1
        grid[1][1] = -1
        center = get_center(grid)             
        p3 = center == 7
                
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname)) 
        
        
    def tester_lists_to_grid():
        li_1 = [1,2]
        li_2 = [1,2,3,4]
        li_3 = [1]
        li_4 = [1,2,3]        
        lists = [li_1, li_2, li_3, li_4]        
        grid = lists_to_grid(lists)
        
        grid_true = np.array([[1,2,-1,-1],[1,2,3,4],[1,-1,-1,-1],[1,2,3,-1]], dtype=int)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            

    def tester_to_row_col():
        li_1 = [0,1,2]
        li_2 = [3,4,5]
        lists = [li_1, li_2]
        grid = np.array(lists)
        
        p1 = to_row_col(grid,0) == (0,0)
        p2 = to_row_col(grid,1) == (0,1)
        p3 = to_row_col(grid,2) == (0,2)
        p4 = to_row_col(grid,3) == (1,0)
        p5 = to_row_col(grid,4) == (1,1)    
        p6 = to_row_col(grid,5) == (1,2) 
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4 and p5 and p6):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_to_idd():
        li_1 = [-1, 1, 2]
        li_2 = [ 3, 4, 5]
        lists = [li_1, li_2]
        grid = np.array(lists)
        
        p1 = (to_idd(grid,0,2) == 2)
        p2 = (to_idd(grid,1,0) == 3)
        p3 = (to_idd(grid,1,1) == 4)
        p4 = (to_idd(grid,3,4) == -1)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_is_valid_row_col():
        li_1 = [0,-1]
        li_2 = [2,3]
        lists = [li_1, li_2]
        grid = np.array(lists)
        
        p1 = is_valid_row_col(grid,1,0) == True
        p2 = is_valid_row_col(grid,2,-1) == False
        p3 = is_valid_row_col(grid,3,4) == False       
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_is_valid_idd():
        li_1 = [0,-1]
        li_2 = [2,3]
        lists = [li_1, li_2]
        grid = np.array(lists)
        
        p1 = is_valid_idd(grid,0) == True
        p2 = is_valid_idd(grid,1) == False
        p3 = is_valid_idd(grid,4) == False       
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
    
    
    def tester_get_valid_idds():
        li_1 = [0,-1]
        li_2 = [2,3]
        lists = [li_1, li_2]
        grid = np.array(lists)        
        valid_idds = get_valid_idds(grid)
        
        valid_idds_true = [0,2,3]
        
        fname = sys._getframe().f_code.co_name[7:]
        if (valid_idds == valid_idds_true):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
        
    

    def tester_get_neighbors():
        li_1 = [-1,  1, -1]
        li_2 = [ 3,  4,  5]
        li_3 = [-1,  7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)
        
        p1 = (get_neighbors(grid,2,2) == [5,7])
        p2 = (get_neighbors(grid,0,1) == [4])    
        p3 = (get_neighbors(grid,1,1) == [1,5,7,3])
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_to_course():
        li_1 = [-1,  1, -1]
        li_2 = [ 3,  4,  5]
        li_3 = [-1,  7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)
        
        p1 = (to_course(grid,1,4) == 'DOWN')
        p2 = (to_course(grid,4,1) == 'UP')
        p3 = (to_course(grid,3,4) == 'RIGHT')
        p4 = (to_course(grid,5,4) == 'LEFT')
        p5 = (to_course(grid,4,7) == 'DOWN')
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4 and p5):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_to_next_idd():
        li_1 = [-1,  1, -1]
        li_2 = [ 3,  4,  5]
        li_3 = [-1,  7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)
        
        p1 = (to_next_idd(grid,1,'DOWN') == 4)
        p2 = (to_next_idd(grid,4,'UP') == 1)
        p3 = (to_next_idd(grid,4,'RIGHT') == 5)
        p4 = (to_next_idd(grid,4,'LEFT') == 3)
        p5 = (to_next_idd(grid,1,'RIGHT') == -1)
        p6 = (to_next_idd(grid,5,'RIGHT') == -1)
        p7 = (to_next_idd(grid,4,'BLOCK') == -1)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4 and p5 and p6 and p7):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            

    def tester_remove_deadlocks():
        li_1 = [ 2,-1,-1]
        li_2 = [-1, 2, 2]
        lists = [li_1, li_2]
        grid = np.array(lists)
        grid = remove_deadlocks(grid)
        
        li_1 = [-1,-1,-1]
        li_2 = [-1, 2, 2]
        lists = [li_1, li_2]
        grid_true = np.array(lists)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_remove_empty_rows():
        li_1 = [-1,-1,-1]
        li_2 = [ 2, 2, 2]
        li_3 = [-1,-1,-1]
        li_4 = [ 2, 2, 2]
        li_5 = [-1,-1,-1]        
        lists = [li_1, li_2, li_3, li_4, li_5]    
        grid = np.array(lists)  
        grid = remove_empty_rows(grid)        
        
        grid_true = np.array([[2,2,2],[2,2,2]], dtype=int)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_remove_empty_cols():
        li_1 = [-1, 2,-1, 2,-1]
        li_2 = [-1, 2,-1, 2,-1]
        
        lists = [li_1, li_2]
        
        grid = np.array(lists)    
        grid = remove_empty_cols(grid)    
        
        grid_true = np.array([[2,2],[2,2]], dtype=int)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_serialize():
        """
        ===========================================================================
         Description: Tester for serialize(grid).
        ===========================================================================
        """
        li_1 = [-1,-1,-1,-1]
        li_2 = [-1, 1, 1,-1]
        li_3 = [-1,-1,-1,-1]    
        lists = [li_1, li_2, li_3]    
        grid = np.array(lists)   
        grid = serialize(grid)
        
        li_1 = [-1, -1, -1, -1]
        li_2 = [-1,  5,  6, -1]
        li_3 = [-1, -1, -1, -1]
        lists = [li_1, li_2, li_3]
        grid_true = np.array(lists)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))


    def tester_canonize():
        li_1 = [-1,-1,-1,-1,-1]
        li_2 = [-1, 1, 1,-1, 1]
        li_3 = [-1,-1,-1, 1,-1]
        li_4 = [-1, 1, 1,-1,-1]
        li_5 = [-1, 1,-1, 1,-1]
        lists = [li_1, li_2, li_3, li_4, li_5]
        grid = np.array(lists)
        grid = canonize(grid)
        
        li_1 = [0,1]
        li_2 = [2,3]
        li_3 = [4,-1]
        lists = [li_1, li_2, li_3]
        grid_true = np.array(lists)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
    
    
    def tester_xor():
        li_11 = [1,2]
        li_12 = [3,4]
        lists_1 = [li_11, li_12]
        grid_1 = lists_to_grid(lists_1)
        
        li_21 = [0,2]
        li_22 = [3,5]
        lists_2 = [li_21, li_22]
        grid_2 = lists_to_grid(lists_2)
        
        li_31 = [1,0]
        li_32 = [0,1]
        lists_true = [li_31, li_32]
        grid_true = lists_to_grid(lists_true)        
        
        fname = sys._getframe().f_code.co_name[7:]
        if (xor(grid_1, grid_2) == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
            
    def tester_manhattan_distance():
        li_0 = [0,1,2]
        li_1 = [3,4,5]
        lists = [li_0, li_1]
        grid = lists_to_grid(lists)
        
        p1 = manhattan_distance(grid, 1, 1) == 0
        p2 = manhattan_distance(grid, 4, 5) == 1
        p3 = manhattan_distance(grid, 3, 1) == 2        
        p4 = manhattan_distance(grid, 2, 3) == 3
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_get_dic_h():
        li_0 = [0,1,2]
        li_1 = [3,4,5]
        lists = [li_0, li_1]
        grid = lists_to_grid(lists)
        lookup = {4:5}
        dic_h = get_dic_h(grid,5,lookup)
        
        dic_h_true = dict()
        dic_h_true[0] = (3,False)
        dic_h_true[1] = (2,False)
        dic_h_true[2] = (1,False)
        dic_h_true[3] = (2,False)
        dic_h_true[4] = (5,True)
        dic_h_true[5] = (0,False)
        
        p1 = dic_h == dic_h_true
        
        grid = gen_symmetric_grid(5)
        grid[1][3] = -1
        grid[2][3] = -1
        grid[3][3] = -1
        grid[4][3] = -1
        lookup = dict()
        lookup[2] = 6
        lookup[7] = 7
        lookup[12] = 8
        lookup[17] = 9
        lookup[22] = 10
        dic_h, pathmax_nodes = get_dic_h(grid,24,lookup,True)
        
        dic_h_true = dict()
        dic_h_true[0] = (8,False)
        dic_h_true[1] = (7,False)
        dic_h_true[2] = (6,True)
        dic_h_true[3] = (5,False)
        dic_h_true[4] = (4,False)
        dic_h_true[5] = (7,False)
        dic_h_true[6] = (6,False)
        dic_h_true[7] = (7,True)
        dic_h_true[9] = (3,False)
        dic_h_true[10] = (6,False)
        dic_h_true[11] = (7,False)
        dic_h_true[12] = (8,True)
        dic_h_true[14] = (2,False)
        dic_h_true[15] = (7,False)
        dic_h_true[16] = (8,False)
        dic_h_true[17] = (9 ,True)
        dic_h_true[19] = (1,False)
        dic_h_true[20] = (8,False)
        dic_h_true[21] = (9,False)
        dic_h_true[22] = (10,True)
        dic_h_true[24] = (0,False)
        
        p2 = dic_h == dic_h_true
        
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
            
    def tester_to_csv():
        path = 'C:\\Temp\\to_csv.csv'
        grid = gen_symmetric_grid(5)
        sub_grid = grid[1:4,1:4]
        to_csv(grid,1,3,1,3,path)
        
        grid_true = np.zeros((4,4),dtype=int)
        
        file = open(path,'r')
        for row, line in enumerate(file):
            vals = line.split(',')
            for col, val in enumerate(vals):
                if (val.isdigit()):
                    grid_true[row][col] = val
        grid_true = grid_true[1:,1:]
       
        fname = sys._getframe().f_code.co_name[7:]
        if (sub_grid == grid_true).all():
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
        
    
    
    print('\n====================\nStart Tester\n====================')    
    tester_gen_symmetric_grid()
    tester_gen_obstacles_grid()
    tester_gen_dict_weights()
    tester_get_center()
    tester_lists_to_grid()
    tester_to_row_col()
    tester_to_idd()
    tester_is_valid_row_col()
    tester_is_valid_idd()
    tester_get_valid_idds()
    tester_get_neighbors()
    tester_to_course()
    tester_to_next_idd()
    tester_remove_deadlocks()
    tester_remove_empty_rows()
    tester_remove_empty_cols()
    tester_serialize()
    tester_canonize()
    tester_xor()
    tester_manhattan_distance()
    tester_get_dic_h()
    #tester_to_csv()
    print('====================\nEnd Tester\n====================')
    
    
#tester()
    
grid = gen_symmetric_grid(5)
grid

