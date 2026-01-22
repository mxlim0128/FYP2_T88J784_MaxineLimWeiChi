import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten, Dropout

def build_seq2point_model(input_shape):
    # ... (The model architecture itself)
    model = Sequential()
    # 1. Feature Extraction Layers (Using 0.3 Dropout)
    model.add(Conv1D(30, 10, activation='relu', input_shape=input_shape, padding='same'))
    model.add(Conv1D(30, 8, activation='relu', padding='same'))
    model.add(Conv1D(40, 6, activation='relu', padding='same'))
    model.add(Conv1D(50, 5, activation='relu', padding='same'))
    model.add(Dropout(0.3)) 
    model.add(Conv1D(50, 5, activation='relu', padding='same'))
    model.add(Dropout(0.3))

    # 2. Regression Head
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.3))
    
    # 3. Final Output
    model.add(Dense(1, activation='linear'))
    
    return model
