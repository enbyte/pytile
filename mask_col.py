import copy
from pprint import pprint

def _convert_tf(d, includes=[0]):
    for key in d.keys():
        x = d[key]
        if not x in includes:
            d[key] = False
        else:
            d[key] = True
            
    return d
def _get_around(matrix, row, col):
    
    build = {1:None, 2:None, 3:None, 4:None}
    
    WIDTH = len(matrix[0])
    HEIGHT = len(matrix)
    
    if not row == 0:
        build[1] = matrix[row - 1][col]
    if not row == HEIGHT - 1:
        build[4] = matrix[row + 1][col]
    if not col == 0:
        build[2] = matrix[row][col - 1]
    if not col == WIDTH - 1:
        build[3] = matrix[row][col + 1]
        
    return build


def genColMask(mat, edge_col_tiles=[0], ignore_tiles=[0]):
    build = copy.deepcopy(mat)
    access = copy.deepcopy(mat)
    hreps = 0
    lreps = 0
    for row in access:
        for item in row:
                #print(hreps, lreps)
                if not item in ignore_tiles: #don't run it on air or whatever
                    around = _get_around(access, hreps, lreps)
                    #print("Around: " + str(around))
                    tf = _convert_tf(around, includes=edge_col_tiles)
                    build[hreps][lreps] = tf
                    #print("TF: " + str(tf))
                    #print(tf, hreps, lreps)
                else:
                    build[hreps][lreps] = {1: False, 2: False, 3: False, 4: False}
                lreps += 1
        lreps = 0
        hreps += 1
    return build

if __name__ == '__main__':
    mat = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 1]
        ]
    a = genColMask(mat)
    
    for row in a:
        print(row)
