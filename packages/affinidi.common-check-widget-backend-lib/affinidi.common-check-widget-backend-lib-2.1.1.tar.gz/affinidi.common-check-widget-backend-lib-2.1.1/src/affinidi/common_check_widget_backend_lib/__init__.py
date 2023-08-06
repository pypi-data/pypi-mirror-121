'''
# @affinidi/common-check-widget-backend-lib [![NPM](https://img.shields.io/npm/v/jsii-code-samples)](https://www.npmjs.com/package/@affinidi/common-check-widget-backend-lib) [![PyPI](https://img.shields.io/pypi/v/aws-jsiisamples.jsii-code-samples)](https://pypi.org/project/common-check-widget-backend-lib) [![Maven](https://img.shields.io/maven-central/v/software.aws.jsiisamples.jsii/jsii-code-samples)](https://search.maven.org/artifact/common.check.widget.backend.lib/backend-ib) [![NuGet](https://img.shields.io/nuget/v/AWSSamples.Jsii)](https://www.nuget.org/packages/CCW.Jsii%22)

> An common-check-widget-backend-lib package authored in TypeScript that gets published as GitHub packages for Node.js, Python etc

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

## Documentations

https://common-check-widget-backend-lib.affinity-project.org/
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

from .common_check_verify import CommonCheckVerify as _CommonCheckVerify_98e4d318


class CommonCheckWidget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi/common-check-widget-backend-lib.CommonCheckWidget",
):
    def __init__(self, request_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param request_id: -
        '''
        jsii.create(CommonCheckWidget, self, [request_id])

    @jsii.member(jsii_name="compareToken")
    def compare_token(
        self,
        token_expected: typing.Any,
        token_compared: typing.Any,
    ) -> builtins.bool:
        '''
        :param token_expected: -
        :param token_compared: -
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "compareToken", [token_expected, token_compared]))

    @jsii.member(jsii_name="decrypt")
    def decrypt(self, data: typing.Any) -> builtins.str:
        '''
        :param data: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "decrypt", [data]))

    @jsii.member(jsii_name="generateHashFromData")
    def generate_hash_from_data(self, data: typing.Any) -> builtins.str:
        '''
        :param data: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateHashFromData", [data]))

    @jsii.member(jsii_name="generateJWTFromData")
    def generate_jwt_from_data(self, data: typing.Any) -> builtins.str:
        '''
        :param data: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateJWTFromData", [data]))

    @jsii.member(jsii_name="generateJWTFromDataHash")
    def generate_jwt_from_data_hash(self, data: typing.Any) -> builtins.str:
        '''
        :param data: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateJWTFromDataHash", [data]))

    @jsii.member(jsii_name="generatePayloadJson")
    def generate_payload_json(
        self,
        flight_number: builtins.str,
        flight_date: builtins.str,
        first_name: builtins.str,
        last_name: builtins.str,
        date_of_birth: builtins.str,
        passport: builtins.str,
        nationality: builtins.str,
    ) -> builtins.str:
        '''
        :param flight_number: -
        :param flight_date: -
        :param first_name: -
        :param last_name: -
        :param date_of_birth: -
        :param passport: -
        :param nationality: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "generatePayloadJson", [flight_number, flight_date, first_name, last_name, date_of_birth, passport, nationality]))

    @jsii.member(jsii_name="getErrorMessage")
    def get_error_message(self, error_obj: typing.Any) -> typing.Any:
        '''
        :param error_obj: -
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "getErrorMessage", [error_obj]))

    @jsii.member(jsii_name="verifyAsync")
    def verify_async(self, obj: typing.Any) -> typing.Any:
        '''
        :param obj: -
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "verifyAsync", [obj]))

    @jsii.member(jsii_name="verifyWithCallback")
    def verify_with_callback(self, obj: typing.Any, callback: typing.Any) -> None:
        '''
        :param obj: -
        :param callback: -
        '''
        return typing.cast(None, jsii.invoke(self, "verifyWithCallback", [obj, callback]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="commonCheckVerify")
    def common_check_verify(self) -> _CommonCheckVerify_98e4d318:
        return typing.cast(_CommonCheckVerify_98e4d318, jsii.get(self, "commonCheckVerify"))

    @common_check_verify.setter
    def common_check_verify(self, value: _CommonCheckVerify_98e4d318) -> None:
        jsii.set(self, "commonCheckVerify", value)


__all__ = [
    "CommonCheckWidget",
]

publication.publish()
