# echo-server.py
import queue
import select
import socket
import asyncio

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)


async def manipulator(reader, writer):
    while True:
        command = input()
        writer.write(bytes(command, "utf-8"))
        await writer.drain()
        if command == "disconnect":
            writer.close()
            await writer.wait_closed()
            print("Я вышел")
            break


async def main():
    server = await asyncio.start_server(
        manipulator, HOST, PORT)

    await asyncio.sleep(5)
    server.close()
    await server.wait_closed()
    # async with server:
    #     await server.wait_closed()

asyncio.run(main())

#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#     server.setblocking(False)
#     server.bind((HOST, PORT))
#     server.listen(5)  # ? почему 5
#     inputs = [server]
#     outputs = []
#     message_queues = {}
#
#     while inputs:
#         readable, writable, exceptional = select.select(inputs, outputs, inputs)
#         for s in readable:
#             if s is server:
#                 connection, client_address = s.accept()
#                 connection.setblocking(False)
#                 inputs.append(connection)
#                 message_queues[connection] = queue.Queue()
#                 with connection:
#                     print(f"Connected by {client_address}")
#                     while True:
#                         command = input()
#                         connection.sendall(bytes(command, "utf-8"))
#                         if command == "disconnect":
#                             break
#                     s.close()
        #     else:
        #         data = s.recv(1024)
        #         if data:
        #             message_queues[s].put(data)
        #             if s not in outputs:
        #                 outputs.append(s)
        #         else:
        #             if s in outputs:
        #                 outputs.remove(s)
        #             inputs.remove(s)
        #             s.close()
        #             del message_queues[s]
        #
        # for s in writable:
        #     try:
        #         next_msg = message_queues[s].get_nowait()
        #     except queue.Empty:
        #         outputs.remove(s)
        #     else:
        #         s.send(next_msg)
        #
        # for s in exceptional:
        #     inputs.remove(s)
        #     if s in outputs:
        #         outputs.remove(s)
        #     s.close()
        #     del message_queues[s]

    # conn, addr = s.accept()
    # with conn:
    #     print(f"Connected by {addr}")
    #     while True:
    #         command = input()
    #         conn.sendall(bytes(command, "utf-8"))
    #         if command == "disconnect":
    #             break
    #     s.close()
