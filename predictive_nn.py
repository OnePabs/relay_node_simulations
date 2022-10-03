import numpy as np
import keras
from keras import models
from keras.utils import to_categorical
from keras.utils.vis_utils import model_to_dot
from sklearn.model_selection import train_test_split

BATCH_SIZE = 100
EPOCHS = 10

# Load data
inputs_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive-training\inputs_test.csv"
labels_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive-training\labels_test.csv"
save_model_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive_models\predictive_nn"

input_data = np.genfromtxt(inputs_path, delimiter=',')
labels_data = np.genfromtxt(labels_path, delimiter=',')

# delete headers
input_data = np.delete(input_data, 0, 0)
labels_data = np.delete(labels_data, 0, 0)

np.delete(labels_data, 0, 0)


print("inputs shape: " + str(input_data.shape))
print("labels shape: " + str(labels_data.shape))

# Split dataset into train (50%), validation (25%), and test (25%)
X_train, X_rem, y_train, y_rem = train_test_split(input_data, labels_data, train_size=0.5)
X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=0.8)

print("X train shape: " + str(X_train.shape))
print("Y train shape: " + str(y_train.shape))
print("X X_test shape: " + str(X_test.shape))
print("Y y_test shape: " + str(y_test.shape))
print("X X_valid shape: " + str(X_valid.shape))
print("Y y_valid shape: " + str(y_valid.shape))

# create and specify the structure of the model
model = models.Sequential()
model.add(keras.layers.Dense(128, input_shape=(5,)))      # batches of 8. innput data of size (num_points,5)
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))

#compile the model
model.compile(optimizer='Adam', loss='binary_crossentropy', metrics=["accuracy"])


#train the model
print()
history = model.fit(X_train, y_train, batch_size=8, epochs=10, validation_data=(X_valid, y_valid))
print(history.history)

# save the model
model.save(save_model_path)

# Evaluate model on Test data
print()
results = model.evaluate(X_test, y_test, batch_size=8)
print('test loss, test acc:', results)

# predict one value
print()
prediction = model.predict([[50, 50, 50, 50, 50]])
print("prediction: ", prediction)

# Summary of neural network
# model.summary()


