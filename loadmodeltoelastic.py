import requests

# Set the endpoint for the Elasticsearch model API
endpoint = 'http://localhost:9200/_ml/inference/my_model'

# Load the model zip file into memory
with open('my_model.zip', 'rb') as f:
    model_data = f.read()

# Make a POST request to the model API to upload the model
response = requests.post(endpoint, data=model_data, headers={'Content-Type': 'application/zip'})

# Check the response status code to see if the model was successfully uploaded
if response.status_code == 200:
    print('Model successfully uploaded to Elasticsearch!')
else:
    print(f'Error uploading model: {response.text}')
