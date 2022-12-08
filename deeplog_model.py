import os
import json
import tensorflow as tf

# Load the jsonl data from the .gz files and return a Dataset object
def load_data(path):
  # Get a list of the file paths that match the given path
  file_paths = tf.io.gfile.glob(path)

  # Create a Dataset from the list of file paths
  dataset = tf.data.Dataset.from_tensor_slices(file_paths)

  # Load the data from the .gz files and return a Dataset object
  dataset = dataset.interleave(
      lambda x: tf.data.TFRecordDataset(x, compression_type='GZIP'),
      cycle_length=4,
      num_parallel_calls=tf.data.experimental.AUTOTUNE
  )
  return dataset

# Load the jsonl data from the .gz files and return a Dataset object
dataset = load_data('/Users/tinoftu/Downloads/dataa/kartta.tuusula.fi/rikastettu/*.gz')

# Preprocess the data by extracting relevant features and attributes
@tf.function
def preprocess_data(data):
  features = {
    'method': tf.train.Feature(bytes_list=tf.train.BytesList(value=[data['method'].numpy()])),
    'status': tf.train.Feature(int64_list=tf.train.Int64List(value=[data['status'].numpy()])),
    'request_path': tf.train.Feature(bytes_list=tf.train.BytesList(value=[data['request_path'].numpy()]))
  }
  example = tf.train.Example(features=tf.train.Features(feature=features))
  return example


# Apply the preprocessing function to each element in the dataset
dataset = dataset.map(preprocess_data)

# Split the dataset into training and validation sets
train_dataset = dataset.take(int(0.8 * dataset.count()))
val_dataset = dataset.skip(int(0.8 * dataset.count()))

# Define the architecture of the DeepLog model
model = tf.keras.Sequential([
  # Use an Embedding layer to convert the input text into dense vectors
  tf.keras.layers.Embedding(input_dim=10000, output_dim=8),
  # Use a LSTM layer to learn sequential dependencies in the data
  tf.keras.layers.LSTM(8),
  # Use a Dense layer with a sigmoid activation to output a binary prediction
  tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model with a binary cross-entropy loss and an Adam optimizer
model.compile(loss='binary_crossentropy', optimizer='adam')

# Train the model on the training set, using the validation set as a validation set
history = model.fit(train_dataset, validation_data=val_dataset)

# Save the trained model in TensorFlow SavedModel format
model.save("/Users/tinoftu/Documents", "tf")