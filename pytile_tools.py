import os
import copy

###################
# Matrix Tools
###################




def Matrix(what,h,l):
    row_build = []
    build = []
    for x in range(l):
        row_build.append(what)
    for i in range(h):
        build.append(copy.deepcopy(row_build))
    return build

def replace_mat_obj(mat, h, l, what):
    mat[h][l] = what
    #return mat
'''
v = fill_mat("cheese",3,3)
#v = mat_rect(v, 1, 0, 3, 0, 2)
print(v)
'''
def getrow(mat, row):
    return mat[row]

def getcol(mat,col):
    v = [x[col] for x in mat]
    return v


def subsection(matrix, firstrow, lastrow, firstcolumn, lastcolumn, includeLast=True):
    if not includeLast:
        inc = 0
    else:
        inc = 1
    t = [x[firstrow:lastrow+inc] for x in matrix[firstcolumn:lastcolumn+inc]]
    #print(t)
    return t

def longestItemInList(mat):
    top = 0
    for item in mat:
        if len(item) > top:
            top = len(item)
    return top

def matToList(mat):
    b = []
    for row in mat:
        b.extend(row)
    return b


######################
# File Tools
######################




class MatrixMissingAttributeError(Exception): pass


def load_tmap_mat(filetoopen, tmap):
    if filetoopen == '':
        return
    p = open(filetoopen, 'r').readlines()
    load = [x.strip() for x in p] #to get rid of \n on the end
    del p
    build = []
    hold = []
    for row in load[1:]:
        splitrow = row.split(",")
        hold = []
        for num in splitrow:
            if num == '':
                break
            #turn them in to ints
            hold.append(int(num))
        build.append(hold)
    if not load[0] == "!!!":
        h_l = load[0].split(",") #list of h and w
        tmap.height = int(h_l[0])
        tmap.width = int(h_l[1])
        #load.pop(0)
    else:
        tmap.width = len(build[0]) #very, very dangerous... matrix must be a rectangle or else the whole thing is going to crash and burn. At least I can fill it with NullTile()...
        tmap.height = len(build)
    tmap.mat = build
    return build

def save(matrix, filename, clearfile=True):
    if filename == '':
        return
    if clearfile:
        f_status = "w+"
    else:
        f_status = "a+"
    if filename == '':
        return
    fil = open(filename, f_status)
    fil.write('!!!\n')
    for row in matrix:
        #print(row)
        for thing in row:
            #print(thing)
            fil.write(str(thing) + ",")
        fil.write("\n")
                      

