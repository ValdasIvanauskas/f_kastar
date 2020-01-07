import sys
sys.path.append('C:\\Python')

import u_grid
from node import Node
from opened import Opened

class KAStar:
    def __init__(self, grid, start, goals):
        """
        ===================================================================
         Description: KA* Algorithm.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start Idd).
            3. goals : set of int (Goal Idd).
        ===================================================================
        """  
        self.start = start
        self.goals = goals
        self._goals_active = set(goals)
        self._grid = grid
        self.nodes = dict()
        idds_valid = u_grid.get_valid_idds(grid)
        for idd in idds_valid:
            self.nodes[idd] = Node(idd)
        
        self._best = self.nodes[start]
        self._best.g = 0
        
        self._closed = set()                     
        self._opened = Opened()
        self._opened.push(self._best)   
        
        self.counter_heuristic = 0
        
        
        
        
    
    def run(self):
        """
        =======================================================================
         Description: Run A* Algorithm.
        =======================================================================
        """
        while (True):
            if (self._opened.is_empty()):
                self._best = None                
                return
            self._best = self._opened.pop()
            self._closed.add(self._best)
            if (self._best.idd in self._goals_active):
                self._goals_active.remove(self._best.idd)
                for node in self._opened._opened:
                    self._update_node(node,node.father,node.g,self._goals_active)
            
            if not self._goals_active:
                return
            self._expand()    
            
            
    def get_path(self, goal):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. goal : Node
        =======================================================================
         Return: List of Nodes.
        =======================================================================
        """            
        node = self.nodes[goal]
        path = [node.idd]
        while (node.idd != self.start):
            node = node.father
            path.append(node.idd)
        path.reverse()        
        return path
    
    
    def get_must_expanded_nodes(self):
        nodes = set()
        for goal in self.goals:
            path = set(self.get_path(goal))
            nodes.update(path)
        return len(nodes)
    
       
    def _expand(self):   
        """
        ===================================================================
         Description: Expand the Best Node's Children.
        ===================================================================
        """     
        row, col = u_grid.to_row_col(self._grid, self._best.idd)
        idds = u_grid.get_neighbors(self._grid, row, col)
        children = {self.nodes[x] for x in idds} - self._closed      
        for child in children:
            g_new = self._best.g + child.w
            if child.g <= g_new:
                continue
            if self._opened.contains(child):
                self._opened.remove(child)
            self._update_node(child,self._best,g_new,self._goals_active)
            self._opened.push(child)
            
            
    def _update_node(self, node, father, g, goals):
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
        h = float('Infinity')
        for goal in goals:
            h_cur = u_grid.manhattan_distance(self._grid,node.idd,goal)
            self.counter_heuristic += 1
            if (h_cur < h):
                h = h_cur
        node.h = h
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
        astar = KAStar(grid,start,{goal})
        astar.run()        
        closed_true = {Node(0),Node(4),Node(8),Node(12)}
        p1 = closed_true == astar._closed
        
        grid = u_grid.gen_symmetric_grid(4)        
        start = 0
        goals = {7,12}
        astar = KAStar(grid,start,goals)
        astar.run()        
        closed_true = {Node(0),Node(4),Node(8),Node(12),Node(5),Node(6),Node(7)}
        p2 = closed_true == astar._closed        
              
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
    def tester_get_path():
        grid = u_grid.gen_symmetric_grid(4)
        start = 0
        goal = 12
        astar = KAStar(grid,start,{goal})
        astar.run()
        optimal_path = [0,4,8,12]
        p1 = astar.get_path(goal) == optimal_path
        
        grid = u_grid.gen_symmetric_grid(4)
        grid[1][1] = -1
        grid[2][1] = -1
        start = 8
        goal = 10
        astar = KAStar(grid,start,{goal})
        astar.run()
        optimal_path = [8,12,13,14,10]
        p2 = astar.get_path(goal) == optimal_path
        
        p3 = True
        for i in range(1000):
            n = u_random.get_random_int(4,4)
            grid = u_grid.gen_symmetric_grid(n)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goals = idds_valid[1:3]
            kastar = KAStar(grid,start,goals)
            kastar.run()
            for goal in goals:
                len_optimal = u_grid.manhattan_distance(grid,start,goal)+1
                if len(kastar.get_path(goal)) != len_optimal:
                    p3 = False
                    print('start={0}'.format(start))
                    print('goal={0}'.format(goals))
                    print('grid:')
                    for row in range(grid.shape[0]):
                        li = list()
                        for col in range(grid.shape[1]):
                            li.append(grid[row][col])
                        li = [str(x) for x in li]
                        print(','.join(li))
                    print('goal[{0}]: {1}'.format(goal,kastar.get_path(goal)))            
        
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
  

"""
grid = u_grid.gen_symmetric_grid(10)
start = 40
goals = [48,34]
kastar = KAStar(grid, start, goals)
kastar.run()
print(kastar.get_path(48))
"""

