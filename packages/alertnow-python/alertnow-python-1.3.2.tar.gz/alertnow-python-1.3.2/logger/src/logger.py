import sys
import requests
from datetime import datetime
import pkg_resources
import jsonpickle

from logger.src.common.dto.payload import Payload
from logger.src.common.dto.payloadDetail import PayloadDetail
from logger.src.common.dto.payloadDetailMetadata import PayloadDetailMetadata
from logger.src.common.dto.payloadDetailSdk import PayloadDetailSdk
from logger.src.common.enums.logLevel import LogLevel
from logger.src.version import __version__

with requests.Session() as session:
    session.headers.update({
        'Content-Type': 'application/json',
    })

    host = 'http://localhost:8080'
    user_api_key = None
    user_info = None
    tags = []


    def set_host(entered_host):
        global host
        host = entered_host


    def set_api_key(api_key):
        global user_api_key
        user_api_key = api_key

        session.headers.update({
            'Authorization': f'X-API-KEY {user_api_key}'
        })


    def set_user(user):
        global user_info
        user_info = user


    def set_tag(property_name, property_value):
        global tags
        tags.append({f'{property_name}': f'{property_value}'})


    def info(message, event_time_required=False):
        installed_packages = [{d.project_name: d.version} for d in pkg_resources.working_set]
        eventTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") if event_time_required else None
        sourceFilePath = str(sys._getframe().f_code.co_filename)
        methodName = str(sys._getframe(1).f_code.co_name)

        detail = [
            PayloadDetail(
                LogLevel.info.value,
                sourceFilePath,
                None,
                None,
                None,
                None,
                message,
                LogLevel.info.value,
                __version__,
                PayloadDetailMetadata(
                    sourceFilePath,
                    methodName,
                    LogLevel.info.value,
                    message
                ),
                PayloadDetailSdk(
                    __version__,
                    installed_packages
                ),
                user_info
            )
        ]

        return create_log(Payload(
            sourceFilePath,
            eventTime,
            message,
            jsonpickle.encode(tags),
            jsonpickle.encode(detail)
        ))


    def error(occurred_error, event_time_required=False):
        message = jsonpickle.encode(occurred_error)
        installed_packages = [{d.project_name: d.version} for d in pkg_resources.working_set]
        eventTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") if event_time_required else None
        sourceFilePath = str(sys._getframe().f_code.co_filename)
        methodName = str(sys._getframe(1).f_code.co_name)

        detail = [
            PayloadDetail(
                LogLevel.error.value,
                sourceFilePath,
                None,
                None,
                None,
                None,
                message,
                LogLevel.error.value,
                __version__,
                PayloadDetailMetadata(
                    sourceFilePath,
                    methodName,
                    LogLevel.error.value,
                    message
                ),
                PayloadDetailSdk(
                    __version__,
                    installed_packages
                ),
                user_info
            )
        ]

        return create_log(Payload(
            sourceFilePath,
            eventTime,
            message,
            jsonpickle.encode(tags),
            jsonpickle.encode(detail)
        ))


    def create_log(payload):
        response = session.post(f'{host}/api/integration/appinsight/v1/{user_api_key}',
                                data=jsonpickle.encode(payload))
        return response
