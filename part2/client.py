## client.py
import socket
from protocol import Protocol

class Client:
    """
    The Client class is responsible for managing the connection to the server,
    sending requests, and receiving responses.
    """

    def __init__(self, server_type: str = 'tcp', server_host: str = 'localhost', server_port: int = 12345):
        self.client_id = None
        self.socket = None
        self.server_host = server_host
        self.server_port = server_port
        self.protocol = Protocol()
        self.game_id = None

    def connect_to_server(self) -> None:
        """
        Establishes a TCP connection to the server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
        except socket.error as e:
            raise ConnectionError(f"Failed to connect to server: {e}")

    def send_password(self, password: str) -> None:
        """
        Sends the password to the server for authentication.

        Args:
            password (str): The password to authenticate with the server.
        """
        message = {'type': 'authentication', 'password': password}
        self._send_message(message)

    def request_opponents_list(self) -> None:
        """
        Requests a list of available opponents from the server.
        """
        message = {'type': 'request_opponents'}
        self._send_message(message)

    def start_game_with_opponent(self, opponent_id: str, word: str) -> None:
        """
        Requests to start a game with the specified opponent and word.

        Args:
            opponent_id (str): The identifier of the opponent to start the game with.
            word (str): The word to be guessed by the opponent.
        """
        message = {'type': 'start_game', 'opponent_id': opponent_id, 'word': word}
        self._send_message(message)

    def send_guess(self, guess: str) -> None:
        """
        Sends a guess to the server.

        Args:
            guess (str): The guess to send to the server.
        """
        message = {'type': 'guess', 'guess': guess, 'game_id': self.game_id}
        self._send_message(message)

    def send_hint(self, hint: str) -> None:
        """
        Sends a hint to the server.

        Args:
            hint (str): The hint to send to the server.
        """
        message = {'type': 'hint', 'hint': hint, 'game_id': self.game_id}
        self._send_message(message)

    def disconnect(self) -> None:
        """
        Closes the connection to the server.
        """
        if self.socket:
            try:
                self.socket.close()
            except socket.error as e:
                print(f"Error closing socket: {e}")
            finally:
                self.socket = None

    def receive_response(self) -> dict:
        """
        Receives a response from the server.

        Returns:
            dict: The decoded message from the server.
        """
        try:
            message_bytes = self.socket.recv(1024)
            if not message_bytes:
                raise ConnectionError("No response received from the server.")
            return self.protocol.decode_message(message_bytes)
        except socket.error as e:
            raise ConnectionError(f"Error receiving response from server: {e}") from e

    def _send_message(self, message: dict) -> None:
        """
        Encodes and sends a message to the server.

        Args:
            message (dict): The message to send.
        """
        try:
            encoded_message = self.protocol.encode_message(message)
            self.socket.sendall(encoded_message)
        except socket.error as e:
            raise ConnectionError(f"Failed to send message to server: {e}")

    def handle_server_response(self) -> None:
        """
        Handles responses from the server, updating the client's state as needed.
        """
        try:
            while True:
                self.display_menu()
                choice = input("Enter your choice (1-5): ")

                if choice == "1":
                    self.request_opponents_list()
                elif choice == "2":
                    opponentID = input("Enter opponent ID: ")
                    guessWord = input("Enter guess word: ")

                    self.start_game_with_opponent(opponentID, guessWord)
                elif choice == "3":
                    guess = input("Enter guess: ")

                    self.send_guess(guess)
                elif choice == "4":
                    hint = input("Enter hint: ")

                    self.send_hint(hint)
                elif choice == "5":
                    print("Exiting the client application. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
                    continue

                response = self.receive_response()
                if response['type'] == 'opponents_list':
                    print(f"Available opponents: {response['opponents']}")
                elif response['type'] == 'game_started':
                    self.game_id = response['game_id']
                    print(f"Game started with ID: {self.game_id}")
                elif response['type'] == 'guess_result':
                    if response['result'] == True:
                        print("Congratulations, you have guessed the word!")
                        self.game_id = None
                    else:
                        print("Guess is not correct")
                elif response['type'] == 'hint_acknowledged':
                    print("Hint acknowledged")
                elif response['type'] == 'hint_received':
                    print(f"Hint received: {response['hint']}")
                elif response['type'] == 'error':
                    print(f"Error from server: {response['message']}")
                else:
                    print(f"Unknown response type: {response['type']}")

                input("Press anything to continue...")
                
        except ConnectionError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def display_menu(self):
        print(f"\n===== Menu {self.client_id}=====")
        print("1. Request Opponents List")
        print("2. Start Game with Opponent")
        if (self.game_id != None):
            print("3. Send Guess")
            print("4. Send Hint")
        print("5. Quit")
        print("=================\n")

    def start(self):
        try:
            self.connect_to_server()

            # password = input("Enter password: ")
            password = "securepassword"
            self.send_password(password)

            response = self.receive_response()
            if response['type'] == 'authentication_success':
                self.client_id = response['client_id']
                print(f"Your IDS is: {self.client_id}")

                self.handle_server_response()
            else:
                print(f"Password is incorrect. Closing connection.")

        finally:
            self.disconnect()         

if __name__ == "__main__":
    # server_type = input("Enter server type (tcp/unix): ")
    # if server_type != "tcp" and server_type != "unix":
    #     print(f"Wrong server type selected.")
    #     exit()
    # server_address = input("Enter server address: ")
    # server_port = int(input("Enter server port: "))
    server_type = "tcp"
    server_address = "localhost"
    server_port = 12345
    client = Client(server_type, server_address, server_port)
    client.start()