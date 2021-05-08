def _convert_tf(d, includes=[0]):
    assert d.keys() == [1,2,3,4]
    for key in d.keys():
        x = d[key]
        if not x in includes:
            d[key] = False
        else:
            d[key] = True
            
def _get_around(matrix, row, col):
    build = {1:None, 2:None, 3:None, 4:None}
    


def genColMask(*args, **kwargs):
	pass


#ding dong robot 2!
