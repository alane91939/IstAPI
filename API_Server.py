from datetime import datetime
from flask import Flask, request, jsonify
from collections import deque


app = Flask("total_points")


def toDatetime(date):
    today = datetime.today()
    return datetime.strptime(date + '2021', '%m/%d  %I%p%Y')

statusCode = 200
fetch_account = {}
point_total = 0


#queue to keep track of incoming transactions


transactions = deque()


@app.route('/points_added',methods=['POST'])

def points_added():


    global point_total
    global statusCode


    info = request.get_json(force=True)
    print(info)
    payer = (info["Brand"])
    points = (info["points"])
    timestamp = toDatetime(info["timestamp"])



        #When the points are positive, append transaction
        #when Negative:
          #  -  payer already exists/ deducting = negative points value
           # - payer already exists / deducting = positive points value
            #- when the first transactional = negative



    if points > 0:
       point_total += points
       transactions.append([payer,points,timestamp])
       if payer is not fetch_account:
            fetch_account[payer] = points
       else:
            fetch_account[payer] += points

    elif points < 0:
        if payer in fetch_account and (fetch_account[payer] - points) < 0:
            statusCode = 400
            return ("transction failed")
        elif payer in fetch_account and (fetch_account[payer] - points) > 0:
            fetch_account[payer] += points
            point_total += points
            for k in range(len(transactions) -1):
                if transactions[k][0] == payer:
                    results = transactions[k][1] + points
                    if results <= 0:
                      del transactions [k]
                      points = results
                    else:
                        transactions[k][1] = results
                        break

        else:
            statusCode = 400
            return("transction failed",int(statusCode))
    return("Trasaction Successful", int(statusCode))



#REST endpoint to deduct points from the User account
@app.route('/remove_points',methods=['DELETE'])
def remove_points():

    global point_total
    global statusCode

    info = request.get_json(force=True)
    points_lost = int(info['points_lost'])
    if point_total < points_lost:
        statusCode = 400
        return("transction failed",int(statusCode))

    else:
        point_list = []
        while (points_lost > 0):
            transaction = transactions.pop()
            points_lost -= transaction[1]
            if points_lost < 0:
                points_removed = transaction[1] + points_lost
                transaction[1] = points_removed
                transactions.append(transaction)
            else:
                points_removed = transaction[1]
            transaction[1] = points_removed
            transaction[2] = "current"
            point_list.append(transaction)
            fetch_account[transaction[0]]-= points_removed
            point_total-= points_removed

    for value in point_list:
        value[1] = -value[1]
    return jsonify(point_list)


@app.route("/balance",methods=['GET'])
def balance():
    return jsonify(fetch_account)

if __name__ == "__main__":

    app.run(debug=True)





















