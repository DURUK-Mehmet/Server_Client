import socket
import threading
import sys

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
#Sunucudan gelen verileri bekle
#.decode, mesajı bayt cinsinden bir dizgeye dönüştürmek için kullanılır
print("-------------------------Client System-------------------------")
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("Sunucuya bağlantı sağlanamadı")
            signal = False
            break

#Get host and port
#Ana bilgisayar ve bağlantı noktası alın
host = input("Host Adresi Giriniz : ")
port = int(input("Port Numarası Giriniz : "))


#Attempt connection to server
#Sunucuya bağlanmayı dene
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Sunucu ile bağlantı kurulamadı")
    input("Çıkmak için tuşa basın")
    sys.exit(0)

#Create new thread to wait for data
#verileri beklemek için yeni thread oluştur
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()


def sezarEncrypt(message):
    encryptMessage=""
    for i in message:
        encryptMessage = encryptMessage+chr(ord(i)+5)
    return encryptMessage

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
#Sunucuya veri gönder
#str.encode, dize mesajını ağ üzerinden gönderilebilmesi için baytlara dönüştürmek için kullanılır

while True:
    message = input()
    newMessage=sezarEncrypt(message)
    sock.sendall(str.encode(newMessage))
