from flask import Flask, request, render_template
import mbta_helper

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form.get("place")

    if not place:
        return render_template("error.html", message="Please enter a place.")

    station, accessibility = mbta_helper.find_stop_near(place)

    if station is None:
        return render_template(
            "error.html",
            message=f"No MBTA stop found near '{place}'."
        )

    return render_template(
        "mbta_station.html",
        place=place,
        station=station,
        accessibility=accessibility,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)



