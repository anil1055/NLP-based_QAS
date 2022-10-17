import spacy
import nltk
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from collections import OrderedDict
from nltk.corpus import wordnet
from spacy import displacy
from collections import Counter
import demoRNP
import qaProcess
import preProcess

def demoProcess(question, paragraph, answer, lemma):
  question = preProcess.punctionProcess(question)
  X_list = word_tokenize(question) 
  questionSearch = qaProcess.defineQuestionTerm([X_list])
  processes = 'Question terms: ' + questionSearch + '\n'
  textSearch, path = qaProcess.searchWord(questionSearch, paragraph, lemma)
  texts = path.split('\n')
  print('Sorted sentence: ' + str(texts))
  txtInd = 0
  sel_sentence = ''
  for txt in texts:
      if (str(txt.lower()).find(answer.lower()) != -1 or str(txt).find(answer) != -1):
          sentence = str(txt).split('sentence - ')
          sentence = str(sentence[1]).strip()
          sel_sentence = str(sentence).replace('\n', '').strip()
          break

  return questionSearch, sel_sentence

paragraph_examples = 'Tarkan Tevetoğlu is a Turkish singer and songwriter. Tarkan was born on 17 October 1972 in Alzey, West Germany, to Neşe and Ali Tevetoğlu. The name Tarkan is said to originate from an ancient Turkic King. Tarkan\'s first album, Yine Sensiz, was released on cassettes on 26 December 1992. Since the early 1990s, with the successful sales of his albums, he has been a prominent figure of pop music, recognized in Turkey and worldwide.'
question_examples = ['Who is Tarkan Tevetoğlu?','When was Tarkan born?','Whose name does Tarkan originate from?']
answer_examples = ['Turkish singer and songwriter', '17 October 1972', 'Turkic King']
  
lemma = False
question = ''
preProcess = '' 
answer = ''
paragraph = paragraph_examples

question = question_examples[0]
answer = answer_examples[0]
response = answer_examples[0]
answ = answer_examples[0].lower().strip().split(' ')
sw = stopwords.words('english')
for stop in sw:
    try: 
        answ.remove(stop)                 
    except: continue
res = ''
for ans in answ:
    res += ans + ' '
answer = res

questionSearch, sel_sentence = demoProcess(question, paragraph, response, lemma)
print('Candidate sentence: ' + sel_sentence)
totalFindAnswer = 0
findCount = totalFindAnswer
totalFindAnswer, process = demoRNP.demo(sel_sentence, answer, questionSearch, question, totalFindAnswer, 1, lemma)
if totalFindAnswer != findCount:
  print('RC: Answer found successfully, answer: ' + answer)
  
  
question = question_examples[1]
answer = answer_examples[1]

questionSearch, sel_sentence = demoProcess(question, paragraph, answer, lemma)
totalFindAnswer = 0
findCount = totalFindAnswer
totalFindAnswer, process = demoRNP.demo(sel_sentence, answer, questionSearch, question, totalFindAnswer, 2, lemma)
if totalFindAnswer != findCount:
  print(process)
  print('SNER: Answer found successfully, answer: ' + answer)
  
  
question = question_examples[2]
answer = answer_examples[2]

questionSearch, sel_sentence = demoProcess(question, paragraph, answer, lemma)
totalFindAnswer = 0
findCount = totalFindAnswer
totalFindAnswer, process = demoRNP.demo(sel_sentence, answer, questionSearch, question, totalFindAnswer, 3, lemma)
if totalFindAnswer != findCount:
  print(process)
  print('SPOS: Answer found successfully, answer:' + answer)
