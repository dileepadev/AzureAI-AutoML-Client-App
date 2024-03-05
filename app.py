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
