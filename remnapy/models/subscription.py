from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from remnapy.enums import TrafficLimitStrategy, UserStatus
from remnapy.models.hosts import HostMapperDto
from remnapy.utils.happ_crypt import create_happ_crypto_link


class HappCrypto(BaseModel):
    crypto_link: str = Field(alias="cryptoLink")


class UserLastConnectedNodeDto(BaseModel):
    connected_at: datetime = Field(alias="connectedAt")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")


class ActiveInternalSquadDto(BaseModel):
    uuid: UUID
    name: str


class UserTrafficDto(BaseModel):
    """User traffic information"""

    used_traffic_bytes: float = Field(alias="usedTrafficBytes")
    lifetime_used_traffic_bytes: float = Field(alias="lifetimeUsedTrafficBytes")
    online_at: Optional[datetime] = Field(None, alias="onlineAt")
    first_connected_at: Optional[datetime] = Field(None, alias="firstConnectedAt")
    last_connected_node_uuid: Optional[UUID] = Field(
        None, alias="lastConnectedNodeUuid"
    )


class UserResponseDto(BaseModel):
    id: Optional[int] = None
    short_uuid: str = Field(alias="shortUuid")
    username: str
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    user_traffic: UserTrafficDto = Field(alias="userTraffic")
    traffic_limit_bytes: Optional[float] = Field(None, alias="trafficLimitBytes")
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, alias="trafficLimitStrategy"
    )
    external_squad_uuid: Optional[UUID] = Field(None, alias="externalSquadUuid")
    expire_at: datetime = Field(alias="expireAt")
    sub_revoked_at: Optional[datetime] = Field(None, alias="subRevokedAt")
    last_traffic_reset_at: Optional[datetime] = Field(None, alias="lastTrafficResetAt")
    trojan_password: str = Field(alias="trojanPassword")
    vless_uuid: UUID = Field(alias="vlessUuid")
    ss_password: str = Field(alias="ssPassword")
    description: Optional[str] = None
    tag: Optional[str] = None
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    email: Optional[str] = None
    hwid_device_limit: Optional[int] = Field(None, alias="hwidDeviceLimit")
    last_triggered_threshold: int = Field(default=0, alias="lastTriggeredThreshold")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    active_internal_squads: list[ActiveInternalSquadDto] = Field(
        alias="activeInternalSquads"
    )
    subscription_url: str = Field(alias="subscriptionUrl")

    # Legacy alias for backward compatibility
    @property
    def used_traffic_bytes(self) -> float:
        """Backward compatibility property"""
        return self.user_traffic.used_traffic_bytes

    @property
    def lifetime_used_traffic_bytes(self) -> float:
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


class HwidCheckupInfo(BaseModel):
    subscription_allowed: bool = Field(alias="subscriptionAllowed")
    max_device_reached: bool = Field(alias="maxDeviceReached")
    hwid_not_supported: bool = Field(alias="hwidNotSupported")
    limit_bypassed: bool = Field(alias="limitBypassed")


class ConvertedUserInfo(BaseModel):
    days_left: int = Field(alias="daysLeft")
    traffic_limit: str = Field(alias="trafficLimit")
    traffic_used: str = Field(alias="trafficUsed")
    lifetime_traffic_used: str = Field(alias="lifetimeTrafficUsed")
    hwid_checkup: Optional[HwidCheckupInfo] = Field(None, alias="hwidCheckup")


class Passwords(BaseModel):
    ss_password: str = Field(alias="ssPassword")
    trojan_password: str = Field(alias="trojanPassword")
    vless_password: str = Field(alias="vlessPassword")


class RawHostAdditionalParams(BaseModel):
    mode: Optional[str] = None
    heartbeat_period: Optional[float] = Field(None, alias="heartbeatPeriod")


class RawHostProtocolOptions(BaseModel):
    class SSOptions(BaseModel):
        method: Optional[str] = None

    ss: Optional[SSOptions] = None


class RawHostDbData(BaseModel):
    raw_inbound: Optional[dict[str, Any]] = Field(None, alias="rawInbound")
    inbound_tag: str = Field(alias="inboundTag")
    uuid: str
    config_profile_uuid: Optional[str] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[str] = Field(
        None, alias="configProfileInboundUuid"
    )
    is_disabled: bool = Field(alias="isDisabled")
    view_position: int = Field(alias="viewPosition")
    remark: str
    is_hidden: bool = Field(alias="isHidden")
    tag: Optional[str] = None
    vless_route_id: Optional[int] = Field(None, alias="vlessRouteId")


class RawSettings(BaseModel):
    """Raw settings for network configuration"""

    header_type: Optional[str] = Field(None, alias="headerType")
    request: Optional[dict[str, Any]] = None


class RawHost(BaseModel):
    password: Passwords
    address: Optional[str] = None
    alpn: Optional[str] = None
    fingerprint: Optional[str] = None
    host: Optional[str] = None
    network: Optional[str] = None
    path: Optional[str] = None
    public_key: Optional[str] = Field(None, alias="publicKey")
    port: Optional[float] = None
    protocol: Optional[str] = None
    remark: Optional[str] = None
    short_id: Optional[str] = Field(None, alias="shortId")
    sni: Optional[str] = None
    spider_x: Optional[str] = Field(None, alias="spiderX")
    tls: Optional[str] = None
    raw_settings: Optional[RawSettings] = Field(None, alias="rawSettings")
    additional_params: Optional[RawHostAdditionalParams] = Field(
        None, alias="additionalParams"
    )
    x_http_extra_params: Optional[dict[str, Any]] = Field(
        None, alias="xHttpExtraParams"
    )
    mux_params: Optional[dict[str, Any]] = Field(None, alias="muxParams")
    sockopt_params: Optional[dict[str, Any]] = Field(None, alias="sockoptParams")
    server_description: Optional[str] = Field(None, alias="serverDescription")
    flow: Optional[str] = None
    allow_insecure: Optional[bool] = Field(None, alias="allowInsecure")
    shuffle_host: Optional[bool] = Field(None, alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, alias="mihomoX25519")
    mldsa65_verify: Optional[str] = Field(None, alias="mldsa65Verify")
    encryption: Optional[str] = None
    protocol_options: Optional[RawHostProtocolOptions] = Field(
        None, alias="protocolOptions"
    )
    db_data: Optional[RawHostDbData] = Field(None, alias="dbData")
    xray_json_template: Optional[dict[str, Any]] = Field(None, alias="xrayJsonTemplate")


class ResolvedProtocolOptions(BaseModel):
    """Protocol-specific options, shape depends on `protocol` (vless/trojan/shadowsocks/hysteria)"""

    encryption: Optional[str] = None
    id: Optional[str] = None
    flow: Optional[str] = None
    password: Optional[str] = None
    method: Optional[str] = None
    uot: Optional[bool] = None
    uot_version: Optional[int] = Field(None, alias="uotVersion")
    version: Optional[int] = None


class ResolvedHttpHeaderRequest(BaseModel):
    """HTTP request block for the `tcp` transport's `http` header camouflage"""

    version: Optional[str] = None
    method: Optional[str] = None
    path: Optional[list[str]] = None
    headers: Optional[dict[str, Any]] = None


class ResolvedHttpHeaderResponse(BaseModel):
    """HTTP response block for the `tcp` transport's `http` header camouflage"""

    version: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    headers: Optional[dict[str, Any]] = None


class ResolvedTransportHeader(BaseModel):
    """`tcp` transport header config, either `none` or `http` camouflage"""

    type: Optional[str] = None
    request: Optional[ResolvedHttpHeaderRequest] = None
    response: Optional[ResolvedHttpHeaderResponse] = None


class ResolvedTransportOptions(BaseModel):
    """Transport-specific options, shape depends on `transport` (tcp/xhttp/ws/httpupgrade/grpc/kcp/hysteria)"""

    header: Optional[ResolvedTransportHeader] = None
    path: Optional[str] = None
    host: Optional[str] = None
    mode: Optional[str] = None
    extra: Optional[dict[str, Any]] = None
    headers: Optional[dict[str, Any]] = None
    heartbeat_period: Optional[float] = Field(None, alias="heartbeatPeriod")
    authority: Optional[str] = None
    service_name: Optional[str] = Field(None, alias="serviceName")
    multi_mode: Optional[bool] = Field(None, alias="multiMode")
    client_mtu: Optional[int] = Field(None, alias="clientMtu")
    client_tti: Optional[int] = Field(None, alias="clientTti")
    congestion: Optional[bool] = None
    version: Optional[int] = None
    auth: Optional[str] = None


class ResolvedSecurityOptions(BaseModel):
    """Security-specific options, shape depends on `security` (tls/reality/none)"""

    pinned_peer_cert_sha256: Optional[str] = Field(None, alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(None, alias="verifyPeerCertByName")
    alpn: Optional[str] = None
    enable_session_resumption: Optional[bool] = Field(
        None, alias="enableSessionResumption"
    )
    fingerprint: Optional[str] = None
    server_name: Optional[str] = Field(None, alias="serverName")
    cipher_suites: Optional[str] = Field(
        None, alias="cipherSuites", description="Panel 3.2.3+."
    )
    ech_config_list: Optional[str] = Field(None, alias="echConfigList")
    ech_force_query: Optional[str] = Field(None, alias="echForceQuery")
    ech_sockopt: Optional[Any] = Field(None, alias="echSockopt")
    public_key: Optional[str] = Field(None, alias="publicKey")
    short_id: Optional[str] = Field(None, alias="shortId")
    spider_x: Optional[str] = Field(None, alias="spiderX")
    mldsa65_verify: Optional[str] = Field(None, alias="mldsa65Verify")


class ResolvedStreamOverrides(BaseModel):
    """Low-level stream overrides (final packet mask, raw socket options)"""

    final_mask: Optional[Any] = Field(alias="finalMask")
    sockopt: Optional[Any]


class ResolvedClientOverrides(BaseModel):
    """Client-side rendering overrides applied to the resolved proxy config"""

    shuffle_host: bool = Field(alias="shuffleHost")
    mihomo_x25519: bool = Field(alias="mihomoX25519")
    mihomo_ip_version: Optional[str] = Field(alias="mihomoIpVersion")
    server_description: Optional[str] = Field(alias="serverDescription")
    xray_json_template: Optional[Any] = Field(alias="xrayJsonTemplate")
    mapper: Optional[HostMapperDto] = Field(None, description="Panel 3.3.0+.")


class ResolvedProxyConfigMetadata(BaseModel):
    """Inbound/host metadata backing the resolved proxy config"""

    uuid: UUID
    tags: list[str]
    exclude_from_subscription_types: list[str] = Field(
        alias="excludeFromSubscriptionTypes"
    )
    inbound_tag: str = Field(alias="inboundTag")
    config_profile_uuid: Optional[UUID] = Field(alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[UUID] = Field(
        alias="configProfileInboundUuid"
    )
    is_disabled: bool = Field(alias="isDisabled")
    is_hidden: bool = Field(alias="isHidden")
    view_position: int = Field(alias="viewPosition")
    remark: str
    vless_route_id: Optional[int] = Field(alias="vlessRouteId")
    raw_inbound: Optional[Any] = Field(alias="rawInbound")


class ResolvedProxyConfig(BaseModel):
    """Resolved proxy config returned in raw subscription"""

    final_remark: str = Field(alias="finalRemark")
    address: str
    port: int
    protocol: str
    protocol_options: ResolvedProtocolOptions = Field(alias="protocolOptions")
    transport: str
    transport_options: ResolvedTransportOptions = Field(alias="transportOptions")
    security: str
    security_options: Optional[ResolvedSecurityOptions] = Field(
        None, alias="securityOptions"
    )
    stream_overrides: ResolvedStreamOverrides = Field(alias="streamOverrides")
    mux: Optional[dict[str, Any]]
    client_overrides: ResolvedClientOverrides = Field(alias="clientOverrides")
    metadata: ResolvedProxyConfigMetadata


class RawSubscriptionResponse(BaseModel):
    """Raw subscription response data"""

    user: UserResponseDto
    converted_user_info: ConvertedUserInfo = Field(alias="convertedUserInfo")
    headers: dict[str, str]
    resolved_proxy_configs: list[ResolvedProxyConfig] = Field(
        alias="resolvedProxyConfigs"
    )


class GetRawSubscriptionByShortUuidResponseDto(RawSubscriptionResponse):
    pass


# Legacy alias for backward compatibility
class UserSubscription(BaseModel):
    short_uuid: str = Field(alias="shortUuid")
    username: str
    days_left: float = Field(alias="daysLeft")
    traffic_used: str = Field(alias="trafficUsed")
    traffic_limit: str = Field(alias="trafficLimit")
    lifetime_traffic_used: str = Field(alias="lifetimeTrafficUsed")
    traffic_used_bytes: str = Field(alias="trafficUsedBytes")
    traffic_limit_bytes: str = Field(alias="trafficLimitBytes")
    lifetime_traffic_used_bytes: str = Field(alias="lifetimeTrafficUsedBytes")
    traffic_limit_strategy: TrafficLimitStrategy = Field(alias="trafficLimitStrategy")
    expires_at: datetime = Field(alias="expiresAt")
    user_status: UserStatus = Field(alias="userStatus")
    is_active: bool = Field(alias="isActive")


class SubscriptionInfoData(BaseModel):
    is_found: bool = Field(alias="isFound")
    user: UserSubscription
    links: list[str]
    ss_conf_links: dict[str, str] = Field(alias="ssConfLinks")
    subscription_url: str = Field(alias="subscriptionUrl")
    happ: HappCrypto


class GetSubscriptionInfoResponseDto(BaseModel):
    is_found: bool = Field(alias="isFound")
    user: UserSubscription
    links: list[str]
    ss_conf_links: dict[str, str] = Field(alias="ssConfLinks")
    subscription_url: str = Field(alias="subscriptionUrl")

    @property
    def happ(self) -> HappCrypto:
        """Generate HAPP link on the fly"""
        crypto_link = create_happ_crypto_link(self.subscription_url)
        return HappCrypto(crypto_link=crypto_link)


class SubscriptionWithoutHapp(BaseModel):
    is_found: bool = Field(alias="isFound")
    user: UserSubscription
    links: list[str]
    ss_conf_links: dict[str, str] = Field(alias="ssConfLinks")
    subscription_url: str = Field(alias="subscriptionUrl")


class GetAllSubscriptionsResponseDto(BaseModel):
    subscriptions: list[SubscriptionWithoutHapp]
    total: float


class GetSubscriptionByUsernameResponseDto(BaseModel):
    is_found: bool = Field(alias="isFound")
    user: UserSubscription
    links: list[str]
    ss_conf_links: dict[str, str] = Field(alias="ssConfLinks")
    subscription_url: str = Field(alias="subscriptionUrl")


class GetSubscriptionByShortUUIDResponseDto(GetSubscriptionByUsernameResponseDto):
    pass


class GetSubscriptionByUserIdResponseDto(GetSubscriptionByUsernameResponseDto):
    """Response for GET /api/subscriptions/by-id/{userId}"""

    pass


class GetConnectionKeysByUserIdResponseDto(BaseModel):
    enabled_keys: list[str] = Field(alias="enabledKeys")
    hidden_keys: list[str] = Field(alias="hiddenKeys")
    disabled_keys: list[str] = Field(alias="disabledKeys")

    @property
    def connection_keys(self) -> list[str]:
        """Backward compatibility: historically SDK exposed a flat list of keys."""
        return self.enabled_keys


# Legacy alias for backward compatibility
SubscriptionInfoResponseDto = GetSubscriptionInfoResponseDto
