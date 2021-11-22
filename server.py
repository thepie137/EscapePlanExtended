import socket
import pickle
from _thread import *
import pygame, os

from pygame.constants import NOEVENT
import buttons
import random 
import Game 
import time


SERVER = "192.168.1.47"
PORT = 5050


#0-accepting connection, 2-game start, (1 for client waiting room), 3-game-ongoing
game_state = 1
ongoing = False


#current prisoner and police
current_T = None
current_P = None

turn = 'police'  #กำหนด turn แรกให้เป็นของ Police

game = Game.Game()

def blit_players(win, players, base_font):
    i = 0
    for player in players:
        text = player+" : "+str(players[player])
        show = base_font.render(text, 1, (255,0,0))
        win.blit(show, (100, 350+(i*60)))
        i = i+1
    text2 = 'Clients :'+ str(i)
    show2 = base_font.render(text2, 1, (255,0,0))
    win.blit(show2, (50,50))

def timer(): 
    time.sleep(3)
    global game_state
    game_state = 3

def timer_two(): 
    time.sleep(1)
    new_game()
    
def new_game(): 
    global turn
    turn = 'police'
    global game_state
    game_state = 2
    start_new_thread(timer, ())
    random_TP(players, False)
    global game
    game.make_zeros()
    game.random_board()

def second_state():
    global turn
    turn = 'police'
    global game_state
    game_state = 2
    start_new_thread(timer, ()) #ทำอะไร
    random_TP(players, True)
    global game
    game.make_zeros()
    game.random_board() 

def random_TP(players, new_game): 
    global current_P, current_T
    if new_game:
        current_T = random.choice(list(players.keys()))
        while current_P == None or current_P == current_T:
            current_P = random.choice(list(players.keys()))
    else: 
        global winner
        current_P = winner
        current_T = random.choice(list(players.keys()))
        while current_T == current_P:
            current_T = random.choice(list(players.keys()))

def server_interface():
    pygame.init()
    BASE_FONT = pygame.font.Font("./Font/MinecraftRegular-Bmg3.otf", 40)
    win = pygame.display.set_mode((300,500))
    pygame.display.set_caption("Server")
    clock = pygame.time.Clock()

    start_img = pygame.image.load('./Assets/start.png').convert_alpha()
    start_btn = buttons.Button(65,100,start_img,0.25, 'start')

    reset_img = pygame.image.load('./Assets/reset.png').convert_alpha()
    reset_btn = buttons.Button(100,200,reset_img,0.1, 'reset')

    mode_img = pygame.image.load('./Assets/spring.png').convert_alpha()
    mode_btn = buttons.Button(10,320,mode_img,0.16, 'mode')

    mode2_img = pygame.image.load('./Assets/fist.png').convert_alpha()
    mode2_btn = buttons.Button(10,380,mode2_img,0.07, 'mode2')

    swap_img = pygame.image.load('./Assets/swap.png').convert_alpha()
    swap_btn = buttons.Button(10,430,swap_img,0.25, 'swap')

    door_img = pygame.image.load('./Assets/door.png').convert_alpha()
    door_btn = buttons.Button(10,260,door_img,0.1, 'door')

    pause_img = pygame.image.load('./Assets/pause.png').convert_alpha()
    pause_btn = buttons.Button(230,270,pause_img,0.1,'pause')

    while True: #คลิก reset -> gamestate = 1, start -> gamestate = 2 , render player name on server ui
        global game_state
        clock.tick(60)
        win.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()
                if game_state != 2:
                    if start_btn.click(pos) and len(players.keys())>= 2:
                        second_state() #รัน method
                    if reset_btn.click(pos):
                        game_state = 1
                        game.reset_power()
                        for player in players:
                            players[player] = 0 #ใส่ลิสplayersด้วย 0
                    if mode_btn.click(pos):
                        game_state = 1
                        game.reset_power()
                        game.spring_mode()
                        for player in players:
                            players[player] = 0
                        second_state()
                    if mode2_btn.click(pos):
                        game_state = 1
                        game.reset_power()
                        game.breaker_mode()
                        for player in players:
                            players[player] = 0
                        second_state()
                    if swap_btn.click(pos):
                        pr_standing = game.get_pri_pos()
                        po_standing = game.get_po_pos()
                        game.swap(pr_standing[0],pr_standing[1],po_standing[0],po_standing[1])
                    if door_btn.click(pos):
                        game_state = 1
                        game.reset_power()
                        game.door_mode()
                        for player in players:
                            players[player] = 0
                        second_state()
                    if pause_btn.click(pos):
                        if game.pause:
                            game.pause = False
                        else:
                            game.pause = True
                    

        blit_players(win, players, BASE_FONT)
        start_btn.draw(win)
        reset_btn.draw(win)
        mode_btn.draw(win)
        mode2_btn.draw(win)
        swap_btn.draw(win)
        door_btn.draw(win)
        pause_btn.draw(win)
        pygame.display.update()

start_new_thread(server_interface, ()) #รันไอนี้ตลอดเวลาที่serverรัน

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)



print("Waiting for a connection, Server Started")

players = {}
chat_log = ['HELLO THERE']
winner = None

s.listen()

def partying():
    for i in range(50):
        game.change_color()
        time.sleep(0.2)

def threaded_client(conn, addr):
    global game_state, current_P, current_T
    name = conn.recv(4096).decode() #receive มาจาก network
    if name in players:
        print("Duplicate Names.")
        conn.close()
    players[name]=0 #ใส่scoreตามชื่อให้เป็น 0
    print("Welcome, ", name, addr)
    conn.sendall(pickle.dumps(players)) #ถ้าไม่มี Client กด Start ไม่ได้
    while True:
        try:
            global winner
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                

                if data == "players":
                    conn.sendall(pickle.dumps((game_state, players)))
                elif data == "role":
                    if current_P == name:
                        conn.sendall(pickle.dumps((game_state,'police')))
                    elif current_T == name:
                        conn.sendall(pickle.dumps((game_state,'prisoner')))
                    else:
                        conn.sendall(pickle.dumps((game_state,'spectator')))
                elif data == "board":
                    global game, turn
                    conn.sendall(pickle.dumps((game_state, turn, game)))
                elif data == "winner":
                    conn.sendall(pickle.dumps((game_state, winner, game, players)))
                elif data == "color":
                    game.change_color()
                elif data == "police":
                    game.poskin()
                elif data == "prisoner":
                    game.priskin()
                
                elif data == "emoji1police":
                    game.emoji1_po()
                elif data == "emoji1prisoner":
                    game.emoji1_pri()

                elif data == "chats":
                    conn.sendall(pickle.dumps(chat_log))
                elif 'msg, ' in data:
                    if 'disco' in data:
                        start_new_thread(partying,())
                    if len(chat_log) >= 10:
                        chat_log.pop(0)
                    chat_log.append(name + ': ' + data[4:])

                else: #รับ movement btns text มาจาก client
                    old_po = game.get_po_pos()
                    old_pr = game.get_pri_pos()
                    tun = game.get_tun_pos()
                    bo = game.get_board()
                    num = 11
                    num1 = 12
                    num2 = 13
                
                    if name == current_P:
                        if data == "up":
                            po = (old_po[0], old_po[1]-1)
                        elif data ==  "right":
                            po = (old_po[0]+1, old_po[1])
                        elif data == "down":
                            po = (old_po[0], old_po[1]+1)
                        elif data == "left":
                            po = (old_po[0]-1, old_po[1])
                        elif data == "jumpup":
                            po = (old_po[0], old_po[1]-2)
                        elif data == "jumpright":
                            po = (old_po[0]+2, old_po[1])
                        elif data == "jumpdown":
                            po = (old_po[0], old_po[1]+2)
                        elif data == "jumpleft":
                            po = (old_po[0]-2, old_po[1])
                        else: 
                            po = (old_po[0],old_po[1])
                        pr = old_pr #กำหนด pos ใหม่
                        
                    else:
                        if data == "up":
                            pr = (old_pr[0], old_pr[1]-1)
                        elif data == "right":
                            pr = (old_pr[0]+1, old_pr[1])
                        elif data == "down":
                            pr = (old_pr[0], old_pr[1]+1)
                        elif data == "left":
                            pr = (old_pr[0]-1, old_pr[1])
                        elif data == "jumpup":
                            pr = (old_pr[0], old_pr[1]-2)
                        elif data == "jumpright":
                            pr = (old_pr[0]+2, old_pr[1])
                        elif data == "jumpdown":
                            pr = (old_pr[0], old_pr[1]+2)
                        elif data == "jumpleft":
                            pr = (old_pr[0]-2, old_pr[1])
                        else:
                            pr = (old_pr[0],old_pr[1])
                        po = old_po #กำหนด pos ใหม่
                    
                    if num in bo:
                        item = game.get_item_pos()
                        if po == pr or pr == tun: #check winner ก่อน move , ถ้ามี winner ก็ state 4 เลยไม่ต้อง move แล้ว
                            if po == pr: #ตำรวจจับโจรได้
                                players[current_P] = players[current_P] + 1 #คะแนน?
                                winner = current_P
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                            else: #โจรเข้าtunnelได้
                                players[current_T] = players[current_T] + 1 #คะแนน?
                                winner = current_T
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                        elif po == item or pr == item: 
                            if po == item:
                                game.policejumper()
                            if pr == item:
                                game.prisonerjumper()
                            if name == current_P and data != "still": 
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": 
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': 
                                turn = 'prisoner'
                            else:
                                turn = 'police'
                            
                        else:
                            if name == current_P and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': # move แล้วเปลี่ยน turn
                                turn = 'prisoner'
                            else:
                                turn = 'police'
                    elif num1 in bo:
                        item2 = game.get_item2_pos()
                        if po == pr or pr == tun: #check winner ก่อน move , ถ้ามี winner ก็ state 4 เลยไม่ต้อง move แล้ว
                            if po == pr: #ตำรวจจับโจรได้
                                players[current_P] = players[current_P] + 1 #คะแนน?
                                winner = current_P
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                            else: #โจรเข้าtunnelได้
                                players[current_T] = players[current_T] + 1 #คะแนน?
                                winner = current_T
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                        elif po == item2 or pr == item2: 
                            if po == item2:
                                game.policebreaker()
                            if pr == item2:
                                game.prisonerbreaker()
                            if name == current_P and data != "still": 
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": 
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': 
                                turn = 'prisoner'
                            else:
                                turn = 'police'
                            
                        else:
                            if name == current_P and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': # move แล้วเปลี่ยน turn
                                turn = 'prisoner'
                            else:
                                turn = 'police'
                    
                    elif num2 in bo:
                        item3 = game.get_item3_pos()
                        door_destination = game.door_where()
                        if po == pr or pr == tun: #check winner ก่อน move , ถ้ามี winner ก็ state 4 เลยไม่ต้อง move แล้ว
                            if po == pr: #ตำรวจจับโจรได้
                                players[current_P] = players[current_P] + 1 #คะแนน?
                                winner = current_P
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                            else: #โจรเข้าtunnelได้
                                players[current_T] = players[current_T] + 1 #คะแนน?
                                winner = current_T
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                        elif po == item3 or pr == item3:
                            if name == current_P and data != "still": 
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": 
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                            if po == item3:
                                game.swap(po[0],po[1],door_destination[0],door_destination[1])
                            if pr == item3:
                                game.swap(pr[0],pr[1],door_destination[0],door_destination[1])
                            if turn =='police': 
                                turn = 'prisoner'
                            else:
                                turn = 'police'
                        
                        else:
                            if name == current_P and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': # move แล้วเปลี่ยน turn
                                turn = 'prisoner'
                            else:
                                turn = 'police'


                    else:
                        if po == pr or pr == tun: #check winner ก่อน move , ถ้ามี winner ก็ state 4 เลยไม่ต้อง move แล้ว
                            if po == pr: #ตำรวจจับโจรได้
                                players[current_P] = players[current_P] + 1 #คะแนน?
                                winner = current_P
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                            else: #โจรเข้าtunnelได้
                                players[current_T] = players[current_T] + 1 #คะแนน?
                                winner = current_T
                                game_state = 4
                                game.reset_power()
                                start_new_thread(timer_two, ())
                        else:
                            if name == current_P and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_po[0], old_po[1], po[0], po[1])
                            elif name == current_T and data != "still": #ถ้ายังไม่หมดเวลา
                                game.move(old_pr[0], old_pr[1], pr[0], pr[1])
                                    
                            if turn =='police': # move แล้วเปลี่ยน turn
                                turn = 'prisoner'
                            else:
                                turn = 'police'

                        
        except:
            break

    print("Lost connection, ", name, addr)
    if name == current_P or name == current_T: #ใครออกให้เปลี่ยน state เป็น 1
        current_P = None
        current_T = None
        game_state = 1
    players.pop(name, None)
    conn.close()
    
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, addr))


    


        