# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:12:18 2022

@author: 13451
"""


import sys
import time
import psutil

input_file = sys.argv[1]
output_file = sys.argv[2]

#hard-code for Delta and Alphas
alpha = {'A':{'C':110,'G':48,'T':94},'C':{'A':110,'G':118,'T':48},'G':{'A':48,'C':118,'T':110},'T':{'A':94,'C':48,'G':110}}
delta = 30


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

            
def alignment_dp(str1,str2):
    n,m = len(str1),len(str2)
    dp = [[0]*(m+1) for i in range(n+1)]
    #Initialize matrix
    for i in range(n+1):
        dp[i][0] = i * delta
    for j in range(m+1):
        dp[0][j] = j * delta
    
    for i in range(1,n+1):
        for j in range(1,m+1):
            temp_1 = alpha[str1[i-1]][str2[j-1]]+dp[i-1][j-1] if str1[i-1]!=str2[j-1] else dp[i-1][j-1]
            temp_2 = delta + dp[i-1][j]
            temp_3 = delta + dp[i][j-1]
            dp[i][j] = min(temp_1,temp_2,temp_3)
    
    backward_1,backward_2 =[],[]
    i,j = n,m
    while i!=0 and j!=0:
        temp_1 = alpha[str1[i-1]][str2[j-1]]+dp[i-1][j-1] if str1[i-1]!=str2[j-1] else dp[i-1][j-1]
        temp_2 = delta + dp[i-1][j]
        temp_3 = delta + dp[i][j-1]
        if dp[i][j] == temp_1:
            backward_1.append(str1[i-1])
            backward_2.append(str2[j-1])
            i -= 1
            j -= 1
        elif dp[i][j] == temp_2: #i consumed and j not consumed
            backward_1.append(str1[i-1])
            backward_2.append('_')
            i -= 1
        else:
            backward_1.append('_')
            backward_2.append(str2[j-1])
            j -= 1
    while i!=0:
        backward_1.append(str1[i-1])
        backward_2.append('_')
        i -= 1
    while j!=0:
        backward_1.append('_')
        backward_2.append(str2[j-1])
        j -= 1
        
    backward_1.reverse()
    backward_2.reverse()
    
    return (dp[n][m],''.join(backward_1),''.join(backward_2))

def output_res(file,res,str1,str2,time_execution,memory_usage):
    f = open(file,'w')
    f.write(str(res))
    f.write('\n')
    f.write(str1)
    f.write('\n')
    f.write(str2)
    f.write('\n')
    f.write(str(time_execution))
    f.write('\n')
    f.write(str(memory_usage))

#temp_res = alignment_dp(string_generator(input_file)[0], string_generator(input_file)[1])
#print(temp_res)

'''
def check_match(str1,str2):
    score = 0
    for i in range(len(str1)):
        if str1[i] == '_' or str2[i] == '_':
            score += delta
        else:
            if str1[i]!= str2[i]:
                score += alpha[str1[i]][str2[i]]
    return score
'''    

start_time = time.time()
string_pair = string_generator(input_file)
res = alignment_dp(string_pair[0],string_pair[1])
end_time = time.time()
time_taken = (end_time - start_time)*1000
process = psutil.Process()
memory_info = process.memory_info()
memory_consumed = int(memory_info.rss/1024)

output_res(output_file,res[0],res[1],res[2],time_taken,memory_consumed)

    