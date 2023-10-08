import asyncio
import websockets
import requests
from typing import Callable, Dict, Optional
import threading

class ChatClient:
    """    
    Args:
        client_id (str): The client ID of the Twitch application.
        client_secret (str): The client secret of the Twitch application.
        channel_name (str): The name of the Twitch channel to connect to.

    Attributes:
        client_id (str): The client ID of the Twitch application.
        client_secret (str): The client secret of the Twitch application.
        channel_name (str): The name of the Twitch channel to connect to.
        URI (str): The URI for connecting to Twitch chat.
        oauth_token (str): The OAuth token used for authentication.
        message_callbacks (Dict[str, Callable]): A dictionary to store message callbacks.
    """
    
    def __init__(self, client_id: str, client_secret: str, channel_name: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.channel_name = channel_name
        self.URI = "wss://irc-ws.chat.twitch.tv:443"
        self.oauth_token = self._get_oauth_token()
        self.message_callbacks: Dict[str, Callable] = {}

    def _get_oauth_token(self) -> str:
        """
        Get an OAuth token using client credentials.
        
        Returns:
            str: The OAuth token.
        """
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, params=params)
        data = response.json()
        return data.get("access_token")

    async def _connect_to_socket(self):
        """
        Connect to the Twitch chat using WebSockets and handle incoming messages.
        """
        async with websockets.connect(self.URI) as ws:
            await ws.send("PASS oauth:" + self.oauth_token)
            await ws.send("NICK justinfan12345")
            await ws.send("JOIN #" + self.channel_name)
            while True:
                response = await ws.recv()
                self._check_for_phrase(response)

    def _check_for_phrase(self, response: str):
        """
        Check if the incoming message contains a registered phrase and trigger the callback.
        
        Args:
            response (str): The incoming chat message.
        """
        for phrase, callback in self.message_callbacks.items():
            if self._message_contains_phrase(response, phrase):
                print("Found phrase: " + response)
                msg_data = { 
                    "message": response.split(" :")[1],
                    "chatter": response.split("#")[1].split(" :")[0]
                }
                callback(msg_data)

    def _message_contains_phrase(self, message: str, phrase: str) -> bool:
        """
        Check if the message contains the specified phrase.
        
        Args:
            message (str): The chat message to check.
            phrase (str): The phrase to look for.
        
        Returns:
            bool: True if the phrase is found in the message, False otherwise.
        """
        return phrase in message
    
    def add_message_callback(self, phrase: str, callback: Callable):
        """
        Register a callback function for a specific chat message phrase.
        
        Args:
            phrase (str): The phrase to trigger the callback.
            callback (callable): The callback function to execute when the phrase is found.
        """
        self.message_callbacks[phrase] = callback

    def start(self):
        """
        Start the chat client by connecting to Twitch chat and handling incoming messages.
        """
        asyncio.run(self._connect_to_socket())

class ChatClientThreaded:
    def __init__(self, client_id: str, client_secret: str, channel_name: str):
        self.chat_client = ChatClient(client_id, client_secret, channel_name)
        self.thread = threading.Thread(target=self._run_client)

    def _run_client(self):
        self.chat_client.start()

    def start(self):
        self.thread.start()

    def stop(self):
        self.chat_client.stop()  # You'll need to implement a stop method in your ChatClient if needed.
        self.thread.join()

    def add_message_callback(self, phrase: str, callback: Callable):
        """
        Register a callback function for a specific chat message phrase.
        
        Args:
            phrase (str): The phrase to trigger the callback.
            callback (callable): The callback function to execute when the phrase is found.
        """
        self.chat_client.add_message_callback(phrase, callback)