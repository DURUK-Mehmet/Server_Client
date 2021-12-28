import socket
import threading

#Variables for holding information about connections
#Bağlantılar hakkında bilgi tutmak için Değişken
connections = []
total_connections = 0
print("-------------------------Server System-------------------------")
#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
#Client sınıfı, her bağlı istemci için oluşturulan yeni örnek
#Her örnek, öğelerle ilişkili sokete ve adrese sahiptir
#Atanan bir kimlik ve müşteri tarafından seçilen bir adla birlikte
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)


    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    #İstemciden veri almaya çalış
    #Yapamıyorsanız, istemcinin bağlantısının kesildiğini varsayın ve onu sunucu verilerinden kaldırın
    #Eğer mümkünse ve biz verileri geri alırsak, sunucuda yazdırın ve her birine geri gönderin.
    #istemci, onu gönderen istemci dışında
    #.decode, bayt verilerini yazdırılabilir bir dizeye dönüştürmek için kullanılır
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Kullanıcı " + str(self.address) + " bağlantısı koptu")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                message=str(data.decode("utf-8"))
                decryptMessage=""
                for i in message:
                    decryptMessage = decryptMessage+chr(ord(i)-5)
                print(decryptMessage)
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)



#Wait for new connections
#yeni bağlantı için bekle
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    #Get host and port
    #host ve port al

    host = input("Host Adresi Giriniz : ")
    port = int(input("Port Adresi Giriniz: "))
    #password=input("Şifre Giriniz : ")

    #Create new server socket
    #yeni server soketi oluştur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #INET internet üzerinden veri aktarımı için (genel)
    #STREAM TCP veri aktarımı için
    sock.bind((host, port))
    sock.listen(10)

    #Create new thread to wait for connections
    #bağlantıyı beklemek için yeni Thread oluştur
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()

main()
