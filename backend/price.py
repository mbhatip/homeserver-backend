import db
import time
import requests

def getPrice(id):
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Price WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row is None:
            response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{id.upper()}/prev?unadjusted=true&apiKey=pBYqVgnpohQmImag5XMM15OsMRkdhPdr")
            if not response:
                raise Exception("API failed to get price")
            body = response.json()
            price = body['results'][0]['c']
            date = body['results'][0]['t']//1000
            cursor.execute("INSERT INTO Price (id, price, date) VALUES (?, ?, ?)",
                (id, price, date))
            conn.commit()
            return price
        elif time.time() - row['date'] > 86400 * 2:
            response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{id.upper()}/prev?unadjusted=true&apiKey=pBYqVgnpohQmImag5XMM15OsMRkdhPdr")
            if not response:
                return row['price']
            body = response.json()
            price = body['results'][0]['c']
            date = body['results'][0]['t']//1000
            cursor.execute("UPDATE Price SET price = ?, date = ? WHERE id = ?",
                (price, date, id))
            conn.commit()
            return price
        else:
            return row['price']



