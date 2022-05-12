import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras import layers, models
import keras.utils as utils
from keras.layers import Conv2D, Flatten, Dense, Dropout, BatchNormalization
from keras.layers.core import Activation
from tensorflow.keras.optimizers import Adam 
from keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import ADASYN
import data_mapping as dm

# Mute down the warning signals
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():

    #Fetch dataset
    try:
        data = pd.read_csv('stroke-dataset.csv')
    except:
        print('File path not correct, please make required adjustments and re-run!')
        exit()

    #assign the null indexed BMI rows a mean value of all other BMIs present
    data = data.fillna(data['bmi'].mean())
   
    #drop rows which do not conclude to our prediction eg id
    data.drop('id', axis=1, inplace=True)

    #calling other class for data mapping
    dm.dataMapping(data)

    # split independant and dependant variables
    x = data.drop('stroke', axis=1)
    y = data['stroke']

    # Solving sample imbalancing issue, regulates the under and over sampling data frequency
    ada = ADASYN() #using ADASYN dataset encoding to increase data effeciency
    x, y = ada.fit_resample(x, y)

    # Training and testing dataset splitting
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    x_val = x_train[:300]
    y_val = y_train[:300]

    #create a sequential model to be trained with various activation neural layers
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(10,), kernel_initializer='uniform'))

    # Hidden layer with 64 neurons
    model.add(layers.Dense(64, activation='relu'))

    # Hidden layer with 32 neurons
    model.add(layers.Dense(32, activation='relu'))

    # Hidden layer with 12 neurons
    model.add(layers.Dense(12, activation='relu'))

    # Output layer: 1 neuron, sigmoid activation 
    model.add(layers.Dense(1, activation='sigmoid'))

    #regression output
    print(model.summary())

    model.compile(optimizer=Adam(0.001), loss='binary_crossentropy', metrics=['binary_accuracy'])

    history = model.fit(x_train, y_train, epochs=18, batch_size=27, validation_data=(x_val, y_val))

    print('Model performance rate as follows :')
    print(model.evaluate(x_test, y_test, batch_size=27))

    # Plot the predicted accuracy and loss variables into graphical representation
    epochs = range(1, len(history.history['loss']) +1)
    plt.plot(epochs, history.history['loss'], color='red', marker='o', label='Train loss')
    plt.plot(epochs, history.history['val_loss'], color='blue', marker='o', label='Validate loss')
    plt.title('Training and Validation Loss Model')
    plt.xlabel('Total Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('loss.png')
    plt.clf()

    plt.plot(epochs, history.history['binary_accuracy'], color='red', marker='o', label='Train accuracy')
    plt.plot(epochs, history.history['val_binary_accuracy'], color='blue', marker='o', label='Validate accuracy')
    plt.title('Training and Validation Accuracy Model')
    plt.xlabel('Total Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('accuracy.png')
    plt.clf()

    #save the model file for further reference
    model.save('model.h5')

if __name__ == '__main__':
    main()
