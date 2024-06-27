import nltk 
from nltk.stem import WordNetLemmatizer
import json 
import numpy as np
import pickle 
import random
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
from keras.optimizers.schedules import ExponentialDecay


data = open('intents_FAQ.json','r', encoding='utf-8').read()
intents=json.loads(data)


lemmatizer= WordNetLemmatizer()

words=[]
classes=[]
documents=[]
ignore_letters=['!','?','.',',']

#recorre cada intencion en el archivo json y sus patrones
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenizar cada palabra
        word_list=nltk.word_tokenize(pattern)
        words.extend(word_list)
        #agregar documentos en el corpus
        documents.append((word_list,intent['tag']))
        #agregar a la lista de clases
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#lemmatizar,convertir en minusculas y excluir palabras ignoradas
words=[lemmatizer.lemmatize(word_list.lower()) for word_list in words if word_list not in ignore_letters]
words=sorted(list(set(words)))

#ordenar clases
clasees=sorted(list(set(classes)))

#guardar palabras y clases en archivos pickle
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training=[]
output_empty=[0]*len(classes)

#creacion de la bolsa de palabras
for document in documents:
    bag=[]
    word_patterns=document[0]
    word_patterns=[lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        #creacion de la bolsa de palabras con 1 si la palabra está en los patrones de la intencion
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row=list(output_empty)
    # crea una fila de salida con 1 en la posicion de la etiqueta de la intencion
    output_row[classes.index(document[1])]=1
    training.append([bag,output_row])

#mezclar aleatoriamente y convertir en array
random.shuffle(training)

#divide el conjunto de entrenamiento en caracteristicas (train_x) y etiquetas (train_y)
training_x=[row[0] for row in training]
training_y=[row[1] for row in training]

#convierte listas en arrays
training_x=np.array(training_x)
training_y=np.array(training_y)

#creacion del modelo de la red neuronal
model=Sequential() #modelo secuencial de red neuronal con capas densas y dropout
model.add(Dense(128,input_shape=(len(training_x[0]),),activation='relu')) #capa densa con 128 neuronas y funcion de activacion relu 
model.add(Dropout(0.5)) #dropout del 50% para evitar el sobreajuste del modelo 
model.add(Dense(64,activation='relu')) #capa densa con 64 neuronas y funcion de activacion relu 
model.add(Dropout(0.5)) #dropout del 50% para evitar el sobreajuste del modelo
model.add(Dense(len(training_y[0]),activation='softmax')) #capa densa con la cantidad de neuronas igual a la cantidad de etiquetas y funcion de activacion softmax que devuelve la probabilidad de cada clase 

#configuracion del optimizador con una tasa de aprendizaje decreciente
lr_schedule=ExponentialDecay(
    initial_learning_rate=0.01, #tasa de aprendizaje inicial 
    decay_steps=10000, #pasos de decaimiento para reducir la tasa de aprendizaje 
    decay_rate=0.9)

sgd=SGD(learning_rate=lr_schedule,momentum=0.9,nesterov=True) #optimizador SGD con tasa de aprendizaje decreciente, momento y nesterov 
model.compile(loss='categorical_crossentropy', optimizer=sgd ,metrics=['accuracy']) #compilacion del modelo con funcion de perdida categorical_crossentropy, optimizador sgd y metrica de precision 

#entrenamiento y guardado del modelo
hist=model.fit(training_x,training_y,epochs=200,batch_size=5,verbose=1) #entrenamiento del modelo con 200 epocas, tamaño de lote de 5 y verbose 1 para mostrar el progreso del entrenamiento 

#guardar el modelo
model.save('chatbot_model.h5',hist) 

print('Modelo creado')