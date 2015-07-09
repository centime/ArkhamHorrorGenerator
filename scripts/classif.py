# coding: utf8

import os
from collections import OrderedDict
import numpy as np
input_dir = '/home/jonas/Code/arkhamnn/datasets/locations/'

#read datas
datasets = OrderedDict()
for filename in os.listdir(input_dir):
    with open(input_dir+filename,'r') as open_file:
        datasets[filename] = [line for line in open_file]

#build target (classes) list
target = np.array([item for place,events in datasets.items() for item in [place]*len(events)])

#build corpus list
corpus = np.array([event for events in datasets.values() for event in events])


#build bag of word repr
# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer = CountVectorizer()
# bag_of_words = vectorizer.fit_transform([event for events in datasets.values() for event in events])

# from sklearn.naive_bayes import MultinomialNB
# clf = MultinomialNB().fit(bag_of_words, target)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
texte_clf_pipeline = Pipeline([('vect', CountVectorizer()),
                               ('tfidf', TfidfTransformer()),
                               ('clf', MultinomialNB()),
                               ])

train_sample_index = np.random.choice(range(len(target)),size=len(target)*4/5,replace = False)
train_mask = np.array([False]*len(target))
train_mask[train_sample_index] = True
test_mask = np.logical_not(train_mask)

texte_clf = texte_clf_pipeline.fit(corpus[train_mask], target[train_mask])
predicted = texte_clf.predict(corpus[test_mask])
probas = texte_clf.predict_proba(corpus[test_mask])
plt.xlim(0,1)
plt.ylim(0,1)
plt.imshow(probas,interpolation='none',
            extent=(0,1,0,1),
            )
plt.show()

from sklearn import metrics
print(metrics.classification_report(target[test_mask], predicted))

#metrics.confusion_matrix(target[test_mask], predicted)
from sklearn import cross_validation
scores = cross_validation.cross_val_score(texte_clf_pipeline, corpus, target, cv=10, scoring='precision_weighted')
print scores.mean(), scores.std()
#Putain mais c'est quoi ces sores pourris, pourquoi ça correspond pas au classification_report ? 




### Idées pour la classif
# 2 systèmes en parallèle : 
#-un système de piles par lieu, les, évènements entrants sont afféctés à un lieu
#-une pile 'de secours', qui sert quand une pile vide est appelée, on prend l'evt
#de la pile de secours le mieux classé pour cette classe.