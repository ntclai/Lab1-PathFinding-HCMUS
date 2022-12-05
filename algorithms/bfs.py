from map import Map
from collections import deque
#sử dụng deque thay vì queue do độ phức tạp về mặt thởi gian
#khi tính toán của deque là O(1).

#khởi tạo list chứa các hướng di chuyển.
directions=['left','right','up','down']
#chi phí cho các hướng di chuyển.
weight   = [1, 1, 1, 1]

def bfs(s, g, w, h, walls):
    opened = [[False] * w for _ in range(h)]
    cost_matrix = [[-1] * w for _ in range(h)]
    dir_matrix = [[-1] * w for _ in range(h)]
    q = deque()
    
    #thêm điểm bất đầu vào hàng đợi.
    q.append(s)

    opened[s[1]][s[0]]=True #điểm bắt đầu luôn được mở.
    cost_matrix[s[1]][s[0]]=0

    while q:
        point = q.popleft()
     
        #Dừng khi đạt đến điểm kết thúc.
        if point[0] == g[0] and point[1] == g[1]:
            break
      
        #Mở hết các nút ở bậc kề với bậc hiện tại. 
        for i in range(len(directions)):
            if directions[i]=='left':
                x, y = point[0] -1, point[1]
            if directions[i]=='right':
                x, y = point[0] +1, point[1]
            if directions[i]=='up':
                x, y = point[0], point[1]-1
            if directions[i]=='down':
                x, y = point[0], point[1]+1

            #Kiểm tra tính hợp lệ của các nút vừa mở và cập nhật chi phí.
            if x in range(w) and y in range(h) and not opened[y][x]:
                opened[y][x] = True

                if (x,y) not in walls:
                    cost_matrix[y][x] = weight[i] + cost_matrix[point[1]][point[0]]
                    dir_matrix[y][x] = i
                    q.append((x,y))

    has_path=opened[g[1]][g[0]]
    cost=-1

    if has_path:
        cost=cost_matrix[g[1]][g[0]]

    return has_path,cost,dir_matrix