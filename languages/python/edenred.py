#!python3

# cf. https://chezsoi.org/lucas/blog/reverse-engineering-the-http-api-behind-an-android-app.html

from binascii import hexlify
from hashlib import sha1
import xml.etree.ElementTree as ET
import os, requests, sys

CONFIG_URL = 'http://m.int.edenred.snapp.fr/service/api'
CONFIG_SALT = '59d1346e:'

def sessionLogin(customer_id=-1, store_id=1, platform_id=2):
    # the customer_id returned is simply an incrementing counter : it does not identify a specific client
    service_name = 'session.login'
    auth = createAuthorization(service_name, *[customer_id, store_id, platform_id])
    print(service_name, '- auth:', auth)
    body = f"<?xml version='1.0'?><methodCall><methodName>{service_name}</methodName><params><param><value><int>{customer_id}</int></value></param><param><value><int>{store_id}</int></value></param><param><value><int>{platform_id}</int></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL, body, auth)

def downloadedAt(session_id, id_card):
    service_name = 'edenred_bascule.downloaded_at'
    auth = createAuthorization(service_name, *[id_card])
    print(service_name, '- auth:', auth)
    body = f"<methodCall><methodName>{service_name}</methodName><params><param><value><string>{id_card}</string></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def isEligibleBascule(session_id, id_card):
    service_name = 'edenred_bascule.is_eligible'
    auth = createAuthorization(service_name, *[id_card])
    print(service_name, '- auth:', auth)
    body = f"<methodCall><methodName>{service_name}</methodName><params><param><value><string>{id_card}</string></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def customerShow(session_id, id_user):
    service_name = 'customer.show'
    auth = createAuthorization(service_name, *[id_user])
    print(service_name, '- auth:', auth)
    body = f"<methodCall><methodName>{service_name}</methodName><params><param><value><int>{id_user}</int></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def customerGetCardInfos(session_id, id_card):
    service_name = 'customer.get_card_infos'
    auth = createAuthorization(service_name, *[id_card])
    print(service_name, '- auth:', auth)
    body = f"<methodCall><methodName>{service_name}</methodName><params><param><value><string>{id_card}</string></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def customerGetBalance(session_id, id_card):
    service_name = 'customer.get_balance'
    auth = createAuthorization(service_name, *[id_card])
    print(service_name, '- auth:', auth)
    body = f"<methodCall><methodName>{service_name}</methodName><params><param><value><string>{id_card}</string></value></param></params></methodCall>"
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def rechercher_support_par_numero_serie(session_id, card_serial_number):
    # should return card_id + code_porte_monnaie_support
    return getResultWS(session_id, 'rechercher_support_par_numero_serie', (('NumeroSerieSupport', card_serial_number),))

def rechercher_solde_millesime(session_id, card_id, code_porte_monnaie_support):
    # not using a dict as `params` to ensure NumeroCompte comes before ReferenceSupport during auth secret generation
    return getResultWS(session_id, 'rechercher_solde_millesime', params=(('NumeroCompte', card_id), ('ReferenceSupport', code_porte_monnaie_support)))

def getResultWS(session_id, service_name, params, en_request=False):
    # useless trick: `params` can be either a dict or an iterable of length-2 tuples
    service_name = 'ctr.' + service_name
    auth = createAuthorizationV2(service_name, *[v for (k, v) in params])
    print(service_name, '- auth V2:', auth)
    body = getXMLFormat(service_name, params, en_request=en_request)
    return soapRequest(CONFIG_URL + ';s=' + session_id, body, auth)

def getXMLFormat(service_name, params, en_request=False):
    request_verb = "request" if en_request else "requete"
    xmlformat = f"<?xml version='1.0' ?><methodCall><methodName>{service_name}</methodName><params><param><value><struct><member><name>{request_verb}</name><value><struct>"
    xmlorder = "<member><name>order!</name><value><array><data>"
    for param_name, param_value in params:
        xmlformat += f"<member><name>{param_name}</name><value><string>{param_value}</string></value></member>"
        xmlorder += f"<value><string>{param_name}</string></value>"
    xmlformat += xmlorder + "</data></array></value></member>" + "</struct></value></member></struct></value></param></params></methodCall>"
    return xmlformat

def soapRequest(url, body, auth):
    response = requests.post(url, data=body, headers={
        'Content-Type': 'text/xml; charset=utf-8',
        'Authorization': auth,
        'User-Agent': 'Edenred Python API 1.0',
    })
    response.raise_for_status()
    return parseXMLmethodResponse(response.text)

def createAuthorization(service_name, *args, args_joiner=','):
    secret = CONFIG_SALT + service_name + ',' + args_joiner.join(str(arg) for arg in args)
    return sha1(secret.encode()).hexdigest()

def createAuthorizationV2(service_name, *args):
    return createAuthorization(service_name, *args, args_joiner='')

def parseXMLmethodResponse(text_response):
    parsed = ET.fromstring(text_response)
    if parsed.find('fault'):
        return {'fault': parseXMLmember(parsed.find('fault/value'))}
    return parseXMLmember(parsed.find('params/param/value'))

def parseXMLmember(member):
    if member.find('string') is not None:
        return member.find('string').text
    if member.find('i4') is not None:
        return int(member.find('i4').text)
    if member.find('boolean') is not None:
        return bool(int(member.find('boolean').text))
    if member.find('struct') is not None:
        return {m.find('name').text: parseXMLmember(m.find('value')) for m in member.find('struct')}

card_id = os.environ.get('CARD_ID', '1234567')
card_serial_number = os.environ.get('CARD_SERIAL_NUMBER', '12345678123455678')

login_resp = sessionLogin(sys.argv[1] if len(sys.argv) > 1 else -1)
print(login_resp)
resp = rechercher_support_par_numero_serie(login_resp['session_id'], card_id)
print(resp)
if 'fault' in resp:
    resp = rechercher_support_par_numero_serie(login_resp['session_id'], card_serial_number)
    print(resp)
    if 'fault' in resp:
        sys.exit(1)
# print(downloadedAt(login_resp['session_id'], card_id))
# print(isEligibleBascule(login_resp['session_id'], card_id))
# print(rechercher_solde_millesime(login_resp['session_id'], card_id))
# print(customerShow(login_resp['session_id'], str(login_resp['customer_id'])))
# print(customerGetCardInfos(login_resp['session_id'], card_id))
# print(customerGetBalance(login_resp['session_id'], card_id))
