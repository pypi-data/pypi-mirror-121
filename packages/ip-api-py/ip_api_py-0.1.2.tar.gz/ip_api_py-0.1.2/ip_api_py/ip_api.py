import ipaddress
import time
from typing import Optional, Union, List, Tuple

import requests

from .dt import IPInfoDt, IpFieldType

__all__ = ["IPInfoApi"]


class IPInfoApi(object):
    """
    https://ip-api.com unofficial API

    warning:
        free version API have max request limit 45 per minutes

    doc: https://ip-api.com/docs/api:json
    """

    def __init__(
        self,
        fields: List[IpFieldType],
        lang: str = "en",
        timeout_seconds: int = 30,
        wait_seconds: Optional[int] = None,
    ):
        """
        :param fields: 需要查询的字段
        :param lang: 默认的语言
        :param timeout_seconds: 查询超时时间
        :param wait_seconds: 等待查询限制时间 None 不等待
        """
        self._lang = lang
        self._fields = ",".join(fields)
        self._timeout_seconds = timeout_seconds
        self._wait_seconds = wait_seconds

    def get_ip_info(self, ip: str) -> Optional[IPInfoDt]:
        if not self._check_valid_ip(ip):
            return None

        counter = 0
        while True:
            rate_limit, info = self._try_get_ip_info(ip)
            if info is not None:
                return info
            if self._wait_seconds is not None and rate_limit:
                time.sleep(self._wait_seconds)
                counter += 1
                if counter * self._wait_seconds > 60:
                    # we have wait for 1 minutes,
                    # return None to prevent infinite wait
                    return None

    def _try_get_ip_info(self, ip: str) -> Tuple[bool, Optional[IPInfoDt]]:
        rate_limit = False
        try:
            url = f"http://ip-api.com/json/{ip}?fields={self._fields}&lang={self._lang}"
            resp: requests.Response = requests.get(url, timeout=self._timeout_seconds)
            if resp.status_code == 429:  # we hit rate limit
                rate_limit = True
            if not resp.ok:
                return rate_limit, None
            info = IPInfoDt(**resp.json())
            if not info.is_success():
                return rate_limit, None
            else:
                return rate_limit, info
        except requests.Timeout:
            return rate_limit, None

    @staticmethod
    def _check_valid_ip(ip: str) -> bool:
        """
        检查是否为有效的 公网 IP 地址
        :param ip:
        :return:
        """
        try:
            ip_a: Union[
                ipaddress.IPv4Address, ipaddress.IPv6Address
            ] = ipaddress.ip_address(ip)
            if ip_a.is_private:  # private address is ignored (MUST BE NO ANSWER)
                return False
            else:
                return True
        except ValueError:
            return False
