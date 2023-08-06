from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class CVSMapModel(BaseModel):
    LogisticsType: Literal["CVS"] = "CVS"
    LogisticsSubType: Literal[
        "FAMI", "UNIMART", "FAMIC2C", "UNIMARTC2C", "HILIFE", "HILIFEC2C", "OKMARTC2C"
    ] = "FAMI"
    IsCollection: Literal["Y", "N"]
    Device: int = 0


class LogisticModel(BaseModel):
    MerchantTradeNo: str
    MerchantTradeDate: str
    LogisticsType: Literal["CVS", "Home"] = "Home"
    LogisticsSubType: Literal[
        "FAMI",
        "UNIMART",
        "HILIFE",
        "FAMIC2C",
        "UNIMARTC2C",
        "HILIFEC2C",
        "OKMARTC2C",
        "TCAT",
        "ECAN",
    ] = "TCAT"
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
    Distance: Optional[Literal["00", "01", "02"]]
    Temperature: Optional[Literal["0001", "0002", "0003"]]
    Specification: Optional[Literal["0001", "0002", "0003", "0004"]]
    ScheduledPickupTime: Optional[Literal["1", "2", "3", "4"]]
    ScheduledDeliveryTime: Optional[Literal["1", "2", "3", "4", "12", "13", "23"]]
    ScheduledDeliveryDate: Optional[str]
    PackageCount: Optional[int]

    # only C2C
    ReturnStoreID: Optional[str]
    LogisticsC2CReplyURL: Optional[str]
