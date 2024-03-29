import urllib.request
import json
import os
import ssl
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if (
        allowed
        and not os.environ.get("PYTHONHTTPSVERIFY", "")
        and getattr(ssl, "_create_unverified_context", None)
    ):
        ssl._create_default_https_context = ssl._create_unverified_context


def predictAPI():
    allowSelfSignedHttps(
        True
    )  # this line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = {
        "Inputs": {
            "data": [
                {
                    "Path": "example_value",
                    "day": 1,
                    "mnth": 1,
                    "year": 2022,
                    "season": 2,
                    "holiday": 0,
                    "weekday": 1,
                    "workingday": 1,
                    "weathersit": 2,
                    "temp": 0.3,
                    "atemp": 0.3,
                    "hum": 0.3,
                    "windspeed": 0.3,
                }
            ]
        },
        "GlobalParameters": 0.0,
    }

    body = str.encode(json.dumps(data))

    url = os.environ.get("ENDPOINT")
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = os.environ.get("KEY")
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {
        "Content-Type": "application/json",
        "Authorization": ("Bearer " + api_key),
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        # Return the result as a string
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", "ignore"))


# print(predictAPI())
