from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InfraProviderSimpleDto(BaseModel):
    """Trimmed provider model as it appears inside billingNodes"""

    uuid: UUID
    name: str
    login_url: Optional[str] = Field(alias="loginUrl")
    favicon_link: Optional[str] = Field(alias="faviconLink")


class InfraBillingHistoryStatsDto(BaseModel):
    """Billing history statistics for a provider"""

    total_amount: float = Field(alias="totalAmount")
    total_bills: float = Field(alias="totalBills")


class InfraBillingNodeDetailsDto(BaseModel):
    """Billing node details"""

    node_uuid: UUID = Field(alias="nodeUuid")
    country_code: str = Field(alias="countryCode")


class InfraBillingNodeSimpleDto(BaseModel):
    """Trimmed billing node model as it appears inside a provider"""

    name: str
    details: Optional[InfraBillingNodeDetailsDto] = None


class InfraProviderDto(BaseModel):
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    billing_history: InfraBillingHistoryStatsDto = Field(alias="billingHistory")
    billing_nodes: list[InfraBillingNodeSimpleDto] = Field(alias="billingNodes")


class NodeDto(BaseModel):
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class InfraBillingHistoryProviderDto(BaseModel):
    """Provider as it appears inside a billing history record"""

    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(alias="faviconLink")


class InfraBillingHistoryDto(BaseModel):
    uuid: UUID
    provider_uuid: UUID = Field(alias="providerUuid")
    amount: float
    billed_at: datetime = Field(alias="billedAt")
    provider: InfraBillingHistoryProviderDto


class InfraBillingNodeDto(BaseModel):
    uuid: UUID
    node_uuid: Optional[UUID] = Field(alias="nodeUuid")
    name: Optional[str] = None
    provider_uuid: UUID = Field(alias="providerUuid")
    provider: InfraProviderSimpleDto
    node: Optional[NodeDto]
    next_billing_at: datetime = Field(alias="nextBillingAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class AvailableBillingNodeDto(BaseModel):
    """Available billing nodes"""

    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class BillingStatsDto(BaseModel):
    """Billing statistics"""

    upcoming_nodes_count: float = Field(alias="upcomingNodesCount")
    current_month_payments: float = Field(alias="currentMonthPayments")
    total_spent: float = Field(alias="totalSpent")


# Provider models
class CreateInfraProviderRequestDto(BaseModel):
    name: str
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class CreateInfraProviderResponseDto(InfraProviderDto):
    pass


class UpdateInfraProviderRequestDto(BaseModel):
    uuid: UUID
    name: Optional[str] = None
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class UpdateInfraProviderResponseDto(InfraProviderDto):
    pass


class AllInfraProvidersData(BaseModel):
    total: float = Field(alias="total")
    providers: list[InfraProviderDto]


class GetInfraProvidersResponseDto(AllInfraProvidersData):
    pass


class GetInfraProviderByUuidResponseDto(InfraProviderDto):
    pass


# Billing History models
class CreateInfraBillingHistoryRecordRequestDto(BaseModel):
    """Request to create a billing history record"""

    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    amount: float = Field(ge=0)
    billed_at: datetime = Field(serialization_alias="billedAt")


class InfraBillingHistoryData(BaseModel):
    records: list[InfraBillingHistoryDto]
    total: float


class CreateInfraBillingHistoryRecordResponseDto(InfraBillingHistoryData):
    pass


class GetInfraBillingHistoryRecordsResponseDto(InfraBillingHistoryData):
    pass


# Billing Nodes models
class CreateInfraBillingNodeRequestDto(BaseModel):
    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    node_uuid: Optional[UUID] = Field(None, serialization_alias="nodeUuid")
    name: Optional[str] = Field(None, max_length=255)
    next_billing_at: Optional[datetime] = Field(
        None, serialization_alias="nextBillingAt"
    )


# The API answers with the full billing-node list, not just the created one.
class CreateInfraBillingNodeResponseDto(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: list[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: list[AvailableBillingNodeDto] = Field(
        alias="availableBillingNodes"
    )
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class UpdateInfraBillingNodeRequestDto(BaseModel):
    uuids: list[UUID]
    next_billing_at: datetime = Field(serialization_alias="nextBillingAt")


class UpdateInfraBillingNodeResponseDto(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: list[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: list[AvailableBillingNodeDto] = Field(
        alias="availableBillingNodes"
    )
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class InfraBillingNodesData(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: list[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: list[AvailableBillingNodeDto] = Field(
        alias="availableBillingNodes"
    )
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class GetInfraBillingNodesResponseDto(InfraBillingNodesData):
    pass


# Legacy aliases
GetAllInfraProvidersResponseDto = GetInfraProvidersResponseDto
GetAllInfraBillingHistoryResponseDto = GetInfraBillingHistoryRecordsResponseDto
GetInfraBillingHistoryByUuidResponseDto = InfraBillingHistoryDto
GetAllInfraBillingNodesResponseDto = GetInfraBillingNodesResponseDto
GetInfraBillingNodeByUuidResponseDto = InfraBillingNodeDto
