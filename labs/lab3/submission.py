## import modules here 

################# Question 1 #################
def tokenize(sms):
    if type(sms) is list:
        return sms
    return sms.split(' ')

def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens

def multinomial_nb(training_data, sms):# do not change the heading of the function
    spam_vector = {}
    spam_sum = 0.0
    spam_rows = 0.0
    ham_vector = {}
    ham_sum = 0.0
    ham_rows = 0.0
    count_vector = {}
    sms_frequency = {}
    vector_length = 0
    p_spam = 0.0
    p_ham = 0.0
    sms_frequency = get_freq_of_tokens(sms)
    #smoothing
    for pair in training_data:
        for feature in pair[0]:
            spam_vector[feature] = 1.0
            ham_vector[feature] = 1.0
            count_vector[feature] = 0
    vector_length = len(spam_vector)
    spam_sum += vector_length
    ham_sum += vector_length
    for pair in training_data:
        if pair[1] == 'spam':
            spam_rows += 1
            for feature in pair[0]:
                spam_vector[feature] += pair[0][feature]
                spam_sum += pair[0][feature]
        else:
            ham_rows += 1
            for feature in pair[0]:
                ham_vector[feature] += pair[0][feature]
                ham_sum += pair[0][feature]
    p_spam = spam_rows / (spam_rows + ham_rows)
    p_ham = ham_rows / (spam_rows + ham_rows)
    for token in sms_frequency:
        if token not in count_vector:
            count_vector[token] = 0
        count_vector[token] += sms_frequency[token]
    for feature in spam_vector:
        spam_vector[feature] = spam_vector[feature]/spam_sum
        ham_vector[feature] = ham_vector[feature]/ham_sum
    for feature in spam_vector:
        p_spam = p_spam * (spam_vector[feature]**count_vector[feature])
        p_ham = p_ham * (ham_vector[feature]**count_vector[feature])
    ratio = p_spam/p_ham
    return ratio