from tkinter import Tk
from threading import Timer
from data import field
import os


class MainEngine(object):

    def __init__(self):
        
        # initialize tkinter window parameters
        self.root = Tk()
        self.root.title("Pac-Man")
        self.root.geometry("240x320")
        self.root.resizable(0, 0)





# initialize map
    # field에서 generate된 맵을 받아와서 widget을 배치한다
    # 각 오브젝트의 개수를 받는다?


# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단, 좌표 이동을 시켜준다

    # 주인공을 이미지파일로 만들어서 쓰겠다면
    # 입을 벌린것과 다문 것 두개를 번갈아 나타나게끔 한다

    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임