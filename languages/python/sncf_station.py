#!/usr/bin/env python

# USAGE: API_KEY=... ./sncf_station.py $stop_area
#                                      87484006 = Angers
#                                      87481002 = Nantes
#                                      87487892 = St Mathurin

import json, os, urllib.request, sys
from base64 import b64encode
from datetime import datetime


def main():
    stop_area = sys.argv[1]
    json_resp = http_get(f'https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:{stop_area}/departures?data_freshness=realtime',
                         auth=(os.environ['API_KEY'], ''), parse_json=True)

    print('Departs en gare:')
    for departure in json_resp['departures']:
        name = departure['display_informations']['name']
        direction = departure['display_informations']['direction'].split(' (')[0]
        commercial_mode = departure['display_informations']['commercial_mode']
        departure_date_time = departure['stop_date_time']['departure_date_time']
        base_departure_date_time = departure['stop_date_time']['base_departure_date_time']
        if departure_date_time != base_departure_date_time:
            delay_msg = f' (retard: {time_diff(base_departure_date_time, departure_date_time)}min)'
        else:
            delay_msg = ''
        print(f'* {direction} [{commercial_mode}] depart: {horaire(departure_date_time)}{delay_msg}')

    if json_resp['disruptions']:
        print('Disruptions:')
    for disruption in json_resp['disruptions']:
        status = disruption['status']  # active, future...
        assert len(disruption['messages']) == 1, len(disruption['messages'])
        msg = disruption['messages'][0]['text']
        updated_at = disruption['updated_at']
        for impacted_object in disruption['impacted_objects']:
            for impacted_stop in impacted_object['impacted_stops']:
                base_arrival_time = impacted_stop['base_arrival_time']
                amended_arrival_time = impacted_stop['amended_arrival_time']
                base_departure_time = impacted_stop['base_departure_time']
                amended_departure_time = impacted_stop['amended_departure_time']
                cause = impacted_stop['cause'] or 'unknown cause'
                stop_point_name = impacted_stop['stop_point']['name']
                train_id = impacted_stop['stop_point']['id']
                print(f'* {stop_point_name}: {msg} - {cause} ({status})')

def http_get(url, auth=None, timeout_in_secs=5, parse_json=False):
    req = urllib.request.Request(url)
    if auth:
        encoded_creds = b64encode(('%s:%s' % auth).encode('utf-8'))
        req.add_header('Authorization', 'Basic %s' % encoded_creds.decode('utf-8'))
    with urllib.request.urlopen(req, timeout=timeout_in_secs) as resp:
        if parse_json:
            return json.load(resp)
        return resp.read().decode('utf-8')

def horaire(time_str):  # convert a string like 20210907T193130 into HHhMM
    time_str = time_str.split('T')[1]
    return time_str[:2] + 'h' + time_str[2:4]

def as_dt(time_str):  # parse a string into a datetime object
    return datetime.strptime(time_str, '%Y%m%dT%H%M%S')

def time_diff(start_time_str, end_time_str):  # result is an integer number of minutes
    return (as_dt(end_time_str) - as_dt(start_time_str)).seconds // 60


if __name__ == '__main__':
    main()