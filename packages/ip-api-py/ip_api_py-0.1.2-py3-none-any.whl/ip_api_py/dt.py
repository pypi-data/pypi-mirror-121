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
    message: Optional[str] = Field(None, title="错误消息", description="只有失败的时候才有此字段")
    continent: Optional[str] = Field(None, title="大陆")
    continentCode: Optional[str] = Field(None, title="大陆代码")
    country: Optional[str] = Field(None, title="国家")
    countryCode: Optional[str] = Field(None, title="国家代码")
    region: Optional[str] = Field(None, title="区域")
    regionName: Optional[str] = Field(None, title="区域名称")
    city: Optional[str] = Field(None, title="城市")
    district: Optional[str] = Field(None, title="地区")
    zip: Optional[str] = Field(None, title="邮编")
    lat: Optional[float] = Field(None, title="经度")
    lon: Optional[float] = Field(None, title="纬度")
    timezone: Optional[str] = Field(None, title="时区")
    offset: Optional[int] = Field(None, title="Timezone UTC DST offset in seconds")
    currency: Optional[str] = Field(None, title="货币")
    isp: Optional[str] = Field(None, title="ISP")
    org: Optional[str] = Field(None, title="组织")
    as_: Optional[str] = Field(None, title="AS", alias="as")
    asname: Optional[str] = Field(None, title="as 名称")
    reverse: Optional[str] = Field(None, title="")
    mobile: Optional[bool] = Field(None, title="手机IP")
    proxy: Optional[bool] = Field(None, title="代理IP")
    hosting: Optional[bool] = Field(None, title="服务器IP")

    def is_success(self) -> bool:
        if self.message is None:
            return True
        return False
