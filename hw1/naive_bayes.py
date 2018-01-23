import sys,re,csv

train_file='train.tsv'#str(sys.argv[1])
result_file='dev.tsv'#str(sys.argv[1])


#
# def read_file(input_file):
#     f = open(input_file, 'r',encoding='latin1')
#
#     str_list = []
#     for l in f.readlines():
#         str_list.append(l.split("\t"))
#     # print(str_list[2])#
#     f.close()
#     return str_list
#
# def tokenize(str):
#     feature=str.split(' ')
#     return feature

#read the file
def read_file(file):
    str_list=[]
    f = open(file, 'r',encoding='latin1')
    for l in f.readlines():
        str_list.append(l.split("\t"))
    # print(str_list[2])
    f.close()
    return str_list



def tokenize(str):
    list=str.split(' ')
    return list

def train(str_list,smoothing_alpha=5):
    #smoothing_alpha=0,feature_list=[],

    feature_dic = {}

    #count for reviews
    all_review_count=0
    reciew_0_count=0
    reciew_1_count=0
    # count for words
    all_word_count = 0
    word_0_count = 0
    word_1_count = 0

    for review in str_list:
        #clean class, cut\n
        review[2] = review[2][:1]
        # P(X=xi)
        if review[2] == '0':
            all_review_count+=1
            reciew_0_count+=1
            # print('review[1]',tokenize(review[1]))
            for word in tokenize(review[1]):
                # print('word:',word)
                all_word_count += 1
                word_0_count += 1
                if word not in feature_dic:
                    feature_dic[word] = [1, 1, 0]
                else:
                    feature_dic[word][0] += 1
                    feature_dic[word][1] += 1


        # P(Y=yi)
        elif review[2]=='1':
            all_review_count += 1
            reciew_1_count+=1
            for word in tokenize(review[1]):
                all_word_count += 1
                word_1_count += 1
                if word not in feature_dic:
                    feature_dic[word] = [1, 0, 1]
                else:
                    feature_dic[word][0] += 1
                    feature_dic[word][2] += 1
    # print(feature_dic)
    for each in feature_dic:
        # print('each',each,feature_dic[each][0])
        feature_dic[each][0] = (feature_dic[each][0] + smoothing_alpha) / (all_word_count + smoothing_alpha)
        feature_dic[each][1] = (feature_dic[each][1] + smoothing_alpha) / (word_0_count + smoothing_alpha)
        feature_dic[each][2] = (feature_dic[each][2] + smoothing_alpha) / (word_1_count + smoothing_alpha)
    # print('feature_dic',feature_dic)

    # all_review_count = 0
    # reciew_0_count = 0
    # reciew_1_count = 0
    p_pos=reciew_0_count/all_review_count
    p_neg = reciew_1_count / all_review_count
    try:
        p_pos+p_neg==1
    except:
        print('not equal to 1')
    train_tuple=(feature_dic,p_pos,p_neg)
    return train_tuple







def classify(list_of_word,train_tuple):

    feature_dic=train_tuple[0]
    p_pos=train_tuple[1]
    p_neg=train_tuple[2]
    p_pos_for_sentence = p_pos
    p_neg_for_sentence = p_neg
    print(p_pos_for_sentence, p_neg_for_sentence)
    for word in list_of_word:
        if word in feature_dic:

            p_pos_for_sentence=p_pos_for_sentence*feature_dic[word][1]
            p_neg_for_sentence=p_neg_for_sentence*feature_dic[word][2]
            print(word, p_pos_for_sentence, p_neg_for_sentence)

        else:
            print(word,'don\'t belong to the training data')

    if p_pos_for_sentence/p_neg_for_sentence>1:
        print('positive:',list_of_word)
        return '0'
    elif p_pos_for_sentence/p_neg_for_sentence<1:
        print('negative:',list_of_word)
        return '1'
    else:
        print('what\'s going on..')


def naive_main ():

    str_list=read_file(train_file)
    # create two lists to saperate
    pos_list=[]
    neg_list=[]
    for each in str_list:
        if each[2]=='0':
            pos_list.append(each[1])
        elif each[2]=='1':
            neg_list.append(each[1])

    train_tuple= train(str_list)

    result_list = read_file(result_file)
    right=0
    wrong=0
    for review in result_list:
        # print(each[1])
        result = classify(review[1].split(),train_tuple)
        print(type(result),type(review[2]))
        print(result, review[2])

        if str(result) != review[2]:
            wrong+=1
        else:
            right+=1
    # print('right:',right,'\nwrong:',wrong)
