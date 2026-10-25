import os
from pathlib import Path

from playwright.sync_api import sync_playwright, Page


def run():
    with sync_playwright() as p:
        TIMEOUT = 120000
        downloads_folder = Path.home() / "Downloads"
        # search_items = [
        #     "index=iib host=d11 AND ES_ManageUserService* AND *Store*User*Activity* AND SC896*",
        #     "index=iib host=d11 AND AS_AssistanceAggregateService* AND *Verify*Assistance* AND SC889*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Validate*Payment*Instructions* AND SC512*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Update*Payment* AND SC547*",
        #     "index=iib host=d11 AND ES_ManageEmploymentService* AND *Update*Job*Seeker*Profile* AND SC921*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Update*Document*Details*(WMB*Proxy)* AND SC733P*",
        #     "index=iib host=d11 AND DP_MyMSD_RESTful_Gateway* AND *Update*Client*Details* AND SC274*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Synchronise*Payment*Card* AND SC535*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Sync*Merchant*Payment*Authority* AND SC553*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*TAS*Reapplication* AND SC893*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*Life*Event* AND SC582*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*Hardship*Assistance* AND SC868*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*Document*Metadata* AND SC885*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*Child*Support*Application* AND SC550*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Submit*Application*Decision* AND SC888*",
        #     "index=iib host=d11 AND ES_ManageUserService* AND *Store*Participant*Consent* AND SC271*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Store*Medical*Certificate* AND SC867*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Set*Payment*Card*PIN* AND SC560*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Send*Password*Token* AND SC241*",
        #     "index=iib host=d11 AND security* AND *ResetCredentialForPrincipal* AND SC236*",
        #     "index=iib host=d11 AND security* AND *ReplaceIGovtLoginToken* AND SC237*",
        #     "index=iib host=d11 AND security* AND *RemoveMemberFromGroup* AND SC234*",
        #     "index=iib host=d11 AND AS_AssistanceAggregateService* AND *Regrant*Assistance* AND SC891*",
        #     "index=iib host=d11 AND security-services.war* AND *Register*Supplier* AND SC250*",
        #     "index=iib host=d11 AND TS_UA_CMS_ProcessApplication* AND *Receive*Application* AND SC583*",
        #     "index=iib host=d11 AND ES_PublishParticipantService* AND *Publish*Provider* AND SC822*",
        #     "index=iib host=d11 AND TS_PublishCMSParticipantService* AND *Publish*Participant*-*Secured*Status*to*WAM* AND SC586*",
        #     "index=iib host=d11 AND ES_PublishParticipantService* AND *Publish*Outbound*Contact*List* AND SC931*",
        #     "index=iib host=d11 AND TS_PublishCMSParticipantService* AND *Publish*Outbound*Campaign*Control* AND SC933*",
        #     "index=iib host=d11 AND API_CampaignManagement* AND *Publish*Outbound*Call*Result* AND SC932*",
        #     "index=iib host=d11 AND ES_PublishCommunicationService* AND *Publish*Notification* AND SC837*",
        #     "index=iib host=d11 AND API_CampaignManagement* AND *Publish*Directory*Content* AND SC1002*",
        #     "index=iib host=d11 AND ES_PublishAppointmentService* AND *Publish*Appointment* AND SC860*",
        #     "index=iib host=d11 AND ES_ManageUserService* AND *Provision*User* AND SC817*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Provide*Payment*Card* AND SC549*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Process*Work*Capacity*Medical*Certificate* AND SC865*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Process*Ongoing*Application* AND SC872*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Process*Hardship*Application* AND SC880*",
        #     "index=iib host=d11 AND TS_ProcessChangeEvent* AND *Process*Change*Event* AND SC950*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Notify*Vacant*Property* AND SC345*",
        #     "index=iib host=d11 AND TS_ProcessChangeEvent* AND *Notify*Vacant*Property* AND SC331*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Notify*Tenancy*Change* AND SC354*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Notify*Tenancy*Change* AND SC340*",
        #     "index=iib host=d11 AND TS_BPMTaskNotificationGateway* AND *Notify*Task*(Outbound)* AND SC584*",
        #     "index=iib host=d11 AND TS_CuramTaskNotificationGateway* AND *Notify*Task*(Inbound)* AND SC585*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*RENT*CHANGE* AND SC342*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*RENT*CHANGE* AND SC356*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Notify*Payment*Transaction* AND SC539*",
        #     "index=iib host=d11 AND TS_ObligationService* AND *Notify*Obligation*Activity* AND SC128*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*IRR*CHANGE* AND SC341*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*IRR*CHANGE* AND SC355*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Notify*Expired*Payments* AND SC559*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Notify*Expired*Payment*Instructions* AND SC540*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *NOTIFY*EXCEPTION* AND SC358*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*EXCEPTION* AND SC344*",
        #     "index=iib host=d11 AND ES_ManageDocumentService* AND *Notify*Document*Stored* AND SC836*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Notify*Document*Store* AND SC730v2*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Notify*Document*Store* AND SC730*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Notify*Document*Change* AND SC731*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *NOTIFY*ADHOC*EVENT* AND SC357*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND ** AND SC343*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Manage*Tenancy*Details* AND SC596*",
        #     "index=iib host=d11 AND * AND *Manage*Proxy*Engagement* AND SC156*",
        #     "index=iib host=d11 AND DP_MyMSD_RESTful_Gateway* AND *Manage*Provider* AND SC281*",
        #     "index=iib host=d11 AND ES_ManageProxyEngagementService* AND *Manage*Provider*Member* AND SC282*",
        #     "index=iib host=d11 AND ES_ManageCommunicationService* AND *Manage*Notification*Status* AND SC834*",
        #     "index=iib host=d11 AND ES_ManageCommunicationService* AND *Manage*Job*Plan*Activities* AND SC152*",
        #     "index=iib host=d11 AND ES_ManageFinancialPositionService* AND *Manage*Debt*and*Arrears* AND SC876*",
        #     "index=iib host=d11 AND ES_ManageFinancialPositionService* AND *Manage*Client*Identity*Token*Registration* AND SC264*",
        #     "index=iib host=d11 AND ES_ManageParticipantService* AND *Manage*Client*Appointments* AND SC863*",
        #     "index=iib host=d11 AND ES_ManageAbsenceService* AND *Manage*Absence*Declares*absence* AND SC801*",
        #     "index=iib host=d11 AND ES_ManageUserService* AND *Mainain*Authorisation* AND SC816*",
        #     "index=iib host=d11 AND TS_LoadMedCertService* AND *Load*Medical*Certificate* AND SC866*",
        #     "index=iib host=d11 AND ES_ManageUserService* AND *List*Participant*Consent* AND SC272*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Link*Medical*Certificate* AND SC874*",
        #     "index=iib host=d11 AND security* AND *Link*IGovt*Login*token*to*Alternate*Principle* AND SC231*",
        #     "index=iib host=d11 AND security* AND *IsMemberOfGroup* AND SC235*",
        #     "index=iib host=d11 AND security* AND *IsIGovtLoginLinked* AND SC238*",
        #     "index=iib host=d11 AND security-services.war* AND *Inquire*Vacancies* AND SC925*",
        #     "index=iib host=d11 AND ES_InquireUserService* AND *Inquire*User*Privilege* AND SC818*",
        #     "index=iib host=d11 AND ES_InquireUserService* AND *Inquire*User*Activity* AND SC897*",
        #     "index=iib host=d11 AND ES_InquireUserService* AND *Inquire*Tenancy* AND SC595*",
        #     "index=iib host=d11 AND ES_InquireWorkflowService* AND *Inquire*Task* AND SC849*",
        #     "index=iib host=d11 AND TS_InquireSwifttUserService* AND *Inquire*SWIFTT*User* AND SC587*",
        #     "index=iib host=d11 AND TS_InquireRiskScoreService* AND *Inquire*Risk*Score* AND SC870*",
        #     "index=iib host=d11 AND ES_InquirePaymentService* AND *Inquire*Pay*period*and*Redirections* AND SC856*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*Ongoing*Assistance* AND SC804v3*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*Ongoing*Assistance* AND SC804v4*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*Ongoing*Assistance* AND SC804v2*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*Ongoing*Assistance* AND SC804v1*",
        #     "index=iib host=d11 AND ES_InquireApplicationService* AND *Inquire*Ongoing*Applications*Summary* AND SC886*",
        #     "index=iib host=d11 AND ES_InquireApplicationService* AND *Inquire*Ongoing*Application* AND SC887*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*One-off*Assistance** AND SC805*",
        #     "index=iib host=d11 AND ES_InquireObligationService* AND *Inquire*Obligation* AND SC845*",
        #     "index=iib host=d11 AND ES_InquireCommunicationService* AND *Inquire*Notification* AND SC833*",
        #     "index=iib host=d11 AND ES_InquireApplicationService* AND *Inquire*Last*Approved*Hardship*Application* AND SC878*",
        #     "index=iib host=d11 AND ES_InquireEmploymentService* AND *Inquire*Job*Seeker*Profile* AND SC922*",
        #     "index=iib host=d11 AND ES_InquireEmploymentService* AND *Inquire*Insight* AND SC1000*",
        #     "index=iib host=d11 AND ES_InquireAssistanceService* AND *Inquire*Hardship*Payment* AND SC873*",
        #     "index=iib host=d11 AND ES_InquireApplicationService* AND *Inquire*Hardship*Application* AND SC879*",
        #     "index=iib host=d11 AND ES_InquirePaymentService* AND *Inquire*Exchange*Rate* AND SC814*",
        #     "index=iib host=d11 AND ES_InquireEntitlementService* AND *Inquire*Entitlement*(Prospective*Hardship)* AND SC864*",
        #     "index=iib host=d11 AND ES_InquireEntitlementService* AND *Inquire*Entitlement** AND SC812*",
        #     "index=iib host=d11 AND ES_InquireDebtService* AND *Inquire*Debt* AND SC806v2*",
        #     "index=iib host=d11 AND ES_InquireDebtService* AND *Inquire*Debt* AND SC806v1*",
        #     "index=iib host=d11 AND ES_InquireParticipantService* AND *Inquire*Client* AND SC825*",
        #     "index=iib host=d11 AND TS_InquireCaseManagementInputService* AND *Inquire*Case*Management*Input* AND SC851*",
        #     "index=iib host=d11 AND ES_InquireChildSupport* AND *Inquire*Card*User* AND SC1001v1*",
        #     "index=iib host=d11 AND ES_InquireApplicationService* AND *Inquire*Application*Attachement* AND SC892*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Initiate*Hardship*Application*Approval* AND SC882*",
        #     "index=iib host=d11 AND TS_ManageCorrespondence* AND *Initiate*Correspondence*Async*Callback* AND SC720*",
        #     "index=iib host=d11 AND ES_ManageCommunicationService* AND *Initiate*Correspondence* AND SC835*",
        #     "index=iib host=d11 AND TS_ManageCorrespondence* AND *Initiate*Correspondence* AND SC720*",
        #     "index=iib host=d11 AND TS_ManageCorrespondence* AND *Initiate*CMS*Correspondence* AND SC852*",
        #     "index=iib host=d11 AND AS_AssistanceAggregateService* AND *Grant*Assistance* AND SC890*",
        #     "index=iib host=d11 AND security* AND *GetIGovtLoginToken* AND SC240*",
        #     "index=iib host=d11 AND security* AND *Get*User*for*IGovt*Login*Token**** AND SC230*",
        #     "index=iib host=d11 AND security* AND *Get*user*for*iGovt*Login*Token* AND SC230B*",
        #     "index=iib host=d11 AND security* AND *Get*User*for*iGovt*Login*token* AND SC230A*",
        #     "index=iib host=d11 AND *Get*Reference*Data* AND SC743 *",
        #     "index=iib host=d11 AND TS_IncomeSupportServices* AND *Get*Product*Delivery*Details* AND SC532v2*",
        #     "index=iib host=d11 AND TS_IncomeSupportServices* AND *Get*Product*Delivery*Details* AND SC532*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Payment*Details* AND SC558*",
        #     "index=iib host=d11 AND TS_IncomeSupportServices* AND *Get*Outbound*Campaign*Status* AND SC934*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Outbound*Campaign*Outcomes* AND SC935*",
        #     "index=iib host=d11 AND API_CampaignManagement* AND *Get*Job*Plan*Outcomes* AND SC151*",
        #     "index=iib host=d11 AND TS_DocumentServices* AND *Get*Document*Details*(WMB*Proxy)* AND SC732P*",
        #     "index=iib host=d11 AND TS_ObligationService* AND *Get*Client*Obligations* AND SC126 V1*",
        #     "index=iib host=d11 AND TS_ObligationService* AND *Get*Client*Obligation*Failures* AND SC127*",
        #     "index=iib host=d11 AND TS_ObligationService* AND *Get*Client*Identity*Token*Registration* AND SC263*",
        #     "index=iib host=d11 AND TS_GetClientSummary* AND *Get*Client*Identification*Status* AND SC205*",
        #     "index=iib host=d11 AND API_ManageClientSummary* AND *Get*Client*Details* AND SC275*",
        #     "index=iib host=d11 AND TS_GetClientContactsService* AND *Get*Client*Contacts* AND SC213*",
        #     "index=iib host=d11 AND TS_GetClientCircumstancesService* AND *Get*Client*Circumstances* AND SC529*",
        #     "index=iib host=d11 AND TS_GetClientContactsService* AND *Get*Client*Circumstances* AND SC529*",
        #     "index=iib host=d11 AND ES_InquireAppointmentService* AND *Get*Client*Appointments* AND SC861*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Card*Transactions* AND SC556*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Card*Statement* AND SC555*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Card*Details* AND SC557*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*Card*Details* AND SC557v2*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Get*BFC*Details* AND SC588*",
        #     "index=iib host=d11 AND ES_InquireAddressService* AND *Get*Associated*Postcodes* AND SC843*",
        #     "index=iib host=d11 AND MyMSDBFC* AND *Get*Address,* AND SC742 *",
        #     "index=iib host=d11 AND ES_InquireAddressService* AND *Get*Address* AND SC841*",
        #     "index=iib host=d11 AND ES_ManageUserService* AND *Generate*Password*Token* AND SC815*",
        #     "index=iib host=d11 AND ES_InquireAddressService* AND *Find*Likely*Postcode* AND SC842*",
        #     "index=iib host=d11 AND TS_FindClientByUniqueIdentifier* AND *Find*Client*By*Assistance* AND SC808*",
        #     "index=iib host=d11 AND TS_FindClientByUniqueIdentifier* AND *Find*Available*Client*Appointment*Times* AND SC862*",
        #     "index=iib host=d11 AND API_AppointmentManagement* AND *Find*Address** AND SC741*",
        #     "index=iib host=d11 AND ES_InquireAddressService* AND *Find*Address* AND SC840*",
        #     "index=iib host=d11 AND TS_IncomeSupportServices* AND *Establish*Entitlement* AND SC531*",
        #     "index=iib host=d11 AND ES_ManageCommunicationService* AND *Dispatch*Message*(B2B)* AND SC832*",
        #     "index=iib host=d11 AND security* AND *DelinkIGovtLogin* AND SC239*",
        #     "index=iib host=d11 AND TS_GetClientSummary* AND *Decline*Client*Identity*Token*Registration* AND SC206*",
        #     "index=iib host=d11 AND TS_DeclareIncomeService* AND *Declare*income* AND SC901*",
        #     "index=iib host=d11 AND ES_ManageAbsenceService* AND *Declare*absence* AND SC526*",
        #     "index=iib host=d11 AND ES_ManageWorkflowService* AND *Create*Task* AND SC850*",
        #     "index=iib host=d11 AND ES_ManageReferralService* AND *Create*Referral* AND SC924*",
        #     "index=iib host=d11 AND ES_ManageCommunicationService* AND *Create*Notifications* AND SC831*",
        #     "index=iib host=d11 AND ES_ManageCaseService* AND *Create*Note* AND SC823*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Create*Hardship*Application* AND SC869*",
        #     "index=iib host=d11 AND ES_ManageDebtService* AND *Create*Debt*and*Redirections* AND SC807*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Create*Address* AND SC744 *",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Confirm*Offer*Outcome* AND SC351*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *Confirm*Offer*Outcome* AND SC337*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *CONFIRM*APPLICATION*REFERRAL* AND SC348*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *CONFIRM*APPLICATION*REFERRAL* AND SC334*",
        #     "index=iib host=d11 AND security* AND *ChangeNameDetails* AND SC232*",
        #     "index=iib host=d11 AND ES_ManageAssistanceService* AND *Change*Payment*Method** AND SC802*",
        #     "index=iib host=d11 AND ES_ManageAssistanceService* AND *Change*Assistance*Status** AND SC803*",
        #     "index=iib host=d11 AND TS_BackDatedReviewService* AND *Calculate*Back*Dated*Review** AND SC820*",
        #     "index=iib host=d11 AND *Build*Address* AND SC745*",
        #     "index=iib host=d11 AND TS_AssessProcessingReviewService* AND *Assess*Processing*Review* AND SC821*",
        #     "index=iib host=d11 AND ES_ManageAssistanceService* AND *Apply*Entitlement*Rate* AND SC813*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Apply*Change*of*Income* AND SC877*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Apply*Change*of*Circumstance** AND SC810v1*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Apply*Change*of*Circumstance* AND SC810v2*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Apply*Change*of*Circumstance* AND SC810v2*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Allocate*Payment*Card* AND SC510*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *ADVISE*VACANCY*MATCH* AND SC333*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *ADVISE*VACANCY*MATCH* AND SC347*",
        #     "index=iib host=d11 AND ES_ManageAssistanceService* AND *Advise*Sanction* AND SC846*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Advise*Hardship*Application*Decision* AND SC881*",
        #     "index=iib host=d11 AND ES_ManageApplicationService* AND *Advise*Evidence*Status* AND SC884*",
        #     "index=iib host=d11 AND ES_ManageCircumstanceService* AND *Advise*Change*of*Housing*Circumstances* AND SC809*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *ADVISE*APPLICATION*SHORTLIST* AND SC346*",
        #     "index=iib host=d11 AND TS_ManageHousingService* AND *ADVISE*APPLICATION*SHORTLIST* AND SC332*",
        #     "index=iib host=d11 AND security* AND *AddMemberToGroup* AND SC233*",
        #     "index=iib host=d11 AND security-services.war* AND *Get*Non-Financial*Sanctions*Upskilling* AND SC153*",
        #     "index=iib host=d11 AND *Manage*Non-Financial*Sanctions*Upskilling* AND SC154*",
        #     "index=iib host=d11 AND API_NFSManagement* AND *Get*Job*Search*Detail*for*Non-Financial*Sanctions* AND SC161*",
        #     "index=iib host=d11 AND API_NFSManagement* AND *Manage*Job*Search*Detail*for*Non-Financial*Sanctions* AND SC162*",
        #     "index=iib host=d11 AND API_NFSManagement* AND *Inquire*Tenancy*Details** AND SC595*",
        #     "index=iib host=d11 AND API_TenancyDetails* AND *Manage*Tenancy*Details* AND SC596*",
        #     "index=iib host=d11 AND TS_FinanceServices* AND *Add*Payment*Instruction* AND SC511*",
        #     "index=iib host=d11 AND API_TenancyManagementr* AND *Inquire*STAR*Letter* AND SC606*",
        #     "index=iib host=d11 AND API_InquireSTARLetters* AND *Notify*Correspondence*Load* AND SC702*"
        # ]

        search_items = [
            "index=iib host=d11 AND ES_ManageUserService* AND *Store*User*Activity* AND SC896*",

        ]

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://splunkdev.ssi.govt.nz/en-US/app/ods/search?earliest=%40d&latest=now",
                  wait_until="domcontentloaded",
                  timeout=TIMEOUT)
        page.get_by_role("textbox", name="Username").type("dev")
        page.get_by_role("textbox", name="Password").type("dev@123")
        page.get_by_role("button", name="Sign In").click()

        page.get_by_role("button", name="Time range: Today").click()
        page.get_by_role("link", name="Other All time").click()

        for item in search_items:
            page.get_by_role("textbox", name="Search").fill(item)
            page.get_by_role("link", name="Search Button").click()
            page.wait_for_load_state(state="domcontentloaded")
            page.get_by_role("button", name="Export").click(delay=200)
            page.get_by_role("button", name="Format: CSV").click()
            page.get_by_role("menuitemradio", name="Format : JSON :").click()
            with page.expect_download() as download_info:
                page.get_by_role("link", name="Export").click()
            download = download_info.value
            download.save_as(downloads_folder / download.suggested_filename)
            print("Suggested filename:", download.suggested_filename)
            print("Download path:", downloads_folder / download.suggested_filename)
            temp_file = download.path()
            os.remove(temp_file)

        browser.close()


if __name__ == "__main__":
    run()
