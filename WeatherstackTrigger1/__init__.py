import logging
import json
import base64
import azure.functions as func
import urllib.parse
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('ContentData')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('ContentData')
    if name:
        decoded = base64.b64decode(name)
        var_type = type(decoded)
        my_json = decoded.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        city = data['data']['customerDetails']['town']
        logging.info(f"Python HTTP trigger function processed a request. {var_type} {my_json}")
        access_key = "c95a3df9c4501d5a1021f2c510965289"
        encoded_city=urllib.parse.quote(city)
        api_url="http://api.weatherstack.com/current?access_key="+access_key+"&query="+encoded_city
        r = requests.get(url=api_url).json()
        return func.HttpResponse(f"Hello, {city}. This HTTP triggered function executed successfully. {r}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )