from typing import Annotated, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnapy.enums import ALPN, MihomoIpVersion, SecurityLayer, SubscriptionType
from remnapy.models.hosts import (
    CreateHostInboundData,
    HostInternalSquadsDto,
    HostMapperDto,
    HostTag,
)


class UpdateManyHostsRequestDto(BaseModel):
    uuids: list[UUID]
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
    tags: Optional[Annotated[list[HostTag], Field(max_length=10)]] = None
    is_hidden: Optional[bool] = Field(None, serialization_alias="isHidden")
    override_sni_from_address: Optional[bool] = Field(
        None, serialization_alias="overrideSniFromAddress"
    )
    keep_blank_sni: Optional[bool] = Field(None, serialization_alias="keepSniBlank")
    vless_route_id: Optional[int] = Field(
        None, serialization_alias="vlessRouteId", ge=0, le=65535
    )
    pinned_peer_cert_sha256: Optional[str] = Field(
        None, serialization_alias="pinnedPeerCertSha256"
    )
    verify_peer_cert_by_name: Optional[str] = Field(
        None, serialization_alias="verifyPeerCertByName"
    )
    shuffle_host: Optional[bool] = Field(None, serialization_alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(
        None, serialization_alias="mihomoIpVersion"
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
        None, serialization_alias="excludeFromSubscriptionTypes"
    )
