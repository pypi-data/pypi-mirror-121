import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .endpoint_service_base import EndpointServiceBase as _EndpointServiceBase_6aa74fa3


class CommonCheckVerify(
    _EndpointServiceBase_6aa74fa3,
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi/common-check-widget-backend-lib.commonCheckVerify.CommonCheckVerify",
):
    def __init__(self, request_id: builtins.str) -> None:
        '''
        :param request_id: -
        '''
        jsii.create(CommonCheckVerify, self, [request_id])

    @jsii.member(jsii_name="fillObj")
    def fill_obj(self, obj: typing.Any) -> None:
        '''
        :param obj: -
        '''
        return typing.cast(None, jsii.invoke(self, "fillObj", [obj]))

    @jsii.member(jsii_name="generateJWT")
    def generate_jwt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateJWT", []))

    @jsii.member(jsii_name="generateOptions")
    def generate_options(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.ainvoke(self, "generateOptions", []))

    @jsii.member(jsii_name="generateResponse")
    def generate_response(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.ainvoke(self, "generateResponse", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="obj")
    def obj(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "obj"))

    @obj.setter
    def obj(self, value: typing.Any) -> None:
        jsii.set(self, "obj", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Any) -> None:
        jsii.set(self, "options", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="requestID")
    def request_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestID"))

    @request_id.setter
    def request_id(self, value: builtins.str) -> None:
        jsii.set(self, "requestID", value)


__all__ = [
    "CommonCheckVerify",
]

publication.publish()
