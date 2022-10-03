import keras
from keras import models

saved_model_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive_models\predictive_nn"
model = models.load_model(saved_model_path)

prediction = model.predict([[100, 100, 100, 100, 100]])
print(prediction)

