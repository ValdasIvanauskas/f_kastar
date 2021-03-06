import sys
sys.path.append('g:\\python modules\f_grid')

import u_grid
from node import Node
from opened import Opened

class AStar:
    def __init__(self, grid, start, goal):
        """
        ===================================================================
         Description: A* Algorithm.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start Idd).
            3. goals : set of int (Goal Idd).
        ===================================================================
        """  
        self.start = start
        self.goal = goal
        self.grid = grid
        
        self.best = Node(start)
        self.best.g = 0
        
        self.closed = set()                     
        self.opened = Opened()
        self.opened.push(self.best)   
        
    
    def run(self):
        """
        =======================================================================
         Description: Run A* Algorithm.
        =======================================================================
        """
        while (True):
            if (self.opened.is_empty()):
                self.best = None
                return
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if (self.best.idd == self.goal):
                return
           
            self._expand()    
            
            
    def get_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: List of Nodes.
        =======================================================================
        """
        node = self.best
        path = [node.idd]
        while (node.idd != self.start):
            node = node.father
            path.append(node.idd)
        path.reverse()
        return path
            
        
       
    def _expand(self):   
        """
        ===================================================================
         Description: Expand the Best Node's Children.
        ===================================================================
        """     
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            if self.opened.contains(child):
                self.opened.remove(child)
            self._update_node(child,self.best,g_new)
            self.opened.push(child)
            
            
    def _update_node(self, node, father, g):
        """
        =======================================================================
         Description: Update Node.
        =======================================================================
         Attributes:
        -----------------------------------------------------------------------
            1. node : Node (node to update)
            2. father : Node
            3. g : int
            4. goals : set of int (active goals)
        =======================================================================
        """
        node.father = father
        node.g = g
        h = u_grid.manhattan_distance(self.grid,node.idd,self.goal)
        node.f = node.g + h        

    
"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    import random
    import u_random
    
    def tester_run():         
        grid = u_grid.gen_symmetric_grid(4)        
        start = 0
        goal = 12
        astar = AStar(grid,start,goal)        
        astar.run()
        closed_true = {Node(0),Node(4),Node(8),Node(12)}
        p1 = closed_true == astar.closed     
        
        grid = u_grid.gen_symmetric_grid(4)
        grid[0][2] = -1
        grid[1][2] = -1
        start = 0
        goal = 3       
        astar = AStar(grid,start,goal)
        astar.run()
        closed_true = {Node(0),Node(1),Node(3),Node(4),Node(5),Node(7),Node(9),Node(10),Node(11)}          
        p2 = closed_true == astar.closed
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))            
            
    def tester_get_path():
        grid = u_grid.gen_symmetric_grid(4)
        start = 0
        goal = 12
        astar = AStar(grid,start,goal)
        astar.run()
        optimal_path = [0,4,8,12]
        p1 = astar.get_path() == optimal_path
        
        grid = u_grid.gen_symmetric_grid(4)
        grid[1][1] = -1
        grid[2][1] = -1
        start = 8
        goal = 10
        astar = AStar(grid,start,goal)
        astar.run()
        optimal_path = [8,12,13,14,10]
        p2 = astar.get_path() == optimal_path
        
        p3 = True
        for i in range(1000):
            n = u_random.get_random_int(3,10)
            grid = u_grid.gen_symmetric_grid(n)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goal = idds_valid[1]
            astar = AStar(grid,start,goal)
            astar.run()
            len_optimal = u_grid.manhattan_distance(grid,start,goal)+1
            if len(astar.get_path()) != len_optimal:
                p3 = False
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
    
    print('\n====================\nStart Tester\n====================')    
    tester_run()
    tester_get_path()
    print('====================\nEnd Tester\n====================')        
    
    
tester()
    
