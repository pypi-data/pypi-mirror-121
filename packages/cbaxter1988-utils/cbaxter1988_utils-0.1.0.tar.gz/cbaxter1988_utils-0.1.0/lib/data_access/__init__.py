from abc import ABC, abstractmethod

from lib.log_utils import get_logger

logger = get_logger("dao")


class DAOMixinInterface(ABC):

    @abstractmethod
    def query_items(self, query):
        """Abstract Method"""

    @abstractmethod
    def get_item(self, item_id, item_key):
        """Abstract Method"""

    @abstractmethod
    def update_item(self, item_id, new_values, item_key):
        """Abstract Method"""

    @abstractmethod
    def add_item(self, item: dict):
        """Abstract Method"""

    @abstractmethod
    def delete_item(self, item_id, item_key):
        """Abstract Method"""

    @abstractmethod
    def scan_items(self):
        """Abstract Method"""


class BaseDAO:
    pass
