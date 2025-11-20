from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get what the user typed
        place_name = request.form.get("place_name", "").strip()
        print("PLACE FROM FORM:", repr(place_name))  # DEBUG

        # if user didn't type anything
        if not place_name:
            return render_template(
                "error.html",
                message="Please enter a location."
            )

        try:
            station, accessible = find_stop_near(place_name)
            print("STATION RESULT:", station, "ACCESSIBLE:", accessible)  # DEBUG
        except Exception as e:
            # print the error for debugging
            print("ERROR in find_stop_near:", e)
            return render_template(
                "error.html",
                message="There was a problem finding a station."
            )

        if station is None:
            return render_template(
                "error.html",
                message="No nearby MBTA stations were found."
            )

        # success
        return render_template(
            "mbta_station.html",
            place=place_name,
            station=station,
            accessible=accessible,
        )

    # GET request – show the form
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
