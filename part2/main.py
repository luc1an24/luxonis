import threading
from server import Server
from web_interface import WebInterface

# Define the main function to start the server and the web interface
def main():
    # Instantiate the Server
    server = Server()

    # Define callback functions for the WebInterface
    def get_game_data_callback(game_id):
        if game_id in server.games:
            game = server.games[game_id]
            return {
                'word': game.word,
                'hints': game.hints,
                'attempts': game.attempts
            }
        return None

    def update_game_data_callback(game_id, hint):
        if game_id in server.games:
            game = server.games[game_id]
            game.add_hint(hint)
            return True
        return False

    # Instantiate the WebInterface with callbacks
    web_interface = WebInterface(get_game_data_callback, update_game_data_callback)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()

    # Start the web interface
    web_interface.run()

# Check if the script is run directly
if __name__ == "__main__":
    main()
