# -*- coding: utf-8 -*-
"""ProiectSACCDMM_epoci30.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kEeG44kpfQBEHsF7s_qf66zAEJ-2CrTD

Importare biblioteci necesare
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import math
import nbconvert

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from keras import Sequential
from tensorflow.keras import layers, losses, metrics
from keras.layers import Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model
from tensorflow.keras.losses import MeanSquaredError

"""Importare baza de date cu imagini"""

(x_train, _), (x_test, _) = fashion_mnist.load_data()

"""Normalizarea imaginilor"""

x_train = x_train.astype('float32')/255
x_test  = x_test.astype('float32')/255

"""Remodelare imagini astfel incat sa fie compatibile cu modelul"""

x_train = x_train.reshape(len(x_train), 28, 28, 1)
x_test = x_test.reshape(len(x_test), 28, 28, 1)
x_test.shape

"""Adaugare zgomot asupra imaginilor"""

noise_factor = 0.4
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)

# modificare valori in intervalul 0-1
x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

"""Afisare cateva imagini pentru a vedea cum arata datele"""

# Alege 5 indici aleatori
indices = np.random.randint(len(x_train), size=5)

# Creează o figură cu 5 subplot-uri aranjate pe 2 rânduri
fig, axes = plt.subplots(2, 5, figsize=(15, 6))

# Iterează prin fiecare subplot și afișează imaginile
for i in range(5):
    # Primul rând: imagini originale
    axes[0, i].imshow(x_train[indices[i]], cmap='gray')
    axes[0, i].axis('off')
    axes[0, i].set_title(f"Imagine Originala {i+1}")

    # Al doilea rând: imagini cu zgomot
    axes[1, i].imshow(x_train_noisy[indices[i]], cmap='gray')
    axes[1, i].axis('off')
    axes[1, i].set_title(f"Imagine cu zgomot {i+1}")

plt.show()

"""Definire Model"""

model = Sequential([
    # retea de codificare
    Conv2D(32, 3, activation='relu', padding='same', input_shape=(28,28,1)),
    MaxPooling2D(2, padding='same'),
    Conv2D(16, 3, activation='relu', padding='same'),
    MaxPooling2D(2, padding='same'),

    # retea de decodificare
    Conv2D(16, 3, activation='relu', padding='same'),
    UpSampling2D(2),
    Conv2D(32, 3, activation='relu', padding='same'),
    UpSampling2D(2),

    # Strat de iesire
    Conv2D(1, 3, activation='sigmoid', padding='same')

])

model.compile(optimizer='adam', loss=losses.MeanSquaredError(), metrics=['accuracy'])
model.summary()

"""Antrenare Model"""

history = model.fit(x_train_noisy, x_train, epochs=30, batch_size=256,  shuffle=True, validation_data=(x_test_noisy, x_test))

"""Afisare grafice pentru pierdere si acuratete in etapa de antrenare si cea de validare"""

# Plot loss and accuracy from training step
def PlotModelHistoryEpoch(model_history):  # plot some data

  print(model_history.history.keys())
  plt.figure(figsize=(20, 5))

  # loss
  plt.subplot(1, 2, 1)
  plt.plot(model_history.history['loss'], label='train loss')
  plt.plot(model_history.history['val_loss'], label='val loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend()
  # plt.show()

  # accuracies
  plt.subplot(1, 2, 2)
  plt.plot(model_history.history['accuracy'], label='train acc')
  plt.plot(model_history.history['val_accuracy'], label='val acc')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend()
  plt.show()


# print model_history for model
PlotModelHistoryEpoch(history)

"""Vizualizare Rezultate"""

# prezicere rezultate de la model
pred = model.predict(x_test_noisy)

# Alege 5 indici aleatori
indices = np.random.randint(len(x_test), size=5)

# Creează o figură cu 5 subplot-uri aranjate pe 2 rânduri
fig, axes = plt.subplots(3, 5, figsize=(15, 6))

# Iterează prin fiecare subplot și afișează imaginile
for i in range(5):
    # Primul rând: imagini originale
    axes[0, i].imshow(x_test[indices[i]], cmap='gray')
    axes[0, i].axis('off')
    axes[0, i].set_title(f"Imagine Originala {i+1}")

    # Al doilea rând: imagini cu zgomot
    axes[1, i].imshow(x_test_noisy[indices[i]], cmap='gray')
    axes[1, i].axis('off')
    axes[1, i].set_title(f"Imagine cu zgomot {i+1}")

    # Al treilea rând: imagini prezise
    axes[2, i].imshow(pred[indices[i]], cmap='gray')
    axes[2, i].axis('off')
    axes[2, i].set_title(f"Imagine prezisa {i+1}")

plt.show()

"""Evaluarea performantei"""

# Calculul erorii pătratice medii (MSE) folosind MeanSquaredError
mse = MeanSquaredError()(x_test, pred) # O valoare MSE mai mică indică o mai bună potrivire
print("MSE (Mean Squared Error) pe setul de validare:", mse.numpy())

# Calculul RMSE ca rădăcina pătrată a MSE
rmse = np.sqrt(mse.numpy())

print("RMSE (Root Mean Squared Error) pe setul de validare:", rmse)

from google.colab import drive
drive.mount('/content/drive')

!jupyter nbconvert --to html "/content/drive/MyDrive/Colab Notebooks/ProiectSACCDMM_epoci30.ipynb" --output "/content/drive/My Drive/ProiectSACCDMM_epoci30.html"