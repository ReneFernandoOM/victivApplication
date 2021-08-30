# victivApplication
Test Task for the Junior Python Developer vacancy at Victiv. 

This application uses the Mapbox API which you can get here: <https://docs.mapbox.com/api/overview/#access-tokens-and-token-scopes>

## Installation
To install this application you should clone this repository and set up the next environment variables:

- FLASK_APP = victiv_test_app.py
- FLASK_ENV = development
- MAPBOX_API_KEY = {YOUR_API_KEY} 

Next you should install the required dependencies:

    pip install -r requirements.txt

Finally, to run the application, simply do:

    flask run

## Using the API
This application only has one endpoint:

GET /api/distance_to_mkad

Required query parameters:

- address
    - Any adress (try to be really specific).

Example request:

    /api/distance_to_mkad?address=1920 S Dobson Rd, Mesa, AZ 85202, Estados Unidos

Example response:

    {
        "data": {
            "1920 North Dobson Road, Chandler, Arizona 85224, United States": {
                "distance_km": 9688.417158948352,
                "distance_mi": 6020.0917700557375,
                "lat": 33.334942,
                "lon": -111.87654
            },
            "1920 South Dobson Road, Chandler, Arizona 85224, United States": {
                "distance_km": 9694.618827519564,
                "distance_mi": 6023.945300855831,
                "lat": 33.276633,
                "lon": -111.876281
            },
            "1920 South Dobson Road, Mesa, Arizona 85202, United States": {
                "distance_km": 9683.69930321826,
                "distance_mi": 6017.16023604073,
                "lat": 33.379619,
                "lon": -111.878006
            },
            "S Dobson Rd, Chandler, Arizona 85286, United States": {
                "distance_km": 9693.777546282758,
                "distance_mi": 6023.422553933717,
                "lat": 33.28569535,
                "lon": -111.8808977
            },
            "S Dobson Rd, Mesa, Arizona 85202, United States": {
                "distance_km": 9684.312025224337,
                "distance_mi": 6017.540963113646,
                "lat": 33.3724146,
                "lon": -111.8722374
            }
        }
    }
