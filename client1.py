# CLIENT 1
import socket
import os

    # 1
server_address = 'localhost'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, 12345))

print(client_socket.recv(1024).decode())

response = input('Начинаем игру? (да/нет): ')
client_socket.sendall(str.encode(response))
if response.lower().lower() != 'да':
    client_socket.close()
    exit()

print(client_socket.recv(1024).decode())
while True:
    print(client_socket.recv(1024).decode())
    move = input('Твой ход: ')
    client_socket.sendall(str.encode(move))
    response = client_socket.recv(1024).decode()
    print(response)
    if 'Player' in response:
        break

play_again = input('Сыграем еще? (да/нет): ')
client_socket.sendall(str.encode(play_again))
play_again_confirmation = client_socket.recv(1024).decode().strip().lower()
if play_again_confirmation.lower() == 'да':
    print(client_socket.recv(1024).decode())
    response = input('Сыграем еще? (да/нет): ')
    client_socket.sendall(str.encode(response))
    if response.lower().lower() != 'да':
        client_socket.close()
        exit()
else:
    client_socket.close()
    exit()


    # 2
server_address = 'localhost'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, 12345))

filename = input('Введите путь к файлу: ')
filesize = os.path.getsize(filename)

client_socket.sendall(f'{filename},{filesize}'.encode())

response = input(client_socket.recv(1024).decode())
if response.lower() != 'да':
    print('Файл перенесен на сервер')
    client_socket.close()
    exit()

with open(filename, 'rb') as f:
    bytes_sent = 0
    while bytes_sent < filesize:
        data = f.read(1024)
        if not data:
            break
        client_socket.sendall(data)
        bytes_sent += len(data)

print(client_socket.recv(1024).decode())

client_socket.close()


    #3
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

print('Подключение к серверу...')

name = input('Введите свой логин: ')
client_socket.send(name.encode())

# вводим пароль пользователя
password = input('Введите свой пароль: ')
client_socket.send(password.encode())

response = client_socket.recv(1024)
if response != b'OK':
    print('Некорректные данные.')
    client_socket.close()
    exit()

while True:
    try:
        message = input()
        client_socket.send(message.encode())
        print(message)
    except KeyboardInterrupt:
        client_socket.close()
        exit()



