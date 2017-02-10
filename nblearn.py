import sys
import math
import string
import re

words_dict = dict()
count_dict = {'total':0,'PT':0,'PF':0,'NT':0,'NF':0}
probability = dict()
label_dict = dict()
class_count = {'PT':0,'PF':0,'NT':0,'NF':0}

"""stop words in english taken from http://www.ranks.nl/stopwords"""
stop_words = ["a","about","above","across","after","again","against","all","almost","alone","along","already","also","although","always","am","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","aren't","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","below","best","better","between","big","both","but","by","c","came","can","cannot","can't","case","cases","certain","certainly","clear","clearly","come","could","couldn't","d","did","didn't","differ","different","differently","do","does","doesn't","doing","done","don't","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","her","here","here's","hers","herself","he's","high","higher","highest","him","himself","his","how","however","how's","i","i'd","if","i'll","i'm","important","in","interest","interested","interesting","interests","into","is","isn't","it","its","it's","itself","i've","j","just","k","keep","keeps","kind","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","let's","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","mustn't","my","myself","n","necessary","need","needed","needing","needs","never","new","newer","newest","next","no","nobody","non","noone","nor","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","ought","our","ours","ourselves","out","over","own","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","shan't","she","she'd","she'll","she's","should","shouldn't","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","such","sure","t","take","taken","than","that","that's","the","their","theirs","them","themselves","then","there","therefore","there's","these","they","they'd","they'll","they're","they've","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","wasn't","way","ways","we","we'd","well","we'll","wells","went","were","we're","weren't","we've","what","what's","when","when's","where","where's","whether","which","while","who","whole","whom","who's","whose","why","why's","will","with","within","without","won't","work","worked","working","works","would","wouldn't","x","y","year","years","yes","yet","you","you'd","you'll","young","younger","youngest","your","you're","yours","yourself","yourselves","you've","z"]

def check_if_valid_word(word):
    if not word:
        return False
    elif word in stop_words:
        return False;
    else:
        return True

def apply_bayes_model(text,polarity,decision):
   
    #text = ''.join(ch for ch in text if ch not in set(string.punctuation))
   
    text = re.sub('[^a-zA-Z0-9]', ' ',text.replace("\n"," ").replace("\r"," ").replace("&"," and "))
    #text = text.replace('\n','').replace('\r',' ')
    
    truth_flag = True if decision=='truthful' else False
    positive_flag = True if polarity=='positive' else False
    words_list = text.split(' ')
    
    class_type = ''
    if positive_flag and truth_flag:
        class_type = 'PT'
        class_count[class_type]+=1
    if positive_flag and not truth_flag:
        class_type = 'PF'
        class_count[class_type]+=1
    if not positive_flag and truth_flag:
        class_type = 'NT'
        class_count[class_type]+=1
    if not positive_flag and not truth_flag:
        class_type = 'NF'
        class_count[class_type]+=1
    for word in words_list:
        if check_if_valid_word(word):
            wordObj =  {'PT':0,'PF':0,'NT':0,'NF':0}
            if not word.isupper():
                word = word.lower()
            if word in words_dict:
                wordObj = words_dict[word]
            else:
                count_dict['total'] = count_dict['total'] + 1
            count_dict[class_type] = count_dict[class_type] + 1
            wordObj[class_type] = wordObj[class_type] + 1
            words_dict[word] = wordObj

def do_smoothing():

    for key in words_dict:
        obj = words_dict[key]
        wordObj =  dict()
        wordObj['PT'] = math.log(obj['PT']+1) - math.log(count_dict['PT']+ count_dict['total'])
        wordObj['PF'] = math.log(obj['PF']+1) - math.log(count_dict['PF']+ count_dict['total'])
        wordObj['NT'] = math.log(obj['NT']+1) - math.log(count_dict['NT']+ count_dict['total'])
        wordObj['NF'] = math.log(obj['NF']+1) - math.log(count_dict['NF']+ count_dict['total'])
        probability[key] = wordObj

def get_model_file():
    model_file = open('nbmodel.txt','w')
    model_file.write("PRIORS "+ str(class_count['PT']/float(total_reviews))+ ' '+str(class_count['PF']/float(total_reviews))+' '+str(class_count['NT']/float(total_reviews))+' '+str(class_count['NF']/float(total_reviews))+' \n');
    model_file.write('\n')
    
    for key in probability:
        strToPrint = key + ' PT ' + str(probability[key]['PT']) + ' PF ' + str(probability[key]['PF']) 
        strToPrint = strToPrint + ' NT ' + str(probability[key]['NT'])+ ' NF ' + str(probability[key]['NF'])
        model_file.write(strToPrint + '\n')
        
"""read label file"""
lines = [line.rstrip('\n') for line in open(sys.argv[2])] 
for line in lines:
    values = line.split();label_dict[values[0]] = [values[1],values[2]]

"""read text file"""
lines = [line.rstrip('\n') for line in open(sys.argv[1])] 
total_reviews = len(lines)

for line in lines:
    values = line.split(' ',1);labels = label_dict[values[0]] 
    apply_bayes_model(values[1],str(labels[1]),str(labels[0]))
                
do_smoothing()
get_model_file()