import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents_FAQ.json','r',encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.h5')


#funcion para limpiar la oracion del usuario
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence) #tokeniza la oracion del usuario ingresada 
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words] #lematiza cada palabra del usuario ingresada
    return sentence_words

#funcion para crear la bolsa de palabras
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence) #limpia la oracion del usuario
    bag = [0]*len(words) #crea una lista de 0 de la longitud de las palabras
    for s in sentence_words: #recorre cada palabra en la oracion del usuario
        for i,word in enumerate(words): #recorre cada palabra en la lista de palabras
            if word == s: #si la palabra en la lista de palabras es igual a la palabra en la oracion del usuario
                bag[i] = 1 #agrega un 1 a la bolsa de palabras
    return(np.array(bag))

#funcion para predecir la clase de la oracion del usuario
def predict_class(sentence):
    bow = bag_of_words(sentence) #crea la bolsa de palabras
    res = model.predict(np.array([bow]))[0] #predice la clase de la oracion del usuario
    ERROR_THRESHOLD = 0.25 #umbral de error, no queremos que el chatbot responda si no está seguro
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] #guarda los resultados que superan el umbral de error
    results.sort(key=lambda x: x[1], reverse=True) #ordena los resultados
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) #agrega la intencion y la probabilidad de la intencion
    return return_list

#funcion para obtener una respuesta
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent'] #obtiene la intencion
    list_of_intents = intents_json['intents'] #obtiene la lista de intenciones
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses']) #elige una respuesta al azar
            break
    return result