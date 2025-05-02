
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
    '''
    merges and pops the name
    '''
    if ',' in lst[1]:

        last, first = lst[1].split(',')
        last, first = last.strip(), first.strip()
        last, first = last.lower(), first.lower()
        lst[1] = first.capitalize() + ' ' + last.capitalize()
    else:
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

def folder_to_list(folder_path:str):

    folder = os.listdir(folder_path)
    folder.remove('.DS_Store')
    files = []
    for file in folder:
        files.append(folder_path + '/' + file)
    
    return files

def folder_to_dict(folder_path:str, test:bool = False) -> dict:
    '''
    Converts the pdf files to a csv file as long as it follows the same format as the example files.
    By product is printing the name of the players. Will fix later for now its a "Quirk".
    '''
    if test:
        folder = [folder_path]
    else:
        folder = folder_to_list(folder_path)

    i = 0 # used to track the number of files

    for file in folder:
        #print(i, file)
        with pdfplumber.open(file, pages= [1]) as pdf:
            
            # Extract text from each page
            text = ""
            for page in pdf.pages:
                text += page.extract_text();


        matches = re.findall(r'Southern Oregon \d+..(#[\s\S]+?..TM T)', text, re.DOTALL)
        matches[0] = matches[0].replace(', ', ',')

        matches_date = re.findall(r'Date: \s*(........)', text)

        stats = matches[0]
        stats = stats.strip().split(sep = '\n')
        split_stats = list(map(str.split, stats))

        opponent = get_opponent(text)
        title = split_stats[0] + ['Opponent'] + ['Date']

        players = split_stats[1:-1]
        #ISSUE HERE

        players = list(map(merge_and_pop, players))
        players = list(map(non_start, players))
        #ISSUE HERE
        if i == 0:
            stat_dict = {key: [] for key in title}

        for player in players:

            for stat, data in zip(title, player):
                stat_dict[stat].append(data)
            # stat_dict['Opponent'].append(opponent)#new
            # stat_dict['Date'].append(matches_date[0])#new
        for name in split_stats[1:-1]:
            stat_dict['Opponent'].append(opponent)
            stat_dict['Date'].append(matches_date[0])
 
        if len(stat_dict['PTS']) != len(stat_dict['Player'] or test == True):
            print(matches_date, 'Length of PTS and Player do not match')
            #return
        i += 1

    return (stat_dict)

# %%
