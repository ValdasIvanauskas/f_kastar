import random
import sys
sys.path.append('C:\\Python')

path_map = 'ost000a.map'

import u_grid
import u_lists

from astar_original import AStar
from kastar import KAStar

def check(lists):
    grid = u_grid.lists_to_grid(lists)
    grid = u_grid.gen_obstacles_grid(20,75)
    #grid = u_grid.gen_symmetric_grid(10)    
    idds = u_grid.get_valid_idds(grid)
    random.shuffle(idds)           
    start = idds[0]
    goals = idds[1:11]
    
    kastar = KAStar(grid, start, goals)
    kastar.run()    
    for goal in goals:
        astar = AStar(grid, start, goal)
        astar.run()
        if (len(astar.get_path()) != len(kastar.get_path(goal))):
            #print('{0} Ok'.format(goal))
        #else:
            #print('{0} Failed'.format(goal))
            print('start=[{0}]'.format(start))
            print('goal=[{0}]'.format(goal))
            for row in range(grid.shape[0]):
                li = list()
                for col in range(grid.shape[1]):
                    li.append(grid[row][col])
                li = [str(x) for x in li]
                print(','.join(li))
            print('goals={0}'.format(goals))
            print(astar.get_path())
            print(kastar.get_path(goal))
            return
        
lists = u_lists.to_lists_mask(path_map,'.')
print('Start')
for i in range(100):
    check(lists)
print('Finish')






