import json
import tensorflow as tf

# Load the JSON data from the log file
with open('/Users/tinoftu/Downloads/syke/syke.jsonl') as f:
    log_data = [json.loads(line) for line in f]

# Extract the relevant features and attributes from the JSON data
features = []
for datapoint in log_data:
    http = datapoint['http']
    subject = datapoint['subject']
    target = datapoint['target']
    features.append([
        http['method'],
        http['status'],
        http['millis'],
        subject['browser'],
        subject['city'],
        subject['country'],
        subject['device'],
        subject['os'],
        target['requestType'],
        target['offering'],
    ])

# Convert the features list into a Tensorflow dataset
dataset = tf.data.Dataset.from_tensor_slices(features)

# Define the deep learning model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the dataset
history = model.fit(dataset, epochs=20)

# Save the trained model in TensorFlow SavedModel format
model.save("/Users/tinoftu/Documents", "tf")