from map import Map

#khởi tạo list chứa các hướng di chuyển.
directions=['left','right','up','down']
#chi phí cho các hướng di chuyển.
weight   = [1, 1, 1, 1]

INF=int(1e9)

def ucs(s, g, w, h, walls):
    cost_matrix = [[INF] * w for _ in range(h)]
    dir_matrix = [[-1] * w for _ in range(h)]
    q = list()
    opened=list()

    #coi cấu trúc list là hàng đợi(tập biên) để tiện cho việc tìm nút
    #có chi phú nhỏ nhất để mở và lấy nút đó ra khỏi hàng đợi.
    q.append((0,s))
    cost_matrix[s[1]][s[0]]=0
    while q!=[]:
        #tìm điểm cần mở
        point=q[0]
        min_index=0
        for i in range(len(q)):
            if point[0]>q[i][0]:
                min_index=i
                point=q[i]
        if min_index==0:
            point=q.pop(0)
        else:
            point=q.pop(min_index)
        opened.append(point[1])
        #xóa bớt những phần tử trong tập biên mà điểm đã được mở.
        masked=[]
        for i in range(len(q)):
            if point[1][0]==q[i][1][0] and point[1][1]==q[i][1][1]:
                masked.append(q[i])
        for e in masked:
            q.remove(e)
        #Dừng khi đạt đến điểm kết thúc.
        if point[1][0] == g[0] and point[1][1] == g[1]:
            break
      
        #Mở hết các nút ở bậc kề với nút hiện tại. 
        for i in range(len(directions)):
            if directions[i]=='left':
                x, y = point[1][0] -1, point[1][1]
            if directions[i]=='right':
                x, y = point[1][0] +1, point[1][1]
            if directions[i]=='up':
                x, y = point[1][0], point[1][1]-1
            if directions[i]=='down':
                x, y = point[1][0], point[1][1]+1

            #Kiểm tra tính hợp lệ của các nút vừa mở và cập nhật chi phí.
            if x in range(w) and y in range(h):
                if (x,y) not in walls:
                    if (x,y) not in opened:
                        cost_matrix[y][x] = weight[i] + cost_matrix[point[1][1]][point[1][0]]
                        dir_matrix[y][x] = i
                        q.append((cost_matrix[y][x],(x,y)))

    has_path=False
    cost=cost_matrix[g[1]][g[0]]
    if cost!=INF:
        has_path=True
    dirs=[]
    dirs.append(dir_matrix)
    return has_path,cost,dirs,opened

def ucs_bonus(s, g, w, h, walls,bonus,bonus_vals):
    cost_matrix = [[INF] * w for _ in range(h)]
    dir_matrix = [[-1] * w for _ in range(h)]
    q = list()
    opened=list()

    #coi cấu trúc list là hàng đợi(tập biên) để tiện cho việc tìm nút
    #có chi phú nhỏ nhất để mở và lấy nút đó ra khỏi hàng đợi.
    q.append((0,s))
    cost_matrix[s[1]][s[0]]=0
    while q!=[]:
        #tìm điểm cần mở
        point=q[0]
        min_index=0
        for i in range(len(q)):
            if point[0]>q[i][0]:
                min_index=i
                point=q[i]
        if min_index==0:
            point=q.pop(0)
        else:
            point=q.pop(min_index)
        opened.append(point[1])
        #xóa bớt những phần tử trong tập biên mà điểm đã được mở.
        masked=[]
        for i in range(len(q)):
            if point[1][0]==q[i][1][0] and point[1][1]==q[i][1][1]:
                masked.append(q[i])
        for e in masked:
            q.remove(e)
        #Dừng khi đạt đến điểm kết thúc.
        if point[1][0] == g[0] and point[1][1] == g[1]:
            break
      
        #Mở hết các nút ở bậc kề với nút hiện tại. 
        for i in range(len(directions)):
            if directions[i]=='left':
                x, y = point[1][0] -1, point[1][1]
            if directions[i]=='right':
                x, y = point[1][0] +1, point[1][1]
            if directions[i]=='up':
                x, y = point[1][0], point[1][1]-1
            if directions[i]=='down':
                x, y = point[1][0], point[1][1]+1

            #Kiểm tra tính hợp lệ của các nút vừa mở và cập nhật chi phí.
            if x in range(w) and y in range(h):
                if (x,y) not in walls:
                    if (x,y) not in opened:
                        cost_matrix[y][x] = weight[i] + cost_matrix[point[1][1]][point[1][0]]
                        for m in range(len(bonus)):
                            if (x,y)==bonus[m]:
                                cost_matrix[y][x]+=bonus_vals[m]
                                break
                        dir_matrix[y][x] = i
                        q.append((cost_matrix[y][x],(x,y)))

    has_path=False
    cost=cost_matrix[g[1]][g[0]]
    if cost!=INF:
        has_path=True
    dirs=[]
    dirs.append(dir_matrix)
    return has_path,cost,dirs,opened