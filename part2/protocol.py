## protocol.py
import json
import struct

class Protocol:
    """
    The Protocol class is responsible for encoding and decoding messages
    to and from a binary format suitable for network transmission.
    """

    @staticmethod
    def encode_message(message: dict) -> bytes:
        """
        Encodes a dictionary message into bytes using JSON for the message
        content and struct for the header containing the length of the message.

        Args:
            message (dict): The message to encode.

        Returns:
            bytes: The encoded message with a header specifying the content length.
        """
        try:
            # Convert the message to JSON and then to bytes
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error encoding message to JSON: {e}")

        # Pack the length of the message as a header
        header = struct.pack('>I', len(message_bytes))

        # Return the header followed by the message
        return header + message_bytes

    @staticmethod
    def decode_message(message_bytes: bytes) -> dict:
        """
        Decodes a message from bytes to a dictionary using struct for the header
        containing the length of the message and JSON for the message content.

        Args:
            message_bytes (bytes): The message to decode.

        Returns:
            dict: The decoded message.
        """
        header_length = 4  # Length of the header in bytes (unsigned int)
        if len(message_bytes) < header_length:
            raise ValueError("Message is too short to contain a valid header.")

        message_length, = struct.unpack('>I', message_bytes[:header_length])

        # Check if the actual message length matches the length specified in the header
        if len(message_bytes) < header_length + message_length:
            raise ValueError("Message content is shorter than the specified length.")

        if len(message_bytes) > header_length + message_length:
            raise ValueError("Message content is longer than the specified length.")

        message_content = message_bytes[header_length:header_length + message_length]

        try:
            # Convert the message content from bytes to JSON and then to a dictionary
            message_json = message_content.decode('utf-8')
            message = json.loads(message_json)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"Error decoding message from JSON: {e}")

        return message
