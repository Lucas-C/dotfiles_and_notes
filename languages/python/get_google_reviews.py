#!/usr/bin/env python
# USAGE:
#   export $(xargs < .env)
#   get_google_reviews.py
import requests
import json
import os
import sys

API_KEY = os.environ["GOOGLE_API_KEY"]


def place_details(place_id, fields="*"):
    # fields could also be: reviews / places.reviews
    resp = requests.get(f"https://places.googleapis.com/v1/places/{place_id}", headers={
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": fields,
    })
    # resp.raise_for_status()
    return resp.json()

def places_search(text_query, fields="*"):
    places = []
    page_token = None
    while page_token is not False:
        resp = requests.post("https://places.googleapis.com/v1/places:searchText", json={
            "textQuery" : text_query,
            "pageToken": page_token,
            # "minRating": 5,
            "locationBias": {
              "circle": {
                "center": {
                  "latitude": 47.51722,
                  "longitude": -0.4471260
                },
                "radius": 100.0
              }
            }
        }, headers={
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": fields,
        })
        resp.raise_for_status()
        data = resp.json()
        if "places" not in data:
            break
        places.extend(data["places"])
        page_token = data.get("nextPageToken", False)
        if page_token:
            print("Fetching another page of results...", file=sys.stderr)
    print(f"{len(places)} matching places found", file=sys.stderr)
    return places


if __name__ == "__main__":
    # https://maps.app.goo.gl/dhyYSnfzMPtPYh3z9
    # => this is probably a ServiceAreaBusiness, and hence does not have a dedicated place ID :(
    # => adding an address to the business could maybe solve this problem
    # https://www.google.com/maps/place/?q=place_id:ChIJ-x1A3FBxCEgR9bscD3btD3g
    print(json.dumps(place_details("ChIJ-x1A3FBxCEgR9bscD3btD3g", fields="id"), indent=4))
        # -> "status": "NOT_FOUND"
        # -> "message": "The provided Place ID is no longer valid...",
    # print(json.dumps(places_search("l'instant présent", fields="places.id,places.displayName,places.formattedAddress,places.shortFormattedAddress,places.nationalPhoneNumber,places.googleMapsUri,places.regularOpeningHours,places.reviews"), indent=4))
