from typing import List, TypeVar, Any
from backend.response.advices.DataResponseParameter import DataResponseParameter
from backend.response.advices.ListResponseParameter import ListResponseParameter
from backend.response.advices.SliceResponseParameter import SliceResponseParameter

T = TypeVar('T')

class ResponseHelper:

    @staticmethod
    def create_response_data(data: T) -> DataResponseParameter[T]:
        return DataResponseParameter(data=data)

    @staticmethod
    def create_response_list(data: List[T]) -> ListResponseParameter[T]:
        return ListResponseParameter(data=data)


    @staticmethod
    def create_response_slice(
        data: List[T],
        total_data: int = None,
        has_next: bool = False,
        is_first: bool = False,
        is_last: bool = False,
        current_page: int = None,
        message: str = None
    ) -> SliceResponseParameter[T]:
        return SliceResponseParameter(
            data=data,
            total_data=total_data,
            has_next=has_next,
            is_first=is_first,
            is_last=is_last,
            current_page=current_page,
            message=message
        )
