#!/usr/bin/env python

# USAGE: API_KEY=... ./sncf_station.py $stop_area
# Documentation: https://doc.navitia.io/#coverage
# Ce script n'inclue pas les changements d'horaires "temps réel" :(
# Note: feed publisher is "SNCF PIV Production"

import json, os, urllib.request, sys
from base64 import b64encode
from datetime import datetime
from urllib.error import HTTPError

STATION_ID_PER_CITY_NAME = {
    "Angers": 87484006,
    "Nantes": 87481002,
    "StMath": 87487892,
    "Champtocé": 87484352,
}

def main():
    station_name = sys.argv[1]
    stop_area = int(STATION_ID_PER_CITY_NAME.get(station_name, station_name))
    # 1st: retrieve & display station name:
    # json_resp = http_get(f'https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:{stop_area}',
                         # auth=(os.environ['API_KEY'], ''), parse_json=True)
    # print(json_resp["stop_areas"][0]["label"])
    # 2nd: retrieve & display departure times:
    json_resp = http_get(f'https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:{stop_area}/departures?data_freshness=realtime&duration=86400&count=20&direction_type=all',
                         auth=(os.environ['API_KEY'], ''), parse_json=True)
    # with open('sncf.json', 'w+') as json_file:
        # json.dump(json_resp, json_file, indent=4)
    print(f'Prochain départs en gare de {station_name}:')
    for departure in json_resp['departures']:
        name = departure['display_informations']['name']
        direction = departure['display_informations']['direction'].split(' (')[0]
        commercial_mode = departure['display_informations']['commercial_mode']
        delay_msg = ''
        departure_date_time = departure['stop_date_time']['departure_date_time']
        base_departure_date_time = departure['stop_date_time'].get('base_departure_date_time', departure_date_time)
        if departure_date_time != base_departure_date_time:
            delay_msg = f'inclus retard au départ: {time_diff(base_departure_date_time, departure_date_time)}min'
        arrival_date_time = departure['stop_date_time']['arrival_date_time']
        base_arrival_date_time = departure['stop_date_time'].get('base_arrival_date_time', arrival_date_time)
        if arrival_date_time != base_arrival_date_time:
            delay_msg = f" retard à l'arrivée: {time_diff(base_arrival_date_time, arrival_date_time)}min"
        if delay_msg:
            delay_msg = f' ({delay_msg})'
        print(f'* {direction} [{commercial_mode}] depart: {horaire(departure_date_time)}{delay_msg}')

    now = datetime.now()
    if json_resp['disruptions']:
        print('Disruptions that applies to current time:')
    for disruption in json_resp['disruptions']:
        status = disruption['status']  # active, future...
        updated_at = disruption['updated_at']
        assert len(disruption['application_periods']) == 1
        application_periods = disruption['application_periods'][0]
        begin, end = as_dt(application_periods["begin"]), as_dt(application_periods["end"])
        if now < begin or now > end:
            continue
        if 'messages' in disruption:
            assert len(disruption['messages']) == 1, len(disruption['messages'])
            msg = disruption['messages'][0]['text']
        else:
            msg = ""
        for impacted_object in disruption['impacted_objects']:
            for impacted_stop in impacted_object['impacted_stops']:
                cause = impacted_stop['cause'] or ''
                departure_status = impacted_stop['departure_status']
                if departure_status != 'unchanged':
                    cause += f" departure={departure_status}"
                arrival_status = impacted_stop['arrival_status']
                if arrival_status != 'unchanged':
                    cause += f" arrival={arrival_status}"
                # ['stop_time_effect'] semble être la combinaison de departure_status & arrival_status
                amended_departure_time = impacted_stop.get('amended_departure_time')
                if amended_departure_time and amended_departure_time != impacted_stop['base_departure_time']:
                    cause += f" +{horaire_diff(impacted_stop['base_departure_time'], amended_departure_time)}min"
                amended_arrival_time = impacted_stop.get('amended_arrival_time')
                if amended_arrival_time and amended_arrival_time != impacted_stop['base_arrival_time']:
                    cause += f" +{horaire_diff(impacted_stop['base_arrival_time'], amended_arrival_time)}min"
                if not cause:
                    cause = ' unknown cause'
                stop_point_name = impacted_stop['stop_point']['name']
                train_id = impacted_stop['stop_point']['id']
                print(f'* {stop_point_name}: {msg} -{cause} ({status} - begin: {begin} - end: {end})')# - updated-on: {as_dt(updated_at)})')

def http_get(url, auth=None, timeout_in_secs=5, parse_json=False):
    req = urllib.request.Request(url)
    if auth:
        encoded_creds = b64encode(('%s:%s' % auth).encode('utf-8'))
        req.add_header('Authorization', 'Basic %s' % encoded_creds.decode('utf-8'))
    try:
        with urllib.request.urlopen(req, timeout=timeout_in_secs) as resp:
            if parse_json:
                return json.load(resp)
            return resp.read().decode('utf-8')
    except HTTPError as error:
        if error.fp:
            print("HTTP response:", error.fp.read().decode())
        raise error

def horaire(time_str):  # convert a string like 20210907T193130 into HHhMM
    time_str = time_str.split('T')[1]
    return time_str[:2] + 'h' + time_str[2:4]

def as_dt(time_str):  # parse a string into a datetime object
    return datetime.strptime(time_str, '%Y%m%dT%H%M%S')

def time_diff(start_time_str, end_time_str):  # result is an integer number of minutes
    return (as_dt(end_time_str) - as_dt(start_time_str)).seconds // 60

def horaire_diff(hh_mm_ss_start, hh_mm_ss_end):  # result is an integer number of minutes
    hh_start = int(hh_mm_ss_start[:2])
    mm_start = int(hh_mm_ss_start[2:4])
    hh_end = int(hh_mm_ss_end[:2])
    mm_end = int(hh_mm_ss_end[2:4])
    return (hh_end * 60 + mm_end) - (hh_start * 60 + mm_start)

if __name__ == '__main__':
    main()
