# NLP-based Question Answering System

NLP-based Question Answering System Extension with 3 developed methods:

NLP-QAS extension is proposed for answer detection. In NLP-QAS, firstly, the most related sentence selection (RSS) process is carried out to search for the answer. Afterwards, the success of RNP methods for answer detection is analyzed in this sentence. An example of NLP-QAS operation is shown in below the figure. Question, paragraph and answer are taken as input and processes between question and answer are analyzed by Remove&Compare, Searching with NER, Searching with POS tagging, namely RNP methods. First of all, the sentences of the question and the related paragraph are preprocessed and paragraph is parsed into sentences. After the sentence is parsed into tokens, the question terms are compared with the terms of each sentence. The question term percentage (QTP) value is obtained for the ratio of the question terms in this sentence. The QTP of each sentence is sorted in descending order. For answer detection, the sentence containing the answer with the highest QTP value is selected. Then, an answer is searched on the selected sentence with RNP methods [1].

![fig_nlp-based](https://user-images.githubusercontent.com/17703776/196274667-cbd05bac-84fd-4e9c-bc3b-e74a88f56693.png)

These RNP methods:

**Remove&Compare (RC)**: When applying the remove and compare (RC) method, question terms are removed from the selected sentence. Then, stopwords are removed from both the selected sentence and the actual answer. If the term count in the selected sentence is equal to the term count in the answer, the remaining terms in the selected sentence are combined and the sentence becomes the candidate answer. This candidate sentence is compared to the actual answer. If the sentence and the actual answer are equal, the candidate answer is determined as correct [1].

**Searching with NER (SNER)**: In the SNER method, answer detection is applied by using the NER method. NER identifies entity names in texts with different labels. That is, the NER method extracts entity types such as person, place, and time in a sentence.  In the application phase of the SNER method, the question pronoun is first sought in the question sentence. The most appropriate NER entity label (PERSON, DATE, etc.) is selected for answer detection by question pronoun. Then, it is checked whether this entity label exists in the NER statements of the sentence selected according to QTP. If this sentence includes this entity label, the term for this entity label is chosen as the candidate answer. Finally, the candidate and actual answers are compared, and if both are equal, the candidate answer is called correct [1].

**Searching with POS tagging (SPOS)**: In SPOS method, POS tagging method is used for answer detection. Special tags for each word are determined in POS tagging. In the first step of the SPOS method, the answer tag is determined by extracting the POS tag of the question pronoun. After removing the question terms from the sentence selected according to QTP, the remaining terms in this sentence is parsed into POS tags. If there is a POS tag with an answer tag in this sentence, the term of this tag is selected as the candidate answer. However, it is checked whether the next term has the same tag. If there is a term with the same tag, the term is added to the candidate answer. Candidate and actual answers are then compared. If both are equal, the candidate answer is correct [1].

![rnp_methods](https://user-images.githubusercontent.com/17703776/196276114-e0f4292a-eff0-4b4a-b6b3-7a8ab9e61b4d.png)

# Reference

Please citation this article:
```
@article{GUVEN2022116592,
title = {Natural language based analysis of SQuAD: An analytical approach for BERT},
journal = {Expert Systems with Applications},
volume = {195},
pages = {116592},
year = {2022},
issn = {0957-4174},
doi = {https://doi.org/10.1016/j.eswa.2022.116592},
url = {https://www.sciencedirect.com/science/article/pii/S0957417422000884},
author = {Zekeriya Anil Guven and Murat Osman Unalir},
keywords = {Natural language processing, BERT, Text analysis, Question answering, SQuAD},
abstract = {In recent years, deep learning models have been used in the implementation of question answering systems. In this study, the performance of the question answering system was evaluated from the perspective of natural language processing using SQuAD, which was developed to measure the performance of deep learning language models. In line with the evaluations, in order to increase the performance, 3 natural language based methods, namely RNP, that can be used with pre-trained BERT language models have been proposed and they have increased the performance of the question answering system in which the pre-trained BERT models are used by 1.1% to 2.4%. As a result of the application of RNP methods with sentence selection, an increase in accuracy between 6.6% and 8.76% was achieved in answer detection. Since these methods don’t require any training process, it has been shown that they can be used in question answering systems to increase the performance of any deep learning model.}
}
}
```
[1] Guven, Z. A., & Unalir, M. O. (2022). Natural language based analysis of SQuAD: An analytical approach for BERT. Expert Systems with Applications, 195, 116592.
