from flask import Flask, render_template, request
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

posts = requests.get("https://api.npoint.io/65b8c9916f80cc2eb302").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    if request.method == 'POST':
        data = request.form
        message_body = (f"Name: {data['name']}\n"
                        f"Email: {data['email']}\n"
                        f"Phone: {data['phone']}\n"
                        f"Message: {data['message']}️")
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=TWILIO_WHATSAPP_TO,
        )
        print(message.sid)
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
