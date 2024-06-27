from flask import Flask, render_template ,request, jsonify
from chatbot import predict_class, get_response, intents


app = Flask(__name__) 

@app.get('/')
def index_get():
    return render_template('base.html')


@app.post('/predict')
def predict():
    data = request.get_json()
    message = data.get('message')  # Obtén el mensaje del objeto JSON

    if message is None:
        return jsonify({"error": "No se proporcionó un mensaje"}), 400

    inst = predict_class(message)
    res = get_response(inst, intents)
    return jsonify({"response": res})

if __name__ == '__main__':
    app.run(debug=True)