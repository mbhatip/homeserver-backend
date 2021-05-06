from bottle import Bottle, run, response, request
import json
import db
from user import User
from stock import Stock
import price
from configparser import ConfigParser

app = Bottle()

def verifiedUser(u, p):
    user = User.find(u)
    if (user.password != p):
        raise Exception(f"Password for user {u} does not match")
    else:
        return user

@app.get('/user')
def getUserSummary():
    try:
        body = request.json
        username = body['username']
        password = body['password']
        user = verifiedUser(username, password).jsonable()
    except Exception as e:
        response.status = 400
        return f"Error: {e}"
    return user 

@app.post('/user')
def makeNewUser():
    try:
        body = request.json
        body["money"] = 1000
        User.createFromJSON(body)
    except Exception as e:
        response.status = 400
        return f"Error: {e}"
    return User.find(body['username']).jsonable()
        
@app.get('/user/<ticker>')
def getUserStock(ticker):
    ticker = ticker.lower()
    try:
        body = request.json
        username = body['username']
        password = body['password']
        user = verifiedUser(username, password).jsonable()
        stocks = [s.jsonable() for s in Stock.findFromUser(username) if s.ticker == ticker]
    except Exception as e:
        response.status = 400
        return f"Error: {e}"
    return {"total": sum([s['amount'] for s in stocks]), "stocks": stocks}

@app.post('/user/<ticker>')
def exchangeStock(ticker):
    ticker = ticker.lower()
    try:
        body = request.json
        username = body['username']
        password = body['password']
        user = verifiedUser(username, password)
        amount = body['amount']
        try:
            price = price.getPrice(ticker)
        except Exception as e:
            response.status = 400
            return f"Error: {e}"
        if (amount == 0):
            raise Exception("Cannot exchange no stocks")
        if(amount * price > user.money):
            raise Exception("This purchase will exceed the available funds")
        stockAmount = sum([s.amount for s in Stock.findFromUser(user.id) if s.ticker == ticker])
        if(stockAmount + amount < 0):
            raise Exception("There is not enough stock to complete this sale")

        user.money -= amount * price
        user.update()
        stock = Stock.createFromJSON({"ticker": ticker, "price": price, "amount": amount, "uid": username})
    except Exception as e:
        response.status = 400
        return f"Error: {e}"
    return stock.jsonable()

@app.get('/stock')
def getStockSummary():
    #TODO: implement reddit api to give info on top stocks in market
    return

@app.get('/stock/<ticker>')
def getStockInfo(ticker):
    ticker = ticker.lower()
    try:
        return {"price": price.getPrice(ticker)}
    except Exception as e:
        response.status = 400
        return f"Error: {e}"

@app.delete('/<id>')
def deleteUser(id):
    '''Implements instance deletion'''

    try:
        user = User.find(id)
    except Exception:
        response.status = 404
        return f"User {id} to delete does not exist"

    user.delete()

    response.content_type = 'application/json'
    return json.dumps(True)

# read from ini file
config = ConfigParser()
config.read("settings.ini")
host = config.get("DEFAULT", "host")
port = config.get("DEFAULT", "port")

# Start the backend
run(app, host=host, port=port, debug=False)
