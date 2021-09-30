/* params=
    {
        "point": {"x": 0.5, "y": 0.5},
        "centroids": [
            {"x": -0.265, "y": -0.265},
            {"x": 0.3733125, "y": 0.3733125},
            {"x": 0.03875, "y": 0.03875}],
        "distances": [262, 5, 101]
    }

    properties:
    CLOUDANT_URL = "xxx"
    CLOUDANT_APIKEY = "xxx"
*/
var Cloudant = require('@cloudant/cloudant');

function main(params) {
    a = params.distances
    var lowest = 0;
    for (var i = 1; i < a.length; i++) {
        if (a[i] < a[lowest]) lowest = i;
    }
    var result = { "point": params.point, "closest_centroid": params.centroids[lowest] }

    var cloudant = Cloudant({ url: params.CLOUDANT_URL, plugins: { iamauth: { iamApiKey: params.CLOUDANT_APIKEY } } });
    var mydb = cloudant.db.use('labeled_data_uc2');
    mydb.insert(result)

    return {
        "inserted": result
    };
}
