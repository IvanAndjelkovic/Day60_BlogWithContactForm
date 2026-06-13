from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()
yahoo_mail = os.getenv("yahoo_mail")
app_password = os.getenv("app_password")
print(yahoo_mail)
print(app_password)

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form
        message_body = f"Name: {data['name']}\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage: {data['message']}"
        # print(data["name"])
        # print(data["email"])
        # print(data["phone"])
        # print(data["message"])
        try:
            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = yahoo_mail
            msg['To'] = data["email"]
            msg['Subject'] = "New Message from Your Website"

            # Add body
            msg.attach(MIMEText(message_body, 'plain', 'utf-8'))

            with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
                connection.starttls()
                connection.login(yahoo_mail, app_password)
                connection.send_message(msg)
                print(f"Email sent successfully to {data['email']}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
        return render_template("contact.html", msg="Successfully sent your message!")
    return render_template("contact.html", msg="Contact Me")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
