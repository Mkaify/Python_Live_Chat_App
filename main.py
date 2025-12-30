from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from dotenv import load_dotenv

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hjhjsdahhds")
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        raw_name = request.form.get("name")
        name = raw_name.strip().title() if raw_name else None
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            # Logic Fix: Use a dictionary 'users' to track connection counts per name
            rooms[room] = {"members": 0, "messages": [], "users": {}} 
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        # Logic Fix: Prevent duplicate names from different users in the same room
        elif name in rooms[room]["users"]:
            return render_template("home.html", error="Name already taken in this room.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    name = session.get("name")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("home"))
    return render_template("room.html", code=room, messages=rooms[room]["messages"], name=name)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    msg_text = data["data"].strip()
    if msg_text:
        msg_text = msg_text[0].upper() + msg_text[1:]
    
    content = {"name": session.get("name"), "message": msg_text}
    send(content, to=room)
    rooms[room]["messages"].append(content)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name or room not in rooms:
        return
    
    join_room(room)
    
    # Logic Fix: Increment the connection count for this specific name
    rooms[room]["users"][name] = rooms[room]["users"].get(name, 0) + 1
    rooms[room]["members"] += 1
    
    # Only send notification if this is the user's first connection (not a second tab)
    if rooms[room]["users"][name] == 1:
        content = {"name": name, "message": "has entered the room", "type": "notification"}
        send(content, to=room)
        rooms[room]["messages"].append(content)
    
    # Send the keys (unique names) to the sidebar
    socketio.emit("user_list", {"names": list(rooms[room]["users"].keys())}, to=room)

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    if room in rooms:
        leave_room(room)
        rooms[room]["members"] -= 1
        
        # Logic Fix: Decrement count and only remove name if all their tabs are closed
        if name in rooms[room]["users"]:
            rooms[room]["users"][name] -= 1
            if rooms[room]["users"][name] <= 0:
                del rooms[room]["users"][name]
                content = {"name": name, "message": "has left the room", "type": "notification"}
                send(content, to=room)
                rooms[room]["messages"].append(content)
        
        socketio.emit("user_list", {"names": list(rooms[room]["users"].keys())}, to=room)

        # Optional: In a real app, you might delay deletion to allow for page refreshes
        if rooms[room]["members"] <= 0:
            del rooms[room]

if __name__ == "__main__":
    socketio.run(app, debug=True)