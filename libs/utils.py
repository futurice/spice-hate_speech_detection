import os

def print_decomposition_topics(decomposition, feature_names, n_top_words=20):
    for topic_idx, topic in enumerate(decomposition.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def get_decomposition_topic(decomposition, feature_names, topic_idx, n_top_words=20):
    components = decomposition.components_[topic_idx]
    return " ".join([feature_names[i] for i in components.argsort()[:-n_top_words - 1:-1]])

def get_vihapuhe_root():
    return '/'.join(os.environ['PWD'].split('/')[0:os.environ['PWD'].split('/').index('vihapuhe')+1])
