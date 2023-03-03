from flask import Flask, render_template, request
from chatbot import check_for_introduction, predict_class, get_response, format_response, intents, name

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key_AAAAA"

response_list = []

@app.route("/")
def home():
    global response_list
    response_list.clear()
    return render_template("index.html")

@app.route("/chatbot", methods=["POST", "GET"])
def chatbot():
    global response_list
    if request.method == "POST":
        message = request.form['message']

        response_list.append({"user": "User", "message": message})

        check_for_introduction(message.lower())

        predicted_intents = predict_class(message.lower())

        bot_response = get_response(predicted_intents, intents)

        formatted_response = format_response(bot_response)
        response_list.append({"user": "Bot", "message": formatted_response})
        return render_template("chatbot.j2", response_list=response_list)

    return render_template("chatbot.j2", response_list=response_list)

if __name__ == '__main__':
    app.run(debug=True)