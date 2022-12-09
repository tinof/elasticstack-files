import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
import time
import json

def generate(name, window_size):
    num_sessions = 0
    inputs = []
    outputs = []
    with open(name, 'r') as f:
        for line in f:
            num_sessions += 1
            data = json.loads(line)
            input_data = [data['requestTime']]
            output_data = [data['requestTime'] + 1]
            for i in range(len(input_data) - window_size):
                inputs.append(input_data[i:i + window_size])
                outputs.append(output_data[i + window_size])
    print('Number of sessions({}): {}'.format(name, num_sessions))
    print('Number of seqs({}): {}'.format(name, len(inputs)))
    return inputs, outputs



def lstm_train(x, y, num_epochs, batch_size):
    model = Sequential()
    model.add(LSTM(64, activation='relu', return_sequences=True, input_shape=(x.shape[1], x.shape[2])))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    model.fit(x, y, epochs=num_epochs, batch_size=batch_size, shuffle=True)
    return model


if __name__ == "__main__":
    start_time = time.time()
    num_classes = 28
    num_epochs = 50
    batch_size = 2048
    window_size = 10

    TP = 0
    FP = 0
    n_candidates = 9  # top n probability of the next tag


    X, Y = generate('/Users/tinoftu/Downloads/dataa/kartta.tuusula.fi/rikastettu/merged.jsonl', window_size)
    X = np.reshape(X, (len(X), window_size, 1))
    X = X / float(num_classes)
    Y = np_utils.to_categorical(Y, num_classes)
    model = lstm_train(X, Y, num_epochs, batch_size)


    def generate1(name, window_size):
        hdfs = set()
        with open(name) as f:
            for ln in f.readlines():
                ln = list(map(lambda n: n - 1, map(int, ln.strip().split())))
                ln = ln + [-1] * (window_size + 1 - len(ln))
                hdfs.add(tuple(ln))
        print('Number of sessions({}): {}'.format(name, len(hdfs)))
        return hdfs

    test_normal_loader = generate1('hdfs_test_normal', window_size)
    test_abnormal_loader = generate1('hdfs_test_abnormal', window_size)

    for line in test_abnormal_loader:
        for i in range(len(line) - window_size):
            seq = line[i: i + window_size]
            label = line[i + window_size]
            X = np.reshape(seq, (1, window_size, 1))
            X = X / float(num_classes)
            Y = np_utils.to_categorical(label, num_classes)
            prediction = model.predict(X, verbose=0)
            if np.argmax(Y) not in prediction.argsort()[0][::-1][: n_candidates]:

                TP += 1
                break

    for line in test_normal_loader:
        for i in range(len(line) - window_size):
            seq = line[i:i + window_size]
            label = line[i + window_size]
            X = np.reshape(seq, (1, window_size, 1))
            X = X / float(num_classes)
            Y = np_utils.to_categorical(label, num_classes)
            prediction = model.predict(X, verbose=0)
            if np.argmax(Y) not in prediction.argsort()[0][::-1][: n_candidates]:
                FP += 1
                break

    elapsed_time = time.time() - start_time
    print('elapsed_time: {:.3f}s'.format(elapsed_time))


    # Compute precision, recall and F1-measure
    FN = len(test_abnormal_loader) - TP
    TN = len(test_normal_loader) - FP
    P = 100 * TP / (TP + FP)
    R = 100 * TP / (TP + FN)
    F1 = 2 * P * R / (P + R)

    print(f"FP:{FP}")
    print(f"FN: {FN}")
    print(f"TP: {TP}")
    print(f"TN: {TN}")

    print('false positive (FP): {}, false negative (FN): {}, Precision: {:.3f}%, Recall: {:.3f}%, F1-measure: {:.3f}%'.format(FP, FN, P, R, F1))
    print('Finished Predicting')