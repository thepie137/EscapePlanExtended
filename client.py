from network import Network
import pygame, time
import buttons
import random 
import webbrowser
from _thread import *



pygame.init()

BASE_FONT = pygame.font.Font("./Font/MinecraftRegular-Bmg3.otf", 40)
font = pygame.font.Font("./Font/MinecraftRegular-Bmg3.otf", 30)



win = pygame.display.set_mode((450,700))
pygame.display.set_caption("Escape Plan")

run = True
clock = pygame.time.Clock()
game_state = 0
ongoing = False
name_input = ""
chat_input = ""
players = {}
role = None
tm = False #ค่าที่ใช้ในtimer()
move = False

def blit_chat(win, chats):
    show_chat = []
    for chat in chats:
        snipped = []
        while len(chat)>18:
            snipped.append(chat[:20])
            chat = chat[20:]
        snipped.append(chat)
        for line in snipped:
            if len(show_chat)>12:
                show_chat.pop(0)
            show_chat.append(line)
    i = 0
    for show in show_chat:
        text = show
        global font
        bb = font.render(text, 1, (0,0,204))
        win.blit(bb, (452, 5+(i*50)))
        i = i+1



def timer():
    global t_timer
    t_timer = 10
    while t_timer >= 0 and turn == role:
        if turn != role or game_state != 3:
            break 
        time.sleep(1) 
        if game.pause == False:
            t_timer = t_timer-1
        if turn == role and t_timer <=0:
            n.oneway_send('still') #ส่งไปให้server เมื่อเวลาหมด ทำให้ player นั้นเดินไม่ได้
    global tm
    tm = False
    
def main_menu(event): #เอาไว้พิมพ์ชื่อ
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            global name_input
            name_input = name_input[:-1]
        else:
            name_input += event.unicode

def draw_board(win, board, pos1, pos2, length, padding, color, po_skin, pri_skin, emo_po, emo_pri): #เอาไว้วาดพื้นหลังและรูปตามตำแหน่งใน board ที่รับมาจาก server
    pygame.draw.rect(win, (11,91,152), pygame.Rect(pos1, pos2, length, length)) #สีและขนาดสีเหลี่ยมสีเข้ม
    rect_size = int((length - (6*padding))/5)
    for y in range(5):
        for x in range(5):
            pos = ((padding*(x+1))+(rect_size*x)+pos1, (padding*(y+1))+(rect_size*y)+pos2)
            posA = ((padding*(x+1))+(rect_size*x)+pos1+(rect_size//3), (padding*(y+1))+(rect_size*y)+pos2-(rect_size//3))
            if color == 'yellow':
                pygame.draw.rect(win, (255,255,0), [pos[0],pos[1],rect_size,rect_size]) #เปลี่ยนสีบอร์ดตรงนี้
            elif color == 'pink' :
                pygame.draw.rect(win, (254,184,198), [pos[0],pos[1],rect_size,rect_size])
            else:
                pygame.draw.rect(win, (254,255,255), [pos[0],pos[1],rect_size,rect_size])
            if board[x][y] == 1:
                img = pygame.image.load('./Assets/obs.png').convert_alpha()
            elif board[x][y] == 2:
                if emo_pri == 0:
                    if pri_skin == 1:
                        img = pygame.image.load('./Assets/pirate.png').convert_alpha()
                    else:
                        img = pygame.image.load('./Assets/prisoner.png').convert_alpha()
                elif emo_pri == 1:
                    if pri_skin == 1:
                        img = pygame.image.load('./Assets/pirate.png').convert_alpha()
                        img2 = pygame.image.load('./Assets/lol.png').convert_alpha()
                    else:
                        img = pygame.image.load('./Assets/prisoner.png').convert_alpha()
                        img2 = pygame.image.load('./Assets/lol.png').convert_alpha()
            elif board[x][y] == 3:
                if emo_po == 0:
                    if po_skin == 1:
                        img = pygame.image.load('./Assets/marine.png').convert_alpha()
                    else:
                        img = pygame.image.load('./Assets/police.png').convert_alpha()
                elif emo_po == 1:
                    if po_skin == 1:
                        img = pygame.image.load('./Assets/marine.png').convert_alpha()
                        img2 = pygame.image.load('./Assets/lol.png').convert_alpha()
                    else:
                        img = pygame.image.load('./Assets/police.png').convert_alpha()
                        img2 = pygame.image.load('./Assets/lol.png').convert_alpha()
            elif board[x][y] == 4:
                img = pygame.image.load('./Assets/tunnel.png').convert_alpha()
            elif board[x][y] == 11:
                img = pygame.image.load('./Assets/spring.png').convert_alpha()
            elif board[x][y] == 12:
                img = pygame.image.load('./Assets/fist.png').convert_alpha()
            elif board[x][y] == 13:
                img = pygame.image.load('./Assets/door.png').convert_alpha()
            if board[x][y] != 0 and board[x][y] != 2 and board[x][y] != 3:
                image = pygame.transform.scale(img,(rect_size, rect_size))
                win.blit(image, pos)
            if board[x][y] == 2:
                if emo_pri == 0:
                    image = pygame.transform.scale(img,(rect_size, rect_size))
                    win.blit(image, pos)
                elif emo_pri == 1:
                    image = pygame.transform.scale(img,(rect_size, rect_size))
                    image2 = pygame.transform.scale(img2,(rect_size, rect_size))
                    win.blit(image, pos)
                    win.blit(image2, posA)
            if board[x][y] == 3:
                if emo_po == 0:
                    image = pygame.transform.scale(img,(rect_size, rect_size))
                    win.blit(image, pos)
                elif emo_po == 1:
                    image = pygame.transform.scale(img,(rect_size, rect_size))
                    image2 = pygame.transform.scale(img2,(rect_size, rect_size))
                    win.blit(image, pos)
                    win.blit(image2, posA)


def blit_players(win, players):  #เอาไว้ blit player name กับ player score
    i = 0
    for player in players:
        text = player+" : "+str(players[player])
        global BASE_FONT
        show = BASE_FONT.render(text, 1, (255,0,0))
        win.blit(show, (100, 100+(i*60)))
        i = i+1

start_img = pygame.image.load('./Assets/start.png').convert_alpha()
start_btn = buttons.Button(124, 450, start_img, 0.3, 'start')
movement_btns = []
img1 = pygame.image.load('./Assets/info.png').convert_alpha()
color_img = pygame.image.load('./Assets/color.png').convert_alpha()
skin_img = pygame.image.load('./Assets/skin.png').convert_alpha()
emoji1_img = pygame.image.load('./Assets/lol.png').convert_alpha()
color_btn = buttons.Button(270, 627, color_img, 0.15, '')
web_btn = buttons.Button(300, 527, img1, 0.05, '')
emoji1_btn = buttons.Button(210, 627, emoji1_img, 0.5, 'emoji1')


skin_btn = buttons.Button(330, 627, skin_img, 0.15, '')
tutorial_btn = buttons.Button(380, 20, img1, 0.05, '')
tutor = 0
tutor1 = pygame.image.load('./Assets/tutorialwarder.png').convert_alpha()
tutor2 = pygame.image.load('./Assets/tutorialprisoner.png').convert_alpha()
tutor1 = pygame.transform.scale(tutor1, (200,120))
tutor2 = pygame.transform.scale(tutor2, (200,120))

while run:
        clock.tick(60)
        if game_state == 0:
            pygame.display.set_mode((450,700))
            win.fill((202, 228, 241))
            start_btn.draw(win)
            tutorial_btn.draw(win)
        else:
            pygame.display.set_mode((800,700))
            win.fill((202, 228, 241))
            pygame.draw.rect(win, (196,215,217), [450,0,350,700])
            pygame.draw.rect(win, (255,255,255),[455,655,340,40])
            chats = n.send('chats')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if game_state == 0:
                
                main_menu(event) #รัน menu method
                name = BASE_FONT.render(name_input, 1, (255,0,0)) #render nameขณะพิมพ์
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        chat_input = chat_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        n.oneway_send('msg, '+chat_input)
                        chat_input = ""
                    else:
                        chat_input += event.unicode

                
            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()
                if game_state == 0:
                    if tutorial_btn.click(pos):
                        if tutor == 0:
                            tutor = 1
                        else:
                            tutor = 0
                    if start_btn.click(pos): #ถ้ากดปุ่ม start ใน client
                        n = Network(name_input) #เรียกใช้ network ตามชื่อ player
                        players = n.getP() #get name_input มาจาก network
                        if players != None:
                            game_state = 1
                    

                if game_state == 3 and turn == role: #ถ้ากด movement btns ใน state 3
                    for btn in movement_btns:
                        if btn.click(pos):
                            n.oneway_send(btn.text)
                            movement_btns = []
                if game_state == 3:
                    if color_btn.click(pos):
                        n.oneway_send('color')
                    if skin_btn.click(pos):
                        n.oneway_send(role)
                    if web_btn.click(pos):
                        webbrowser.open('https://docs.google.com/presentation/d/1wXQKwDV1_fThpQOeAKbLQuf1CWebunX_6RaFULjj2mA/edit?usp=sharing',new = 2)
                    if emoji1_btn.click(pos):
                        n.oneway_send(emoji1_btn.text+role)
                        print(emoji1_btn.text+role)
                    
        if game_state != 0:
            chat_log = n.send('chats')
            blit_chat(win, chat_log)
            show = font.render(chat_input, 1, (0,0,0))
            win.blit(show, (457,652))
        if game_state == 0: #หน้าพิมพ์ชื่อ
            win.blit(name, (100,200))
            if tutor == 1:
                text_tutor = BASE_FONT.render('Tutorial', 1, (0,0,255))
                win.blit(text_tutor, (135,20))
                win.blit(tutor1, (10,50))
                win.blit(tutor2, (210,50))

        elif game_state == 1: #หน้า lobby
            try:
                recieved_data = n.send("players") 
                game_state, new_players = recieved_data #game state จะเป็น 2 เมื่อ server กด start และเรารับเข้ามา
                if new_players != players:  
                    players = new_players.copy()  
                blit_players(win, players)
            except:
                game_state = 0  #คือไรนะ

        elif game_state == 2: #หน้าบอกrole
            try:
                game_state, role = n.send("role")
                game_state, turn, game = n.send("board")
                mode = game.get_mode()
                text_role = BASE_FONT.render('You are '+role, 1, (0,0,255))
                text_welcome = BASE_FONT.render('Welcome to Escapeplan', 1, (0,0,255))
                text_mode = BASE_FONT.render('Mode : '+mode, 1, (0,0,255))
                win.blit(text_role, (100,320))  #ทั้งหน้ามีแค่ text_role
                win.blit(text_welcome, (10,120))
                win.blit(text_mode, (100,420))
                pygame.display.update()  
                time.sleep(3)
                game_state = 3
            except:
                game_state = 0

        elif game_state == 3: #หน้าboard
            try:
                for btn in movement_btns: #draw movement btns จากด้านล่างตาม turn
                    btn.draw(win)
                game_state, turn, game = n.send("board") #รับตัวแปรมา
                draw_board(win, game.get_board(), 0, 50, 450, 5, game.c_color, game.po_skin, game.pri_skin, game.emo_po, game.emo_pri)
                
                color_btn.draw(win)
                skin_btn.draw(win)
                web_btn.draw(win)
                emoji1_btn.draw(win)

                if turn == role:
                    if move == False: #move ไว้checkแค่ตรงนี้
                        move = True
                        if tm == False: #tm ไว้checkแค่ตรงนี้
                            start_new_thread(timer, ()) #timer จบจะส่ง still เข้า server
                            tm = True
                        if role == 'prisoner':
                            pos1, pos2 = game.get_pri_pos() #pos1 = x, pos2 = y ของ prisoner
                            pr_power = game.get_pr_power()
                            if pr_power == 'jumper':
                                if game.check_legit((pos1, pos2-1)): #check legit ของตำแหน่งเดินขึ้น
                                    if not game.check_obs((pos1, pos2-1)):
                                        img = pygame.image.load('./Assets/up.png').convert_alpha()
                                        up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                        if up_btn not in movement_btns: 
                                            movement_btns.append(up_btn) #ใส่button ไว้ใน list movement_btns
                                    if game.check_obs((pos1, pos2-1)):
                                        if game.check_legit((pos1, pos2-2)) and not game.check_obs((pos1, pos2-2)):
                                            img = pygame.image.load('./Assets/up.png').convert_alpha()
                                            jumpup_btn = buttons.Button(100, 600, img, 0.05, 'jumpup')
                                            if jumpup_btn not in movement_btns: 
                                                movement_btns.append(jumpup_btn)

                                if game.check_legit((pos1+1, pos2)):
                                    if not game.check_obs((pos1+1, pos2)): 
                                        img = pygame.image.load('./Assets/right.png').convert_alpha()
                                        right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                        if right_btn not in movement_btns:
                                            movement_btns.append(right_btn)
                                    if game.check_obs((pos1+1, pos2)):
                                        if game.check_legit((pos1+2, pos2)) and not game.check_obs((pos1+2, pos2)):
                                            img = pygame.image.load('./Assets/right.png').convert_alpha()
                                            jumpright_btn = buttons.Button(127, 627, img, 0.05, 'jumpright')
                                            if jumpright_btn not in movement_btns: 
                                                movement_btns.append(jumpright_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    if not game.check_obs((pos1, pos2+1)):
                                        img = pygame.image.load('./Assets/down.png').convert_alpha()
                                        down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                        if down_btn not in movement_btns:
                                            movement_btns.append(down_btn)
                                    if game.check_obs((pos1, pos2+1)):
                                        if game.check_legit((pos1, pos2+2)) and not game.check_obs((pos1, pos2+2)):
                                            img = pygame.image.load('./Assets/down.png').convert_alpha()
                                            jumpdown_btn = buttons.Button(100, 627, img, 0.05, 'jumpdown')
                                            if jumpdown_btn not in movement_btns: 
                                                movement_btns.append(jumpdown_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    if not game.check_obs((pos1-1, pos2)):
                                        img = pygame.image.load('./Assets/left.png').convert_alpha()
                                        left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                        if left_btn not in movement_btns:
                                            movement_btns.append(left_btn)
                                    if game.check_obs((pos1-1, pos2)):
                                        if game.check_legit((pos1-2, pos2)) and not game.check_obs((pos1-2, pos2)):
                                            img = pygame.image.load('./Assets/left.png').convert_alpha()
                                            jumpleft_btn = buttons.Button(73, 627, img, 0.05, 'jumpleft')
                                            if jumpleft_btn not in movement_btns: 
                                                movement_btns.append(jumpleft_btn)
                            
                            elif pr_power == 'mortal':
                                if game.check_legit((pos1, pos2-1)): #check legit ของตำแหน่งเดินขึ้น
                                    if not game.check_obs((pos1, pos2-1)):
                                        img = pygame.image.load('./Assets/up.png').convert_alpha()
                                        up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                        if up_btn not in movement_btns: 
                                            movement_btns.append(up_btn) #ใส่button ไว้ใน list movement_btns

                                if game.check_legit((pos1+1, pos2)):
                                    if not game.check_obs((pos1+1, pos2)): 
                                        img = pygame.image.load('./Assets/right.png').convert_alpha()
                                        right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                        if right_btn not in movement_btns:
                                            movement_btns.append(right_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    if not game.check_obs((pos1, pos2+1)):
                                        img = pygame.image.load('./Assets/down.png').convert_alpha()
                                        down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                        if down_btn not in movement_btns:
                                            movement_btns.append(down_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    if not game.check_obs((pos1-1, pos2)):
                                        img = pygame.image.load('./Assets/left.png').convert_alpha()
                                        left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                        if left_btn not in movement_btns:
                                            movement_btns.append(left_btn)
                            elif pr_power == 'breaker':
                                if game.check_legit((pos1, pos2-1)): #check legit ของตำแหน่งเดินขึ้น
                                    img = pygame.image.load('./Assets/up.png').convert_alpha()
                                    up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                    if up_btn not in movement_btns: 
                                        movement_btns.append(up_btn) #ใส่button ไว้ใน list movement_btns

                                if game.check_legit((pos1+1, pos2)): 
                                    img = pygame.image.load('./Assets/right.png').convert_alpha()
                                    right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                    if right_btn not in movement_btns:
                                        movement_btns.append(right_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    img = pygame.image.load('./Assets/down.png').convert_alpha()
                                    down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                    if down_btn not in movement_btns:
                                        movement_btns.append(down_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    img = pygame.image.load('./Assets/left.png').convert_alpha()
                                    left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                    if left_btn not in movement_btns:
                                        movement_btns.append(left_btn)


                        if role == 'police':
                            pos1, pos2 = game.get_po_pos()
                            po_power = game.get_po_power()
                            if po_power == 'jumper':
                                if game.check_legit((pos1, pos2-1)):
                                    if not game.check_obs((pos1, pos2-1)) and not game.check_tunnel((pos1, pos2-1)): #check obs และ tunnel
                                        img = pygame.image.load('./Assets/up.png').convert_alpha()
                                        up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                        if up_btn not in movement_btns:
                                            movement_btns.append(up_btn)
                                    if game.check_obs((pos1, pos2-1)) or game.check_tunnel((pos1, pos2-1)):
                                        if game.check_legit((pos1, pos2-2)) and not game.check_obs((pos1, pos2-2)) and not game.check_tunnel((pos1, pos2-2)):
                                            img = pygame.image.load('./Assets/up.png').convert_alpha()
                                            jumpup_btn = buttons.Button(100, 600, img, 0.05, 'jumpup')
                                            if jumpup_btn not in movement_btns: 
                                                movement_btns.append(jumpup_btn)

                                if game.check_legit((pos1+1, pos2)):
                                    if not game.check_obs((pos1+1, pos2)) and not game.check_tunnel((pos1+1, pos2)):
                                        img = pygame.image.load('./Assets/right.png').convert_alpha()
                                        right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                        if right_btn not in movement_btns:
                                            movement_btns.append(right_btn)
                                    if game.check_obs((pos1+1, pos2)) or game.check_tunnel((pos1+1, pos2)):
                                        if game.check_legit((pos1+2, pos2)) and not game.check_obs((pos1+2, pos2)) and not game.check_tunnel((pos1+2, pos2)):
                                            img = pygame.image.load('./Assets/right.png').convert_alpha()
                                            jumpright_btn = buttons.Button(127, 627, img, 0.05, 'jumpright')
                                            if jumpright_btn not in movement_btns: 
                                                movement_btns.append(jumpright_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    if not game.check_obs((pos1, pos2+1)) and not game.check_tunnel((pos1, pos2+1)):
                                        img = pygame.image.load('./Assets/down.png').convert_alpha()
                                        down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                        if down_btn not in movement_btns:
                                            movement_btns.append(down_btn)
                                    if game.check_obs((pos1, pos2+1)) or game.check_tunnel((pos1, pos2+1)):
                                        if game.check_legit((pos1, pos2+2)) and not game.check_obs((pos1, pos2+2)) and not game.check_tunnel((pos1, pos2+2)):
                                            img = pygame.image.load('./Assets/down.png').convert_alpha()
                                            jumpdown_btn = buttons.Button(100, 627, img, 0.05, 'jumpdown')
                                            if jumpdown_btn not in movement_btns: 
                                                movement_btns.append(jumpdown_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    if not game.check_obs((pos1-1, pos2)) and not game.check_tunnel((pos1-1, pos2)):
                                        img = pygame.image.load('./Assets/left.png').convert_alpha()
                                        left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                        if left_btn not in movement_btns:
                                            movement_btns.append(left_btn)
                                    if game.check_obs((pos1-1, pos2)) or game.check_tunnel((pos1-1, pos2)):
                                        if game.check_legit((pos1-2, pos2)) and not game.check_obs((pos1-2, pos2)) and not game.check_tunnel((pos1-2, pos2)):
                                            img = pygame.image.load('./Assets/left.png').convert_alpha()
                                            jumpleft_btn = buttons.Button(73, 627, img, 0.05, 'jumpleft')
                                            if jumpleft_btn not in movement_btns: 
                                                movement_btns.append(jumpleft_btn)
                            
                            elif po_power == 'mortal':
                                if game.check_legit((pos1, pos2-1)):
                                    if not game.check_obs((pos1, pos2-1)) and not game.check_tunnel((pos1, pos2-1)): #check obs และ tunnel
                                        img = pygame.image.load('./Assets/up.png').convert_alpha()
                                        up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                        if up_btn not in movement_btns:
                                            movement_btns.append(up_btn)

                                if game.check_legit((pos1+1, pos2)):
                                    if not game.check_obs((pos1+1, pos2)) and not game.check_tunnel((pos1+1, pos2)):
                                        img = pygame.image.load('./Assets/right.png').convert_alpha()
                                        right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                        if right_btn not in movement_btns:
                                            movement_btns.append(right_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    if not game.check_obs((pos1, pos2+1)) and not game.check_tunnel((pos1, pos2+1)):
                                        img = pygame.image.load('./Assets/down.png').convert_alpha()
                                        down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                        if down_btn not in movement_btns:
                                            movement_btns.append(down_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    if not game.check_obs((pos1-1, pos2)) and not game.check_tunnel((pos1-1, pos2)):
                                        img = pygame.image.load('./Assets/left.png').convert_alpha()
                                        left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                        if left_btn not in movement_btns:
                                            movement_btns.append(left_btn)
                            elif po_power == 'breaker':
                                if game.check_legit((pos1, pos2-1)):
                                    if not game.check_tunnel((pos1, pos2-1)): #check obs และ tunnel
                                        img = pygame.image.load('./Assets/up.png').convert_alpha()
                                        up_btn = buttons.Button(100, 600, img, 0.05, 'up')
                                        if up_btn not in movement_btns:
                                            movement_btns.append(up_btn)

                                if game.check_legit((pos1+1, pos2)):
                                    if not game.check_tunnel((pos1+1, pos2)):
                                        img = pygame.image.load('./Assets/right.png').convert_alpha()
                                        right_btn = buttons.Button(127, 627, img, 0.05, 'right')
                                        if right_btn not in movement_btns:
                                            movement_btns.append(right_btn)

                                if game.check_legit((pos1, pos2+1)):
                                    if not game.check_tunnel((pos1, pos2+1)):
                                        img = pygame.image.load('./Assets/down.png').convert_alpha()
                                        down_btn = buttons.Button(100, 627, img, 0.05, 'down')
                                        if down_btn not in movement_btns:
                                            movement_btns.append(down_btn)

                                if game.check_legit((pos1-1, pos2)):
                                    if not game.check_tunnel((pos1-1, pos2)):
                                        img = pygame.image.load('./Assets/left.png').convert_alpha()
                                        left_btn = buttons.Button(73, 627, img, 0.05, 'left')
                                        if left_btn not in movement_btns:
                                            movement_btns.append(left_btn)

                    if t_timer >=8:
                        tm_color = (0,153,51)
                    elif t_timer >=3:
                        tm_color = (255,153,51) 
                    else:
                        tm_color =  (255,0,0)
                    text_timer =   'Your turn, '+role+': '+str(t_timer)
                    if game.pause == True:
                        text_timer = text_timer +'(p)'       
                    text_ren = font.render(text_timer, 1, tm_color) 
                    
                    win.blit(text_ren, (5,5)) #blit timer บนหน้าจอ
                elif turn != role :
                    movement_btns = []
                    move = False
            except:
                game_state = 0

        
        elif game_state == 4: #เมื่อเจอ winner จาก server
            try:
                move = False
                game_state, winner, game, players = n.send("winner") #รับตัวแปร
                draw_board(win, game.get_board(), 0, 50, 450, 5, game.c_color, game.po_skin, game.pri_skin, game.emo_po, game.emo_pri)
                winner_text = BASE_FONT.render(winner+' wins', 1, (255, 0, 0))
                win.blit(winner_text, (100, 320)) #blit winner
                pygame.display.update()
                time.sleep(1)
                win.fill((202, 228, 241))
                draw_board(win, game.get_board(), 0, 50, 450, 5, game.c_color, game.po_skin, game.pri_skin, game.emo_po, game.emo_pri)
                blit_players(win, players) #blit player กับ score
                pygame.display.update()
                time.sleep(2)
                game_state = 2 #กลับไปหน้าเลือก role
            except:
                game_state = 0
                
        pygame.display.update()