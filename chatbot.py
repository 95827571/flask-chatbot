import json
import random
import pickle
import tensorflow as tf
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

name = ""

lemmatizer =  WordNetLemmatizer()
intents = json.loads(open('data.json').read())
words = pickle.load(open('words.pk1', 'rb'))
classes = pickle.load(open('classes.pk1', 'rb'))

model = tf.keras.models.load_model("chatbot_model.model")

def clean_up_sentence(sentence: str):
    sentence_words = word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence: str):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for i in sentence_words:
        for x, word in enumerate(words):
            if word == i:
                bag[x] = 1

    return np.array(bag)


THRESHOLD = 0.30
def predict_class(sentence: str) -> list:
    bow = bag_of_words(sentence)
    model_results = model.predict(np.array([bow]))[0]
    results = [[intent, probability] for intent, probability, in enumerate(model_results) if probability > THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for result in results:
        return_list.append({'intent': classes[result[0]], 'probablity': str(result[1])})

    return return_list


def get_response(intents_list: list, intents_json) -> str:
    result = ""
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for intent in list_of_intents:
            if intent['tag'] == tag:
                result = random.choice(intent['responses'])
                break
    except:
        result = "Sorry i'm not sure how to respond to that."
    
    return result

def check_for_introduction(user_response: str) -> None:
    global name
    for intent in intents['intents']:
        tag = intent["tag"]
        if tag != "introduction":
            continue

        for pattern in intent["patterns"]:
            if pattern not in user_response:
                continue
            
            name = user_response.split(pattern)[1].strip()

def validate_user_input(user_response: str) -> bool:
    user_response = user_response.lower()
    if user_response == "exit":
        return False

    check_for_introduction(user_response)

    return True

def format_response(bot_response: str) -> str:
    bot_response = bot_response.replace("<name>", name.capitalize())

    return bot_response.strip()

def main():
    print("Chatbot is running, say hi...")
    while True:
        user_response = input()
        if not validate_user_input(user_response):
            break

        predicted_intents = predict_class(user_response)
        bot_response = get_response(predicted_intents, intents)
        print(format_response(bot_response))


if __name__ == '__main__':
    main()