import pypyodbc
import azurecred


class AzureDB:
    dsn = 'DRIVER='+azurecred.AZDBDRIVER+';SERVER='+azurecred.AZDBSERVER+';PORT=1433;DATABASE='+azurecred.AZDBNAME+';UID='+azurecred.AZDBUSER+';PWD='+ azurecred.AZDBPW

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT * from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

    def azureAddData(self, name, text, date):
        query = f"INSERT into data (name, text, date) values ('{name}', '{text}', '{date}')"
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

    def azureDeleteData(self, index):
        self.cursor.execute(f"DELETE FROM data WHERE id = {index}")
        self.conn.commit()

    def azureGetOneData(self, index):
        self.cursor.execute(f"SELECT * from data WHERE id = {index}")
        data = self.cursor.fetchone()
        return data

    def azureUpdateData(self, index, name, text):
        self.cursor.execute(f"UPDATE data set name='{name}', text='{text}' WHERE id ='{index}'")
        self.conn.commit()
