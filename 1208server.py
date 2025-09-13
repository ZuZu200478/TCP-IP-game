import socket
import threading
import time  
import random

# 存儲玩家的暱稱
nicknames = []  
avatar_images = []  
lock = threading.Lock()  # 用於保護共享資源

# 問題資料庫
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


# 追蹤遊戲分數
scores = [0, 0]
players = []  # 玩家連接的客戶端
questions =random.sample(question_bank, 10)  # 隨機選擇10道問題


# 檢查玩家是否已全部連接
def all_players_connected():
    return len(players) == 2

# 發送等待畫面
def send_waiting_screen():
    for player in players:
        try:
            player.send("Waiting for the other player to connect...".encode('utf-8'))
        except:
            pass

# 發送問題給所有玩家
def send_question_to_all(question_idx):
    for i, client_socket in enumerate(players):
        try:
            question_text = f"Question {question_idx+1}: {questions[question_idx]['question']}\n"
            choices_text = "\n".join([f"{idx+1}. {choice}" for idx, choice in enumerate(questions[question_idx]['choices'])])
            full_message = question_text + choices_text
            print(f"Sending to player {i}: {full_message}")
            client_socket.send(full_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending question to player {i}: {e}")

# 處理玩家的回答並檢查答案
def handle_response(client_socket, player_id, question_idx):
    try:
        client_socket.settimeout(10)  # 設置10秒的超時
        response = client_socket.recv(1024).decode('utf-8')
        if response:
            print(f"Received response from player {player_id}: {response}")
            answer_idx = int(response)
            if answer_idx == questions[question_idx]['answer']:
                scores[player_id] += 1
                client_socket.send("正確".encode('utf-8'))
            else:
                client_socket.send("錯誤".encode('utf-8'))
        else:
            print(f"No response from player {player_id} within 10 seconds.")
            client_socket.send("No response. Moving to next question.".encode('utf-8'))
    except Exception as e:
        print(f"No response or timeout from player {player_id}. Exception: {e}")
        client_socket.send("No response. Moving to next question.".encode('utf-8'))

# 遊戲邏輯
def game_thread():
    for question_idx in range(len(questions)):
        send_question_to_all(question_idx)  # Send question to all players

        threads = []
        for i in range(len(players)):
            thread = threading.Thread(target=handle_response, args=(players[i], i, question_idx))
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()  # Wait for all threads to finish

        time.sleep(1)  # Delay between questions

    # Send final scores  avatar_images
    final_scores = f"Game Over!\nScores:\n{nicknames[0]}: {scores[0]}:{avatar_images[0]}\n{nicknames[1]}: {scores[1]}:{avatar_images[1]}"
    for player in players:
        try:
            player.send(final_scores.encode('utf-8'))
        except:
            print("Could not send final results to player")

    # Disconnect all players
    for player in players:
        try:
            player.close()
        except:
            print("Error while closing player connection")

    players.clear()  # Clear the player list
    print("All players disconnected. Waiting for new connections...")
    start_server()



# 處理客戶端的連接
def handle_client(client_socket, address, player_id):
    client_socket.send("Welcome! Please enter your nickname:".encode('utf-8'))
    nickname = client_socket.recv(1024).decode('utf-8').strip()
    avatar_image = client_socket.recv(1024).decode('utf-8').strip()
    nicknames.append(nickname)
    print(f"Player {player_id} connected with nickname: {nickname}")

# 啟動伺服器
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)
    print("Server is waiting for connections...")
    player_nicknames = {}
    player_avatar_images = {}
    # 等待兩位玩家連接
    while len(players) < 2:
        client_socket, address = server_socket.accept()
        print(f"Player connected from {address}")
        data = client_socket.recv(1024).decode('utf-8').strip()
        nickname, avatar_image = data.split('|')  # 根據分隔符分開暱稱和大頭貼路徑
        print(f"Player {nickname} connected.") 
        print(f"Player {avatar_image} connected.")
        
        player_nicknames[client_socket] = nickname
        player_avatar_images[client_socket]= avatar_image
        avatar_images.append(avatar_image)
        nicknames.append(nickname)
        print(f"Player {client_socket} connected.") 
        players.append(client_socket)
        print(f"Player {nickname} connected.") 
        print(f"Player {avatar_image} connected.")

        # 如果還有玩家在等待，顯示等待畫面
        if len(players) < 2:
            send_waiting_screen()

    # 當兩位玩家連接後，開始遊戲
    if all_players_connected():
        print("Both players connected. Starting game...")
        threading.Thread(target=game_thread).start()

if __name__ == "__main__":
    start_server()