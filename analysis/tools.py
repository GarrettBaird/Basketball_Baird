
#%% Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pdfplumber
import re

#%% Functions
def int_convet(x:str):
    try:
        return int(x)
    except ValueError:
        return x
    
def merge_and_pop(lst:list):
    '''merges and pops the name'''
    lst[1] = lst[1] + ' ' + lst[2]
    lst.pop(2)
    return lst

def non_start(lst:list):
    '''fills in a value if the player didn't start'''
    if lst[2] != '*':
        lst = lst[:2] + ['-'] + lst[2:]
    return  lst

def get_opponent(raw_text:str):
    """
    The first line should hold something like
    'Southern Oregon (7-0, 1-0) -vs- College of Idaho (2-4, 0-1):'
    """
    line = raw_text.split('\n')[0]
    teams = line.split(' -vs- ')
    try:
        team1 = re.findall(r'(^.+)(?: \(\S+\s\S+)', teams[0])[0]
        team2 = re.findall(r'(^.+)(?: \(\S+\s\S+)', teams[1])[0]
    except IndexError:
         team1 = re.findall(r'(^.+) ', teams[0])[0]
         team2 = re.findall(r'(^.+) ', teams[1])[0]
    # Check if the first team is Southern Oregon
    if team1 == 'Southern Oregon':
            return team2
    return team1


