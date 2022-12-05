from map import Map
import heuristic

#khởi tạo list chứa các hướng di chuyển.
directions=['left','right','up','down']
weight   = [1, 1, 1, 1]
#Khác với các thuật toán tìm kiếm không có thông tin
#điều kiện để quyết định đường đi là heuristic+trọng số

INF=int(1e9)

def a_star(s, g, w, h, walls,h_option):
    cost_matrix = [[INF] * w for _ in range(h)]
    dir_matrix = [[-1] * w for _ in range(h)]
    q = list()
    opened=list()

    #coi cấu trúc list là hàng đợi(tập biên) để tiện cho việc tìm nút
    #có chi phú nhỏ nhất để mở và lấy nút đó ra khỏi hàng đợi.
    q.append((0,s))
    if h_option==1:
        cost_matrix[s[1]][s[0]]=heuristic.ManhattanDistance(s,g)
    if h_option==2:
        cost_matrix[s[1]][s[0]]=heuristic.EuclideanDistance(s,g)
    if h_option==3:
        cost_matrix[s[1]][s[0]]=heuristic.BreakingTie(s,s,g)
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
                        if h_option==1:
                            cost_matrix[y][x] = weight[i]+heuristic.ManhattanDistance((x,y),g)+cost_matrix[point[1][1]][point[1][0]]-heuristic.ManhattanDistance(point[1],g)
                        if h_option==2:
                            cost_matrix[y][x] = weight[i]+heuristic.EuclideanDistance((x,y),g)+cost_matrix[point[1][1]][point[1][0]]-heuristic.EuclideanDistance(point[1],g)
                        if h_option==3:
                            cost_matrix[y][x] = weight[i]+heuristic.BreakingTie(s,(x,y),g)+cost_matrix[point[1][1]][point[1][0]]-heuristic.BreakingTie(s,point[1],g)
                        dir_matrix[y][x] = i
                        q.append((cost_matrix[y][x],(x,y)))

    has_path=False
    cost=cost_matrix[g[1]][g[0]]
    if cost!=INF:
        has_path=True
    dirs=[]
    dirs.append(dir_matrix)
    return has_path,cost,dirs,opened