from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import backoff
import socket

from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials


class MctAccountLostAccessException(Exception):
    """Raised when we cannot access to an account."""
    pass


class MerchantCenterServiceDownException(Exception):
    """Raised when we cannot access to MCC service """
    pass


def get_mct_service(
    adscale_key: str = None,
    access_token: str = None,
    cache_discovery=True
):
    """ adscale_key or access_token must be specified """

    if access_token:
        credentials = Credentials(access_token, scopes='https://www.googleapis.com/auth/content')
    elif adscale_key:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            adscale_key, scopes=['https://www.googleapis.com/auth/content']
        )
    else:
        raise ValueError('one of the following arguments must be specified: adscale_key or access_token')

    service = discovery.build('content', 'v2.1', credentials=credentials, cache_discovery=cache_discovery)
    return service


@backoff.on_exception(backoff.expo, (socket.timeout), max_tries=3)
def get_mct_account_details(
    merchant_id: int,
    adscale_key: str = None,
    access_token: str = None
):
    """
        From mct id check if user has access to it.

        adscale_key or access_token must be specified
    """
    service = get_mct_service(adscale_key, access_token)

    try:
        # Get account status alerts from MCT
        request_account_statuses = service.accounts().get(merchantId=merchant_id,
                                                          accountId=merchant_id)
        response_account_statuses = request_account_statuses.execute()
    # RefreshError is raised when we have invalid merchant_id or we don't have access to the account
    except RefreshError as err:
        raise MctAccountLostAccessException(f"We cannot access your Merchant Center account with the id: {merchant_id}. Are you sure you grant access and give correct ID?")
    except HttpError as err:
        if err.resp.status >= 400 and err.resp.status < 500:
            raise MctAccountLostAccessException(f"We cannot access your Merchant Center account with the id: {merchant_id}. Are you sure you grant access and give correct ID?")
        else:
            raise MerchantCenterServiceDownException(f"The Merchent Center API does not respond. Thus, we cannot check if we can access your Merchant Center account with the id: {merchant_id}. Please try later" )
    return response_account_statuses['name']


@backoff.on_exception(backoff.expo, (socket.timeout), max_tries=3)
def check_if_multi_client_account(
    merchant_id: int,
    adscale_key: str = None,
    access_token: str = None
):
    """
        Sends an error if the account is a MCA

        adscale_key or access_token must be specified
    """
    service = get_mct_service(adscale_key, access_token)
    try:
        # This API method is only available to sub-accounts, thus it will fail if the merchant id is a MCA
        request_account_products = service.products().list(merchantId=merchant_id)
        response_account_statuses = request_account_products.execute()
    # RefreshError is raised when we have invalid merchant_id or we don't have access to the account
    except RefreshError as err:
        raise MctAccountLostAccessException(f"We cannot access your Merchant Center account with the id: {merchant_id}. Are you sure you grant access and give correct ID?")
    except HttpError as err:
        if err.resp.status >= 400 and err.resp.status < 500:
            raise MctAccountLostAccessException(f"This merchant id ({merchant_id} is for multi acccounts. You can only link sub-accounts.")
        else :
            raise MerchantCenterServiceDownException(f"The Merchent Center API does not respond. Thus, we cannot check if we can access your Merchant Center account with the id: {merchant_id}. Please try later" )
    return response_account_statuses
