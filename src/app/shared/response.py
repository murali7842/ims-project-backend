from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class Response(BaseModel, Generic[T]):
    success: bool = True
    msg: str | None = None
    msg_code: str | None = None
    body: T | None = None


class PaginationResponse(BaseModel, Generic[T]):
    success: bool = True
    msg: str | None = None
    msg_code: str | None = None
    total_pages: int = 0
    total_elements: int = 0
    page_elements: int = 0
    page_number: int = 0
    size: int = 0
    body: list[T]

    def set_page_info(self, total_elements: int, page: int, size: int):
        self.page_number = page
        self.size = size
        self.page_elements = self.body.__len__()
        self.total_elements = total_elements
        self.total_pages = (self.total_elements / self.size).__ceil__()
        return self