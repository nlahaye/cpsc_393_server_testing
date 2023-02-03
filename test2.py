from tensorflow.keras.datasets import mnist
import tensorflow.keras as kb
from tensorflow.keras import backend
import tensorflow as tf
from sklearn.preprocessing import LabelBinarizer
import pandas as pd
from tensorflow.keras.optimizers import SGD
import pathlib

((trainX, trainY), (testX, testY)) = mnist.load_data()
trainX = trainX.reshape((trainX.shape[0], 28 * 28 * 1))
testX = testX.reshape((testX.shape[0], 28 * 28 * 1))
trainX = trainX.astype("float32") / 255.0
testX = testX.astype("float32") / 255.0

lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

trainX_df = pd.DataFrame(trainX)
# trainX_df.iloc[1:100].to_csv("out.csv")

#structure of the model

model = kb.Sequential([
    kb.layers.Dense(250, input_shape =[784]), #input
    kb.layers.Dense(100),
    kb.layers.Dense(50),
    kb.layers.Dense(30),
    kb.layers.Dense(20),
    kb.layers.Dense(10),
    kb.layers.Dense(10, activation = "softmax") #output
])

#how to train the model
model.compile(loss="categorical_crossentropy", optimizer=SGD(0.01),
	metrics=["accuracy"])

#fit the model (same as SKlearn)
model.fit(trainX,trainY, epochs = 100)

export_dir = "./1/"
tf.saved_model.save(model, export_dir)
# Convert the model into TF Lite.
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()
#save model 
tflite_model_files = pathlib.Path('./my_test_mod.tflite')
tflite_model_files.write_bytes(tflite_model)

