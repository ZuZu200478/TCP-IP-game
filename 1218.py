import pygame
import sys
from pygame.locals import *
from tkinter import filedialog
import tkinter as tk
import random
import time
import socket
import os


# 初始化 pygame
pygame.init()

# 視窗大小
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("選擇遊戲模式")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 字型
font = pygame.font.Font("msjhbd.ttc", 50)
input_font = pygame.font.Font("msjhbd.ttc", 40)

# 初始暱稱與頭像
nickname = ""
avatar_image = "usg.jpg"



# 輸入框類別
class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.active = False
        self.text_surface = input_font.render(self.text, True, BLUE)
        self.cursor = '_'
        self.timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(f"暱稱: {self.text}")
                    nickname=self.text
                    return True
                else:
                    self.text += event.unicode
                self.text_surface = input_font.render(self.text, True, BLUE)

        return False

    def update(self):
        self.timer += 1
        if self.timer > 30:
            self.timer = 0
            self.cursor = '' if self.cursor == '_' else '_'
            self.text_surface = input_font.render(self.text + self.cursor, True, BLUE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))


# 按鈕類別
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color_inactive = (255, 246, 198)
        self.color_active = (169, 169, 169)
        self.color = self.color_inactive
        self.text_surface = input_font.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
                                        self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def choose_avatar():
    pygame.init()
    # 設置窗口大小和標題
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("選擇圖片")

    # 圖片目錄（假設圖片存放在當前目錄下的 "images" 文件夾中）
    image_dir = "images"
    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f in ["eight.jpg", "eight1.jpg", "eight2.jpg", "gikw1.png","gikw2.png", "gikw.png", "usg.jpg", "usg1.jpg", "usg2.jpg", "HH.jpg", "kk1.jpg", "go.jpg"]]

    # 加載圖片
    if not images:
        print("沒有圖片可供選擇！")
        pygame.quit()
        return None

    image_data = []
    for image_path in images:
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, (150, 150))  # 調整圖片大小為 150x150
        image_data.append((img, image_path))

    # 布局參數
    cols = 4  # 每行顯示的圖片數量
    spacing = 20  # 圖片之間的間距
    start_x = (screen_width - (150 * cols + spacing * (cols - 1))) // 2
    start_y = 50

    running = True
    selected_image = None

    while running:
        # 填充背景顏色
        screen.fill((255, 255, 255))

        # 繪製圖片
        for idx, (img, path) in enumerate(image_data):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (150 + spacing)
            y = start_y + row * (150 + spacing)
            screen.blit(img, (x, y))

            # 滑鼠高亮和點擊檢測
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if x <= mouse_x <= x + 150 and y <= mouse_y <= y + 150:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, 150, 150), 5)  # 綠框高亮
                if pygame.mouse.get_pressed()[0]:  # 左鍵點擊
                    selected_image = path
                    running = False
                    break

        # 更新屏幕
        pygame.display.flip()

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    
    return selected_image

# 顯示問題與倒計時
def show_question_and_timer(question, choices, answer, screen, clock):
    font = pygame.font.Font("msjhbd.ttc", 40)
    score = 0
    start_time = time.time()

    buttons = []
    for i, option in enumerate(choices):
        button = Button(screen_width // 2 - 150, 200 + i * 60, 300, 50, option)
        buttons.append(button)

    # 設置作答頁面的背景
    answer_background = pygame.image.load('answer_background.jpg')  # 加載背景圖片
    answer_background = pygame.transform.scale(answer_background, (screen_width, screen_height))  # 調整大小

    while True:
        screen.fill(WHITE)
        screen.blit(answer_background, (0, 0))  # 繪製背景圖片

        question_text = font.render(question, True, BLACK)
        screen.blit(question_text, (screen_width // 2 - question_text.get_width() // 2, 100))

        for button in buttons:
            button.draw(screen)

        elapsed_time = int(time.time() - start_time)
        time_left = max(0, 10 - elapsed_time)
        timer_text = font.render(f"剩餘時間: {time_left}s", True, BLACK)
        screen.blit(timer_text, (screen_width // 2 - timer_text.get_width() // 2, screen_height - 50))

        if time_left == 0:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_clicked(event.pos):
                        if i == answer:
                            score = 1
                            answer_text = font.render("正確", True, GREEN)
                        else:
                            answer_text = font.render("錯誤", True, RED)
                        # 顯示答案訊息並暫停
                        screen.blit(answer_text, (screen_width // 2 - answer_text.get_width() // 2, 50))
                        pygame.display.flip()
                        pygame.time.delay(1000)  # 暫停 1 秒
                        return score

        pygame.display.flip()
        clock.tick(30)

    return score
# 顯示結束頁面並新增返回主頁面按鈕
def show_end_screen(nickname, avatar_image, score):
    clock = pygame.time.Clock()
    # 設置結束頁面的背景
    end_background = pygame.image.load('end_background.jpg')  # 加載背景圖片
    end_background = pygame.transform.scale(end_background, (screen_width, screen_height))  # 調整大小


    # 按鈕：返回主頁面
    back_to_main_button = Button(400, 500, 200, 50, "返回主頁面")

    while True:
        screen.blit(end_background, (0, 0))  # 繪製背景圖片

        title = font.render("遊戲結束", True, BLACK)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        if avatar_image:
            avatar = pygame.image.load(avatar_image)
            avatar = pygame.transform.scale(avatar, (150, 150))
            screen.blit(avatar, (screen_width // 2 - 75, 150))

        nickname_text = font.render(f"暱稱: {nickname}", True, BLACK)
        screen.blit(nickname_text, (screen_width // 2 - nickname_text.get_width() // 2, 320))

        score_text = font.render(f"分數: {score}", True, BLACK)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 400))

        # 畫出「返回主頁面」按鈕
        back_to_main_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main_button.is_clicked(event.pos):  # 按下返回主頁面按鈕
                    return 'back_to_main'  # 返回主頁面

        pygame.display.flip()
        clock.tick(30)

def start_multiplayer_game(nickname, avatar_image):
    # 連接伺服器
    def connect_to_server():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        return client_socket

    def display_question_and_choices(question, choices):
        # 加載並調整背景圖片
        answer_background = pygame.image.load('answer_background.jpg')
        answer_background = pygame.transform.scale(answer_background, (screen_width, screen_height))
        screen.blit(answer_background, (0, 0))  # 繪製背景圖片

        # 繪製問題文字
        question_surface = input_font.render(question, True, BLACK)
        screen.blit(question_surface, (screen.get_width() // 2 - question_surface.get_width() // 2, 120))

        # 繪製選項按鈕（無文字）和獨立的選項文字
        buttons = []
        option_rects = []
        for i, choice in enumerate(choices):
            # 按鈕繪製（不包含文字）
            button = Button(screen_width // 2 - 150, 200 + i * 60, 300, 50, "")
            buttons.append(button)
            button.draw(screen)

            # 選項文字獨立繪製
            choice_surface = input_font.render(choice, True, BLACK)
            rect = choice_surface.get_rect(center=(screen_width // 2, 225 + i * 60))
            screen.blit(choice_surface, rect.topleft)
            option_rects.append(rect)

        return option_rects



    def display_timer(seconds_left):
        pygame.draw.rect(screen, WHITE, (0, 0, 350, 55))  # 擦除計時器區域
        timer_surface = input_font.render(f"Time left: {seconds_left}s", True, RED)
        screen.blit(timer_surface, (10, 10))

    client_socket = connect_to_server()
    data = f"{nickname}|{avatar_image}"
    client_socket.send(data.encode('utf-8'))
    #client_socket.send(nickname.encode('utf-8'))  # 發送暱稱到伺服器
    #client_socket.send(avatar_image.encode('utf-8'))  # 發送大頭貼到伺服器
    print(f"Player {avatar_image} connected.")
    game_over = False

    while not game_over:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if "Game Over" in message:
                end_background = pygame.image.load('end_background.jpg')  # 加载新的背景图片
                end_background = pygame.transform.scale(end_background, (screen_width, screen_height))  # 调整大小
                screen.blit(end_background, (0, 0))  # 绘制背景图片

                end_surface = input_font.render(message, True, BLACK)
                screen.blit(end_surface, (screen.get_width() // 2 - end_surface.get_width() // 2, screen.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(5000)
                game_over = True
                break

            if "Question" in message:
                lines = message.split("\n")
                question_text = lines[0]
                choices = lines[1:]
                option_rects = display_question_and_choices(question_text, choices)

                answered = False
                start_time = time.time()

                while not answered:
                    elapsed_time = time.time() - start_time
                    remaining_time = max(0, 10 - int(elapsed_time))
                    if remaining_time == 0:  # 時間到，發送超時訊息，切換下一題
                        client_socket.send("timeout".encode('utf-8'))
                        answered = True
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            for i, rect in enumerate(option_rects):
                                if rect.collidepoint(mouse_pos):
                                    client_socket.send(str(i).encode('utf-8'))
                                    answered = True
                                    break

                    # 更新計時器並刷新屏幕
                    display_timer(remaining_time)
                    pygame.display.flip()
                feedback = client_socket.recv(1024).decode('utf-8')
                feedback_surface = font.render(feedback, True, GREEN if "正確" in feedback else RED)
                screen.blit(feedback_surface, (screen.get_width() // 2 - feedback_surface.get_width() // 2, screen.get_height() // 10))
                pygame.display.flip()
                pygame.time.delay(1000)

        except Exception as e:
            print(f"Error: {e}")
            break
    # 在游戏结束后，重新连接到服务器开始新一轮
    client_socket.close()
    game()  # 再次调用main_game()来重新开始游戏


# 主循環修改
def main():
    global nickname, avatar_image
    input_box = InputBox(400, 200, 200, 60)
    single_player_button = Button(400, 300, 200, 50, "單人遊戲")
    multi_player_button = Button(400, 380, 200, 50, "多人遊戲")
    choose_avatar_button = Button(400, 460, 200, 50, "選擇頭像")

    clock = pygame.time.Clock()
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    while True:
        screen.blit(background_image, (0, 0))
        title = font.render("知識王", True, BLACK)
        screen.blit(title, (430, 80))

        if avatar_image:
            avatar = pygame.image.load(avatar_image)
            avatar = pygame.transform.scale(avatar, (200, 200))
            screen.blit(avatar, (150, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if input_box.handle_event(event):
                nickname = input_box.text
                print(f"暱稱: {nickname}")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_button.is_hovered(event.pos):
                    return 'single', nickname, avatar_image
                if multi_player_button.is_hovered(event.pos):
                    return 'multi', nickname, avatar_image
                if choose_avatar_button.is_hovered(event.pos):
                    pygame.time.delay(100)
                    avatar_image = choose_avatar()

        input_box.update()
        input_box.draw(screen)

        single_player_button.draw(screen)
        multi_player_button.draw(screen)
        choose_avatar_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

question_bank = [
    {"question": "世界上最大的動物是?", "choices": ["大象", "藍鯨", "長頸鹿", "鯊魚"], "answer": 1},
    {"question": "太陽系中哪顆行星最靠近太陽?", "choices": ["地球", "金星", "水星", "火星"], "answer": 2},
    {"question": "電腦的中央處理單元（CPU）是什麼?", "choices": ["內存", "硬碟", "處理器", "顯示卡"], "answer": 2},
    {"question": "人類第一顆進入太空的衛星名稱是?", "choices": ["阿波羅11號", "月球一號", "探測者1號", "斯普特尼克1號"], "answer": 3},
    {"question": "地球的重力加速度是多少?", "choices": ["9.8 m/s²", "10 m/s²", "8.9 m/s²", "9.5 m/s²"], "answer": 0},
    {"question": "哪一位物理學家提出了相對論?", "choices": ["牛頓", "愛因斯坦", "霍金", "居里夫人"], "answer": 1},
    {"question": "中國的首都是哪個城市?", "choices": ["上海", "廣州", "北京", "成都"], "answer": 2},
    {"question": "世界上最大的沙漠是哪個?", "choices": ["撒哈拉沙漠", "戈壁沙漠", "阿拉伯沙漠", "卡拉哈里沙漠"], "answer": 0},
    {"question": "人類大腦的主要成分是?", "choices": ["水", "脂肪", "蛋白質", "糖"], "answer": 0},
    {"question": "誰發明了電話?", "choices": ["托馬斯·愛迪生", "亞歷山大·貝爾", "尼古拉·特斯拉", "艾倫·圖靈"], "answer": 1},
    {"question": "地球的表面大約有多少百分比被水覆蓋?", "choices": ["50%", "60%", "70%", "80%"], "answer": 2},
    {"question": "世界上最長的河流是?", "choices": ["亞馬遜河", "尼羅河", "長江", "密西西比河"], "answer": 1},
    {"question": "哪種動物被稱為‘沙漠之船’?", "choices": ["駱駝", "羊", "牛", "馬"], "answer": 0},
    {"question": "地球上最大的島嶼是哪個?", "choices": ["格陵蘭島", "新幾內亞島", "蘇門答臘島", "加那利群島"], "answer": 0},
    {"question": "世界上最大的城市是哪一個?", "choices": ["上海", "東京", "紐約", "倫敦"], "answer": 1},
    {"question": "世界上最小的國家是?", "choices": ["摩納哥", "聖馬力諾", "梵蒂岡", "列支敦士登"], "answer": 2},
    {"question": "哪位作家創作了《哈利·波特》系列?", "choices": ["J.R.R.托爾金", "J.K.羅琳", "喬治·馬丁", "阿基米德"], "answer": 1},
    {"question": "數學符號π代表什麼?", "choices": ["圓周率", "數字7", "平方根", "對數"], "answer": 0},
    {"question": "人類的基因組包含多少對染色體?", "choices": ["23", "24", "22", "21"], "answer": 0},
    {"question": "世界上最大的體育賽事是哪個?", "choices": ["奧運會", "世界杯", "美洲杯", "歐洲杯"], "answer": 0},
    {"question": "哪一種動物是唯一能夠飛行的哺乳類?", "choices": ["蝙蝠", "鴿子", "企鵝", "鷹"], "answer": 0},
    {"question": "太陽是一顆什麼類型的恆星?", "choices": ["紅巨星", "藍巨星", "白矮星", "黃矮星"], "answer": 3},
    {"question": "世界上最深的海洋是?", "choices": ["太平洋", "大西洋", "印度洋", "北冰洋"], "answer": 0},
    {"question": "法國的國旗顏色是?", "choices": ["紅、白、藍", "紅、黃、藍", "綠、白、紅", "藍、白、紅"], "answer": 3},
    {"question": "有關愛因斯坦的哪個成就最為著名?", "choices": ["發明相對論", "發明電燈", "發明電話", "創立量子力學"], "answer": 0},
    {"question": "東京的知名地標是?", "choices": ["東京塔", "大阪塔", "京都塔", "名古屋塔"], "answer": 0},
    {"question": "發明了第一部汽車的工程師是?", "choices": ["亨利·福特", "卡尔·本茨", "查爾斯·達爾文", "克勞斯·梅茨"], "answer": 1},
    {"question": "鮮花‘玫瑰’的顏色有?", "choices": ["紅色、黃色、白色", "紅色、紫色、藍色", "黃色、白色、綠色", "白色、綠色、紫色"], "answer": 0},
    {"question": "現代化的空氣交通工具是哪一種?", "choices": ["飛機", "汽車", "火車", "船"], "answer": 0},
    {"question": "曼哈頓在哪個國家?", "choices": ["美國", "加拿大", "英國", "澳大利亞"], "answer": 0},
    {"question": "標準國際單位制（SI）的基本單位中，哪一個代表長度?", "choices": ["米", "秒", "安培", "千克"], "answer": 0},
    {"question": "‘奧林匹克運動會’的起源在哪個國家?", "choices": ["希臘", "法國", "英國", "德國"], "answer": 0},
    {"question": "大部分地球的水來自?", "choices": ["大海", "湖泊", "江河", "冰川"], "answer": 0},
    {"question": "地球上的三大陸是哪三個?", "choices": ["亞洲、非洲、歐洲", "美洲、非洲、亞洲", "美洲、亞洲、歐洲", "非洲、歐洲、大洋洲"], "answer": 2}
    ]

# 遊戲邏輯
def game():
    mode, nickname, avatar_image = main()

    if mode == 'single':

    # 隨機選擇 10 題
        questions = random.sample(question_bank, 10)

        score = 0
        for q in questions:
            score += show_question_and_timer(q["question"], q["choices"], q["answer"], screen, pygame.time.Clock())
            time.sleep(1)

        result = show_end_screen(nickname, avatar_image, score)

        # 如果結果是返回主頁面，則重新開始
        if result == 'back_to_main':
            game()

    elif mode == 'multi':
        print(f"{nickname} 正在進行多人遊戲...")
        # 開始多人遊戲邏輯
        start_multiplayer_game(nickname, avatar_image)

# Client code
if __name__ == "__main__":
    game()
