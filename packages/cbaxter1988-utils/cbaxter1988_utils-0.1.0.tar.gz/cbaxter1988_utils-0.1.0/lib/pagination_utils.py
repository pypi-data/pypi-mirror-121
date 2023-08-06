from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List


class IPaginatorPage(ABC):

    @abstractmethod
    def add_item(self, item: Any):
        pass


class IPaginator(ABC):

    @abstractmethod
    def add_page(self, item: IPaginatorPage):
        pass

    @abstractmethod
    def get_page(self, page_number: int):
        pass


@dataclass(frozen=True)
class BasePage(IPaginatorPage):
    page_id: int
    items: List[Any]
    next_page: int
    previous_page: int
    item_count: int

    def __post_init__(self):
        self.next_page = self.page_id + 1
        self.previous_page = self.page_id - 1


class BasePaginator(IPaginator):

    def __init__(self, **kwargs):
        self._page_map = {}
        self._page_list = []

        self._active_page = None
        self._total_pages = None
        self.total_records = 0

    def _check_page_map_list(self):
        if len(self._page_list) == len(self._page_map.keys()):
            return True
        else:
            return False

    def add_page(self, page: BasePage):
        if self._check_page_map_list():
            self._page_map[page.page_id] = page
            self._page_list.append(page)
            return True
        else:
            print(f"Unable to add page {page}")
            return False

    def remove_page(self, page_id: int):
        page = self._page_map[page_id]
        self._page_list.remove(page)
        del self._page_map[page_id]

    def add_pages(self, pages: List[BasePage]):
        _ = [
            self.add_page(page=page)
            for page in pages
        ]

    def get_page(self, page_number: int):
        return self._page_map[page_number]

    @property
    def pages(self):
        return self._page_list

    @property
    def page_count(self):
        if len(self._page_map.keys()) == len(self.pages):
            return len(self.pages)

    def paginate(self):
        cur_page = 0
        total_pages = 10
        while cur_page <= total_pages:
            pass


@dataclass
class PaginationPage:
    cursor: Any
    next_page: int
    current_page: int
    item_count: int

    def __iter__(self):
        return self.cursor


@dataclass
class NewPage:
    cursor: Any
    last_id: str
    total_items: int

    def __iter__(self):
        return self.cursor


class PyMongoPaginator(BasePaginator):
    pass


s
