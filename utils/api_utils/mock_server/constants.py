# Employer Profile API responses
EMPLOYER_PUBLISH_SUCCESS = {
    "status": 202,
    "headers": {
        "transactionId": "1a4bd3c0-3827-11eb-adc1-0242ac120002",
        "correlationId": "1a4bd3c0-3827-11eb-adc1-0242ac120002",
        "requestDateTime": "2025-07-08T15:41:13.581+13:00",
    },
}

EMPLOYER_PUBLISH_BAD_REQUEST = {
    "status": 400,
    "body": {
        "serviceResults": [
            {
                "result": "400",
                "message": "Missing required field: businessName",
                "resultDescription": "Bad Request",
            }
        ]
    },
}

# SEP Event API responses
SEP_MESSAGE_SUCCESS = {
    "status": 201,
    "headers": {
        "BrokerProperties": {
            "DeliveryCount": 1,
            "EnqueuedSequenceNumber": 1,
            "EnqueuedTimeUtc": "Fri, 30 May 2025 01:41:22 GMT",
            "LockToken": "827c2db9-1355-4251-a469-3bd48209ec6b",
            "LockedUntilUtc": "Fri, 30 May 2025 03:28:17 GMT",
            "MessageId": "9108224805f84885b27d8f6971c6201e",
            "SequenceNumber": 1,
            "State": "Active",
            "TimeToLive": 1209600,
        }
    },
    "body": {
        "header": {
            "eventType": "CREATE",
            "eventDateTime": "2025-07-08T15:41:13.581+13:00",
            "sourceSystem": "CMS",
            "transactionId": "1a4bd3c0-3827-11eb-adc1-0242ac120002",
        },
        "data": {
            "businessName": "Test Employer Ltd",
            "tradingName": "Test Trading Name",
            "industry": {
                "highLevel": "Accommodation and Food Services",
                "lowLevel": "Food Services",
                "className": "Restaurant Services",
            },
            "identities": [
                {
                    "identifier": "1234567890",
                    "type": {"code": "IRD", "description": "IRD Number"},
                }
            ],
            "status": {"code": "ACTIVE", "description": "Active"},
        },
    },
}

SEP_NO_MESSAGES = {"status": 204}

SEP_INVALID_SUBSCRIPTION = {
    "status": 410,
    "body": {"message": "Specified queue or subscription doesn't exist."},
}

SEP_MESSAGE_DELETED = {"status": 200}

SEP_MESSAGE_NOT_FOUND = {
    "status": 404,
    "body": {"message": "No message was found with the specified MessageId or LockToken."},
}

SEP_MESSAGE_UNLOCKED = {"status": 200}
