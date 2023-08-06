import base64

from ..HTTP.Requests import *
from ..Utils import Utils
from datetime import datetime

BASE_URL = 'https://api.trinet.com'


class trinet:
  headers = None
  expires_at = None
  access_token = None
  auth_refreshed = False
  account_identifier = None

  def __init__(self, account_identifier, access_token, expires_at, client_id, client_secret):
    self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
    self.headers['Authorization'] = f"Bearer {access_token}"
    self.expires_at = expires_at
    self.access_token = access_token
    self.account_identifier = account_identifier
    self.base_url = f"{BASE_URL}/v1/company/{self.account_identifier}"
    self.auth_refreshed = False
    if datetime.now().timestamp() > expires_at:
      self.authenticate(client_id, client_secret)
      self.auth_refreshed = True

  def authenticate(self, client_id, client_secret):
    user = f"{client_id}:{client_secret}"
    AUTH_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(user.encode('UTF-8')).decode('UTF-8')}"
    }
    post_url = f"{BASE_URL}/oauth/accesstoken"
    auth_body = {
        'grant_type': 'client_credentials'
    }
    result = post(post_url, AUTH_HEADERS, auth_body)
    auth_result = result['content']
    self.access_token = auth_result['access_token']
    self.headers['Authorization'] = f"Bearer {self.access_token}"
    self.expires_at = datetime.now().timestamp() + auth_result['expires_in']

  def list_all_employees(self):
    post_url = f"{self.base_url}/employees"
    result = get(post_url, self.headers)
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to get employees. Result: {result}")
    return result
