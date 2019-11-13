from src.ArtGallery import *


'''
Not used this function anywhere in the application so please ignore
'''
def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return a_set & b_set
    else:
        return 0

