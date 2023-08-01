# SERVER
import socket
import threading

    # 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

print('Ожидаем игроков...')

player1, address1 = server_socket.accept()
player2, address2 = server_socket.accept()

print(f'{address1} подключился. Ожидаем {address2} для начала игры.')

player2_confirmation = player2.recv(1024).decode()
if player2_confirmation.lower() != 'да':
    player1.sendall(bytes('Второй игрок отказался играть.', encoding='utf-8'))
    player1.close()
    player2.close()
    server_socket.close()
    exit()

player1.sendall(bytes('Игра начинается!!', encoding='utf-8'))
player2.sendall(bytes('Игра начинается!!', encoding='utf-8'))

game = [[' ' for x in range(3)] for y in range(3)]
current_player = 'X'
winner = None

def check_for_win(game):
    for i in range(3):
        if game[i][0] != ' ' and game[i][0] == game[i][1] == game[i][2]:
            return game[i][0]
        elif game[0][i] != ' ' and game[0][i] == game[1][i] == game[2][i]:
            return game[0][i]

    if game[0][0] != ' ' and game[0][0] == game[1][1] == game[2][2]:
        return game[0][0]
    elif game[0][2] != ' ' and game[0][2] == game[1][1] == game[2][0]:
        return game[0][2]

    for x in range(3):
        for y in range(3):
            if game[x][y] == ' ':
                return None
    return ' '


while not winner:
    player1.sendall(str.encode('\n'.join(['|'.join(row) for row in game])))
    player2.sendall(str.encode('\n'.join(['|'.join(row) for row in game])))

    if current_player == 'X':
        player = player1
        player_number = '1'
    else:
        player = player2
        player_number = '2'

    player.sendall(str.encode(f'Игрок {player_number}: твой ход: ', encoding='utf-8'))
    move = player.recv(1024).decode().strip()
    x, y = map(int, move.split(','))

    if game[x][y] == ' ':
        game[x][y] = current_player
        winner = check_for_win(game)
        if winner:
            if winner == ' ':
                message = 'Ничья!'
            else:
                message = f'Игрок {player_number} выиграл!'
            player1.sendall(str.encode(message))
            player2.sendall(str.encode(message))
            continue
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        player.sendall(bytes('Некорректный ход!', encoding='utf-8'))

player1.sendall(bytes('Игра закончена, сыграем еще? (да/нет): ', encoding='utf-8'))
player2.sendall(bytes('Игра закончена, сыграем еще? (да/нет): ', encoding='utf-8'))
play_again = player1.recv(1024).decode().strip().lower()
if play_again == 'да':
    player2.sendall(bytes('Игрок 1 хочет сыграть еще, а ты? (да/нет): ', encoding='utf-8'))
    play_again = player2.recv(1024).decode().strip().lower()
    if play_again != 'да':
        player2.close()
        player1.close()
        server_socket.close()
        exit()
else:
    player2.close()
    player1.close()
    server_socket.close()
    exit()

game = [[' ' for x in range(3)] for y in range(3)]
current_player = 'X'
winner = None



    # 2
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

print('Ожидаем подключения...')
client_socket, client_address = server_socket.accept()
print(f'Подключено к {client_address}')

while True:
    request = client_socket.recv(1024).decode()
    if not request:
        break

    filename, filesize = request.split(',')
    filename = filename.strip()

    client_socket.sendall(bytes('Готов к приему файла? (да/нет): ', encoding='utf-8'))
    response = client_socket.recv(1024).decode().strip().lower()
    if response != 'y':
        client_socket.sendall(bytes('Перенос отменен получателем', encoding='utf-8'))
        break

    with open(filename, 'wb') as f:
        bytes_received = 0
        while bytes_received < int(filesize):
            data = client_socket.recv(1024)
            if not data:
                break
            # Write received data to file
            f.write(data)
            bytes_received += len(data)

    client_socket.sendall(bytes('Файл передан успешно', encoding='utf-8'))

client_socket.close()
server_socket.close()


    # 3
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
PASSWORDS = {
    'user1': 'password1',
    'user2': 'password2'
}

server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Запущен сервер: {SERVER_HOST}:{SERVER_PORT}')

clients = {}

def send_all(message, sender):
    for name, sock in clients.items():
        if sock != sender:
            sock.send(message)

def handle_client(connection, address):
    name = connection.recv(1024).decode()
    password = connection.recv(1024).decode()

    if name in PASSWORDS and PASSWORDS[name] == password:
        connection.send(b'OK')
        clients[name] = connection
        message = f'{name} подключился к чату.'
        print(message)
        send_all(message.encode(), connection)
    else:
        connection.send(b'Error')
        print(f'Некорректный логин {address}')

    while True:
        try:
            message = connection.recv(1024)
            if message:
                send_all(message, connection)
            else:
                connection.close()
                del clients[name]
                message = f'{name} вышел из чата'
                print(message)
                send_all(message.encode(), connection)
                break
        except Exception as e:
            print(e)
            break

while True:
    connection, address = server_socket.accept()
    print(f'Подключение к чату: {address}')
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    client_thread.start()