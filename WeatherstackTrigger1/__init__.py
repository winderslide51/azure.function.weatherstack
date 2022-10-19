import logging
import requests
import urllib.parse
import os

import azure.functions as func

access_key=str(os.getenv('weatherstack'))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    city = req.params.get('city')
    if not city:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            city = req_body.get('city')

    if city:
        encoded_city=urllib.parse.quote(city)
        api_url="http://api.weatherstack.com/current?access_key="+access_key+"&query="+encoded_city
        r = requests.get(url=api_url).json()
        return func.HttpResponse(f"{r}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a city in the query string or in the request body for a personalized response.",
             status_code=200
        )
