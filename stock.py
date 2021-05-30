import db

class Stock:

    def __init__(self, id, ticker, price, amount, uid):
        '''Constructor'''
        self.id = id
        self.ticker = ticker
        self.price = price
        self.amount = amount
        self.uid = uid

    def update(self):
        '''Writes back instance values into database'''
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Stock SET ticker = ?, price = ?, amount = ?, uid = ? WHERE id = ?",
                               (self.ticker, self.price, self.amount, self.uid, self.id))
            conn.commit()
        
    def updateFromJSON(self, q_data):
        '''Unpack JSON representation to update instance variables and then
           calls update to write back into database'''
        
        self.ticker = q_data['ticker']
        self.price = q_data['price']
        self.amount = q_data['amount']
        self.uid = q_data['uid']
        self.update()

    def delete(self):
        '''Deletes instance from database, any object representations of the
           instance are now invalid and shouldn't be used including this one'''
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Stock WHERE id = ?", (self.id, ))            

    
    def jsonable(self):
        '''Returns a dict appropriate for creating JSON representation
           of the instance'''
        
        return {'id': self.id, 'ticker': self.ticker, 'price': self.price, 'amount': self.amount, 'uid': self.uid}

        

    @staticmethod
    def createFromJSON(q_data):
        '''Creates new instance object using dict created from JSON representation
           using create'''
        
        # Unpack the instance data from JSON
        # Should validate information here and throw exception
        # if something is not right.
        ticker = q_data['ticker']
        price = q_data['price']
        amount = q_data['amount']
        uid = q_data['uid'] 

        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Stock (ticker, price, amount, uid) VALUES (?, ?, ?, ?)",
                               (ticker, price, amount, uid))
                               
            conn.commit()

        return Stock.find(cursor.lastrowid)
        

    @staticmethod
    def find(id):
        '''If row with specified id exists, creates and returns corresponding ORM
           instance. Otherwise Exception raised.'''
        
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stock WHERE id = ?", (id,))
            row = cursor.fetchone()

        if row is None:
            raise Exception(f'No such Stock with id: {id}')
        else:
            return Stock(row['id'], row['ticker'], row['price'], row['amount'], row['uid'])
    
    @staticmethod
    def findFromUser(uid):
        '''If row with specified id exists, creates and returns corresponding ORM
           instance. Otherwise Exception raised.'''
        
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stock WHERE uid = ?", (uid,))
            rows = cursor.fetchall()

        if rows is None:
            raise Exception(f'User {uid} has no stocks')
        else:
            return [Stock(row['id'], row['ticker'], row['price'], row['amount'], row['uid']) for row in rows]