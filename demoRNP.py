from collections import OrderedDict
import nltk
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import preProcess
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
def findAnswerType(pos_txt):
	ansType = ''
	if pos_txt == 'people' or pos_txt == 'person':
		ansType = 'PERSON'
	if pos_txt == 'nationality' or pos_txt == 'religion' or pos_txt == 'politic':
		ansType = 'NORP'
	if pos_txt == 'country' or pos_txt == 'city' or pos_txt == 'state':
		ansType = 'GPE'
	if pos_txt == 'company' or pos_txt == 'agency' or pos_txt == 'institution':
		ansType = 'ORG'
	if pos_txt == 'building' or pos_txt == 'airport' or pos_txt == 'highway' or pos_txt == ' bridge':
		ansType = 'FAC'
	if pos_txt == 'location' or pos_txt == 'range':
		ansType = 'LOC'
	if pos_txt == 'hurricane' or pos_txt == 'battle' or pos_txt == 'war':
		ansType = 'EVENT'
	if pos_txt == 'song' or pos_txt == 'title':
		ansType = 'WORK_OF_ART'
	if pos_txt == 'language':
		ansType = 'LANGUAGE'
	if pos_txt == 'time' or pos_txt == 'date' or pos_txt == 'period' or pos_txt == 'duration' or pos_txt == 'year' or pos_txt == 'month' or pos_txt == 'day':
		ansType = 'DATE'
	if pos_txt == 'percentage':
		ansType = 'PERCENT'
	if pos_txt == 'measurement' or pos_txt == 'weight' or pos_txt == 'distance':
		ansType = 'QUANTITY'
		
	return ansType

def demo(related_sentence, answerTerm, questionSearch, quesNormal, totalFindAnswer, methodNo, isLemmatization):
    processes = ''
    sentence = related_sentence
    try:         
        question = questionSearch.split(',')
        if isLemmatization == True:          
            sentence = preProcess.lemmaProcess(sentence)
            quesNormal = preProcess.lemmaProcess(quesNormal)
            answerTerm = preProcess.lemmaProcess(answerTerm)
        
        sentenceTerm = []
        if methodNo == 1:            
            question = preProcess.punctionProcess(quesNormal)  
            question = question.lower().strip().split(' ')
            sentence = preProcess.punctionProcess(sentence)  
            sentence = sentence.lower().strip().split(' ')
            answer = preProcess.punctionProcess(answerTerm)   
            answer = answer.lower().strip().split(' ')
            sw = stopwords.words('english')
            processes += '\nRemoving question words in sentence: ' 
            for ques in question:                
                try: 
                    sentence.remove(ques)
                    processes += ques + ','
                except: 
                    for synset in wordnet.synsets(ques):
                        cnt = False
                        for syn in synset.lemmas():
                            if str(txt).find(syn.name()) != -1:
                                try:
                                    sentence.remove(str(syn.name()))
                                    cnt = True
                                    break
                                except: continue
                        if cnt == True:
                            break
                    continue
            processes += '\n\nRemoving stopwords in sentence: '
            for stop in sw:
                try: 
                    sentence.remove(stop)
                    processes += stop + ','                    
                except: 
                    continue
            processes += '\n\nRemoving stopwords in answer: '
            for stop in sw:
                try: 
                    answer.remove(stop)
                    processes += stop + ',' 
                except: 
                    continue
            if len(sentence) == len(answer):
                sent = ''
                ans = ''
                for s in sentence:
                    sent += s + ' '
                for a in answer:
                    ans += a + ' '
                if sent.strip() == ans.strip():
                    totalFindAnswer += 1

        if methodNo == 2:
            text = str(quesNormal).lower()
            ansType = ''
            if text.find('who') != -1:
                ansType = 'PERSON'
            if text.find('when') != -1:
                ansType = 'DATE'
            if text.find('how many') != -1:
                ansType = 'QUANTITY'
            if text.find('how much') != -1:
                ansType = 'QUANTITY, MONEY'
            if text.find('where') != -1:
                ansType = 'GPE'
            pos = preProcess.posTag(quesNormal.lower())
            if len(pos)> 2:
                for i in range(len(pos)-1):
                    if pos[i][0] == 'what' or pos[i][0] == 'which' or pos[i][0] == 'where' or pos[i][0] == 'whose':
                        ansType = findAnswerType(pos[i+1][0])
                if ansType == '':
                    for i in range(len(pos)-1):
                        ansType = findAnswerType(pos[i+1][0])
                if ansType != '':                   
                    sentence = nlp(sentence)
                    labels = [x.label_ for x in sentence.ents]
                    sentences = [x for x in sentence.sents]
                    processes += 'Question\'s NER label: ' + ansType + '\n\n'
                    processes += 'Related sentence\'s NER labels:\n' 
                    answer = ''
                    ind = 0
                    for k in nlp(str(sentences[0])).ents:
                        processes += str(k) + ': ' + str(labels[ind]) + '\n' 
                        ind += 1
                    ind = 0
                    for k in nlp(str(sentences[0])).ents:
                        if ansType.find(labels[ind]) != -1 and text.find(str(k)) == -1:
                            answer = str(k)
                            break
                        ind += 1
                    if answer == answerTerm or answer == answerTerm.lower():
                        totalFindAnswer += 1

        if methodNo == 3:
            pos = preProcess.posTag(quesNormal.lower())
            ansType = ''
            if len(pos) > 2:
                for i in range(len(pos)-1):         
                    if pos[i][1] == 'NNP' or pos[i][1] == 'WP$':
                        if pos[i][0] == 'whose': ansType = "NNP"
                    if pos[i][1] == 'WP' or pos[i][1] == 'WP':
                        if pos[i][0] == 'who': ansType = "NNP"
                        if pos[i][0] == 'what': ansType = "NN"
                    if pos[i][1] == "WRB":
                        if pos[i][0] == 'when': ansType = "CD"
                        if pos[i][0] == 'how': 
                            if pos[i+1][1] == 'JJ': ansType = "CD"
                            else: ansType = "JJ,RB"
                        if pos[i][0] == 'where': ansType = "NN"
                        if pos[i][0] == 'why': ansType = "IN"
                    if pos[i][1] == "WDT":
                        ansType = "NN"
                    if ansType != '':
                        break
        
                if ansType != '':
                    processes += 'Question\'s POS tag: ' + ansType + '\n\n'
                    processes += 'Removing question terms in sentence: '
                    question = quesNormal[:-1].split(' ')
                    for ques in question:
                        if sentence.find(ques) != -1:
                            ind = sentence.index(ques)
                            processes += ques + ','
                            sentence = sentence[:ind-1] + sentence[ind+len(ques):]                 
                    posSent = preProcess.posTag(sentence.strip())
                    processes += '\nRelated sentence\'s POS tags:\n'
                    ans = ''
                    ind = 0
                    for key, p in posSent:
                        processes += str(key) + ': ' + str(p) + '\n' 
                        ind += 1
                    ind = 0
                    for key, p in posSent:
                        if ansType.find(p) != -1:
                            ans += str(key) + ' '
                            if ind+1 < len(posSent)-1:
                                for k in range(ind+1,len(posSent)):
                                    if ansType.find(str(posSent[k][1])) != -1:
                                        ans += str(posSent[k][0]) + ' '
                                    else: break
                            break
                        ind += 1
                    if ans != '':
                        if ans[:-1] == answerTerm or ans[:-1] == answerTerm.lower():
                            totalFindAnswer += 1        

    except Exception as e:
        print('Error Answer detection: ' + str(e) + ' - method:' + str(methodNo))        
    return totalFindAnswer, processes
