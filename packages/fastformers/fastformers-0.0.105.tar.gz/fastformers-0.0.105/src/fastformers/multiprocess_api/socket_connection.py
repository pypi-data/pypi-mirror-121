from typing import Any

import socket
import pickle as pkl

from ..utils import logger
from .configs import Config


class SocketConnection:
    __slots__ = ('connection', 'message_size', 'alive', 'info_string')

    def __init__(self, connection: socket.socket, message_size: int, info_string: str = ''):
        self.connection = connection
        self.connection.settimeout(Config.socket_timeout)
        self.message_size = message_size
        self.alive = True
        self.info_string = ' at ' + info_string if info_string else ''

    def fileno(self) -> int:
        return self.connection.fileno()

    def close(self):
        if self.alive:
            logger.debug(f'Closing connection {self.fileno()}{self.info_string}')
            self.alive = False
            self.connection.close()

    def read_buffer(self) -> bytes:
        response = bytes()
        while True:
            buffer = self.connection.recv(self.message_size)
            if not buffer:
                raise ConnectionError(f'No response{self.info_string}, other side probably died')
            response += buffer
            if response.endswith(Config.end_delimiter):
                return response.split(Config.end_delimiter)[-2]

    def receive_message(self) -> Any:
        if not self.alive:
            raise ConnectionError(f'Trying to receive message over closed connection{self.info_string}')
        try:
            data = self.read_buffer()
            if data.startswith(Config.error_prefix):
                raise ConnectionError(data[len(Config.error_prefix):].decode('utf-8'))
            return pkl.loads(data)
        except (pkl.UnpicklingError, ConnectionError):
            self.close()
            raise

    def send_data(self, data: bytes):
        if not self.alive:
            raise ConnectionError(f'Trying to send message over closed connection{self.info_string}')
        try:
            self.connection.send(data + Config.end_delimiter)
        except ConnectionError:
            self.close()
            raise

    def send_message(self, message_id: bytes, data: Any):
        self.send_data(message_id + pkl.dumps(data))

    def send_error(self, message_id: bytes, error: str):
        self.send_data(message_id + Config.error_prefix + error.encode('utf-8'))
