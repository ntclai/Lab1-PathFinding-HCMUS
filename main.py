from algorithms.algo1 import algo1
from map import Map
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.greedy_bfs import gbfs
from algorithms.a_star import a_star
from algorithms.algo1 import algo1
import pygame
import os

level=['level_2']
input_path='../input/'
inputs=[]
for l in level:
    files=os.listdir(input_path+l+'/')
    if len(files)>0:
        for file in files:
            inputs.append(input_path+l+'/'+file)


for i in inputs:
    if 'level_1' in i:
        for j in range(0,9):
            pygame.init()

            #define font text
            font = pygame.font.SysFont('Futura', 40)
            m=Map(font)
            m.load(i)
            out_path='../output'+i[8:-4]+'/'
            if j==0:
                has_path,cost,dirs=bfs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls)
                index,algo,heuristic=int(i[-5]),'bfs',''
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo,heuristic)
            if j==1:
                has_path,cost,dirs=dfs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls)
                index,algo,heuristic=int(i[-5]),'dfs',''
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo,heuristic)
            if j==2:
                has_path,cost,dirs,_=ucs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls)
                index,algo,heuristic=int(i[-5]),'ucs',''
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo,heuristic)
            if j==3:
                has_path,cost,dirs=gbfs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,1)
                index,algo,heuristic=int(i[-5]),'gbfs:heuristic:ManhattanDistance','_heuristic_1'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:4],heuristic)
            if j==4:
                has_path,cost,dirs=gbfs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,2)
                index,algo,heuristic=int(i[-5]),'gbfs:heuristic:EuclideanDistance','_heuristic_2'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:4],heuristic)
            if j==5:
                has_path,cost,dirs=gbfs(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,3)
                index,algo,heuristic=int(i[-5]),'gbfs:heuristic:BreakingTie','_heuristic_3'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:4],heuristic)
            if j==6:
                has_path,cost,dirs,_=a_star(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,1)
                index,algo,heuristic=int(i[-5]),'a_star:heuristic:ManhattanDistance','_heuristic_1'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:6],heuristic)
            if j==7:
                has_path,cost,dirs,_=a_star(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,2)
                index,algo,heuristic=int(i[-5]),'a_star:heuristic:EuclideanDistance','_heuristic_2'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:6],heuristic)
            if j==8:
                has_path,cost,dirs,_=a_star(m.S,m.G,m.WIDTH,m.HEIGHT,m.walls,3)
                index,algo,heuristic=int(i[-5]),'a_star:heuristic:BreakingTie','_heuristic_3'
                m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo[0:6],heuristic)
            pygame.quit()
    if 'level_2' in i:
        pygame.init()
        font = pygame.font.SysFont('Futura', 40)
        m=Map(font)
        m.load(i)
        out_path='../output'+i[8:-4]+'/'
        has_path,cost,dirs=algo1(m.S,m.G,m.bonus,m.bonus_vals,m.WIDTH,m.HEIGHT,m.walls)
        index,algo,heuristic=int(i[-5]),'algo1',''
        m.run(has_path,cost,dirs,pygame,index,algo,out_path+algo,heuristic)
        pygame.quit()