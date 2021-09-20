'''
公众号：一行玩python，关注领取5T编程资料
'''
#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import main
import cProfile


if __name__=='__main__':
    main()
    pg.quit()
    sys.exit()
