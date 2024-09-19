#!/usr/bin/env python3
# INSTALL: pip install requests-ip-rotator fake-useragent
# AWS policy needed: AmazonAPIGatewayAdministrator works, but is maybe "too much"
# Note: this is not enough to bypass CloudFront
import sys
from urllib.parse import urlparse
from fake_useragent import FakeUserAgent
import requests
from requests_ip_rotator import ApiGateway

test_url = sysLargv[1] if len(sys.argv) > 1 else "http://ipv4.icanhazip.com"

test_uri = urlparse(test_url)
test_base_url = f"{test_uri.scheme}://{test_uri.netloc}/"

fakeuseragent = FakeUserAgent()

# Create gateway object and initialise in AWS
with ApiGateway(test_base_url, verbose=True) as gateway:
    # Assign gateway to session
    session = requests.Session()
    session.mount(test_base_url, gateway)

    # Send request (IP & User-Agent will be randomised)
    response = session.get(test_url, headers={
        "User-Agent": fakeuseragent.random
    })
    print("HTTP status:", response.status_code)
    print(response.text)
