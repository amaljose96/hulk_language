from corenlp import *
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)


def getPOS(pos_set,word):
    for pair in pos_set:
        if(pair[0]==word):
            return pair[1]


def transform(sentence):
     for rel, _, head, word, n in sentence['dependencies']:
         n = int(n)
         word_info = sentence['words'][n - 1][1]
         tag = word_info['PartOfSpeech']
         lemma = word_info['Lemma']
         if rel == 'root':
             rel = 'ROOT'
         yield n, '_', word, lemma, tag, tag, '_', head, rel, '_', '_'






parser = argparse.ArgumentParser(description='Given a passage, outputs a preprocessed version of the passage with the following:\n\t\t1.Sentence and word tokenize \n\t\t2.Pronoun Replacement\n\t\t3.Synonym Replacement\n\t\t4.Stopword Removal.')
parser.add_argument('inputfile', metavar='inputfile', type=str, nargs=1,
                   help='Input file containing passage')
args = parser.parse_args()
inputfilename=args.inputfile[0]
print inputfilename


inputfile=open(inputfilename,'r')

















print "Loading CoreNLP"
corenlp = StanfordCoreNLP()
print "CoreNLP Loaded."
passage=inputfile.read();
output=''
print "Passage : "+passage;

#FIRST STEP : SENTENCE AND WORD TOKENIZE TO OUR FORMAT.
stop_words = ['a','the','an'] #set(stopwords.words('english'))
sentences=sent_tokenize(passage);
data=[];
for sentence in sentences:
    words=word_tokenize(sentence)
    filtered_sentence = [w for w in words if not w in stop_words]
    data.append(filtered_sentence)
print "\tFirst step : Sentence and word tokenize :\t"
#pp.pprint(data);
print "\tSecond step : Pronoun replacement :\t"
corenlp_op=json.loads(corenlp.parse(passage));
if(corenlp_op.has_key(u'coref')):
    coref_data=corenlp_op[u'coref']
    for a_pair in coref_data:
        for pair in a_pair:
            print "\t\tPrinting pair"
            pp.pprint(pair)
            to_replace=pair[0]
            with_replace=pair[1]
            if(to_replace[2]==to_replace[3]):
                print "\t\tReplacing "+data[to_replace[1]][to_replace[2]]+" with "+str(with_replace[0])+" from "+str(to_replace[3])+" to "+str(to_replace[2]);
                data[to_replace[1]][to_replace[3]]=str(with_replace[0])
else:
    print "No pronouns to replace"


"""
#pp.pprint(data);

#FOURTH STEP : SYNONYMN REPLACEMENT USING wordnet
#INPUT : The given passage
#OUTPUT : The given passage in a format(wordwise) with each word reduced to the first word in its synset.
stage_output=[];
print "\tThird step : Synonym replacement:\t"

print "\t\tSYNREPLACE O/P"
for sentence in data:
    outputsentence=[]
    for word in sentence:
        synset=wordnet.synsets(word)
        postag=getPOS(nltk.pos_tag(sentence),word);
        if(len(synset)==0 or postag=='VBD' or postag=='VBZ'):
            simplest_synonymn=str(word)
        else:
            print word+":"+getPOS(nltk.pos_tag(sentence),word)
            simplest_synonymn=synset[0].lemma_names()[0]
        print "\t\t\tSYNREPLACE: Replacement for "+word+" is "+simplest_synonymn
        outputsentence.append(simplest_synonymn);
    stage_output.append(outputsentence);
data=stage_output

"""








print "\tFourth step : Prepare output sentence :\t"
index=0
pw=''
for sentence in data:
    for word in sentence:
        if(word=="." or word==',' or word=='\''):
            output=output+pw
        else:
            output=output+pw+" "
        pw=word
output=output+pw

print "Output="+output



outputfilename=inputfilename.split(".")[0]+"_preprocessed."+inputfilename.split(".")[1]
print "Writing to "+outputfilename;
outputfile=open(outputfilename,'w')
outputfile.write(output)
