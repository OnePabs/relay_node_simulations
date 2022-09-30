from keras import models
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from keras.datasets import mnist
from keras.utils.vis_utils import model_to_dot

NUM_ROWS = 8
NUM_COLS = 8
BATCH_SIZE = 100
EPOCHS = 10
