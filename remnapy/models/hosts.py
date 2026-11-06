from typing import Annotated, Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, RootModel, StringConstraints

from remnapy.enums import (
    ALPN,
    InternalSquadsMode,
    MihomoIpVersion,
    SecurityLayer,
    SubscriptionType,
)

HostTag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]


class HostInternalSquadsDto(BaseModel):
    """Which internal squads see the host (panel 3.4.0+)."""

    mode: InternalSquadsMode
    squads: list[UUID] = Field(default_factory=list)


class HostMapperOperationDto(BaseModel):
    """One rewrite of the config generated for the host (panel 3.3.0+)."""

    model_config = ConfigDict(populate_by_name=True)

    op: Literal["copy", "set", "unset"]
    to: str
    from_: Optional[str] = Field(None, alias="from")
    value: Optional[Any] = None


class HostMapperDto(BaseModel):
    """Per-client rewrites of the config generated for the host (panel 3.3.0+)."""

    model_config = ConfigDict(populate_by_name=True)

    xray_json: Optional[list[HostMapperOperationDto]] = Field(None, alias="xrayJson")
    mihomo: Optional[list[HostMapperOperationDto]] = None
    singbox: Optional[list[HostMapperOperationDto]] = None
    base64: Optional[list[HostMapperOperationDto]] = None


class ReorderHostItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderHostRequestDto(BaseModel):
    hosts: list[ReorderHostItem]


class HostInboundData(BaseModel):
    config_profile_uuid: Optional[UUID] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[UUID] = Field(
        None, alias="configProfileInboundUuid"
    )


class CreateHostInboundData(BaseModel):
    config_profile_uuid: UUID = Field(serialization_alias="configProfileUuid")
    config_profile_inbound_uuid: UUID = Field(
        serialization_alias="configProfileInboundUuid"
    )


class UpdateHostRequestDto(BaseModel):
    uuid: UUID
    inbound: Optional[CreateHostInboundData] = None
    remark: Annotated[Optional[str], StringConstraints(max_length=40)] = None
    address: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    is_disabled: Optional[bool] = Field(None, serialization_alias="isDisabled")
    security_layer: Optional[SecurityLayer] = Field(
        None, serialization_alias="securityLayer"
    )
    server_description: Optional[str] = Field(
        None, serialization_alias="serverDescription", max_length=30
    )
    tags: Optional[Annotated[list[HostTag], Field(max_length=10)]] = None
    is_hidden: Optional[bool] = Field(None, serialization_alias="isHidden")
    override_sni_from_address: Optional[bool] = Field(
        None, serialization_alias="overrideSniFromAddress"
    )
    keep_blank_sni: Optional[bool] = Field(None, serialization_alias="keepSniBlank")
    vless_route_id: Optional[int] = Field(
        None, serialization_alias="vlessRouteId", ge=0, le=65535
    )
    shuffle_host: Optional[bool] = Field(None, serialization_alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(
        None, serialization_alias="mihomoIpVersion"
    )
    xhttp_extra_params: Optional[dict[str, Any]] = Field(
        None, serialization_alias="xhttpExtraParams"
    )
    mux_params: Optional[dict[str, Any]] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[dict[str, Any]] = Field(
        None, serialization_alias="sockoptParams"
    )
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    pinned_peer_cert_sha256: Optional[str] = Field(
        None, serialization_alias="pinnedPeerCertSha256"
    )
    verify_peer_cert_by_name: Optional[str] = Field(
        None, serialization_alias="verifyPeerCertByName"
    )
    nodes: Optional[list[UUID]] = None
    xray_json_template_uuid: Optional[UUID] = Field(
        None, serialization_alias="xrayJsonTemplateUuid"
    )
    excluded_internal_squads: Optional[list[UUID]] = Field(
        None,
        serialization_alias="excludedInternalSquads",
        description="Panel before 3.4.0; ignored by 3.4.0+, use internal_squads.",
    )
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None,
        serialization_alias="internalSquads",
        description="Panel 3.4.0+. Replaces excluded_internal_squads.",
    )
    mapper: Optional[HostMapperDto] = Field(None, description="Panel 3.3.0+.")
    exclude_from_subscription_types: Optional[list[SubscriptionType]] = Field(
        None,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid if self.inbound else None


class HostResponseDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    remark: str
    address: str
    port: int
    path: str | None = Field(alias="path")
    sni: str | None = Field(alias="sni")
    host: str | None = Field(alias="host")
    alpn: str | None = Field(alias="alpn")
    fingerprint: str | None = Field(alias="fingerprint")
    xhttp_extra_params: dict[str, Any] | None = Field(alias="xhttpExtraParams")
    mux_params: dict[str, Any] | None = Field(alias="muxParams")
    sockopt_params: dict[str, Any] | None = Field(alias="sockoptParams")
    final_mask: Any | None = Field(None, alias="finalMask")
    inbound: HostInboundData
    server_description: str | None = Field(alias="serverDescription")
    tags: list[str] = Field(default_factory=list, alias="tags")
    vless_route_id: int | None = Field(alias="vlessRouteId")
    pinned_peer_cert_sha256: str | None = Field(None, alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: str | None = Field(None, alias="verifyPeerCertByName")
    shuffle_host: bool = Field(alias="shuffleHost")
    mihomo_x25519: bool = Field(alias="mihomoX25519")
    mihomo_ip_version: MihomoIpVersion | None = Field(None, alias="mihomoIpVersion")
    nodes: list[UUID]
    is_disabled: bool = Field(False, alias="isDisabled")
    security_layer: SecurityLayer = Field(SecurityLayer.DEFAULT, alias="securityLayer")
    is_hidden: bool = Field(False, alias="isHidden")
    override_sni_from_address: bool = Field(False, alias="overrideSniFromAddress")
    keep_blank_sni: bool = Field(False, alias="keepSniBlank")
    xray_json_template_uuid: UUID | None = Field(alias="xrayJsonTemplateUuid")
    excluded_internal_squads: list[UUID] = Field(
        default_factory=list,
        alias="excludedInternalSquads",
        description="Panel before 3.4.0; empty on 3.4.0+, see internal_squads.",
    )
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None, alias="internalSquads", description="Panel 3.4.0+."
    )
    mapper: Optional[HostMapperDto] = Field(None, description="Panel 3.3.0+.")
    exclude_from_subscription_types: list[SubscriptionType] = Field(
        default_factory=list,
        alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host is excluded.",
    )

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid


class CreateHostRequestDto(BaseModel):
    inbound: CreateHostInboundData
    remark: Annotated[str, StringConstraints(min_length=1, max_length=40)]
    address: str
    port: int
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    xhttp_extra_params: Optional[dict[str, Any]] = Field(
        None, serialization_alias="xhttpExtraParams"
    )
    mux_params: Optional[dict[str, Any]] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[dict[str, Any]] = Field(
        None, serialization_alias="sockoptParams"
    )
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    server_description: Optional[str] = Field(
        None, serialization_alias="serverDescription", max_length=30
    )
    tags: Annotated[list[HostTag], Field(max_length=10)] = Field(default_factory=list)
    vless_route_id: Optional[int] = Field(
        None, serialization_alias="vlessRouteId", ge=0, le=65535
    )
    pinned_peer_cert_sha256: Optional[str] = Field(
        None, serialization_alias="pinnedPeerCertSha256"
    )
    verify_peer_cert_by_name: Optional[str] = Field(
        None, serialization_alias="verifyPeerCertByName"
    )
    shuffle_host: bool = Field(False, serialization_alias="shuffleHost")
    mihomo_x25519: bool = Field(False, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(
        None, serialization_alias="mihomoIpVersion"
    )
    nodes: list[UUID] = Field(default_factory=list)
    is_disabled: bool = Field(False, serialization_alias="isDisabled")
    security_layer: SecurityLayer = Field(
        SecurityLayer.DEFAULT, serialization_alias="securityLayer"
    )
    is_hidden: bool = Field(False, serialization_alias="isHidden")
    override_sni_from_address: bool = Field(
        False, serialization_alias="overrideSniFromAddress"
    )
    keep_blank_sni: bool = Field(False, serialization_alias="keepSniBlank")
    xray_json_template_uuid: Optional[UUID] = Field(
        None, serialization_alias="xrayJsonTemplateUuid"
    )
    excluded_internal_squads: list[UUID] = Field(
        default_factory=list,
        serialization_alias="excludedInternalSquads",
        description="Panel before 3.4.0; ignored by 3.4.0+, use internal_squads.",
    )
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None,
        serialization_alias="internalSquads",
        description="Panel 3.4.0+. Replaces excluded_internal_squads.",
    )
    mapper: Optional[HostMapperDto] = Field(None, description="Panel 3.3.0+.")
    exclude_from_subscription_types: list[SubscriptionType] = Field(
        default_factory=list,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid

    def __init__(
        self,
        inbound_uuid: Optional[UUID] = None,
        config_profile_uuid: Optional[UUID] = None,
        **data,
    ):
        # Backward-compatible support for misspelled helper argument used in old tests/examples
        if config_profile_uuid is None and "config_profile_inbound_uuid" in data:
            config_profile_uuid = data.pop("config_profile_inbound_uuid")

        if inbound_uuid is not None and "inbound" not in data:
            data["inbound"] = CreateHostInboundData(
                config_profile_uuid=config_profile_uuid
                or UUID("107541f1-ae1a-4e2d-9dec-7297557b5125"),
                config_profile_inbound_uuid=inbound_uuid,
            )
        super().__init__(**data)


class GetAllHostTagsResponseDto(BaseModel):
    tags: list[str]


# Response wrappers
class CreateHostResponseDto(HostResponseDto):
    """Create host response"""

    pass


class UpdateHostResponseDto(CreateHostResponseDto):
    """Update host response"""

    pass


class GetAllHostsResponseDto(RootModel[list[HostResponseDto]]):
    root: list[HostResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


class GetOneHostResponseDto(HostResponseDto):
    """Get one host response"""

    pass


class ReorderHostResponseDto(BaseModel):
    """Reorder hosts response"""

    is_updated: bool = Field(alias="isUpdated", default=True)


class HostsResponseDto(HostResponseDto):
    """Host response data with backward compatibility properties"""

    @property
    def allow_insecure(self) -> bool:
        """Backward compatibility property"""
        return self.security_layer == SecurityLayer.NONE
