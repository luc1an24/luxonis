## web_interface.py
from flask import Flask, jsonify, request
from typing import Callable, Optional

class WebInterface:
    """
    The WebInterface class is responsible for providing a web-based interface
    to interact with the game server. It uses Flask to run a simple web server.
    """

    def __init__(self, get_game_data: Callable[[str], Optional[dict]], update_game_data: Callable[[str, str], bool]):
        """
        Initializes the WebInterface with callback functions to interact with the game server.

        Args:
            get_game_data (Callable[[str], Optional[dict]]): Callback to get game data.
            update_game_data (Callable[[str, str], bool]): Callback to update game data with a new hint.
        """
        self.app = Flask(__name__)
        self.get_game_data = get_game_data
        self.update_game_data = update_game_data

    def run(self, host: str = 'localhost', port: int = 5000) -> None:
        """
        Starts the Flask web server.

        Args:
            host (str): The hostname to listen on. Defaults to 'localhost'.
            port (int): The port of the web server. Defaults to 5000.
        """
        self._register_routes()
        self.app.run(host=host, port=port)

    def _register_routes(self) -> None:
        """
        Registers the routes for the Flask web server.
        """
        @self.app.route('/game/<game_id>', methods=['GET'])
        def get_game(game_id: str):
            """
            Endpoint to get the current state of a game.

            Args:
                game_id (str): The unique identifier of the game.

            Returns:
                Response: JSON containing the game state or error message.
            """
            game_data = self.get_game_data(game_id)
            if game_data:
                return jsonify(game_data), 200
            else:
                return jsonify({'error': 'Game not found'}), 404

        @self.app.route('/game/<game_id>/hint', methods=['POST'])
        def add_hint(game_id: str):
            """
            Endpoint to add a hint to a game.

            Args:
                game_id (str): The unique identifier of the game.

            Returns:
                Response: JSON containing the acknowledgement or error message.
            """
            hint = request.json.get('hint')
            if not hint:
                return jsonify({'error': 'No hint provided'}), 400

            if self.update_game_data(game_id, hint):
                return jsonify({'message': 'Hint added successfully'}), 200
            else:
                return jsonify({'error': 'Failed to add hint or game not found'}), 404
