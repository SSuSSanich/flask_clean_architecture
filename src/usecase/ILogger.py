from typing import List

from src.dto.ResponseLog import ResponseLog
from src.dto.SearchLogParameter import SearchLogParameter


class ILogger:
    def save_log(self, remote_id: str, user_id: int, action: str) -> None:
        raise "not implemented interface method"

    def get_logs_by_parameters(self, offset: int, parameter: SearchLogParameter) -> List[ResponseLog]:
        raise "not implemented interface method"
