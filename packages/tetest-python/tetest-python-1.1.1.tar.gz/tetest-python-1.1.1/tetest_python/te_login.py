import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def loginSsoWithTeslaAccount(initial_url: str, username: str, password: str, cookies=None):
    session = requests.session()
    if cookies:
        session.cookies.update(cookies)
    host = f"{urlparse(initial_url)[0]}://{urlparse(initial_url)[1]}"
    sso_page_text = session.get(initial_url).text
    sso_page_dom = BeautifulSoup(sso_page_text, features="html.parser")
    if sso_page_dom.find("div", {"id": "openingMessage"}):
        login_method_url = host + sso_page_dom.find("form", {"id": "hrd"}).attrs['action']
        login_method_data = {
            "HomeRealmSelection": "AD AUTHORITY",
            "Email": ""
        }
        sso_page_text = session.post(login_method_url, data=login_method_data).text
        sso_page_dom = BeautifulSoup(sso_page_text, features="html.parser")
    action_url = host + sso_page_dom.find("form", {"id": "loginForm"}).attrs['action']
    sso_data = {
        'UserName': username,
        'Password': password,
        'AuthMethod': 'FormsAuthentication'
    }
    sso_response = session.post(action_url, data=sso_data)
    sso_response.cookies.update(session.cookies)
    return sso_response


def loginAuthWithExternalAccount(initial_url: str, username: str, password: str, cookies=None):
    session = requests.session()
    if cookies:
        session.cookies.update(cookies)
    auth_page_text = session.get(initial_url).text
    auth_page_dom = BeautifulSoup(auth_page_text, features="html.parser")
    auth_data = {
        "_csrf": auth_page_dom.find("input", {"name": "_csrf"}).attrs['value'],
        "_phase": auth_page_dom.find("input", {"name": "_phase"}).attrs['value'],
        "_process": auth_page_dom.find("input", {"name": "_process"}).attrs['value'],
        "transaction_id": auth_page_dom.find("input", {"name": "transaction_id"}).attrs['value'],
        "cancel": auth_page_dom.find("input", {"name": "cancel"}).attrs['value'],
        "identity": username,
        "credential": password
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    auth_response = session.post(initial_url, headers=headers, data=auth_data)
    auth_response.cookies.update(session.cookies)
    return auth_response
