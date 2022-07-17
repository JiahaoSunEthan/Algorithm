# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:32:33 2022

@author: 13451
"""


import os

def string_generator(file):
    f = open(file,'r')
    string_1 = f.readline().strip()
    next_line = f.readline()
    while ord(next_line[0])>=48 and ord(next_line[0])<=57: #ASCII for 0-9
        slice_index = int(next_line.strip())
        if slice_index == len(string_1)-1:
            string_1 = string_1 + string_1
        else:
            string_1_left = string_1[:slice_index+1]
            string_1_right = string_1[slice_index+1:]
            string_1 = string_1_left + string_1 + string_1_right
        next_line = f.readline()
    
    string_2 = next_line.strip()
    next_line = f.readline()
    while len(next_line)>0: 
        slice_index = int(next_line.strip())
        if slice_index == len(string_2)-1:
            string_2 = string_2 + string_2
        else:
            string_2_left = string_2[:slice_index+1]
            string_2_right = string_2[slice_index+1:]
            string_2 = string_2_left + string_2 + string_2_right
        next_line = f.readline()
    return (string_1,string_2)

file_lst = os.listdir('datapoints')
res = dict()
#load file index and problem_size
for file in file_lst:
    if file.startswith('i'):
        file_number = int(file.split('.')[0][2:])
        string_pair = string_generator('datapoints/'+file)
        problem_size = len(string_pair[0])+len(string_pair[1])
        res[file_number] = [problem_size]

#load memory usage and excution time - basic
for file in file_lst:
    if file.startswith('o') and file.split('.')[0].endswith('b'):
        file_number = int(file.split('.')[0].split('_')[0][3:])
        f = open('datapoints/'+file,'r')
        content = f.readlines()
        time = float(content[3].strip())
        memory = float(content[4].strip())
        res[file_number].append(time)
        res[file_number].append(memory)
        