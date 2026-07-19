from flask import Flask, render_template, request, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

# ---------------- MySQL Configuration ----------------

import os

app.config["MYSQL_HOST"] = os.getenv(mysql.railway.internal)
app.config["MYSQL_PORT"] = int(os.getenv(3306, 3306))
app.config["MYSQL_USER"] = os.getenv(root)
app.config["MYSQL_PASSWORD"] = os.getenv(ZiPXKVwfPvKJHwMFvYlntaHrjluibPLF)
app.config["MYSQL_DB"] = os.getenv(railway)

mysql = MySQL(app)

TOTAL_VOTES = 100000

# ---------------- Home Page ----------------

@app.route("/")
def home():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM votes WHERE team=%s", ("spain",))
    spainVotes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM votes WHERE team=%s", ("argentina",))
    argVotes = cur.fetchone()[0]

    cur.close()

    votesLeft = TOTAL_VOTES - (spainVotes + argVotes)

    return render_template(
        "index.html",
        spainVotes=spainVotes,
        argVotes=argVotes,
        votesLeft=votesLeft
    )

# ---------------- Vote API ----------------

@app.route("/vote", methods=["POST"])
def vote():

    # Allow only one vote per browser
    if request.cookies.get("voted"):
        return jsonify({
            "error": "You have already voted!"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    team = data.get("team")

    if team not in ["spain", "argentina"]:
        return jsonify({
            "error": "Invalid team selected"
        }), 400

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO votes(team) VALUES(%s)",
        (team,)
    )

    mysql.connection.commit()

    cur.execute("SELECT COUNT(*) FROM votes WHERE team=%s", ("spain",))
    spainVotes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM votes WHERE team=%s", ("argentina",))
    argVotes = cur.fetchone()[0]

    cur.close()

    votesLeft = TOTAL_VOTES - (spainVotes + argVotes)

    response = make_response(jsonify({
        "spainVotes": spainVotes,
        "argVotes": argVotes,
        "votesLeft": votesLeft
    }))

    # Cookie valid for one year
    response.set_cookie(
        "voted",
        "yes",
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax"
    )

    return response

# ---------------- Reset API (Development Only) ----------------

@app.route("/reset", methods=["POST"])
def reset():

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM votes")
    cur.execute("ALTER TABLE votes AUTO_INCREMENT = 1")

    mysql.connection.commit()

    cur.close()

    response = make_response(jsonify({
        "message": "Poll reset successfully."
    }))

    # Remove vote cookie so you can vote again
    response.set_cookie("voted", "", expires=0)

    return response

# ---------------- Run ----------------

if __name__ == "__main__":
    app.run(debug=True)