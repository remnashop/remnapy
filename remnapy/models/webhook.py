from datetime import datetime
from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from remnapy.enums import (
    TCRMEvents,
    TErrorsEvents,
    TNodeEvents,
    TResetPeriods,
    TServiceEvents,
    TSubpageConfigAction,
    TTorrentBlockerEvents,
    TUserEvents,
    TUserHwidDevicesEvents,
    TUsersStatus,
)
from remnapy.models.node_plugins import TorrentBlockerReportPayloadDto

# ---------------- SHARED ---------------- #


class WebhookMetaDto(BaseModel):
    """Extra metadata for notification-style events (null for most events)."""

    expiration: Optional[int] = None
    not_connected_after_hours: Optional[int] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- USER ---------------- #


class WebhookInternalSquadDto(BaseModel):
    """Internal squad reference (uuid + name) attached to a user"""

    uuid: UUID
    name: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookUserTrafficDto(BaseModel):
    """User traffic information for webhooks"""

    used_traffic_bytes: int
    lifetime_used_traffic_bytes: int
    online_at: Optional[datetime]
    first_connected_at: Optional[datetime]
    last_connected_node_uuid: Optional[UUID]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class BaseUserDto(BaseModel):
    """Core user fields shared by every webhook that carries a user record"""

    id: int
    short_uuid: str
    username: str
    status: TUsersStatus

    traffic_limit_bytes: float
    traffic_limit_strategy: TResetPeriods

    expire_at: datetime
    telegram_id: Optional[int]
    email: Optional[str]
    description: Optional[str]
    tag: Optional[str]
    hwid_device_limit: Optional[int]
    external_squad_uuid: Optional[UUID]

    trojan_password: str
    vless_uuid: UUID
    ss_password: str

    last_triggered_threshold: int
    sub_revoked_at: Optional[datetime]
    last_traffic_reset_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    subscription_url: str

    user_traffic: WebhookUserTrafficDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    # Backward compatibility properties
    @property
    def used_traffic_bytes(self) -> int:
        """Backward compatibility property"""
        return self.user_traffic.used_traffic_bytes

    @property
    def lifetime_used_traffic_bytes(self) -> int:
        """Backward compatibility property"""
        return self.user_traffic.lifetime_used_traffic_bytes

    @property
    def online_at(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.online_at

    @property
    def first_connected_at(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.first_connected_at

    @property
    def last_connected_node_uuid(self) -> Optional[UUID]:
        """Backward compatibility property"""
        return self.user_traffic.last_connected_node_uuid


class UserDto(BaseUserDto):
    """Full user payload for webhooks: `BaseUserDto` plus active internal squads"""

    active_internal_squads: list[WebhookInternalSquadDto]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserEventDto(BaseModel):
    """Envelope for `user.*` webhook events"""

    scope: Literal["user"]
    event: TUserEvents
    timestamp: datetime
    data: UserDto
    meta: Optional[WebhookMetaDto]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- HWID DEVICES ---------------- #


class HwidUserDeviceDto(BaseModel):
    """HWID device fingerprint attached to a user"""

    hwid: str
    user_id: int
    platform: Optional[str]
    os_version: Optional[str]
    device_model: Optional[str]
    user_agent: Optional[str]
    request_ip: Optional[str]

    created_at: datetime
    updated_at: datetime

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserHwidDeviceEventDataDto(BaseModel):
    """Data payload for `user_hwid_devices.*` webhook events"""

    user: UserDto
    hwid_user_device: HwidUserDeviceDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserHwidDeviceEventDto(BaseModel):
    """Envelope for `user_hwid_devices.*` webhook events"""

    scope: Literal["user_hwid_devices"]
    event: TUserHwidDevicesEvents
    timestamp: datetime
    data: UserHwidDeviceEventDataDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    @classmethod
    def build(
        cls,
        user: UserDto,
        hwid_device: HwidUserDeviceDto,
        event: TUserHwidDevicesEvents,
        timestamp: datetime,
    ) -> "UserHwidDeviceEventDto":
        return cls(
            scope="user_hwid_devices",
            event=event,
            timestamp=timestamp,
            data=UserHwidDeviceEventDataDto(user=user, hwid_user_device=hwid_device),
        )

    @property
    def user(self) -> UserDto:
        return self.data.user

    @property
    def hwid_user_device(self) -> HwidUserDeviceDto:
        return self.data.hwid_user_device


# ---------------- SERVICE EVENTS ---------------- #


class LoginAttemptDto(BaseModel):
    """Failed/successful login attempt details for `service.login_attempt_*` events"""

    username: str
    ip: str
    user_agent: str
    description: Optional[str] = None
    password: Optional[str] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ServiceApiTokenDto(BaseModel):
    """API token summary for `service.api_token_*` webhook events"""

    name: str
    uuid: UUID
    expire_at: datetime
    scopes: list[str]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ServiceSubpageConfigDto(BaseModel):
    """Subpage config change summary for `service.subpage_config_changed` events"""

    action: TSubpageConfigAction
    uuid: UUID

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ServiceEventDataDto(BaseModel):
    """Data payload for `service.*` webhook events; which field is populated
    depends on `event`."""

    login_attempt: Optional[LoginAttemptDto] = None
    panel_version: Optional[str] = None
    subpage_config: Optional[ServiceSubpageConfigDto] = None
    api_token: Optional[ServiceApiTokenDto] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ServiceEventDto(BaseModel):
    """Envelope for `service.*` webhook events"""

    scope: Literal["service"]
    event: TServiceEvents
    timestamp: datetime
    data: ServiceEventDataDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- NODE ENTITIES ---------------- #


class ConfigProfileInboundDto(BaseModel):
    """Inbound active on a node's config profile"""

    uuid: UUID
    profile_uuid: UUID

    tag: str
    type: str
    network: Optional[str]
    security: Optional[str]
    port: Optional[int]

    raw_inbound: Optional[dict]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookInfraProviderDto(BaseModel):
    """Infra provider hosting a node, as sent in node.* webhook events"""

    uuid: UUID
    name: str
    favicon_link: Optional[str]
    login_url: Optional[str]

    created_at: datetime
    updated_at: datetime

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookNodeConfigProfileDto(BaseModel):
    """Nested config profile for node webhook events"""

    active_config_profile_uuid: Optional[UUID]
    active_inbounds: list[ConfigProfileInboundDto]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class NodeSystemInfoDto(BaseModel):
    """Static system info reported by a node"""

    arch: str
    cpus: int
    cpu_model: str
    memory_total: float
    hostname: str
    platform: str
    release: str
    type: str
    version: str
    network_interfaces: list[str]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class NodeSystemInterfaceDto(BaseModel):
    """Per-interface network throughput counters"""

    interface: str
    rx_bytes_per_sec: float
    tx_bytes_per_sec: float
    rx_total: float
    tx_total: float

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class NodeSystemStatsDto(BaseModel):
    """Live resource usage stats reported by a node"""

    memory_free: float
    memory_used: float
    uptime: float
    load_avg: list[float]
    interface: Optional[NodeSystemInterfaceDto]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class NodeSystemDto(BaseModel):
    """System info + live stats reported by a node"""

    info: NodeSystemInfoDto
    stats: NodeSystemStatsDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class NodeVersionsDto(BaseModel):
    """Xray/node-agent versions running on a node"""

    xray: str
    node: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookNodeDto(BaseModel):
    """Node entity as sent in node.* and torrent_blocker.report webhook events"""

    uuid: UUID
    id: Optional[int] = None  # panel 3.1.0+
    name: str
    address: str
    port: Optional[int]
    proxy_url: Optional[str]
    is_connected: bool
    is_disabled: bool
    is_connecting: bool
    last_status_change: Optional[datetime]
    last_status_message: Optional[str]

    is_traffic_tracking_active: bool
    traffic_reset_day: Optional[int]
    traffic_limit_bytes: Optional[float]
    traffic_used_bytes: Optional[float]
    notify_percent: Optional[int]

    view_position: int
    country_code: str
    consumption_multiplier: float
    node_consumption_multiplier: float

    tags: list[str]

    created_at: datetime
    updated_at: datetime

    config_profile: WebhookNodeConfigProfileDto

    provider_uuid: Optional[UUID]
    provider: Optional[WebhookInfraProviderDto]

    active_plugin_uuid: Optional[UUID]
    system: Optional[NodeSystemDto]
    versions: Optional[NodeVersionsDto]

    xray_uptime: float
    users_online: float
    note: Optional[str]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    # Backward-compat shims for code that used the flat fields directly
    @property
    def active_config_profile_uuid(self) -> Optional[UUID]:
        return self.config_profile.active_config_profile_uuid

    @property
    def active_inbounds(self) -> list[ConfigProfileInboundDto]:
        return self.config_profile.active_inbounds


class NodeEventDto(BaseModel):
    """Envelope for `node.*` webhook events"""

    scope: Literal["node"]
    event: TNodeEvents
    timestamp: datetime
    data: WebhookNodeDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- ERROR EVENTS ---------------- #

# https://github.com/remnawave/backend/blob/main/src/queue/user-jobs/user-jobs.processor.ts#L224
# Not implemented yet!


class ErrorDto(BaseModel):
    """Error details payload for `errors.*` webhook events"""

    description: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class CustomErrorEventDto(BaseModel):
    """Envelope for `errors.*` webhook events"""

    scope: Literal["errors"]
    event: TErrorsEvents
    timestamp: datetime
    data: ErrorDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- CRM EVENTS ---------------- #


class BillingNodeDto(BaseModel):
    """Infra-billing node payment reminder payload for `crm.*` webhook events"""

    provider_name: str
    node_name: str
    next_billing_at: datetime
    login_url: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class CrmEventDto(BaseModel):
    """Envelope for `crm.*` webhook events"""

    scope: Literal["crm"]
    event: TCRMEvents
    timestamp: datetime
    data: BillingNodeDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- TORRENT BLOCKER EVENTS ---------------- #


class TorrentBlockerReportDto(BaseModel):
    """Torrent-blocker report bundle: node, user and blocker report payload"""

    node: WebhookNodeDto
    user: UserDto
    report: TorrentBlockerReportPayloadDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class TorrentBlockerEventDto(BaseModel):
    """Envelope for `torrent_blocker.*` webhook events"""

    scope: Literal["torrent_blocker"]
    event: TTorrentBlockerEvents
    timestamp: datetime
    data: TorrentBlockerReportDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- WEBHOOK PAYLOAD ---------------- #


class WebhookPayloadDto(BaseModel):
    """Convenience wrapper the SDK builds from any raw webhook body, exposing
    a typed `data` regardless of which of the seven event scopes it is."""

    event: str
    timestamp: datetime
    meta: Optional[WebhookMetaDto] = None
    data: Union[
        UserDto,
        WebhookNodeDto,
        HwidUserDeviceDto,
        LoginAttemptDto,
        UserHwidDeviceEventDto,
        BillingNodeDto,
        TorrentBlockerReportDto,
        dict,
    ]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    @classmethod
    def from_dict(cls, payload: dict) -> "WebhookPayloadDto":
        event = payload.get("event", "")
        data_raw = payload.get("data", {})

        timestamp_raw = payload.get("timestamp")
        if isinstance(timestamp_raw, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp_raw)
        else:
            timestamp = timestamp_raw

        if event.startswith("user."):
            data = UserDto(**data_raw)
        elif event.startswith("user_hwid_devices."):
            user = UserDto(**data_raw["user"])
            hwid_device = HwidUserDeviceDto(**data_raw["hwidUserDevice"])
            data = UserHwidDeviceEventDto.build(
                user=user,
                hwid_device=hwid_device,
                event=event,
                timestamp=timestamp,
            )
        elif event.startswith("node."):
            data = WebhookNodeDto(**data_raw)
        elif event.startswith("service."):
            if event.startswith("service.login_attempt"):
                login_attempt_data = data_raw.get("loginAttempt", {})
                data = LoginAttemptDto(**login_attempt_data)
            else:  # service.panel_started carries an empty json object
                data = data_raw
        elif event.startswith("errors."):
            data = ErrorDto(**data_raw)
        elif event.startswith("crm."):
            data = BillingNodeDto(**data_raw)
        elif event.startswith("torrent_blocker."):
            data = TorrentBlockerReportDto(**data_raw)
        else:
            data = data_raw

        meta_raw = payload.get("meta")
        meta = WebhookMetaDto(**meta_raw) if meta_raw else None

        return cls(event=event, data=data, timestamp=timestamp, meta=meta)
