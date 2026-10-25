from types import SimpleNamespace

search_pattern = {
    "status_message": "//serviceResult/message",
    "result_message": "//serviceResult/message",
    "request_datetime": "//requestDateTime",
    "audit_id": "//auditId",
    "transaction_id": "//transactionId",
    "client_number": "//clientNumber",
    "result_code": "//serviceResult/result",
    "body": "//Body",
    "identifier": "//identifier",
    "subresult_code": "//subResult/result",
    "subresult_message": "//subResult/message",
    "exception_code": "//code",
    # SC575 specific alias
    "match_outcome": "//subResult/message",
    # SC830 - Programme tag details
    "programme_tag_category_code": "//programmeTag/category/code",
    "programme_tag_category_description": "//programmeTag/category/description",
    "programme_tag_code": "//programmeTag/code",
    "programme_tag_description": "//programmeTag/description",
    "programme_tag_start_date": "//programmeTag/effective/startDate",
    "programme_tag_end_date": "//programmeTag/effective/endDate",
    # SC830 - Client flag details
    "client_flag_code": "//clientFlag/code",
    "client_flag_description": "//clientFlag/description",
    "client_flag_start_date": "//clientFlag/effective/startDate",
    "client_flag_end_date": "//clientFlag/effective/endDate",
    # SC898 - Click to Enrol client flag details
    "client_flag_status": "//clientFlag/status",
    "client_flag_expiry_date": "//clientFlag/expiryDate",
    "client_flag_code": "//clientFlag/code",
    "client_flag_description": "//clientFlag/description",
    "exception_message": "//detail",
    # SC828 response fields
    "message_type": "//messageType",
    "identity_match_list": "//identityMatchList",
    "identity_match": "//identityMatch",
    "name_confidence_level": "//identityMatch/nameConfidenceLevel",
    "date_of_birth_confidence_level": "//identityMatch/dateOfBirthConfidenceLevel",
    "client_exists_in_swiftt": "//identityMatch/clientExistsInSWIFTT",
    "family_name": "//identityMatch/participant/name/familyName",
    "first_name": "//identityMatch/participant/name/firstName",
    "middle_names": "//identityMatch/participant/name/middleNames",
    "date_of_birth": "//identityMatch/participant/person/dateOfBirth",
    "gender": "//identityMatch/participant/person/gender",
    # SC875
    "has_medical_appeal_decision": "//hasMedicalAppealDecision",
    # SC8424 - inquire provider user
    "inq_provider": "//data/participant/contact/contactDetails/value",
    # SC847 - Drug Test Referral Delay notification details
    "dtrd_notification": "//notification",
    "dtrd_category_code": "//notification/category/code",
    "dtrd_category_description": "//notification/category/description",
    "dtrd_type_code": "//notification/type/code",
    "dtrd_type_description": "//notification/type/description",
    "dtrd_effective_start": "//notification/effective/start",
    "dtrd_effective_end": "//notification/effective/end",
    "dtrd_notes": "//notification/notes"
}

dot_xml_pattern = SimpleNamespace(**search_pattern)
