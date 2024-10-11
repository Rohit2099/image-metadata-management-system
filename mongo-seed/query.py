from pymongo import MongoClient
import pprint


if __name__ == "__main__":
    PORT = 8000
    client = MongoClient('localhost', PORT)
    db = client['data_base_name']
    collection = db['collection_name']
    # query 1
    # returns only the "file_encoded" attribute
    query_results = collection.find({"ExifImageHeight": "1200"}, {"file_encoded":1})
    for result in query_results:
        pprint.pprint(result)
    # query 2
    query_results = collection.find({"ExifImageWidth": "1920"})
    for result in query_results:
        pprint.pprint(result)
    # query 3
    query_results = collection.find({"BitsPerSample": "(8, 8, 8)"})
    for result in query_results:
        pprint.pprint(result)
    # query 4
    query_results = collection.find({"ColorSpace": "1"})
    for result in query_results:
        pprint.pprint(result)
