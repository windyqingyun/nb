import pymongo


conn = pymongo.MongoClient(host='localhost',port=27017,connect=False)
db = conn.nb


class User():

    userCol = db.user	

    def __init__(self,account,password):
        self.account = account
        self.password = password

    def save(self):	
        userDict = self.__dict__
        self.userCol.insert(userDict)

    def find(self):
        return self.userCol.find_one({"account":self.account,"password":self.password})

    def findAccount(self):
        return self.userCol.find_one({"account":self.account})
	
    def update(self,newPassword):
        self.userCol.update({"account":self.account},{"$set":{"password":newPassword}})
	
    def delete(self):
        self.userCol.remove({"account":self.account})


class Blog():

    blogCol = db.blog	

    def __init__(self,uid="",account="",title="",content="",contentTxt="",time=""):
		
        self.uid = uid
        self.account = account
        self.title = title
        self.content = content
        self.contentTxt = contentTxt
        self.time = time

    def save(self):	
        blogDict = self.__dict__
        self.blogCol.insert(blogDict)
	

    def findByAccount(self,account,page=1):
        s = 0 
        if page > 1:
           s = (page-1)*5
        return self.blogCol.find({"account":account},{'_id':0}).sort("time",pymongo.DESCENDING).skip(s).limit(5)

    def findById(self,uid):
        return self.blogCol.find_one({"uid":uid})

    def findAll(self,page=1):
        s = 0
        if page > 1:
           s = (page-1)*5
        return self.blogCol.find({},{'_id':0}).sort("time",pymongo.DESCENDING).skip(s).limit(5)

    def update(self):
        pass
	
    def deleteById(self,uid):
        self.blogCol.remove({"uid":uid})

