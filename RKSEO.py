'''
Created on Feb 18 2022

@author: ScottFenstermaker
'''

import requests, time
from multiprocessing.managers import State

domain = "riskonnect.okta.com"
username = "scott.fenstermaker@riskonnect.com"
password = "DX%xc4479#!"
options = {
    "multiOptionalFactorEnroll": "false",
    "warnBeforePasswordExpired": "false"
  }

def oktaAuthenticate():
    try:
        hders = {"Accept":"application/json", "Content-Type":"application/json"}
        authpayload = {"username":username, "password":password, "options": options}
        r = requests.post('https://' + domain + '/api/v1/authn', json=authpayload, headers=hders) 
    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)
    return r

def oktaMFAAuthenticate(r):
    try:
        stateToken = r.json()['stateToken']
        factorid = r.json()['_embedded']['factors'][0]['id']
        hders = {"Accept":"application/json", "Content-Type":"application/json"}
        authpayload = {"stateToken":stateToken}
        r = requests.post('https://' + domain + '/api/v1/authn/factors/' + factorid + '/verify', json=authpayload, headers=hders) 
    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)
    return r

def oauth2RetrieveSessionCookie(p, r, s):
    try:
        client_id = r.json()['_embedded']['client'][0]['id']
        response_type = "id_token"
        scope = "openid"
        prompt = "none"
        state = p.json()['stateToken']
        redirect_uri="http%3A%2F%2Flocalhost%3A8080"
        response_mode="form_post"
        sessionToken = r.json()['sessionToken']
        payload = {"stateToken":stateToken}
        r = requests.post('https://' + domain + '/oauth2/v1/authorize', data=apayload) 
    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)
    return s


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

print("Sending primary authentication...")
resp=oktaAuthenticate()
print("RESPONSE...")
print(resp.json())
if resp.ok:
    print("Sending MFA Push Notification...")
    mfaResp=oktaMFAAuthenticate(resp)

    while "factorResult" in mfaResp.json():
        if mfaResp.json()['factorResult'] == "WAITING":
            print("Waiting...")
            time.sleep(1)
            mfaResp=oktaMFAAuthenticate(resp)

if mfaResp.ok:
    sessionToken=mfaResp.json()['sessionToken']
    print ("REQUEST...")
    print(pretty_print_POST(mfaResp.request))
    print("RESPONSE...")
    print (mfaResp.json())
    print("sessionToken = " + sessionToken)


s = requests.Session()
#oauth2RetrieveSessionCookie(resp, mfaResp, s)


# Next - Create new session using sessionToken and OpenID endpoint, receive session cookie
# Instructions here: https://developer.okta.com/docs/guides/session-cookie/main/




# Log into RK Okta SSO, and open the proper Excel file




# Establish writing to / reading from Excel file



# Ping the Google Search Console API (might want to review Google app dev setup)



# Pull list of URLS from Excel file into a data structure, iterate through and pull search console data