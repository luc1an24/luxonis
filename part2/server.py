import socket
import threading
import select
from protocol import Protocol
from game import Game
import bcrypt

class Server:
    """
    The Server class is responsible for handling incoming client connections,
    managing active games, and authenticating clients.
    """

    def __init__(self, host: str = 'localhost', port: int = 12345):
        self.host = host
        self.port = port
        self.clients = {}  # client_id: client_socket
        self.games = {}  # game_id: Game instance
        self.protocol = Protocol()
        self.server_socket = None
        # self.unix_socket = None
        self.client_id_counter = 0
        self.game_id_counter = 0
        self.lock = threading.Lock()
        # Assume hashed_password is the hashed password retrieved from a secure storage
        self.hashed_password = bcrypt.hashpw("securepassword".encode('utf-8'), bcrypt.gensalt())

    def start_server(self) -> None:
        """
        Starts the TCP/UNIX server to listen for incoming connections.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Server started on {self.host}:{self.port}")

            # self.unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            # self.unix_socket.bind(unix_socket_path)
            # self.unix_socket.listen()

            # Main server loop
            while True:
                readable, _, _ = select.select([self.server_socket], [], [], 0.1)
                for sock in readable:
                    if sock is self.server_socket:
                        client_socket, _ = self.server_socket.accept()
                        threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Server encountered an error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handles the client connection, processing incoming messages.

        Args:
            client_socket (socket.socket): The client's socket connection.
        """
        try:
            while True:
                message_bytes = client_socket.recv(1024)
                if not message_bytes:
                    break
                message = self.protocol.decode_message(message_bytes)
                self.process_client_message(client_socket, message)
        except ConnectionError:
            print("Client disconnected")
        finally:
            client_socket.close()

    def process_client_message(self, client_socket: socket.socket, message: dict) -> None:
        """
        Processes the received message from the client.

        Args:
            client_socket (socket.socket): The client's socket connection.
            message (dict): The decoded message from the client.
        """
        message_type = message.get('type')
        if message_type == 'authentication':
            self.authenticate_client(client_socket, message.get('password'))
        elif message_type == 'request_opponents':
            client_id = self.get_client_id(client_socket)
            opponents_list = self.get_opponents_list(client_id)
            response = {'type': 'opponents_list', 'opponents': opponents_list}
            self.send_message_to_client(client_socket, response)
        elif message_type == 'start_game':
            client_id = self.get_client_id(client_socket)
            opponent_id = message.get('opponent_id')
            if client_id not in self.clients or opponent_id not in self.clients:
                response = {'type': 'error', 'message': 'Invalid client or opponent ID'}
                self.send_message_to_client(client_socket, response)
                return
            self.initiate_game(client_id, opponent_id, message.get('word'))
        elif message_type == 'guess':
            game_id = message.get('game_id')
            if game_id in self.games:
                game = self.games[game_id]
                result = game.guess_word(message.get('guess'))
                response = {'type': 'guess_result', 'result': result}
                self.send_message_to_client(client_socket, response)
        elif message_type == 'hint':
            game_id = message.get('game_id')
            if game_id in self.games:
                game = self.games[game_id]
                hint = message.get('hint')
                game.add_hint(hint)
                response = {'type': 'hint_acknowledged'}
                self.send_message_to_client(client_socket, response)
                
                # response = {'type': 'hint_received', 'hint': hint}
                # opponent_id = game.get_opponent()
                # self.send_message_to_client(self.clients[opponent_id], response)
        else:
            response = {'type': 'error', 'message': f"Unknown message type: {message_type}"}
            self.send_message_to_client(client_socket, response)

    def get_client_id(self, client_socket):
        for client_id, socket in self.clients.items():
            if socket == client_socket:
                return client_id

    def authenticate_client(self, client_socket: socket.socket, password: str) -> None:
        """
        Authenticates the client using the provided password.

        Args:
            client_socket (socket.socket): The client's socket connection.
            password (str): The password provided by the client for authentication.
        """
        if bcrypt.checkpw(password.encode('utf-8'), self.hashed_password):
            client_id = self.generate_unique_id('client')
            self.clients[client_id] = client_socket
            response = {'type': 'authentication_success', 'client_id': client_id}
            self.send_message_to_client(client_socket, response)
        else:
            response = {'type': 'authentication_failure', 'message': 'Invalid password'}
            self.send_message_to_client(client_socket, response)

    def generate_unique_id(self, id_type: str) -> str:
        """
        Generates a unique identifier for a client or game.

        Args:
            id_type (str): The type of ID to generate ('client' or 'game').

        Returns:
            str: A unique identifier.
        """
        with self.lock:
            if id_type == 'client':
                self.client_id_counter += 1
                return f"client_{self.client_id_counter}"
            elif id_type == 'game':
                self.game_id_counter += 1
                return f"game_{self.game_id_counter}"
            else:
                raise ValueError("Unknown ID type specified.")

    def get_opponents_list(self, request_client_id: str) -> list:
        """
        Retrieves a list of available opponents.

        Returns:
            list: A list of client identifiers.
        """
        opponents = [client_id for client_id in self.clients.keys() if client_id != request_client_id]
        return list(opponents)

    def initiate_game(self, client_id: str, opponent_id: str, word: str) -> None:
        """
        Initiates a new game session between two clients.

        Args:
            client_id (str): The identifier of the client initiating the game.
            opponent_id (str): The identifier of the opponent.
            word (str): The word to be guessed in the game.
        """
        if opponent_id in self.games:
            response = {'type': 'error', 'message': 'Opponent is already in a game'}
            self.send_message_to_client(self.clients[client_id], response)
            return
        game_id = self.generate_unique_id('game')
        self.games[game_id] = Game()
        self.games[game_id].start_game(client_id, opponent_id, word)
        response = {'type': 'game_started', 'game_id': game_id}
        self.send_message_to_client(self.clients[client_id], response)
        self.send_message_to_client(self.clients[opponent_id], response)

    def send_message_to_client(self, client_socket: socket.socket, message: dict) -> None:
        """
        Sends a message to the client.

        Args:
            client_socket (socket.socket): The client's socket connection.
            message (dict): The message to send.
        """
        try:
            encoded_message = self.protocol.encode_message(message)
            client_socket.sendall(encoded_message)
        except socket.error as e:
            print(f"Failed to send message to client: {e}")

    def end_game(self, game_id: str) -> None:
        """
        Ends the game with the specified identifier.

        Args:
            game_id (str): The unique identifier for the game.
        """
        if game_id in self.games:
            del self.games[game_id]
            # Additional cleanup and notification to clients can be added here
