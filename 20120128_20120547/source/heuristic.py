import math

def ManhattanDistance(x1,g):
    #x1, g là tuple chứa tọa đổ điểm.
    D=1
    return D*(abs(x1[0]-g[0])+abs(x1[1]-g[1]))

def EuclideanDistance(x1,g):
    D=1
    return D*math.sqrt((x1[0]-g[0])**2+(x1[1]-g[1])**2)

def BreakingTie(s,x1,g):
    #hệ số p: cho thấy sự mong đợi về số bước dài nhất.
    assume_max=1000
    p=1/assume_max
    #s là tọa độ điểm bắt đầu.
    dx1 = x1[0] - g[0]
    dy1 = x1[1] - g[1]
    dx2 = s[0] - g[0]
    dy2 = s[1] - g[1]
    cross = abs(dx1*dy2 - dx2*dy1)
    return cross*p
