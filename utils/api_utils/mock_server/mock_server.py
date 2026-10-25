from flask import Flask

import utils.api_utils.mock_server.mock_routes_obj as mock_routes_obj
from utils.api_utils.mock_server.base import Routes

app = Flask(__name__)


def call_create_routes(routes: Routes, arg=None):
    routes_def_obj = routes.create_routes_def_obj()
    return routes_def_obj.create_routes_def(arg)


@app.route("/msd/participant/v1/providers/members/inquire", methods=["GET"])
def inquire_provider_member():
    call_create_routes(mock_routes_obj.MSDProviderInquire())


@app.route("/msd/participant/v1/prospectpersons/registration", methods=["POST"])
def register_prospect_person():
    call_create_routes(mock_routes_obj.MSDRegistration())


@app.route("/msd/participant/accounts/v1/flts/link", methods=["POST"])
def link_accounts():
    call_create_routes(mock_routes_obj.MSDLinkAccounts())


@app.route("/msd/participant/v1/connectivity-check", methods=["GET"])
def connectivity_check():
    call_create_routes(mock_routes_obj.MSDCheckConnectivity())


@app.route("/weka/participant/v1/contractDetails", methods=["GET"])
@app.route("/internal/weka/participant/v1/contractDetails", methods=["GET"])
def get_contract_details():
    call_create_routes(mock_routes_obj.WekaContractDetailsRoutes())


@app.route("/publish", methods=["PUT"])
def provider_publish():
    call_create_routes(mock_routes_obj.Publish())


@app.route("/members/publish", methods=["PUT"])
def provider_member_publish():
    call_create_routes(mock_routes_obj.PublishMember())


# MBIE NZBN API endpoints
@app.route("/mbie/nzbn/v1/entities/<nzbn>", methods=["GET"])
def get_entity_by_nzbn(nzbn):
    call_create_routes(mock_routes_obj.MBIEGetEntities(), nzbn)


@app.route("/mbie/nzbn/v1/watchlists/<watchlist_id>/nzbns", methods=["GET"])
def get_watchlist_nzbns(watchlist_id):
    call_create_routes(mock_routes_obj.MBIEGetWatchList(), watchlist_id)


@app.route("/mbie/nzbn/v1/watchlists/<watchlist_id>/action-append-nzbns", methods=["POST"])
def append_watchlist_nzbns(watchlist_id):
    call_create_routes(mock_routes_obj.MBIEAppendWatchList(), watchlist_id)


@app.route("/mbie/nzbn/v1/watchlists/<watchlist_id>/action-delete-nzbns", methods=["POST"])
def delete_watchlist_nzbns(watchlist_id):
    call_create_routes(mock_routes_obj.MBIEDeleteWatchList(), watchlist_id)


@app.route(
    "/mbie/nzbn/v1/watchlists/<watchlist_id>/action-send-test-notification",
    methods=["POST"],
)
def send_test_notification(watchlist_id):
    call_create_routes(mock_routes_obj.MBIESendNotification(), watchlist_id)


@app.route(
    "/internal/d01/msd/participant-management/v1/clients/<participant_id>",
    methods=["GET"],
)
def inquire_client_by_id(participant_id):
    """Get client profile by participant ID."""
    call_create_routes(mock_routes_obj.InternalInquireParticipant(), participant_id)


@app.route("/internal/d01/msd/participant-management/v1/clients", methods=["GET"])
def inquire_clients():
    """Get multiple clients or search by FLT token."""
    call_create_routes(mock_routes_obj.InternalInquireClients())


# Employer Profile API routes
@app.route("/msd/employment-mgmt/employers/v1/messages", methods=["POST"])
def publish_employer_event():
    call_create_routes(mock_routes_obj.MSDPublishEmployerEvent())


# SEP Event API routes
@app.route("/employer-events/subscriptions/<subscription_name>/messages/head", methods=["POST"])
def consume_sep_messages(subscription_name):
    call_create_routes(mock_routes_obj.EmployerEventsConsumeSep(), subscription_name)


@app.route(
    "/employer-events/subscriptions/<subscription_name>/messages/<message_id>/<lock_token>",
    methods=["DELETE"],
)
def delete_sep_message(message_id):
    call_create_routes(mock_routes_obj.EmployerEventsDeleteSep(), message_id)


@app.route(
    "/employer-events/subscriptions/<subscription_name>/messages/<message_id>/<lock_token>",
    methods=["PUT"],
)
def unlock_sep_message(message_id):
    call_create_routes(mock_routes_obj.EmployerEventsUnlockSep(), message_id)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
