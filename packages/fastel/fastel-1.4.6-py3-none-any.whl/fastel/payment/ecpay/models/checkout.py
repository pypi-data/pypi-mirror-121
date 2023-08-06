from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


def default_trade_date() -> str:
    now = datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S")


def default_trade_no() -> str:
    now = datetime.now()
    return str(round(now.timestamp() * 1000))


class CheckoutModel(BaseModel):
    MerchantTradeNo: str = Field(default_factory=default_trade_no)
    MerchantTradeDate: str = Field(default_factory=default_trade_date)
    TotalAmount: int
    ItemName: str = "Online Payment To Ecpay"
    TradeDesc: str = "no description"
    ChoosePayment: Literal["ALL", "Credit", "WebATM", "ATM", "CVS", "BARCODE"] = "ALL"
    BindingCard: Optional[Literal[0, 1]]
    MerchantMemberID: Optional[str]
    RelateNumber: Optional[str]
    PaymentType: str = "aio"
    InvoiceMark: Optional[Literal["Y", "N"]] = "N"
    # only fill this if InvoiceMark is Y
    TaxType: Optional[Literal["1", "2", "3", "9"]]
    ReturnURL: Optional[str]
    OrderResultURL: Optional[str]
    PaymentInfoURL: Optional[str]
    ClientRedirectURL: Optional[str]
