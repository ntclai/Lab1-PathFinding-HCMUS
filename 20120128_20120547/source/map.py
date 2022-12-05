# from itertools import count
# from turtle import Screen
import pygame
import cv2
import time
import os

class Map:
    cell_scale=25 #tỉ lệ vẽ ô.
    #define color:
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    GREEN=(0,255,0)
    def __init__(self,font):
        self.S=() #lưu tọa độ điểm bắt đầu.
        self.G=() #lưu tạo độ điểm đích.
        self.walls=[] #lưu tọa độ các bức tường.
        self.bonus=[] #lưu tọa độ các điểm thưởng đối với map có điểm thưởng.
        self.bonus_vals=[] #lưu giá trị điểm thưởng.
        self.WIDTH=0 #chiều dài bản đồ.
        self.HEIGHT=0 #chiều cao bản đồ.
        self.screen=None #screen object.
        self.font=font #font cho việc hiện text.
    def load(self,path):
        f=open(path,'r')
        data=f.readlines()
        f.close()
        #xóa ký tự xuống dòng trong notepad.
        for i in range(len(data)):
            data[i]=data[i].replace('\n','')
        #lưu thông tin điểm thưởng nếu có.
        n=int(data[0])
        if n>0:
            for i in range(1,n+1):
                infos=data[i].split()
                # self.bonus.append((int(infos[1]),int(infos[0])))
                self.bonus_vals.append(int(infos[2]))
        #xóa các dòng thông tin về điểm thưởng.
        for i in range(n+1):
            data.pop(0)
        #lưu thông tin bản đồ.
        for i in range(len(data)):
            data[i]=list(data[i])
        self.WIDTH=len(data[-1])
        self.HEIGHT=len(data)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if data[i][j]=='x':
                    self.walls.append((j,i))
                elif data[i][j]=='S':
                    self.S=(j,i)
                elif data[i][j]=='+':
                    self.bonus.append((j,i))
                elif (data[i][j]==' ' and i==0) or (data[i][j]==' ' and j==0) or (data[i][j]==' ' and i==self.HEIGHT-1) or (data[i][j]==' ' and j==self.WIDTH-1):
                    self.G=(j,i)

    def display(self,pygame,video,image_path):
        #tải ảnh cho tường, start, exit, bonus_point
        wall_img=pygame.image.load('image/wall.png').convert_alpha()
        wall_img=pygame.transform.scale(wall_img,(Map.cell_scale,Map.cell_scale))
        start_img=pygame.image.load('image/start.png').convert_alpha()
        start_img=pygame.transform.scale(start_img,(Map.cell_scale,Map.cell_scale))
        exit_img=pygame.image.load('image/exit.png').convert_alpha()
        exit_img=pygame.transform.scale(exit_img,(Map.cell_scale,Map.cell_scale))
        bonus_img=pygame.image.load('image/bonus.png').convert_alpha()
        bonus_img=pygame.transform.scale(bonus_img,(Map.cell_scale,Map.cell_scale))
        #vẽ điểm start.
        self.screen.blit(start_img,(self.S[0]*Map.cell_scale,self.S[1]*Map.cell_scale))
        #vẽ điểm đích.
        self.screen.blit(exit_img,(self.G[0]*Map.cell_scale,self.G[1]*Map.cell_scale))
        #vẽ tường.
        for i in range(len(self.walls)):
            self.screen.blit(wall_img,(self.walls[i][0]*Map.cell_scale,self.walls[i][1]*Map.cell_scale))
        self.writeVideo(video,image_path)
        #vẽ điểm thưởng.
        for i in range(len(self.bonus)):
            self.screen.blit(bonus_img,(self.bonus[i][0]*Map.cell_scale,self.bonus[i][1]*Map.cell_scale))
        self.writeVideo(video,image_path)

    def display_path(self,has_path,finded_path,pygame,video,image_path):
        clock=pygame.time.Clock()
        FPS = 20
        if ('level_1' in image_path) and ('input2' in image_path):
            FPS=300 
        if has_path:
            start_img=pygame.image.load('image/start.png').convert_alpha()
            start_img=pygame.transform.scale(start_img,(Map.cell_scale,Map.cell_scale))
            for p in finded_path:
                self.screen.blit(start_img,(p[0]*Map.cell_scale,p[1]*Map.cell_scale))
                self.writeVideo(video,image_path)
                pygame.display.update()
                clock.tick(FPS)
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('No Path', True, (255,0,0), (0,0,0))
            self.screen.blit(text,((self.WIDTH//2)*(Map.cell_scale-5),(self.HEIGHT//2)*(Map.cell_scale-5)))
            self.writeVideo(video,image_path)
            pygame.display.update()
            clock.tick(FPS)

    def trace_path(self,has_path,dir_matrix,s_g):
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

    #Các phương thức cho việc chuyển cảnh
    def draw_text(self,index,algo,count,video,image_path):
        self.screen.fill(Map.GREEN)
        if len(algo)<=5:
            text=text = self.font.render(f'MAP{index}:{algo}', True, Map.WHITE, Map.BLACK)
            self.screen.blit(text,((self.WIDTH//2)*(Map.cell_scale-5),(self.HEIGHT//2)*(Map.cell_scale-5)))
        else:
            pos=algo.find(':')
            algo_name=algo[:pos]
            heu_name=algo[pos+1:]
            text1=self.font.render(f'MAP{index}:{algo_name}', True, Map.WHITE, Map.BLACK)
            text2=self.font.render(f'{heu_name}', True, Map.WHITE, Map.BLACK)
            self.screen.blit(text1,((self.WIDTH//2)*(Map.cell_scale-5),(self.HEIGHT//2)*(Map.cell_scale-5)))
            self.screen.blit(text2,((self.WIDTH//2-5)*(Map.cell_scale-5),(self.HEIGHT//2+3)*(Map.cell_scale-5)))
        self.writeVideo(video,image_path)
        if count<8:
            return True
        else:
            return False
    
    def close(self,count,video,image_path):
        self.writeVideo(video,image_path)
        if count<8:
            return True
        else:
            return False

    def writeVideo(self,video,image_path):
        f_name=image_path+'/%d.png'%(self.frame_count)
        self.frame_count+=1
        pygame.image.save(self.screen,f_name)
        img=cv2.imread(f_name)
        video.write(img)

    def run(self,has_path,cost,dir_matrix,s_g,pygame,index,algo,out_path,heuristic):
        clock = pygame.time.Clock()
        FPS = 20
        self.frame_count=0

        self.screen = pygame.display.set_mode((self.WIDTH*Map.cell_scale,self.HEIGHT*Map.cell_scale))
        WHITE=(255,255,255)
        self.screen.fill(WHITE)
        
        check_draw=0
        check_draw2=True
        check_fill=False
        check_close=0
        check_done_path=False

        algo2=''
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        if heuristic=='':
            f=open(out_path+f'/{algo}.txt','w')
        else:
            algo2=algo[:algo.find(':')]
            f=open(out_path+f'/{algo2+heuristic}.txt','w')
        if has_path:
            f.write(str(cost))
            finded_path=self.trace_path(has_path,dir_matrix,s_g)
        else:
            f.write('No Path')
            finded_path=[]
        f.close()

        fourcc=cv2.VideoWriter_fourcc(*'mp4v')
        if heuristic=='':
            video=cv2.VideoWriter(out_path+'/%s.mp4'%(algo),fourcc,FPS-5,(self.WIDTH*Map.cell_scale,self.HEIGHT*Map.cell_scale))    
        else:
            video=cv2.VideoWriter(out_path+'/%s.mp4'%(algo2+heuristic),fourcc,FPS-5,(self.WIDTH*Map.cell_scale,self.HEIGHT*Map.cell_scale))

        image_path=out_path.replace('output','image')
        image_path=image_path[3:]
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        
        check_done_file=False

        run=True
        while run:
            clock.tick(FPS)
            self.writeVideo(video,image_path)
            if check_draw2:
                check_draw2=self.draw_text(index,algo,check_draw,video,image_path)
                check_draw+=1
            elif check_done_path==False:
                if check_fill==False:
                    self.screen.fill(WHITE)
                    check_fill=True
                self.display(pygame,video,image_path)
                self.display_path(has_path,finded_path,pygame,video,image_path)
                check_done_path=True
            else:
                run=self.close(check_close,video,image_path)
                check_close+=1
            
            pygame.display.update()
            
