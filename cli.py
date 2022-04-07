import socket, select, string, sys

##Formatting
def show():
    pr = "> "
    sys.stdout.write(pr)
    sys.stdout.flush()


def main():
    #if len(sys.argv) < 2:
    #    host_add = input("Enter host ip address: ")
    #else:
    #    host_add = sys.argv[1]
    host_add = "127.0.0.1"

    port_numb = 8888

    # asks for user name
    username = input("CREATING NEW ID:\nEnter username: ")
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(2)

    # connecting host
    try:
        skt.connect((host_add, port_numb))
    except:
        print("Can not connect to the server")
        sys.exit()
    
    #If connected
    skt.send(username.encode())
    show()

    while 1:
        socket_list = [sys.stdin, skt]
        
        #Access the readable list of sockets
        readList, whiteList, error_list = select.select(socket_list, [], [])

        for socks in readList:
            #Recieve message from server
            if socks == skt:
                data = socks.recv(4096)
                if not data:
                    print('\33[31m\33[1m \rDISCONNECTED!\n \33[0m')
                    sys.exit()
                else:
                    sys.stdout.buffer.write(data)
                    show()
            
            #Send message from User
            else:
                message = sys.stdin.readline()
                skt.send(message.encode(encoding='UTF-8'))
                show()


if __name__ == "__main__":
    main()
