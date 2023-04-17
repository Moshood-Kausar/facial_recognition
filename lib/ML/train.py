import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.python.keras.layers import layers

# Define emotions
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Resize images to 48x48 and convert to grayscale
data = []
labels = []
for i, emotion in enumerate(emotions):
    for filename in os.listdir(emotion):
        image = cv2.imread(os.path.join(emotion, filename))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (48, 48))
        data.append(resized)
        labels.append(i)

# Conversion of data to numpy array and normalize
data = np.array(data) / 255.0
labels = np.array(labels)

# Split data into training and validation sets
train_data, val_data, train_labels, val_labels = train_test_split(data, labels, test_size=0.2, random_state=42)

#Define the CNN model
model = tf.keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(emotions), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Train the model
history = model.fit(train_data.reshape(-1, 48, 48, 1), train_labels, epochs=50, validation_data=(val_data.reshape(-1, 48, 48, 1), val_labels))

# Convert Keras model to TFLite model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save TFLite model to file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)