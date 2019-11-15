from bottom.mongoset import*
import json
data=mongoDB('localhost',27017,'MyTest','untreatData')
print(data.find())