import os
from flask import Flask, request, jsonify, abort
import boto3
from datetime import date

app = Flask(__name__)


TODOS_TABLE = os.environ['TODOS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TODOS_TABLE)




def get_todo(username):
    res = table.get_item(Key={ 'username': username })
    year, month, day = res["date_of_birth"].split("-")
    today = date.today()
    if today.month == int(month) and today.day == int(day):
       return jsonify({"message": f"Hello, {username}! Happy birthday!"})

    else:
        month_diff = today.month - int(month)
        day_diff = today.day - int(day)
        return jsonify({"message": f"Hello, {username}! Your birthday is in {(12 + month_diff) * 30 + day_diff} day(s)"})



def new_id():
    res = table.scan()
    ary = res['Items']
    if len(ary) == 0:
        return '1'
    else:
        ary = sorted(ary, key=lambda x: x['username'], reverse=True)
        return str(int(ary[0]['username']) + 1)



@app.route("/hello/<username>")
def show(username):
    todo = get_todo(username)
    return jsonify(todo),


@app.route("/hello/<username>", methods=["POST"])
def update(username):
    date_of_birth = request.json.get('date_of_birth')
    if not date_of_birth:
        return jsonify({'error': 'Please provider todo  date_of_birth'}), 422
    new_todo = { 'username': new_id(), 'date_of_birth': date_of_birth }
    res = table.put_item(Item=new_todo)

     return jsonify(new_todo), 201


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
