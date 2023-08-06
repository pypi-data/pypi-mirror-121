import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ..._jsii import *


class EndpointServiceBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@affinidi/common-check-widget-backend-lib.commonCheckVerify.endpointServiceBase.EndpointServiceBase",
):
    def __init__(
        self,
        api_endpoint: builtins.str,
        api_key: builtins.str,
        error_code: builtins.str,
        private_key_file: builtins.str,
        secret_passphrase: builtins.str,
        request_id: builtins.str,
    ) -> None:
        '''
        :param api_endpoint: -
        :param api_key: -
        :param error_code: -
        :param private_key_file: -
        :param secret_passphrase: -
        :param request_id: -
        '''
        jsii.create(EndpointServiceBase, self, [api_endpoint, api_key, error_code, private_key_file, secret_passphrase, request_id])

    @jsii.member(jsii_name="callAPIEndpoint")
    def call_api_endpoint(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.ainvoke(self, "callAPIEndpoint", []))

    @jsii.member(jsii_name="compare")
    def compare(
        self,
        token_expected: typing.Any,
        token_compared: typing.Any,
    ) -> builtins.bool:
        '''
        :param token_expected: -
        :param token_compared: -
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "compare", [token_expected, token_compared]))

    @jsii.member(jsii_name="decrypt")
    def decrypt(self, data: typing.Any) -> builtins.str:
        '''
        :param data: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "decrypt", [data]))

    @jsii.member(jsii_name="fillOptions")
    def fill_options(self, options: typing.Any) -> None:
        '''
        :param options: -
        '''
        return typing.cast(None, jsii.invoke(self, "fillOptions", [options]))

    @jsii.member(jsii_name="generateHashFromData")
    def generate_hash_from_data(self, data_to_sign: typing.Any) -> builtins.str:
        '''
        :param data_to_sign: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateHashFromData", [data_to_sign]))

    @jsii.member(jsii_name="generateJWTFromData")
    def generate_jwt_from_data(self, data_to_sign: typing.Any) -> builtins.str:
        '''
        :param data_to_sign: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateJWTFromData", [data_to_sign]))

    @jsii.member(jsii_name="generateJWTFromDataHash")
    def generate_jwt_from_data_hash(self, data_to_sign: typing.Any) -> builtins.str:
        '''
        :param data_to_sign: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "generateJWTFromDataHash", [data_to_sign]))

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
    def get_error_message(self, error_obj: typing.Any = None) -> typing.Any:
        '''
        :param error_obj: -
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "getErrorMessage", [error_obj]))

    @jsii.member(jsii_name="retrieveApiKey")
    def retrieve_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "retrieveApiKey", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiEndpoint"))

    @api_endpoint.setter
    def api_endpoint(self, value: builtins.str) -> None:
        jsii.set(self, "apiEndpoint", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        jsii.set(self, "apiKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="errorCode")
    def error_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorCode"))

    @error_code.setter
    def error_code(self, value: builtins.str) -> None:
        jsii.set(self, "errorCode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="errors")
    def errors(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "errors"))

    @errors.setter
    def errors(self, value: typing.Any) -> None:
        jsii.set(self, "errors", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Any) -> None:
        jsii.set(self, "options", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateKeyFile")
    def private_key_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyFile"))

    @private_key_file.setter
    def private_key_file(self, value: builtins.str) -> None:
        jsii.set(self, "privateKeyFile", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="requestID")
    def request_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestID"))

    @request_id.setter
    def request_id(self, value: builtins.str) -> None:
        jsii.set(self, "requestID", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretPassphrase")
    def secret_passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretPassphrase"))

    @secret_passphrase.setter
    def secret_passphrase(self, value: builtins.str) -> None:
        jsii.set(self, "secretPassphrase", value)


class _EndpointServiceBaseProxy(EndpointServiceBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EndpointServiceBase).__jsii_proxy_class__ = lambda : _EndpointServiceBaseProxy


__all__ = [
    "EndpointServiceBase",
]

publication.publish()
