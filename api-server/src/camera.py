import bdb
from contextlib import nullcontext
import math
from re import A
from matplotlib.cbook import print_cycles
import numpy as np


def angle(left_shoulder,left_hip,count):
    price = False

    waist = left_hip
    after_neck = left_shoulder
    
    vec1 = [1-waist.x,0-waist.y]
    vec2 = [after_neck.x-waist.x,after_neck.y-waist.y]
    absvec1=np.linalg.norm(vec1)
    absvec2=np.linalg.norm(vec2)
    inner=np.inner(vec1,vec2)
    cos_theta=inner/(absvec1*absvec2)
    theta=math.degrees(math.acos(cos_theta))
    game_count =count_angle(price,count,theta)
    print(count)
    print('angle='+str(round(theta,2))+'deg')

    return game_count

def count_angle(price,count,theta):

    if theta >= 60 and price == False:
        #game_count +=1
        price = True
    elif theta < 10 and price == True:
        price = False
    return count
