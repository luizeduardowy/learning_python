# 24 NNs with 3 input neurons, 2 hidden layers with 2 neurons each and a output neuron, each one gets the same word (probably unbiased) to make a text
import numpy as np
import math
import os
import unicodedata

nn_count = 24
max_text_length = 20
epoch_started = False
user_interupted = False
initial_prompts = ["Hi"] # "Alive?", "To be or", "Bye" # The initial prompts that the NNs can be given to write a text
prompt_idx = 0
last_word = "" # The NN´s last 5 characters written
nnlist = {}
learning_rate = 0.03
epoch = 0
letter_frequencies = {"e": 0.1249, "t": 0.0928, "a": 0.0804, "o": 0.0764, "i": 0.0757, "n": 0.0723, "s": 0.0651, "r": 0.0628, "h": 0.0505, "l": 0.0407, "d": 0.0382}

# Build a simple custom ascii mapping programmatically to avoid mistakes
my_own_ascii_table = {}
# characters to include: space, digits, lowercase, uppercase and common punctuation
chars = [' '] + list('0123456789') + list('abcdefghijklmnopqrstuvwxyz') + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + [',',';','.','?','!','']
for idx, ch in enumerate(chars):
    my_own_ascii_table[ch] = idx

# inverse map for fast lookup
int_to_char = {v: k for k, v in my_own_ascii_table.items()}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def int_to_ascii(i):
    try:
        i = int(i)
    except (ValueError, TypeError):
        random_char = list(my_own_ascii_table.keys())[np.random.randint(0, len(my_own_ascii_table))]
        return random_char
    if i == 0:
        return " "
    elif i < 0:
        return " "
    # decode a hex-packed integer where each byte encodes one table index
    hexstr = format(i, 'x')
    if len(hexstr) % 2 != 0:
        hexstr = '0' + hexstr
    out_chars = []
    for j in range(0, len(hexstr), 2):
        val = int(hexstr[j:j+2], 16)
        random_char = list(my_own_ascii_table.keys())[np.random.randint(0, len(my_own_ascii_table))]
        out_chars.append(int_to_char.get(val, {random_char}))
    return ''.join(out_chars)

def ascii_to_int(s):
    if not s:
        return 0
    if len(s) == 1:
        return my_own_ascii_table.get(s, 0)
    # pack each character as a two-digit hex value based on our table
    hex_parts = []
    for ch in s:
        val = my_own_ascii_table.get(ch, 0)
        hex_parts.append(f"{val:02x}")
    return int(''.join(hex_parts), 16)

def leakyReLU(x):
    if x <= 0:
        return 0.025 * x
    else:
        return x

def send_neural_value(nn_index, fweight, fbias, fvalue, fneuron, flayer, tvalue, tlayer, tneuron):
    nn_key = f"NN{nn_index+1}"
    src_val = nnlist[nn_key][flayer][fneuron].get(fvalue, 0)
    try:
        src_f = float(src_val)
    except (ValueError, TypeError):
        src_f = 0.0
    add = leakyReLU((src_f * float(fweight)) + float(fbias))

    # ensure target structure exists and increment target value
    if flayer != "input":
        if tneuron not in nnlist[nn_key][tlayer]:
            nnlist[nn_key][tlayer][tneuron] = {}
        nnlist[nn_key][tlayer][tneuron][tvalue] = nnlist[nn_key][tlayer][tneuron].get(tvalue, 0) + add

    else:
        if tneuron not in nnlist[nn_key][tlayer]:
            nnlist[nn_key][tlayer][tneuron] = {}
        nnlist[nn_key][tlayer][tneuron][tvalue] = nnlist[nn_key][tlayer][tneuron].get(tvalue, 0) + add

def clear_values(nn_index, fvalue, fneuron, flayer, tlayer, tneuron, text_progress):
    nn_key = f"NN{nn_index+1}"
    if flayer != "input":
        if tneuron not in nnlist[nn_key][tlayer]:
            nnlist[nn_key][tlayer][tneuron] = {}
        nnlist[nn_key][flayer][fneuron][fvalue] = 0
    else:
        if tneuron not in nnlist[nn_key][tlayer]:
            nnlist[nn_key][tlayer][tneuron] = {}
        if fneuron == "text_size" and text_progress != 0:
            nnlist[nn_key][flayer][fneuron][fvalue] = len(nnlist[nn_key]["text"])
        elif fneuron == "text_size" and text_progress == 0:
            nnlist[nn_key][flayer][fneuron][fvalue] = len(nnlist[nn_key]["text"]) + 1
        elif fneuron == "wrote":
            nnlist[nn_key][flayer][fneuron][fvalue] = ascii_to_int(nnlist[nn_key]["last_word"])

def parse_score(raw_score):
    if raw_score is None:
        return 0.0
    if isinstance(raw_score, str):
        cleaned = raw_score.strip().lower()
        if cleaned == "best":
            return "best"
        try:
            return float(cleaned)
        except (TypeError, ValueError):
            return 0.0
    try:
        return float(raw_score)
    except (TypeError, ValueError, OverflowError):
        return 0.0
        


for i in range(nn_count):
    nnlist[f"NN{i+1}"] = {
        "input": {},
        "hidden1": {},
        "hidden2": {},
        "output": {},
        "text": "",
        "last_word": "",
        "text_length": 0, # How long each NN´s text will be
        "score": -1,
        "text_progress": 0, # How many characters the NNs have written (because of the structure of the code, which hopefully is somewhat optimal, each NN writes a single character at a time and "waits" for the others to write before writing its own)
        "finished": False,
        "prompt_idx": 0
    }

    for ii in range(4):
        if ii == 0: # Input layer
            for iii in range(3):
                if iii == 0: # initial prompt
                    nnlist[f"NN{i+1}"]["input"]["prompt"] = {
                        "weight1": np.random.uniform(0, 3),
                        "weight2": np.random.uniform(0, 3),
                        "bias1": np.random.uniform(-10, 10),
                        "bias2": np.random.uniform(-10, 10),
                        "value1": ascii_to_int(initial_prompts[nnlist[f"NN{i+1}"]["prompt_idx"]]),
                        "value2": ascii_to_int(initial_prompts[nnlist[f"NN{i+1}"]["prompt_idx"]])
                    }

                elif iii == 1: # already_wrote
                    nnlist[f"NN{i+1}"]["input"]["wrote"] = {
                        "weight1": np.random.uniform(0, 3),
                        "weight2": np.random.uniform(0, 3),
                        "bias1": np.random.uniform(-10, 10),
                        "bias2": np.random.uniform(-10, 10),
                        "value1": ascii_to_int(last_word),
                        "value2": ascii_to_int(last_word)
                    } # weight n is the weight for value n which is sent to neuron n on the next layer


                elif iii == 2: # text size
                    nnlist[f"NN{i+1}"]["input"]["text_size"] = {
                        "weight1": np.random.uniform(0, 3),
                        "weight2": np.random.uniform(0, 3),
                        "bias1": np.random.uniform(-10, 10),
                        "bias2": np.random.uniform(-10, 10),
                        "value1": len(nnlist[f"NN{i+1}"]["text"])
                    }
                    nnlist[f"NN{i+1}"]["input"]["text_size"]["value2"] = nnlist[f"NN{i+1}"]["input"]["text_size"]["value1"]

        elif ii == 1: # First hidden layer
            for iii in range(2):
                nnlist[f"NN{i+1}"]["hidden1"][f"neuron{iii+1}"] = {
                    "weight1": np.random.uniform(0, 3),
                    "weight2": np.random.uniform(0, 3),
                    "bias1": np.random.uniform(-10, 10),
                    "bias2": np.random.uniform(-10, 10),
                    "value1": 0,
                    "value2": 0
                }

        elif ii == 2: # Second hidden layer
            for iii in range(2):
                nnlist[f"NN{i+1}"]["hidden2"][f"neuron{iii+1}"] = {
                    "weight1": np.random.uniform(0, 3),
                    "bias1": np.random.uniform(-10, 10),
                    "value1": 0
                }

        else: # Output neuron (not defined for now)
            nnlist[f"NN{i+1}"]["output"]["neuron1"] = {"value1": 0, "score": -1}


while (True and (not user_interupted)): # Main loop
    try:
        if not epoch_started:
            print(f"Epoch {epoch+1})")
            print( )
            epoch_started = True
        nns_scored = False
        nnlist = dict(sorted(nnlist.items(), key=lambda x: float(x[1]["score"]), reverse=True))
        
        for nn in range(nn_count): # Checks each NN
            current_nn = nnlist[f"NN{nn+1}"]

            for neuron in current_nn["hidden1"].values():
                neuron["value1"] = 0
                neuron["value2"] = 0

            for neuron in current_nn["hidden2"].values():
                neuron["value1"] = 0

            current_nn["output"]["neuron1"]["value1"] = 0
            
            text_progress = current_nn["text_progress"] # How many characters the NNs have written (because of the structure of the code, which hopefully is somewhat optimal, each NN writes a single character at a time and "waits" for the others to write before writing its own)
            
            last_word = current_nn["text"][-5:] if len(current_nn["text"]) >= 5 else current_nn["text"]
            current_nn["last_word"] = last_word
            clear_screen = False
            
            
            for l_name, layer in current_nn.items(): # Checks each layer
                current_layer = current_nn[l_name]
                if l_name in ["input", "hidden1", "hidden2", "output"]:
                    for n_name, neuron in current_nn[l_name].items(): # Checks each neuron
                        current_neuron = current_layer[n_name]

                        for wb_name, w_or_b in current_nn[l_name][n_name].items(): # Checks every weight/bias
                            if wb_name == "weight1" or wb_name == "weight2":
                                if l_name in ["input", "hidden1", "hidden2"]:

                                    _fweight = current_neuron[wb_name]
                                    _fbias = current_neuron[f"bias{wb_name[-1]}"]
                                    _fvalue = f"value{wb_name[-1]}"
                                    _fneuron = n_name
                                    _flayer = l_name
                                    _tlayer = "hidden1" if l_name == "input" else "hidden2" if l_name == "hidden1" else "output"
                                    _tneuron = "neuron" + str(wb_name[-1])

                                    if _flayer != "hidden2":
                                        for ii in range(2):
                                            send_neural_value(nn, _fweight, _fbias, _fvalue, _fneuron, _flayer, f"value{ii+1}", _tlayer, _tneuron)
                                        clear_values(nn, _fvalue, _fneuron, _flayer, _tlayer, _tneuron, text_progress)
                                    else:
                                        send_neural_value(nn, _fweight, _fbias, _fvalue, _fneuron, _flayer, "value1", _tlayer, _tneuron)
                                        clear_values(nn, _fvalue, _fneuron, _flayer, _tlayer, _tneuron, text_progress)

                            

                        if l_name == "output":
                            current_nn = nnlist[f"NN{nn+1}"]
                            current_layer = current_nn[l_name]
                            current_neuron = current_layer[n_name]
                            if current_nn["text_length"] == 0 and current_nn["text_progress"] == 0: # Sets text length
                                try:
                                    current_nn["text_length"] = min(int(current_layer["neuron1"]["value1"]), max_text_length)
                                except (ValueError, TypeError, OverflowError):
                                    current_nn["text_length"] = max_text_length

                                try:
                                    if int(current_layer["neuron1"]["value1"]) == "" or int(current_layer["neuron1"]["value1"]) <= 0:
                                        current_nn["input"]["text_size"]["value1"] = len(nnlist[f"NN{i+1}"]["text"])
                                        current_nn["input"]["text_size"]["value2"] = len(nnlist[f"NN{i+1}"]["text"])
                                        current_nn["text_length"] = max_text_length
                                    else:
                                        current_nn["text_length"] = min(max(abs(int(current_layer["neuron1"]["value1"])), 10), max_text_length)
                                    current_nn["input"]["text_size"]["value1"] = current_nn["text_length"]
                                    current_nn["input"]["text_size"]["value2"] = current_nn["text_length"]
                                
                                except (ValueError, TypeError, OverflowError):
                                    current_nn["input"]["text_size"]["value1"] = len(current_nn["text"])
                                    current_nn["text_length"] = max_text_length

                                current_layer["neuron1"]["value1"] = 0
                                if current_nn == nnlist["NN1"] and clear_screen == True:
                                    clear()

                            elif (current_nn["text_length"] != 0 and (current_nn["text_length"] != float) or text_progress != 0):
                                try:
                                    if current_nn["text_length"] > text_progress: # Adds a letter to the text
                                        current_nn["text"] += int_to_ascii(int(current_neuron["value1"]))
                                        current_neuron["value1"] = 0
                                        text_progress += 1
                                        current_nn["text_progress"] += 1
                                        if current_nn == nnlist["NN1"] and clear_screen == True:
                                            clear()

                                    else: # Prints the response
                                        if epoch >= 50000 or user_interupted == True:
                                            if nnlist[f"NN{nn+1}"]["prompt_idx"] >= len(initial_prompts):
                                                nnlist[f"NN{nn+1}"]["prompt_idx"] = 0
                                            print(f"NN{nn+1} is writing its text...")
                                            print(f"NN{nn+1}´s response no.{epoch+1}:")
                                            print()
                                            print(current_nn["text"]) # (finally) prints the text that the NN created
                                            print()
                                            raw_score = input(f"Rate this text with a consistent metric(on a scale of 0-10(not limited to integers or to 10 in case you started training with scores that are too high, however, negatives scores will be nullified), with a fair rating), given that the AI was given the following prompt: '{initial_prompts[nnlist[f"NN{nn+1}"]["prompt_idx"]]}'. If you want to know the best NN´s weights and biases, enter 'best' (without quotes) and the program will end. The NNs will also receive a bonus based on the frequencies of some letters in their texts: ")
                                            print("\n", end="")
                                            clear_screen = True
                                            parsed_score = parse_score(raw_score)
                                            if parsed_score == "best":
                                                valid_scores = []
                                                for nn_key, nn_score in nnlist.items():
                                                    try:
                                                        valid_scores.append((nn_key, float(nn_score["score"])))
                                                    except (TypeError, ValueError):
                                                        continue
                                                if valid_scores:
                                                    clear()
                                                    print("Best NN´s weights and biases:")
                                                    for nn_key, nn_score in nnlist.items():
                                                        if float(nn_score["score"]) == max(float(nnlist[nn]["score"]) for nn in nnlist):
                                                            best_nn = nn_score
                                                            print(f"{nn_key}: {float(nn_score['score'])}")
                                                            for l_name, layer in best_nn.items():
                                                                if l_name in ["input", "hidden1", "hidden2", "output"]:
                                                                    print(f"  {l_name}:")
                                                                    for n_name, neuron in best_nn[l_name].items():
                                                                        print(f"    {n_name}:")
                                                                        for wb_name, w_or_b in best_nn[l_name][n_name].items():
                                                                            print(f"      {wb_name}: {w_or_b}")
                                                    exit()
                                            current_nn["score"] = float(parsed_score) if parsed_score is not None else 0.0
                                            current_nn["score"] = max(0.0, current_nn["score"])



                                            

                                        if float(current_nn["score"]) < 0.0:
                                            current_nn["score"] = 0.0
                                        nns_scored = all((nnlist[f"NN{i+1}"]["score"] != -1) for i in range(nn_count))
                                        nnlist[f"NN{nn+1}"]["prompt_idx"] += 1
                                        nnlist[f"NN{nn+1}"]["prompt_idx"] = nnlist[f"NN{nn+1}"]["prompt_idx"] % 5

                                        
                                    for letter, frequency in letter_frequencies.items():
                                        try:
                                            raw_score = raw_score
                                        except NameError:
                                            raw_score = 0
                                        letter_frequency = 0
                                        for char in current_nn["text"]:
                                            if char.lower() not in list("abcdefghijklmnopqrstuvwxyz"):
                                                current_nn["text"].replace(char, " ")
                                        letter_frequency = current_nn["text"].count(letter)
                                        try:
                                            current_nn["score"] += min(letter_frequency / frequency, frequency / letter_frequency) / len(letter_frequencies.keys())
                                            current_nn["output"]["neuron1"]["score"] += min(letter_frequency / frequency, frequency / letter_frequency) / len(letter_frequencies.keys())
                                        except ZeroDivisionError:
                                            current_nn["score"] += 0
                                            current_nn["output"]["neuron1"]["score"] += 0
                                            
                                except (ValueError, TypeError, OverflowError):
                                    nnlist[f"NN{nn+1}"]["prompt_idx"] += 1
                                    nnlist[f"NN{nn+1}"]["prompt_idx"] = nnlist[f"NN{nn+1}"]["prompt_idx"] % 5
                                    current_nn["text"] += int_to_ascii(np.random.randint(0, len(my_own_ascii_table)))
                                    text_progress += 1
                                    current_nn["text_progress"] += 1

            # Start the end process: sort the NNs based on their scores, from highest to lowest, reset most of the NNs´s value, then, with the average weights and biases of the best 3 NNs, create 3 new NNs based on the same weights/biases values, but with a small random variation, and then reset the scores of all NNs to 0
            
            nns_finished = all(nnlist[f"NN{i+1}"]["text_progress"] >= nnlist[f"NN{i+1}"]["text_length"] for i in range(nn_count))
            if nns_finished and nns_scored:
                clear()
                nnlist = dict(sorted(nnlist.items(), key=lambda x: float(x[1]["score"]), reverse=True))
                print("Scores of the NNs (from highest to lowest):")
                for nn_key, nn_score in nnlist.items():
                    nn_score["score"] = max(0.0, nn_score["score"])
                    print(f"{nn_key}: {float(nn_score['score'])}")
            
            if nns_finished and nns_scored:
                print(f"Epoch {epoch+1} completed. Starting next epoch...\n")
                epoch += 1
                epoch_started = False

        
            if nns_finished and nns_scored:
                for nn in range(nn_count):
                    nnlist[f"NN{nn+1}"]["finished"] = True
                    nnlist[f"NN{nn+1}"]["input"]["text_size"]["value1"] = 0
                    nnlist[f"NN{nn+1}"]["input"]["text_size"]["value2"] = 0
                    nnlist[f"NN{nn+1}"]["text"] = ""
                    nnlist[f"NN{nn+1}"]["text_progress"] = 0
                    nnlist[f"NN{nn+1}"]["score"] = -1
                    nnlist[f"NN{nn+1}"]["last_word"] = ""
                    nnlist[f"NN{nn+1}"]["output"]["neuron1"]["value1"] = 0

            if epoch >= 1:
                best_nns = list(nnlist.keys())[:int(nn_count/2)]  # Get the keys of the best half of the NNs
                worst_nns = list(nnlist.keys())[int(nn_count/2):]  # Get the keys of the worst half of the NNs
                average_weights_biases = {"input": {"prompt": {}, "wrote": {}, "text_size": {}}, "hidden1": {f"neuron{neuron}": {} for neuron in nnlist["NN1"]["hidden1"]}, "hidden2": {f"neuron{neuron}": {} for neuron in nnlist["NN1"]["hidden2"]}}
                for nn in range(nn_count):
                    current_nn = nnlist[f"NN{nn+1}"]
                    for l_name in ["input", "hidden1", "hidden2"]:
                        for n_name, neuron in current_nn[l_name].items():
                            average_weights_biases[l_name][n_name] = {}
                            for wb_name, w_or_b in current_nn[l_name][n_name].items():
                                average_weights_biases[l_name][n_name][wb_name] = 0
                for nn in range(nn_count):
                    current_nn = nnlist[f"NN{nn+1}"]
                    if f"NN{nn+1}" in best_nns:
                        for l_name in ["input", "hidden1", "hidden2"]:
                            for n_name, neuron in current_nn[l_name].items():
                                for wb_name, w_or_b in current_nn[l_name][n_name].items():
                                    average_weights_biases[l_name][n_name][wb_name] += current_nn[l_name][n_name][wb_name]
                for nn in range(nn_count):
                    current_nn = nnlist[f"NN{nn+1}"]
                    if f"NN{nn+1}" in best_nns:
                        for l_name in ["input", "hidden1", "hidden2"]:
                            for n_name, neuron in current_nn[l_name].items():
                                for wb_name in average_weights_biases[l_name][n_name]:
                                    average_weights_biases[l_name][n_name][wb_name] /= (nn_count / 2)
                        
                for nn in range(nn_count):
                    current_nn = nnlist[f"NN{nn+1}"]
                    if f"NN{nn+1}" in worst_nns:
                        for l_name in ["input", "hidden1", "hidden2"]:
                            for n_name in current_nn[l_name]:
                                for wb_name in current_nn[l_name][n_name]:
                                    if not wb_name.startswith("value"):
                                        current_nn[l_name][n_name][wb_name] = current_nn[l_name][n_name][wb_name] + (((average_weights_biases[l_name][n_name][wb_name] - current_nn[l_name][n_name][wb_name]) * learning_rate) + (np.random.uniform(-0.5, 0.5) * learning_rate)) # Small random variation
    except KeyboardInterrupt:
        user_interupted = True

while True: # Main loop if the user decides to interrupt the letter frenquency training
    if not epoch_started:
        print(f"Epoch {epoch+1})")
        print( )
        epoch_started = True
    nns_scored = False
    nnlist = dict(sorted(nnlist.items(), key=lambda x: float(x[1]["score"]), reverse=True))
    
    for nn in range(nn_count): # Checks each NN
        current_nn = nnlist[f"NN{nn+1}"]

        for neuron in current_nn["hidden1"].values():
            neuron["value1"] = 0
            neuron["value2"] = 0

        for neuron in current_nn["hidden2"].values():
            neuron["value1"] = 0

        current_nn["output"]["neuron1"]["value1"] = 0
        
        text_progress = current_nn["text_progress"] # How many characters the NNs have written (because of the structure of the code, which hopefully is somewhat optimal, each NN writes a single character at a time and "waits" for the others to write before writing its own)
        
        last_word = current_nn["text"][-5:] if len(current_nn["text"]) >= 5 else current_nn["text"]
        current_nn["last_word"] = last_word
        clear_screen = False
        
        
        for l_name, layer in current_nn.items(): # Checks each layer
            current_layer = current_nn[l_name]
            if l_name in ["input", "hidden1", "hidden2", "output"]:
                for n_name, neuron in current_nn[l_name].items(): # Checks each neuron
                    current_neuron = current_layer[n_name]

                    for wb_name, w_or_b in current_nn[l_name][n_name].items(): # Checks every weight/bias
                        if wb_name == "weight1" or wb_name == "weight2":
                            if l_name in ["input", "hidden1", "hidden2"]:

                                _fweight = current_neuron[wb_name]
                                _fbias = current_neuron[f"bias{wb_name[-1]}"]
                                _fvalue = f"value{wb_name[-1]}"
                                _fneuron = n_name
                                _flayer = l_name
                                _tlayer = "hidden1" if l_name == "input" else "hidden2" if l_name == "hidden1" else "output"
                                _tneuron = "neuron" + str(wb_name[-1])

                                if _flayer != "hidden2":
                                    for ii in range(2):
                                        send_neural_value(nn, _fweight, _fbias, _fvalue, _fneuron, _flayer, f"value{ii+1}", _tlayer, _tneuron)
                                    clear_values(nn, _fvalue, _fneuron, _flayer, _tlayer, _tneuron, text_progress)
                                else:
                                    send_neural_value(nn, _fweight, _fbias, _fvalue, _fneuron, _flayer, "value1", _tlayer, _tneuron)
                                    clear_values(nn, _fvalue, _fneuron, _flayer, _tlayer, _tneuron, text_progress)

                        

                    if l_name == "output":
                        current_nn = nnlist[f"NN{nn+1}"]
                        current_layer = current_nn[l_name]
                        current_neuron = current_layer[n_name]
                        if current_nn["text_length"] == 0 and current_nn["text_progress"] == 0: # Sets text length
                            try:
                                current_nn["text_length"] = min(int(current_layer["neuron1"]["value1"]), max_text_length)
                            except (ValueError, TypeError, OverflowError):
                                current_nn["text_length"] = max_text_length

                            try:
                                if int(current_layer["neuron1"]["value1"]) == "" or int(current_layer["neuron1"]["value1"]) <= 0:
                                    current_nn["input"]["text_size"]["value1"] = len(nnlist[f"NN{i+1}"]["text"])
                                    current_nn["input"]["text_size"]["value2"] = len(nnlist[f"NN{i+1}"]["text"])
                                    current_nn["text_length"] = max_text_length
                                else:
                                    current_nn["text_length"] = min(max(abs(int(current_layer["neuron1"]["value1"])), 10), max_text_length)
                                current_nn["input"]["text_size"]["value1"] = current_nn["text_length"]
                                current_nn["input"]["text_size"]["value2"] = current_nn["text_length"]
                            
                            except (ValueError, TypeError, OverflowError):
                                current_nn["input"]["text_size"]["value1"] = len(current_nn["text"])
                                current_nn["text_length"] = max_text_length

                            current_layer["neuron1"]["value1"] = 0
                            if current_nn == nnlist["NN1"] and clear_screen == True:
                                clear()

                        elif (current_nn["text_length"] != 0 and (current_nn["text_length"] != float) or text_progress != 0):
                            try:
                                if current_nn["text_length"] > text_progress: # Adds a letter to the text
                                    current_nn["text"] += int_to_ascii(int(current_neuron["value1"]))
                                    current_neuron["value1"] = 0
                                    text_progress += 1
                                    current_nn["text_progress"] += 1
                                    if current_nn == nnlist["NN1"] and clear_screen == True:
                                        clear()

                                else: # Prints the response
                                    if user_interupted == True:
                                        if nnlist[f"NN{nn+1}"]["prompt_idx"] >= len(initial_prompts):
                                            nnlist[f"NN{nn+1}"]["prompt_idx"] = 0
                                        print(f"NN{nn+1} is writing its text...")
                                        print(f"NN{nn+1}´s response no.{epoch+1}:")
                                        print()
                                        print(current_nn["text"]) # (finally) prints the text that the NN created
                                        print()
                                        raw_score = input(f"Rate this text with a consistent metric(on a scale of 0-10(not limited to integers or to 10 in case you started training with scores that are too high, however, negatives scores will be nullified), with a fair rating), given that the AI was given the following prompt: '{initial_prompts[nnlist[f"NN{nn+1}"]["prompt_idx"]]}'. If you want to know the best NN´s weights and biases, enter 'best' (without quotes) and the program will end. The NNs will also receive a bonus based on the frequencies of some letters in their texts: ")
                                        print("\n", end="")
                                        clear_screen = True
                                        parsed_score = parse_score(raw_score)
                                        if parsed_score == "best":
                                            valid_scores = []
                                            for nn_key, nn_score in nnlist.items():
                                                try:
                                                    valid_scores.append((nn_key, float(nn_score["score"])))
                                                except (TypeError, ValueError):
                                                    continue
                                            if valid_scores:
                                                clear()
                                                print("Best NN´s weights and biases:")
                                                for nn_key, nn_score in nnlist.items():
                                                    if float(nn_score["score"]) == max(float(nnlist[nn]["score"]) for nn in nnlist):
                                                        best_nn = nn_score
                                                        print(f"{nn_key}: {float(nn_score['score'])}")
                                                        for l_name, layer in best_nn.items():
                                                            if l_name in ["input", "hidden1", "hidden2", "output"]:
                                                                print(f"  {l_name}:")
                                                                for n_name, neuron in best_nn[l_name].items():
                                                                    print(f"    {n_name}:")
                                                                    for wb_name, w_or_b in best_nn[l_name][n_name].items():
                                                                        print(f"      {wb_name}: {w_or_b}")
                                                exit()
                                        current_nn["score"] = float(parsed_score) if parsed_score is not None else 0.0
                                        current_nn["score"] = max(0.0, current_nn["score"])



                                        

                                    if float(current_nn["score"]) < 0.0:
                                        current_nn["score"] = 0.0
                                    nns_scored = all((nnlist[f"NN{i+1}"]["score"] != -1) for i in range(nn_count))
                                    nnlist[f"NN{nn+1}"]["prompt_idx"] += 1
                                    nnlist[f"NN{nn+1}"]["prompt_idx"] = nnlist[f"NN{nn+1}"]["prompt_idx"] % 5

                                    
                                for letter, frequency in letter_frequencies.items():
                                    try:
                                        raw_score = raw_score
                                    except NameError:
                                        raw_score = 0
                                    letter_frequency = 0
                                    for char in current_nn["text"]:
                                        if char.lower() not in list("abcdefghijklmnopqrstuvwxyz"):
                                            current_nn["text"].replace(char, " ")
                                    letter_frequency = current_nn["text"].count(letter)
                                    try:
                                        current_nn["score"] += min(letter_frequency / frequency, frequency / letter_frequency) / len(letter_frequencies.keys())
                                        current_nn["output"]["neuron1"]["score"] += min(letter_frequency / frequency, frequency / letter_frequency) / len(letter_frequencies.keys())
                                    except ZeroDivisionError:
                                        current_nn["score"] += 0
                                        current_nn["output"]["neuron1"]["score"] += 0
                                        
                            except (ValueError, TypeError, OverflowError):
                                nnlist[f"NN{nn+1}"]["prompt_idx"] += 1
                                nnlist[f"NN{nn+1}"]["prompt_idx"] = nnlist[f"NN{nn+1}"]["prompt_idx"] % 5
                                current_nn["text"] += int_to_ascii(np.random.randint(0, len(my_own_ascii_table)))
                                text_progress += 1
                                current_nn["text_progress"] += 1

        # Start the end process: sort the NNs based on their scores, from highest to lowest, reset most of the NNs´s value, then, with the average weights and biases of the best 3 NNs, create 3 new NNs based on the same weights/biases values, but with a small random variation, and then reset the scores of all NNs to 0
        
        nns_finished = all(nnlist[f"NN{i+1}"]["text_progress"] >= nnlist[f"NN{i+1}"]["text_length"] for i in range(nn_count))
        if nns_finished and nns_scored:
            clear()
            nnlist = dict(sorted(nnlist.items(), key=lambda x: float(x[1]["score"]), reverse=True))
            print("Scores of the NNs (from highest to lowest):")
            for nn_key, nn_score in nnlist.items():
                nn_score["score"] = max(0.0, nn_score["score"])
                print(f"{nn_key}: {float(nn_score['score'])}")
        
        if nns_finished and nns_scored:
            print(f"Epoch {epoch+1} completed. Starting next epoch...\n")
            epoch += 1
            epoch_started = False

    
        if nns_finished and nns_scored:
            for nn in range(nn_count):
                nnlist[f"NN{nn+1}"]["finished"] = True
                nnlist[f"NN{nn+1}"]["input"]["text_size"]["value1"] = 0
                nnlist[f"NN{nn+1}"]["input"]["text_size"]["value2"] = 0
                nnlist[f"NN{nn+1}"]["text"] = ""
                nnlist[f"NN{nn+1}"]["text_progress"] = 0
                nnlist[f"NN{nn+1}"]["score"] = -1
                nnlist[f"NN{nn+1}"]["last_word"] = ""
                nnlist[f"NN{nn+1}"]["output"]["neuron1"]["value1"] = 0

        if epoch >= 1:
            best_nns = list(nnlist.keys())[:int(nn_count/2)]  # Get the keys of the best half of the NNs
            worst_nns = list(nnlist.keys())[int(nn_count/2):]  # Get the keys of the worst half of the NNs
            average_weights_biases = {"input": {"prompt": {}, "wrote": {}, "text_size": {}}, "hidden1": {f"neuron{neuron}": {} for neuron in nnlist["NN1"]["hidden1"]}, "hidden2": {f"neuron{neuron}": {} for neuron in nnlist["NN1"]["hidden2"]}}
            for nn in range(nn_count):
                current_nn = nnlist[f"NN{nn+1}"]
                for l_name in ["input", "hidden1", "hidden2"]:
                    for n_name, neuron in current_nn[l_name].items():
                        average_weights_biases[l_name][n_name] = {}
                        for wb_name, w_or_b in current_nn[l_name][n_name].items():
                            average_weights_biases[l_name][n_name][wb_name] = 0
            for nn in range(nn_count):
                current_nn = nnlist[f"NN{nn+1}"]
                if f"NN{nn+1}" in best_nns:
                    for l_name in ["input", "hidden1", "hidden2"]:
                        for n_name, neuron in current_nn[l_name].items():
                            for wb_name, w_or_b in current_nn[l_name][n_name].items():
                                average_weights_biases[l_name][n_name][wb_name] += current_nn[l_name][n_name][wb_name]
            for nn in range(nn_count):
                current_nn = nnlist[f"NN{nn+1}"]
                if f"NN{nn+1}" in best_nns:
                    for l_name in ["input", "hidden1", "hidden2"]:
                        for n_name, neuron in current_nn[l_name].items():
                            for wb_name in average_weights_biases[l_name][n_name]:
                                average_weights_biases[l_name][n_name][wb_name] /= (nn_count / 2)
                    
            for nn in range(nn_count):
                current_nn = nnlist[f"NN{nn+1}"]
                if f"NN{nn+1}" in worst_nns:
                    for l_name in ["input", "hidden1", "hidden2"]:
                        for n_name in current_nn[l_name]:
                            for wb_name in current_nn[l_name][n_name]:
                                if not wb_name.startswith("value"):
                                    current_nn[l_name][n_name][wb_name] = (average_weights_biases[l_name][n_name][wb_name] + (np.random.uniform(-0.5, 0.5) * learning_rate)) # Small random variation