from pathlib import Path

root_path = str(Path(__file__).resolve().parent) + "/"

RANDOM_JS_CLIENT = Path(f"{root_path}get_random_client_query.sql")
RANDOM_SPS_CLIENT = Path(f"{root_path}get_random_sps_client.sql")
RANDOM_SPS_CLIENT_NO_DEBT = Path(f"{root_path}get_sps_client_no_debt.sql")
RANDOM_SPS_CLIENT_WITH_INCOME_NO_DEBT = Path(f"{root_path}get_sps_client_no_debt_has_income.sql")
RANDOM_SPS_CLIENT_WITH_INCOME = Path(f"{root_path}get_sps_client_with_income.sql")
RANDOM_JS_CLIENT_WITH_ASUP = Path(f"{root_path}js_client_with_asup.sql")
RANDOM_CLIENT_SUSPENDED_OR_CANCELLED_MEDICAL_BENE = Path(
    f"{root_path}get_suspended_or_cancelled_medical_benefit_client.sql"
)
RANDOM_CLIENT_PARTNER_CHILDREN_CARDS = Path(f"{root_path}get_client_with_partner_and_children_with_cards.sql")
RANDOM_52_WEEKS_REAPP_CLIENT = Path(f"{root_path}get_52_weeks_reapp_clients.sql")
RANDOM_CURRENT_SINGLE_WITH_EXISTING_DEBT = Path(f"{root_path}get_current_single_with_existing_debt_swn.sql")
RANDOM_NS_SINGLE_CLIENT = Path(f"{root_path}get_single_ns_client_swrg_004_8.sql")
RANDOM_NS_CLIENT_WITH_NO_RESIDENCY_RECORDS = Path(f"{root_path}get_single_ns_client_with_no_residency_records.sql")
RANDOM_CLIENT_WITH_CHILD_AS_AND_113_EXPIRED_JS_52_WEEK_REAPPLICATION = Path(
    f"{root_path}get_client_with_js_with_expiry_113_and_as_and_children_52_week_reapplication.sql"
)
RANDOM_CLIENT_WITH_CHILD_AS_AND_113_EXPIRED_JS_26_WEEK_REAPPLICATION = Path(
    f"{root_path}get_client_with_js_with_expiry_113_and_as_partner_and_children_26_week_reapplication.sql"
)
RANDOM_SINGLE_CLIENT_WITH_NO_CHILDREN_AS_AND_113_EXPIRED_JS_26_WEEK_REAPPLICATION = Path(
    f"{root_path}get_client_with_js_with_expiry_113_and_as_single_no_children_26_week_reapplication.sql"
)
ALL_CLIENTS = Path(f"{root_path}get_all_clients_query.sql")

sc806_client_with_debt_query = Path(f"{root_path}get_sc806_client_with_debt.sql")

SC531_52_WEEK_REAPP_CLIENT = Path(f"{root_path}get_sc531_52_week_reapp_client.sql")
SC531_SUSPENDED_52_WEEK_REAPP_CLIENT = Path(f"{root_path}get_sc531_suspended_52_week_reapp_client.sql")
sc596_manage_tenancy_clients_query = Path(f"{root_path}get_sc596_manage_tenancy_clients.sql")
SC893_TAS_REAPPLICATION_CLIENT = Path(f"{root_path}get_sc893_tas_reapplication_client.sql")
SC810_SUCCESSFUL_TRANSACTION_CLIENT = Path(f"{root_path}get_sc810_successful_transaction_client.sql")

SC810_INCOME_ALREADY_HELD_CLIENT = Path(f"{root_path}get_sc810_income_already_held_client.sql")

SC890_SUCCESSFUL_RESPONSE_CLIENT = Path(f"{root_path}get_sc890_successful_client.sql")

SC846_SUCCESSFUL_TRANSACTION_CLIENT = Path(f"{root_path}get_sc846_successful_transaction_client.sql")
SC803_SUCCESSFUL_TRANSACTION_CLIENT = Path(f"{root_path}get_sc803_successful_transaction_client.sql")
SC526_SUCCESSFUL_TRANSACTION_CLIENTS = Path(f"{root_path}get_sc526_candidate_clients.sql")
