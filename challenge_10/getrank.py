#!/usr/bin/env python3

import sys
from pymongo import MongoClient
from bson.son import SON

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    a = contests.aggregate([{"$group":{"_id":"$user_id","score":{"$sum":"$score"},"submit_time":{"$sum":"$submit_time"}}},{"$sort":SON([("score",-1),("submit_time",1)])}])
    i = 0
    for x in a:
        i += 1
        if x['_id'] == user_id:
            rank = i
            score = x['score']
            submit_time = x['submit_time']
    return rank, score, submit_time

if __name__ == '__main__':
    try:
        if len(sys.argv[1:]) != 1 or sys.argv[1] is str:
            raise ValueError
        else:
            user_id = int(sys.argv[1])
            userdata = get_rank(user_id)
            print(userdata)
    except ValueError:
        print("Parameter Error")
