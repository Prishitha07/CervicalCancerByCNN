# -*- coding: utf-8 -*-
"""CervicalCancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t_HUPVBkneBok0Vt3DFjUI6zi74s2-u7
"""

import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

cancer = pd.read_csv("/content/drive/MyDrive/kag_risk_factors_cervical_cancer.csv")
cancer.head()

cancer.shape

cancer.info()

X=cancer.drop('Biopsy',axis=1)
y=cancer['Biopsy']

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Iterate through columns and apply LabelEncoder to object (string) columns
for column in X.columns:
    if X[column].dtype == 'object':
        label_encoder = LabelEncoder()
        X[column] = label_encoder.fit_transform(X[column])

# Now proceed with scaling (if needed)
min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X.select_dtypes(include=['number']))
print(X_scale)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X_scale,y,test_size=0.20,random_state=0)

from tensorflow import keras
from keras.models import Sequential
from keras.layers import LeakyReLU
from keras.layers import Dense

"""without dropouts"""

model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(35,)))
model.add(Dense(32, activation='relu'))

#Output layer
model.add(Dense(1, activation='sigmoid'))


model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train,epochs=2)

from tensorflow.keras.layers import Dropout

model = Sequential()
model.add(Dropout(0.3, input_shape=(35,)))
model.add(Dense(32,activation='relu'))
model.add(Dense(32, activation='relu', input_shape=(35,)))
model.add(Dropout(0.4))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))

#Output layer
model.add(Dense(1, activation='sigmoid'))


model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=2)

#SDG with Momentum
opt = keras.optimizers.SGD(
    learning_rate=0.01,
    momentum=0.9,
)
model.compile(optimizer=opt,
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train,batch_size=32, epochs=2)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=2)

model.compile(optimizer='adadelta',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=2)

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=2)

model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=1, epochs=2)

model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train,batch_size=32, epochs=2)

y_pred=model.predict(X_test)
y_pred
y_pred = np.where(y_pred > 0.5, 1, 0)
y_pred = y_pred.astype(int)
import numpy as np
np.column_stack((y_pred, y_test))

from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
print(confusion_matrix(y_test,y_pred))
print(accuracy_score(y_test,y_pred))

y_pred=model.evaluate(X_test,y_test)[1]

!pip install lime
import lime
import lime.lime_tabular

from lime.lime_tabular import LimeTabularExplainer
explainer = LimeTabularExplainer(X.values,feature_names=X.columns.values.tolist(),class_names=['TYPE'],mode='regression')
# Now explain a prediction
exp = explainer.explain_instance(X.values[10], model.predict,num_features=5)

exp.as_pyplot_figure()
from matplotlib import pyplot as plt
plt.tight_layout()

exp.show_in_notebook(show_table=True)