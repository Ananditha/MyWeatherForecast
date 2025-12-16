from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    forecast_result = ""
    if request.method == "POST":
        country = request.form.get("country")

        subprocess.run(["python", "WeekForecast.py"])

        result = subprocess.run(
            ["python", "e2stest.py", country],
            capture_output=True,
            text=True
        )
        forecast_result = result.stdout

    return render_template("Forecast.7.html", forecast=forecast_result)



if __name__ == "__main__":
    app.run(debug=True)


