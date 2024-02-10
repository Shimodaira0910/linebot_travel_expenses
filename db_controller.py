from pymongo import MongoClient


class DbController:
    
    def __init__(self):
        self.__HOST = "mongo"
        self.__PORT = 27017
        self.__USERNAME = 'root'
        self.__PASSWORD = 'example'
        self.__DB_NAME = 'travel_expenses'
        self.__COLLECTION_NAME = 'expenses'
        self.__collection = self.__db_connection()
        
    def __db_connection(self):
        client = MongoClient(host=self.__HOST, port=self.__PORT, username=self.__USERNAME, password=self.__PASSWORD)
        db = client[self.__DB_NAME]
        collection = db[self.__COLLECTION_NAME]
        
        return collection
    
    def insert_member_name(self, name):
        try:
            result = self.__collection.insert_one({'username': name})
            print("データが正常に挿入されました。") if result.acknowledged else print("データの挿入に失敗しました。")
        except Exception as e:
            print(f"データの挿入中にエラーが発生しました: {e}")