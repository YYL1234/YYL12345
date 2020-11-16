import pymongo

# 从库里取词向量求和
def sum_of_vectors():
    client = pymongo.MongoClient('mongodb://192.168.1.115:27017/')
    # 验证登录mongodb
    client.admin.authenticate("kus", "kus", mechanism='SCRAM-SHA-1')
    mydb = client["documents"]
    mycol = mydb["texts"]
    sum = []
    for item2 in mycol.find({}):
        vectors = []
        wordlist = []
        try:
            for item3 in item2['keywords']:
                wordlist.append(item3)
        except Exception as e:
            pass
            continue
        for item3 in item2['keywords']:
            wordlist.append(item3)
        # 取关键词词向量
        i = 0
        for i in range(len(wordlist)):
            temp1 = find_vectors(wordlist[i])
            #求和
            if vectors:
                for j in range(len(vectors)):
                    vectors[j] = (float(temp1[j]) + float(vectors[j]))
            else:
                vectors = temp1
        sum.append(vectors)
    add_to_mongodb(sum)

#找每个关键词地词向量
def find_vectors(word):
    vector=[]
    client = pymongo.MongoClient('mongodb://192.168.1.115:27017/')
    # 验证登录mongodb
    client.admin.authenticate("kus", "kus", mechanism='SCRAM-SHA-1')
    mydb = client["documents"]
    mycol = mydb["words_vector"]
    for item1 in mycol.find({}):
        if item1['word'] == word:
            vector.append(item1['vector'])
            break
    return vector[0]

#将词向量加入mongodb中
def add_to_mongodb(result):
    myclient = pymongo.MongoClient('mongodb://192.168.1.115:27017/')
    # 验证登录mongodb
    myclient.admin.authenticate("kus", "kus", mechanism='SCRAM-SHA-1')
    # （其中admin可以换成你的用户名能登录的库名）

    mydb = myclient["documents"]
    mycol = mydb["texts"]
    # mydict = {"f2": data}
    # mycol.insert_one(mydict)
    i = 0
    for c in mycol.find():
        if i<len(result):
            mycol.update({'_id': c['_id']}, {'$set': {'f2': result[i]}})
            i=i+1
        else:
            break

sum_of_vectors()
print('结束')
