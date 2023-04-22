from datetime import datetime
from typing import List

import pytz

from config import TIMEZONE
from src.database.ILogGateway import ILogGateway
from src.dto.LogInfo import LogInfo
from src.dto.ResponseLog import ResponseLog
from src.dto.SearchLogParameter import SearchLogParameter
from src.usecase.ILogger import ILogger


class SimpleLogger(ILogger):
    def __init__(self, log_gateway: ILogGateway):
        self.__log_gateway = log_gateway

    def save_log(self, remote_id: str, user_id: int, action: str) -> None:
        vladivostok_timezone = pytz.timezone(TIMEZONE)
        now = datetime.now(vladivostok_timezone)

        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second

        date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        log_info = LogInfo(
            remote_id,
            date,
            user_id,
            action
        )

        self.__log_gateway.save_log(log_info)

    def get_logs_by_parameters(self, offset: int, parameter: SearchLogParameter) -> List[ResponseLog]:
        logs_count = 10
        response_log_list: List[ResponseLog] = self.__log_gateway.get_logs(logs_count, offset)
        # check parameters and request new items if necessary
        return response_log_list