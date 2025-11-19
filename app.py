from flask import Flask, render_template, request
from mbta_helper import find_stop_near   # your helper file

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get the value from the form
        place_name = request.form.get("place_name", "").strip()
        print("PLACE FROM FORM:", repr(place_name))  # DEBUG

        if not place_name:
            # if the user didn’t type anything
            return render_template("error.html",
                                   message="Please enter a location.")

        try:
            station, accessible = find_stop_near(place_name)
        except Exception as e:
            print("ERROR in find_stop_near:", e)
            return render_template("error.html",
                                   message="There was a problem finding a station.")

        return render_template(
            "mbta_station.html",
            place_name=place_name,
            station=station,
            accessible=accessible
        )

    # GET request → just show the form
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)



