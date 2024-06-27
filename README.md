# Azure AI Auto ML Client App

Demo application to interact with Azure AI by exploring Automated Machine Learning in Azure Machine Learning.

## Getting Started

### ✨ Option 1: Using the template

Follow these steps to set up and run the application locally by cloning the repository.

1. **Clone the repository:**

   ```shell
   git clone https://github.com/dileepadev/AzureAI-AutoML-Client-App.git
   ```

2. **Navigate to the project directory:**

   ```shell
    cd AzureAI-AutoML-Client-App
    ```

3. **Create and activate a virtual environment:**

    ```python
    ## Create virtual environment
    python -m venv venv
    ```

    ```shell
    ## Activate on Windows
    venv\Scripts\activate.bat

    ## Activate on macOS/Linux
    source venv/bin/activate
    ```

4. **Install requirements:**

    ```shell
    pip install -r requirements.txt
    ```

5. **Create `.env` file to store the key**

    ```.env
    KEY=your_key
    ENDPOINT=your_endpoint
    ```

6. **Run the application:**

    ```shell
    python app.py
    ```

### ✨ Option 2: Creating as a new project

Follow these steps to set up and run the application locally from the beginning.

1. **Setup project directory**

   Create directory:

   ```shell
   mkdir AzureAI-AutoML-Client-App
   ```

2. **Navigate to the project directory:**

   ```shell
   cd AzureAI-AutoML-Client-App
   ```

3. **Create and activate a virtual environment:**

    Create virtual environment:

    ```python
    python -m venv venv
    ```

    Activate on Windows:

    ```shell
    venv\Scripts\activate.bat
    ```

    Activate on macOS/Linux:

    ```shell
    source venv/bin/activate
    ```

4. **Install Flask:**

   ```shell
   pip install flask
   ```

5. **Open the project in your preferred code editor:**

    Type this command to open in Visual Studio Code:

   ```shell
   code .
   ```

6. **Create `app.py` for your Flask application:**

   ```python
   from flask import Flask, render_template

   app = Flask(__name__)

   @app.route('/')
   def index():
       return render_template('index.html')

   if __name__ == '__main__':
       app.run(debug=True)
   ```

7. **Create a `templates` directory for HTML templates:**

   ```shell
   mkdir templates
   ```

8. **Create an HTML template inside the `templates` directory, for example, `index.html`:**

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Azure ML Web App</title>
   </head>
   <body>
       <h1>Azure ML Web App</h1>
       <p>This is my Python based web app to working with Azure ML.
   </body>
   </html>
   ```

9. **Run the application:**

    ```shell
    python app.py
    ```

10. **Visit `http://127.0.0.1:5000` in your web browser to see your web app in action.**

11. **Create a `static` directory for static files such as CSS, JavaScript, etc.:**

    ```shell
    mkdir static
    ```

12. **Create a CSS file inside the static directory, for example, `styles.css.` You can add your CSS styles here.**

    ```css
    /* styles.css */
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
    }

    h1 {
        color: #333;
    }

        /* Add more styles as needed */
    ```

13. **Add a link tag `<link>`to your HTML template (index.html) to include the CSS file:**

    Add this line to the `index.html`:

    ```html
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
    ```

    This will be the updated `index.html`:

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Azure ML Web App</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
    </head>
    <body>
        <h1>Azure ML Web App</h1>
        <p>This is my Python based web app to working with Azure ML.
    </body>
    </html>
    ```

14. **Install `python-dotenv` to maintain the .env file, and install `requests` to make requests

    ```shell
    pip install python-dotenv
    pip install requests
    ```

15. **Create `.env` file to store the key**

    ```.env
    KEY=your_key
    ENDPOINT=your_endpoint
    ```

16. **Create `predictAPI.py` to connect with Azure ML**

    ```python
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
    ```

17. **Update `app.py` to use requests**

    ```python
    from flask import Flask, render_template
    import predictAPI

    app = Flask(__name__)


    @app.route("/")
    def index():
        # Call Azure ML API
        prediction = str(predictAPI.predictAPI())
        print("Prediction: ", prediction)

        # Pass data to HTML template for display
        return render_template("index.html", prediction=prediction)


    if __name__ == "__main__":
        app.run(debug=True)
    ```

18. **Update `index.html` to use requests**

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Azure ML Web App</title>
        <link
        rel="stylesheet"
        href="{{ url_for('static', filename='styles.css') }}"
        />
    </head>
    <body>
        <h1>Azure ML Prediction Result</h1>
        {% if prediction %}
        <p>{{ prediction }}</p>
        {% else %}
        <p>Failed to retrieve prediction. Please try again later.</p>
        {% endif %}
    </body>
    </html>
    ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Dileepa Bandara  
[@dileepadev](https://github.com/dileepadev)
