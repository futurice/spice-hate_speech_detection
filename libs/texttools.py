from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

baseform_to_original = dict()

def stemming_messages(messages, method='voikko'):
    if method == 'voikko':
        stemmed_messages, baseform_to_original = stemming_messages_voikko(messages)
    elif method == 'snowball':
        stemmed_messages, baseform_to_original = stemming_messages_snowball(messages)

def stemming_message_voikko(message):
    import libvoikko
    voikko = libvoikko.Voikko('fi')

    stemmed_message = []
    for token in voikko.tokens(message):
        if token.tokenType == token.WORD:
            res = voikko.analyze(token.tokenText)
            if len(res) > 0:
                stemmed_message += [res[0]['BASEFORM']]
                baseform_to_original[res[0]['BASEFORM']] = token.tokenText
            else:
                stemmed_message += [token.tokenText]
    return ' '.join(stemmed_message), baseform_to_original


def stemming_messages_voikko(messages):
    stemmed_messages = []
    for message in messages:
        stemmed_message, baseform_to_original = stemming_message_voikko(message)
        stemmed_messages.append(stemmed_message)
    return stemmed_messages, baseform_to_original


def stemming_message_snowball(message, stemmings_to_words=dict()):
    from nltk.stem.snowball import SnowballStemmer
    from nltk.tokenize import casual_tokenize
    stemmer = SnowballStemmer('finnish')

    if type(message) == None:
        return '', stemmings_to_words

    message.replace('#','')

    stemmed_message = []

    for word in casual_tokenize(message):

        stemmed_word = stemmer.stem(word.lower())
        stemmed_message.append(stemmed_word)
        stemmings_to_words[stemmed_word] = word

    stemmed_message = ' '.join(stemmed_message)

    return stemmed_message, stemmings_to_words


def stemming_messages_snowball(messages, stemmings_to_words=dict()):

    stemmed_messages = []

    for message in messages:
        try:
            stemmed_message, stemmings_to_words = stemming_message_snowball(message, stemmings_to_words)
        except:
            stemmed_message = 'nan'
            print('Failed! %s' % (message))
        stemmed_messages.append(stemmed_message)

    return stemmed_messages, stemmings_to_words

def vectorize_messages(messages, method='tfidf'):

    if method == 'tfidf':
        tfidf = TfidfVectorizer(min_df=2, max_df=0.9).fit(messages)
        x = tfidf.transform(messages)
        return x, tfidf
    elif method == 'count':
        counts = CountVectorizer().fit(messages)
        x = counts.transform(messages)
        return x, counts
