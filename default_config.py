import os


def check_and_set(param: str, default_value: any) -> any:
    """
    Safely retrieve a parameter from local_config or return default.

    Args:
        param: Name of the parameter to look up
        default_value: Value to return if parameter not found

    Returns:
        The parameter value or default_value
    """
    try:
        import local_config as local

        if hasattr(local, param):
            return getattr(local, param)

    except (ModuleNotFoundError, AttributeError):
        pass

    return default_value


# Common setup
ENVIRONMENT = os.getenv("ENVIRONMENT", check_and_set("ENVIRONMENT", "dev11"))
PROJECT_NAME = check_and_set("PROJECT_NAME", "Automation Testing")
ALLURE_RESULTS_DIR = check_and_set("ALLURE_RESULTS_DIR", "allure-results")
KEY = check_and_set("KEY", None)
DB_LOCATION = check_and_set("DB_LOCATION", "D:/a/1/s/")

# API Keys TODO setup ado library with these values for pipeline runs?
APIM_SUBSCRIPTION_KEY = "08f98e584d0243ea872e51f0969a612e"
JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY = "d9a54de8e11c41fb954e5c61dadee351"
# EVENT_NOTIFICATIONS_APIM_SUBSCRIPTION_KEY = "30605c90f4e8408983bc6f429640201c"
EVENT_NOTIFICATIONS_APIM_SUBSCRIPTION_KEY = "d9a54de8e11c41fb954e5c61dadee351"
PUBLISH_OBLIGATIONS_APIM_SUBSCRIPTION_KEY = "d9a54de8e11c41fb954e5c61dadee351"
# SC550_IBM_CL_SE = "pA2xA4yS0jR8vD6uT1vO5iH2pM1gV6gG3lB0pO0yN6sD4aH4yA"
# SC550_IBM_CL_ID = "7364ea40-728a-4891-920c-b29069415227"

PRIVACY_DOMAIN = "http://workandincome.govt.nz/clients/CIAM-Dev"
FLTTOKEN = "AZUB558A22F378D42028696F3781C33DC14"

DP603_JWS_IIB = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwIjoiL21zZC9hcGkvc3Rhci9wYXJ0aWNpcGFudC9"
    "2MS9jbGllbnRzL01ESXhNak00TWprMSIsInRzIjoxNjE3MTU1MjUzLCJxIjoiIiwiaCI6Ilczc2lTMlY"
    "1SWpvaVFXTmpaWEIwSWl3aVZtRnNkV1VpT2xzaVlYQndiR2xqWVhScGIyNHZhbk52YmlKZGZTeDdJa3R"
    "sZVNJNklrTnZiblJsYm5SVWVYQmxJaXdpVm1Gc2RXVWlPbHNpWVhCd2JHbGpZWFJwYjI0dmFuTnZiaUp"
    "kZlN4N0lrdGxlU0k2SW5SeVlXNXpZV04wYVc5dVNXUWlMQ0pXWVd4MVpTSTZXeUpqT1RFd1l6WXhaQzF"
    "tWWprNExUUmxOakF0WVRjMU5pMDBaV05rWkdKaFpXRXdZemNpWFgwc2V5SkxaWGtpT2lKaGRXUnBkRWx"
    "rSWl3aVZtRnNkV1VpT2xzaVl6a3hNR00yTVdRdFptSTVPQzAwWlRZd0xXRTNOVFl0TkdWalpHUmlZV1Z"
    "oTUdNM0lsMTlMSHNpUzJWNUlqb2ljbVZ4ZFdWemRFUmhkR1ZVYVcxbElpd2lWbUZzZFdVaU9sc2lNakF"
    "5TVMwd015MHpNVlF3TVRvME56b3hOUzQ1TURFck1UTTZNREFpWFgwc2V5SkxaWGtpT2lKemIzVnlZMlZ"
    "UZVhOMFpXMGlMQ0pXWVd4MVpTSTZXeUpUVkVGU0lsMTlYUSIsIm0iOiJHRVQifQ.aT0JqG11Hw-yzePl"
    "NV4gzcZTafPy4_ruginHtG4Lil9TVuqxzmXaM6lSqn1PKXjxWDy5vUZmt38XBU2wBoXvn3bOimEvLzwt"
    "MggRIR2n3n712QB_6hqmxBKxKwdTV6r5lHDQ5Px1_Fvd4i90qM-zEfTe_S1-YXWwkp4Xh06aqnjYDCxt"
    "6l9qk7lwlhpRbl6mvsXdtla4QL_eUixBceCx_YxbYTXPC6VTKM3Yh1VeCKpBsYlEHzq_-IIJPjtJHOG1"
    "tobPuHXk7D_aYjT2g5Z2QknRXFJilsl7rI-_k2vPjO8E_I0Enc5UEuktA7b0LdjojTbpKw_Dxx4IgX-"
    "Oo_6xow"
)

azure_private_key = """-----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtY8UIt5xkZ7/C
    szKu7yC1O0RE2ZrJNqFljYYZYwVUYPSmQhWkMeQ0u0OcVdH4Q6jWtypamHxMdk2d
    6PLkRH5FPPQkzmdorwkuHWG0XZlePA0j49MJdHg+NN3oq7dtSHcPlF97SyA+4x7F
    bQ7tSWzsc0/xhPUJ1ZvYIAA+BZzgDINqgGiSvXq0JsrdN82abKyJki8eLXY7QlIc
    tB+cLKRpd3P8Nwt4S7jt8qjLKWpv/u8W6YL7OgZOdWPERfQ4RL+XqolA/W8pHNoz
    vMczeUpdnUq073Aq6MY2A8M3V1/5htV3BTi6aYMMOOGyKw37s89xMBwPhH2FAla1
    YUig5FORAgMBAAECggEAI3BX7k8w/OijrhTYUB76DXC+pF/hniy3Uj1Z4kh152gl
    uPGa4MN9xDVePU7hKqARm0k2s+ukxDAN7y+UrYk+UcKCmB9DzYaxFqbUuHvFBBi8
    CtDe6njOttAxZwPp6sE77IhD97xEK/ZZ7Lo8qc0vISj0dwXY25i4ULVBt2uIQ9aU
    jefjDP6AkZXMe1ub+i9NsX0yeGONRgsEDtubPSaxGIUPDbv1IbjfH0F8j3b9o1PA
    zfgEg98eJVAShx5LM7XW8mMmO+Gia4MeodEelBjnAGmRjoDF1AbCt3l0DaLyedPP
    ztwr/1tEJBLZb9f4Rdcg43ObwJ8Y+kdys10BvVG2XQKBgQDiz5OQVXmoUfRokmMJ
    oxdFL8HhXccn4fyFupzjCTVfuKJw1BMQdKBa/8kvnbTTPfwGaZhg7629YTYjhM7r
    MC3jZkT5OXTnVngD7Hr+rNY2QWg4cj+Yw1qWODCw2fYbG95iq2X2WTl8AgC/4DYC
    +xa8ehRgC1BGcB58hNhTjo1MuwKBgQDDtDOO97nwndFpDgkMZzBAyZ5ijYsQam3p
    ZaIBEK7x/aOAlxoyrGfeIOkqkouZWVED+UUVW2wjiUUj8KIMpMP15MuqAGNaS9H+
    uD/iOhX5xLQWcc9P2Yaa5bi07SgVva3Etsp0SgAMQDqWdtNFQhn0W0NFv9g4M7V8
    6NCRCQYiIwKBgH0vLLchNkCc21VMVrVe+t0I+u20oNN2e7YjxavZzUfD1ISJyOvw
    MwGG5DgPx1pAf/XaGmyGXVKFcSgxiTNuKCW2sKMN/2Qf6aXgxBIEu0a+2xMsm8Vp
    LXp0EQvLgXZ870VubJyHqp6zTE6bJbSHeYkVqGFKXUhDYdBAUlXr/Dk5AoGAaU0J
    vPCAZP6V0eAScFEJfqK9jSu52tBZaY8c91PBvkWKd0NWflOT48pzi0ukv5N2axvx
    1wcFDa3rvOXaW9E/+4vrJgLlco1/ZX5AKXq1nln/yF/ee4mAytG2a+t7eQ9Bc6oj
    DyVOF0lr/M/c59QkYP3GGb6bGcqA6b/fkVp4qV8CgYEApz8pxs20IUU4zs2eB6EA
    yfROgqv77k0qjFAq+VjzYKqgqtaAwLUSf0981Dp1FwBdwE88fKN48bttGmNbc8fE
    1f+Tnw0GMBzd/v2y8jV4G45Qz3WRa8vhZT6/yv9mXEuKVM4/QyyxTUNdfKicfySL
    jh4Z7JlOO/BRRX1eqsNNlAQ=
    -----END PRIVATE KEY-----"""

# INBOUND_API_KEY = "2f69dd2b6d1a4900ae01323b1bd9af27"
# OUTBOUND_API_KEY = "7cdac7b9a5ae40e98da6a1822ed6ce09"
# WEKA_API_KEY = "7cdac7b9a5ae40e98da6a1822ed6ce09"
# NZBN_API_KEY = "ef6a37042f9b413abd86c8c9922b2d64"
# NZBN_WATCHLIST_API_KEY = "a10d6b2dd33c48cb9294285629f0f4ea"
# SEP_API_KEY = ""
# ART_API_KEY = "bf0d690391c941b5a1261f9052bebd91"
# MYMSD_API_KEY = "53d1b16ab78e47dca698125c2d1534ee"
# SB_REST_API_URL = "https://dev-msg.int-npe.msd.govt.nz"
# INBOUND_PFX_CERT_PATH = "kv-int-dev-aue-001-apim-shared-cert-dev-20251010.pfx"
# OUTBOUND_PFX_CERT_PATH = "cloudapi-dev-fixed.pfx"
# SERVICEBUS_PFX_CERT_PATH = r"C:\Users\mgier001\Downloads\apim-shared-cert-test.pfx"
BULK_DATA_TEST = check_and_set("BULK_DATA_TEST", False)


#True = attempts to retrieve db connection details based on ENVIRONMENT
#False = will default to suat1
EXTERNAL_DB = check_and_set("EXTERNAL_DB", False)

# False - generate the local sqlite db first
# True - skip the local sqlite db generation (Export CSV files only)
EXPORT_DB_ONLY = check_and_set("EXPORT_DB_ONLY", False)

RUN_IN_SIT_ENV = check_and_set("RUN_IN_SIT_ENV", False)

DEL_ALLURE_RESULTS_AUTO = check_and_set("DEL_ALLURE_RESULTS_AUTO", False)
