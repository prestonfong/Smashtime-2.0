from flask import Flask, request, Response
import socket
import json


app = Flask(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5000))

@app.route("/", methods=["POST"])
def incoming():
    # Send message through socket as string
    message = json.dumps(request.form.to_dict())
    sock.sendto(message.encode(), ("127.0.0.1", 5001))
    return Response("OK", status=200)

if __name__ == "__main__":
    app.run(debug=False)


