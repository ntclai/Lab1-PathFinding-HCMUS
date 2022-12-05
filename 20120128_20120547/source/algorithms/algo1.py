#Sử dụng thuật toán Simulated Annealing và UCS
#để tìm đường đi với chi phí tốt qua các điểm thưởng.

import random
from math import exp
from algorithms.ucs import ucs
from algorithms.ucs import ucs_bonus
import itertools

INF=10**9

def trace_path(has_path,dir_matrix,s_g):
    paths=[]
    directions=['left','right','up','down']
    if has_path:
        for i in range(len(s_g)):
            path=[]
            fx,fy=s_g[i][1][0],s_g[i][1][1]
            path.append((fx,fy))
            while not(s_g[i][0][0]==fx and s_g[i][0][1]==fy):
                dir=dir_matrix[i][fy][fx]
                if directions[dir]=='left':
                    fx,fy=fx+1,fy
                elif directions[dir]=='right':
                    fx,fy=fx-1,fy
                elif directions[dir]=='up':
                    fx,fy=fx,fy+1
                elif directions[dir]=='down':
                    fx,fy=fx,fy-1
                
                if fx==s_g[i][0][0] and fy==s_g[i][0][1]:
                    break
                path.append((fx,fy))
            path.reverse()
            paths=paths+path
    return paths

def algo1(s, g, bonus, bonus_vals, w, h, walls):
    #xác định số lượng điểm thưởng nhiều hay ít.
    big_stops=False
    if len(bonus)>6:
        big_stops=True
    check_exist_state=[] #kiểm tra trạng thái next_path đã tồn tại chưa.
    #Khởi tạo ma trận khoảng cách của tất cả
    #các điểm điểm thưởng, điểm bắt đầu, điểm kết thúc.
    points=bonus.copy()
    points.insert(0,s)
    points.append(g)
    dis_matrix=[[0]*len(points) for _ in range(len(points))]
    temp=points.copy()

    #tính khoảng cách của từng cặp điểm trong points
    for i in range(len(points)):
        for j in range(len(points)):
            _,cost,_,_=ucs(points[i],points[j],w,h,walls)
            dis_matrix[i][j]=cost
    #Hàm dưới đây tính xác suất xem xét chuyển đổi trạng thái
    #Nếu delta <= 0, chấp nhận trạng thái mới và cho P=1.
    #Nếu delta > 0, chấp nhận trạng thái cũ (tồi) với
    #xác suất tuân theo luật Boltzman
    def Boltzman_prob(delta,T): 
        return 1 if delta<=0 else exp(-delta/T)

    #hàm dưới đây tính chi phí đường đi ở trạng thái đang xét.
    def compute_cost(path):
        route = path.copy()
        route.insert(0, s)
        route.append(g)
        
        num_points  = len(route)
        total    = 0

        for i in range(num_points - 1):
            i1,i2=0,0
            for m in range(len(temp)):
                if route[i] == temp[m]:
                    i1=m
                if route[i+1] == temp[m]:
                    i2=m
            total += dis_matrix[i1][i2]
        return total

    #hàm dưới đây tạo ra trạng thái mới
    def next_path(next_paths,T):
        return next_paths[T]
    
    def big_next_path(path):
        new_path=path.copy()
        n=len(new_path)
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        new_path[i], new_path[j]=new_path[j], new_path[i]
        return new_path

    #Khởi tạo trạng thái ban đầu bằng cách
    #sắp xếp các điểm thưởng theo tứ tự tăng dần giá tri điểm.
    init_path=bonus.copy()
    next_paths=list(itertools.permutations(init_path))
    for i in range(len(next_paths)):
        next_paths[i]=list(next_paths[i])
    
    prev_path = init_path.copy()
    best_path = prev_path.copy()
    prev_cost = best_cost = compute_cost(prev_path)
    # Khởi tạo các Annealing parameters
    alpha = -1 # hệ số để giảm T
    if big_stops:
        T=1000
    else:
        T = 0 # T ban đầu
    T_min = 1 # điều kiện để dừng của T

    #Khởi tạo các giá trị cần trả về
    total=0
    dirs=[]
    s_g=[]
    dir_matrix=[[-1]*w for _ in range(h)]
    index=0
    has_path=ucs(s,g,w,h,walls)[0]

    if big_stops==False:
        while T < len(next_paths):
            cur_path = next_path(next_paths,T)
            cur_cost = compute_cost(cur_path)

            delta = cur_cost - prev_cost
            P = Boltzman_prob(delta, T)
        
            # Kiểm tra xem trạng thái mới có được chấp nhận không.
            if P == 1:
                prev_path  = cur_path.copy()
                prev_cost = cur_cost

            #Cập nhật lại best_cost, best_path và giảm T
            if cur_cost < best_cost:
                best_path  = cur_path.copy()
                best_cost = cur_cost
            T  += 1
    else:
        while T > T_min:
            cur_path = big_next_path(prev_path)
            cur_cost = compute_cost(cur_path)

            delta = cur_cost - prev_cost
            P = Boltzman_prob(delta, T)
        
            # Kiểm tra xem trạng thái mới có được chấp nhận không.
            if P == 1:
                prev_path  = cur_path.copy()
                prev_cost = cur_cost

            #Cập nhật lại best_cost, best_path và giảm T
            if cur_cost < best_cost:
                best_path  = cur_path.copy()
                best_cost = cur_cost
            T  += alpha

    best_path.insert(0,s)
    best_path.append(g)
    
    #tính chi phí đường đi của best_path
    Opened=[]
    if has_path:
        _,cost_ucs,dir_ucs,_=ucs_bonus(s,g,w,h,walls,bonus,bonus_vals)
        # opened_ucs=trace_path(has_path,dir_ucs,[[s,g]])
        # for i in range(len(bonus)):
        #     if bonus[i] in opened_ucs:
        #         cost_ucs+=bonus_vals[i]
        while has_path and index < len(best_path) - 1:
            p1,p2 = best_path[index], best_path[index + 1]
            index1,index2=0,0
            for m in range(len(temp)):
                if p1 == temp[m]:
                    index1=m
                if p2 == temp[m]:
                    index2=m
            cost = dis_matrix[index1][index2]
            if cost!=INF:
                has_path=True
            else:
                has_path=False
            if has_path:
                _,_,dir,_=ucs(p1,p2,w,h,walls)
                dirs.append(dir[0])
                s_g.append([p1,p2])
                o=trace_path(has_path,dir,[[p1,p2]])
                Opened=Opened+o
            total += cost
            index += 1
        Opened=list(set(Opened))
        for i in range(len(bonus)):
            if bonus[i] in Opened:
                total+=bonus_vals[i]
        if cost_ucs<total:
            dir2=[]
            dir2.append(dir_ucs[0])
            return has_path,cost_ucs,dir2,[[s,g]]
    return has_path,total,dirs,s_g

