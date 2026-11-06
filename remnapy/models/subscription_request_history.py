from datetime import datetime

from pydantic import BaseModel, Field


class SubscriptionRequestHistoryRecord(BaseModel):
    id: int
    user_id: int = Field(alias="userId")
    srr_response_type: str | None = Field(
        None, alias="srrResponseType", description="Panel 3.1.0+."
    )
    srr_rule_name: str | None = Field(None, alias="srrRuleName")
    request_ip: str | None = Field(alias="requestIp")
    user_agent: str | None = Field(alias="userAgent")
    request_at: datetime = Field(alias="requestAt")


class SubscriptionRequestHistoryData(BaseModel):
    records: list[SubscriptionRequestHistoryRecord]
    total: int


class GetAllSubscriptionRequestHistoryResponseDto(SubscriptionRequestHistoryData):
    pass


class AppStatItem(BaseModel):
    app: str
    count: float


class HourlyRequestStat(BaseModel):
    date_time: datetime = Field(alias="dateTime")
    request_count: float = Field(alias="requestCount")


class SubscriptionRequestHistoryStatsData(BaseModel):
    by_parsed_app: list[AppStatItem] = Field(alias="byParsedApp")
    hourly_request_stats: list[HourlyRequestStat] = Field(alias="hourlyRequestStats")


class GetSubscriptionRequestHistoryStatsResponseDto(
    SubscriptionRequestHistoryStatsData
):
    pass
