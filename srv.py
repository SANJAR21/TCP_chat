import socket, select,sys


##Forward user message to all connected users
def send_all(socks, message):
    for sockets in connect_list:
        #If message not forwarded
        if sockets != server_socket and sockets != socks:
            try:
                sockets.send(message)
            except:
                #Connection still not available
                sockets.close()
                connect_list.remove(sockets)


if __name__ == "__main__":
    #Address of username
    store = {}
    name = ""
    use = 0
    #List for storing socket descriptors
    connect_list = []
    buffer = 4096
    port_numb = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("127.0.0.1", port_numb))

    server_socket.listen(1000)  # listen atmost 1000 connection at one time
    
    #Adding server socket to readable list of connections
    connect_list.append(server_socket)

    print( "\33[32m \t\t\t\tSERVER WORKING \33[0m")

    while 1:
        #List of sockets readable using select
        readList, whiteList, error_sockets = select.select(connect_list, [], [])

        for socks in readList:
            #New user connection
            if socks == server_socket:
                #New user recieved through through server socket
                socketfd, addr = server_socket.accept()
                name = socketfd.recv(buffer)
                connect_list.append(socketfd)
                store[addr] = ""
                #If username is repeated
                if name.decode() in store.values():
                    socketfd.send("Username already taken!".encode(encoding='UTF-8'))
                    del store[addr]
                    connect_list.remove(socketfd)
                    socketfd.close()
                    continue
                else:
                    #Adding address and name
                    use =use+1
                    store[addr] = name.decode()
                    print("Client (%s, %s) entered " % addr, " [", store[addr], "] ( "+str(use)+" users online)")
                    se = "Connected to the chat server ("+str(use) +" user online)\n"
                    socketfd.send(se.encode(encoding='UTF-8'))
                    de = " entered the conversation( "+str(use)+" users online)\n"
                    send_all(socketfd, name+ de.encode(encoding='UTF-8'))
            #Handle message from client
            else:
                #Recieving data from client
                try:
                    data1 = socks.recv(buffer)
                    new = data1.decode()
                    data = new[:new.index("\n")]
                    print(name.decode()+":"+data)
                    #Address of client who is sending message
                    i, p = socks.getpeername()
                    try:
                        if data == "bye":
                            use = use - 1
                            msg = store[(i, p)] + " left the conversation( " + str(use) + " users online)" + "\n"
                            send_all(socks, msg.encode(encoding='UTF-8'))
                            print("Client (%s, %s) is offline" % (i, p), " [", store[(i, p)], "]")
                            del store[(i, p)]
                            connect_list.remove(socks)
                            socks.close()
                            continue

                        else:
                            message = store[(i, p)] + ": " + data + "\n"
                            send_all(socks, message.encode(encoding='UTF-8'))
                    except KeyboardInterrupt:
                        print("exit")
                        sys.exit()


                # unexpected user exit
                except:
                    use = use-1
                    (i, p) = socks.getpeername()
                    send_all(socks,store[(i, p)] + " left the conversation unexpectedly( "+use+" users online)\n")
                    print("Client (%s, %s) is offline (error)" % (i, p), " [", store[(i, p)], "]\n")
                    del store[(i, p)]
                    connect_list.remove(socks)
                    socks.close()
                    continue

    server_socket.close()
