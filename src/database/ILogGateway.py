from typing import List

from src.dto.LogInfo import LogInfo
from src.dto.ResponseLog import ResponseLog
from src.dto.SearchLogParameter import SearchLogParameter


class ILogGateway:
    def save_log(self, log_info: LogInfo) -> None:
        raise "not implemented interface method"

    def get_logs(self, count: int, offset: int) -> List[ResponseLog]:
        raise "not implemented interface method"