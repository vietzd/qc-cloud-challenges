from cloudant.client import Cloudant
from cloudant.query import Query

def centroid(color):
    client = Cloudant.iam(CLOUDANT_ACCOUNT_NAME, CLOUDANT_API_KEY, connect=True)
    kmeans_train = client['kmeans_train']
    query = Query(kmeans_train, selector={"Class": color}, fields=["x", "y"])
    x_sum = 0.0
    y_sum = 0
    count = 0
    for doc in query.result:
        x_sum += doc['x']
        y_sum += doc['y']
        count += 1
    client.disconnect()
    if (count == 0):
        return {"Class": color, "x": 0.0, "y": 0.0}
    return {"x": x_sum/count, "y": y_sum/count}


def saveToDB(color, centroid):
    client = Cloudant.iam(CLOUDANT_ACCOUNT_NAME, CLOUDANT_API_KEY, connect=True)
    db_centroids = client['kmeans_centroids']
    doc = db_centroids[color]
    doc['x'] = centroid['x']
    doc['y'] = centroid['y']
    doc.save()
    print("saved", color, centroid)
    client.disconnect()

def main(dict):
    global CLOUDANT_ACCOUNT_NAME
    CLOUDANT_ACCOUNT_NAME = dict['CLOUDANT_ACCOUNT_NAME']
    global CLOUDANT_API_KEY
    CLOUDANT_API_KEY = dict['CLOUDANT_API_KEY']

    colors = ['Green', 'Blue', 'Black']

    result = {}
    for color in colors:
        x = centroid(color)
        saveToDB(color, x)
        result[color] = x

    return{"message": "Updated Centroids", "Centroids": result}


print(result)
