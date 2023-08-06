from typing import Literal, Optional

from pydantic import BaseModel, EmailStr

CvsMapSubTypeOptions = Literal[
    "FAMI", "UNIMART", "FAMIC2C", "UNIMARTC2C", "HILIFE", "HILIFEC2C", "OKMARTC2C"
]

LogisticsTypeOptions = Literal["CVS", "Home"]

LogisticSubTypeOptions = Literal[
    "FAMI",
    "UNIMART",
    "HILIFE",
    "FAMIC2C",
    "UNIMARTC2C",
    "HILIFEC2C",
    "OKMARTC2C",
    "TCAT",
    "ECAN",
]

DistanceOptions = Literal["00", "01", "02"]
TemperatureOptions = Literal["0001", "0002", "0003"]
SpecificationOptions = Literal["0001", "0002", "0003", "0004"]
ScheduledPickupTimeOptions = Literal["1", "2", "3", "4"]
ScheduledDeliveryTimeOptions = Literal["1", "2", "3", "4", "12", "13", "23"]


class CVSMapModel(BaseModel):
    LogisticsType: Literal["CVS"] = "CVS"
    LogisticsSubType: CvsMapSubTypeOptions = "FAMI"
    IsCollection: Literal["Y", "N"]
    Device: int = 0


class LogisticModel(BaseModel):
    MerchantTradeNo: str
    MerchantTradeDate: str
    LogisticsType: LogisticsTypeOptions = "Home"
    LogisticsSubType: LogisticSubTypeOptions = "TCAT"
    GoodsName: Optional[str]
    GoodsAmount: int
    SenderName: str
    SenderPhone: str
    SenderCellPhone: Optional[str]
    SenderZipCode: str
    SenderAddress: str
    ReceiverName: str
    ReceiverCellPhone: str
    ReceiverEmail: EmailStr
    ReceiverZipCode: str
    ReceiverAddress: str
    IsCollection: Optional[bool]
    CollectionAmount: Optional[int]
    ReceiverStoreID: Optional[str]
    TradeDesc: Optional[str]
    Remark: Optional[str]

    # if LogisticsType = Home
    Distance: Optional[DistanceOptions]
    Temperature: Optional[TemperatureOptions]
    Specification: Optional[SpecificationOptions]
    ScheduledPickupTime: Optional[ScheduledPickupTimeOptions]
    ScheduledDeliveryTime: Optional[ScheduledDeliveryTimeOptions]
    ScheduledDeliveryDate: Optional[str]
    PackageCount: Optional[int]

    # only C2C
    ReturnStoreID: Optional[str]
    LogisticsC2CReplyURL: Optional[str]
