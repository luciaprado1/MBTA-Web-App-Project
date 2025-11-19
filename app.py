from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form.get("place", "")
    station, accessible = mbta_helper.find_stop_near(place)
    if station is None:
        return render_template("error.html", place=place)
    return render_template(
        "mbta_station.html",
        place=place,
        station=station,
        accessibility=accessible,
    )

if __name__ == "__main__":
    app.run(debug=True)



