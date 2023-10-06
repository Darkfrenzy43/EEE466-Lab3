from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SatelliteRequest(_message.Message):

    __slots__ = ["sat_id", "req_type", "thrust_angle", "thrust_dura"]

    class RequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        LOCATION_REQ: _ClassVar[SatelliteRequest.RequestType]
        TIME_REQ: _ClassVar[SatelliteRequest.RequestType]
        MOVE_REQ: _ClassVar[SatelliteRequest.RequestType]

    LOCATION_REQ: SatelliteRequest.RequestType
    TIME_REQ: SatelliteRequest.RequestType
    MOVE_REQ: SatelliteRequest.RequestType
    SAT_ID_FIELD_NUMBER: _ClassVar[int]
    REQ_TYPE_FIELD_NUMBER: _ClassVar[int]
    THRUST_ANGLE_FIELD_NUMBER: _ClassVar[int]
    THRUST_DURA_FIELD_NUMBER: _ClassVar[int]
    sat_id: int
    req_type: SatelliteRequest.RequestType
    thrust_angle: float
    thrust_dura: float

    def __init__(self, sat_id: _Optional[int] = ..., req_type: _Optional[_Union[SatelliteRequest.RequestType, str]] = ..., thrust_angle: _Optional[float] = ..., thrust_dura: _Optional[float] = ...) -> None: ...


class SatelliteResponse(_message.Message):

    __slots__ = ["loca_resp", "time_resp", "move_resp"]

    class LocationResponse(_message.Message):
        __slots__ = ["latitude", "longitude"]
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        latitude: float
        longitude: float

        def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...


    class TimeResponse(_message.Message):
        __slots__ = ["curr_time"]
        CURR_TIME_FIELD_NUMBER: _ClassVar[int]
        curr_time: int

        def __init__(self, curr_time: _Optional[int] = ...) -> None: ...


    class MoveResponse(_message.Message):
        __slots__ = ["resp_code", "updated_loca"]
        RESP_CODE_FIELD_NUMBER: _ClassVar[int]
        UPDATED_LOCA_FIELD_NUMBER: _ClassVar[int]
        resp_code: int
        updated_loca: SatelliteResponse.LocationResponse

        def __init__(self, resp_code: _Optional[int] = ..., updated_loca: _Optional[_Union[SatelliteResponse.LocationResponse, _Mapping]] = ...) -> None: ...


    LOCA_RESP_FIELD_NUMBER: _ClassVar[int]
    TIME_RESP_FIELD_NUMBER: _ClassVar[int]
    MOVE_RESP_FIELD_NUMBER: _ClassVar[int]
    loca_resp: SatelliteResponse.LocationResponse
    time_resp: SatelliteResponse.TimeResponse
    move_resp: SatelliteResponse.MoveResponse

    def __init__(self, loca_resp: _Optional[_Union[SatelliteResponse.LocationResponse, _Mapping]] = ..., time_resp: _Optional[_Union[SatelliteResponse.TimeResponse, _Mapping]] = ..., move_resp: _Optional[_Union[SatelliteResponse.MoveResponse, _Mapping]] = ...) -> None: ...
