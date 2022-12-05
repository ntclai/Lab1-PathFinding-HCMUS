from map import Map
from collections import deque

#list chứa thông tin hướng đi
directions=['left','right','up','down']
#list chứa trọng số của các hướng đi
weight=[1,1,1,1]

def dfs(s,g,w,h,walls):
    opened=[[False] * w for _ in range(h)]
    cost_matrix=[[-1] * w for _ in range(h)]
    dir_matrix=[[-1] * w for _ in range(h)]
    stack=deque()

    #Thêm điểm bắt đầu (s) vào trong stack
    stack.append(s)

    #matrix
    opened[s[1]][s[0]]=True
    cost_matrix[s[1]][s[0]]=0

    while stack:
        point=stack.pop()

        #Dừng khi gặp điểm đích (goal)
        if(point[0]==g[0] and point[1]==g[1]):
            break

        #mở mọi nút kề với nút hiện tại
        for i in range(len(directions)):
            if directions[i]=='left':
                x=point[0]-1
                y=point[1]
            if directions[i]=='right':
                x=point[0]+1
                y=point[1]
            if directions[i]=='up':
                x=point[0]
                y=point[1]-1
            if directions[i]=='down':
                x=point[0]
                y=point[1]+1
            #kiểm tra tính hợp lệ của các nút vừa mở và cập nhật chi phí đường đi
            if x in range(w) and y in range(h) and not opened[y][x]:
                opened[y][x]=True
                if (x,y) not in walls:
                    cost_matrix[y][x]=weight[i]+cost_matrix[point[1]][point[0]]
                    dir_matrix[y][x]=i #0,1,2,3 (left, right, up, down)
                    stack.append((x,y))

    has_path=opened[g[1]][g[0]] # điểm đến goal (true/false)
    cost=-1

    if has_path: # nếu has_path =true, tức đã thăm tới điểm đến
        cost=cost_matrix[g[1]][g[0]]
    dirs=[]
    dirs.append(dir_matrix)
    return has_path, cost, dirs

