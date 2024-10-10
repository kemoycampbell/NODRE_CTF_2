import socket

# The secret must be scriptkiddies
secret = "scriptkiddies"

def handle_client(client_socket):
    while True:
        # Ask them for the secret
        client_socket.send(b"What is the secret: ")
        answer = client_socket.recv(1024).decode().strip()

        # Remove scriptkiddies from the answer
        answer = answer.replace('scriptkiddies', '') #you need to get around this. If you are a true script kiddie, you will know :-)

        print(f"You answered: {answer}")

        # Check if it matches
        if answer == secret:
            # The answer is correct, show them the flag from a file
            try:
                with open("flag.txt") as file:
                    flag = file.read()
                client_socket.send(f"The flag is: {flag}\n".encode())
                client_socket.close()
                break #they got the flag so no need to ask them again
            except FileNotFoundError:
                client_socket.send(b"Flag file not found.\n")
        else:
            client_socket.send(b"I am sorry, you are not a script kiddie!!!\n")
            client_socket.send(b"Intruder!!!\n" * 3)

    client_socket.close()

def main():
    # Setup the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(1024)
    print("Server listening on port 12345")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
