import sys
from cloudant.client import Cloudant

def main(dict):
    global CLOUDANT_ACCOUNT_NAME
    CLOUDANT_ACCOUNT_NAME = dict['CLOUDANT_ACCOUNT_NAME']
    global CLOUDANT_API_KEY
    CLOUDANT_API_KEY = dict['CLOUDANT_API_KEY']

    # assemble random data point
    randPoint = assembleDatapoint(dict["random_bitstring"])

    # store data point to DB
    saveToDB(randPoint)

    return { 'message': 'OK' }

def assembleDatapoint(bitstring):
    length = len(bitstring)
    rand_1 = int(bitstring[:len(bitstring)//2], 2)
    rand_2 = int(bitstring[len(bitstring)//2:], 2)
    return {"x": rand_1, "y": rand_2}

def saveToDB(point):
    client = Cloudant.iam(CLOUDANT_ACCOUNT_NAME, CLOUDANT_API_KEY, connect=True)
    db_centroids = client['random_data_points']
    data = {
        'x': point["x"],
        'y': point["y"]
    }
    doc = db_centroids.create_document(data)
    client.disconnect()