from typing import Optional, Literal

from pydantic import BaseModel, Field

IpFieldType = Literal[
    "query",
    "status",
    "continent",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "isp",
    "query",
    "lat",
    "lon",
]


class IPInfoDt(BaseModel):
    query: Optional[str] = Field(None, title="IP地址", description="查询的IP地址")
    status: Optional[str] = Field(None, title="状态")
    continent: Optional[str] = Field(None, title="大洋")
    country: Optional[str] = Field(None, title="国家")
    countryCode: Optional[str] = Field(None, title="国家代码")
    region: Optional[str] = Field(None, title="区域")
    regionName: Optional[str] = Field(None, title="区域名称")
    city: Optional[str] = Field(None, title="城市")
    isp: Optional[str] = Field(None, title="ISP")
    lat: Optional[float] = Field(None, title="经度")
    lon: Optional[float] = Field(None, title="纬度")

    def is_success(self) -> bool:
        return self.status == "success"
