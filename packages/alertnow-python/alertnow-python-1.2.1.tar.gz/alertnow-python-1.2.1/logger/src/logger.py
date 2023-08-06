import json
import sys

import requests
from datetime import datetime
import pkg_resources

from logger.src.common.configuration.httpClientConfig import HttpClientConfig
from logger.src.common.dto.payload import Payload
from logger.src.common.dto.payloadDetail import PayloadDetail
from logger.src.common.dto.payloadDetailMetadata import PayloadDetailMetadata
from logger.src.common.dto.payloadDetailSdk import PayloadDetailSdk

from logger.src.common.enums.logLevel import LogLevel

with requests.Session() as session:
    session.headers.update({
        'Content-Type': 'application/json',
    })

    apiKey = None
    userInfo = None
    tags = []

    def set_api_key(api_key):
        apiKey = api_key

        session.headers.update({
            'Authorization': f'X-API-KEY {apiKey}'
        })

    def set_user(user):
        userInfo = user

    def set_tag(property_name, property_value):
        tags.insert({ property_name: property_value })

    def info(message, eventTimeRequired = False):
        installed_packages = [{d.project_name: d.version} for d in pkg_resources.working_set]
        print('installed_packages => ', installed_packages)

        eventTime = eventTimeRequired if datetime.now().strftime("%m/%d/%Y, %H:%M:%S") else None
        print('eventTime => ', eventTime)

        sourceFilePath = sys._getframe().f_code
        print('sourceFilePath => ', sourceFilePath)

        methodName = sys._getframe(1).f_code.co_name
        print('methodName => ', methodName)

        version = pkg_resources.require('alertnow-phyton')[0].version
        print('version => ', version)
        detail = [
            PayloadDetail(
                LogLevel.info,
                sourceFilePath,
                None,
                None,
                None,
                None,
                message,
                LogLevel.info,
                version,
                PayloadDetailMetadata(
                    sourceFilePath,
                    methodName,
                    LogLevel.info,
                    message
                ),
                PayloadDetailSdk(
                    version,
                    installed_packages
                )
            )
        ]

        return create_log(Payload(
            sourceFilePath,
            eventTime,
            message,
            json.dumps(vars(tags)),
            json.dumps(vars(detail))
        ))

    def error(occurred_error):
        message = json.dumps(vars(occurred_error))

        installed_packages = [{d.project_name: d.version} for d in pkg_resources.working_set]
        print('installed_packages => ', installed_packages)

        eventTime = eventTimeRequired if datetime.now().strftime("%m/%d/%Y, %H:%M:%S") else None
        print('eventTime => ', eventTime)

        sourceFilePath = sys._getframe().f_code
        print('sourceFilePath => ', sourceFilePath)

        methodName = sys._getframe(1).f_code.co_name
        print('methodName => ', methodName)

        version = pkg_resources.require('alertnow-phyton')[0].version
        print('version => ', version)
        detail = [
            PayloadDetail(
                LogLevel.error,
                sourceFilePath,
                None,
                None,
                None,
                None,
                message,
                LogLevel.error,
                version,
                PayloadDetailMetadata(
                    sourceFilePath,
                    methodName,
                    LogLevel.error,
                    message
                ),
                PayloadDetailSdk(
                    version,
                    installed_packages
                )
            )
        ]

        return create_log(Payload(
            sourceFilePath,
            eventTime,
            message,
            json.dumps(vars(tags)),
            json.dumps(vars(detail))
        ))

    def create_log(payload):
        response = session.post(f'{HttpClientConfig.alertNowURL}/integration/appinsight/v1/{apiKey}',
                                data=json.dumps(vars(payload)))
        return response
