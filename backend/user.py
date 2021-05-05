import db

class User:
    def __init__(self, id, password, money):
        '''Constructor'''
        self.id = id
        self.password = password
        self.money = money

    def update(self):
        '''Writes back instance values into database'''
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET password = ?, money = ? WHERE id = ?",
                               (self.password, self.money, self.id))
            conn.commit()
        
    def updateFromJSON(self, q_data):
        '''Unpack JSON representation to update instance variables and then
           calls update to write back into database'''
        
        self.password = q_data['password']
        self.money = q_data['money']
        self.update()

    def delete(self):
        '''Deletes instance from database, any object representations of the
           instance are now invalid and shouldn't be used including this one'''
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM User WHERE id = ?", (self.id, ))
            cursor.execute("DELETE FROM Stock WHERE uid = ?", (self.id, ))
            
    
    def jsonable(self):
        '''Returns a dict appropriate for creating JSON representation
           of the instance'''
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT ticker, SUM(amount) AS amount FROM Stock WHERE uid='{self.id}' GROUP BY ticker")
            rows = [{"ticker": row['ticker'], "amount": row['amount']} for row in cursor.fetchall()]
            #TODO: implement average price for each stock
            
        
        return {'id': self.id, 'password': self.password, 'money': self.money, 'stocks': rows}

        

    @staticmethod
    def createFromJSON(q_data):
        '''Creates new instance object using dict created from JSON representation
           using create'''
        
        # Unpack the instance data from JSON
        # Should validate information here and throw exception
        # if something is not right.
        id = q_data['username']
        password = q_data['password']
        money = q_data['money']

        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (id, password, money) VALUES (?, ?, ?)",
                               (id, password, money))
                               
            conn.commit()

        return User.find(id)
        

    @staticmethod
    def find(id):
        '''If row with specified id exists, creates and returns corresponding ORM
           instance. Otherwise Exception raised.'''
        
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE id = ?", (id,))
            row = cursor.fetchone()

        if row is None:
            raise Exception(f'No such User with id: {id}')
        else:
            return User(row['id'], row['password'], row['money'])