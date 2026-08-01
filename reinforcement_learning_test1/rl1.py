import numpy as np

inputs = [1, 2, 3, 4, 5]
output_target = [13, 16, 19, 22, 25]

w = np.random.uniform(0.1, 10)
learning_rate = 0.01
epochs = 2500
bias = np.random.uniform(0.1, 20)

def predict(i):
    return w * i + bias

for epoch in range(epochs):
    prediction_list = [predict(i) for i in inputs]
    error_list = [ot - p for p, ot in zip(prediction_list, output_target)]

    sign_error_list = [1 if e > 0 else -1 for e in error_list]

    error_average = sum(abs(e) for e in error_list) / len(error_list)

    print(f"Epoch:{epoch}, Weight: {w:.2f}, Bias:{bias}, Error:{error_average:.2f}")    

    w += learning_rate * sum(e * x for e, x in zip(sign_error_list, inputs)) / len(inputs)
    bias += learning_rate * sum(sign_error_list) / len(sign_error_list)

test_inputs = [6, 7]
test_output_targets = [28, 31]

prediction_list = [predict(i) for i in test_inputs]

for i, t, p in zip(test_inputs, test_output_targets, prediction_list):
    print(f"Input:{i}, Target:{t}, Prediction:{p}")