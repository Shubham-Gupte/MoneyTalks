import urllib, json,requests
def locationVerify():
    requestURL = "https://env-72355.customer.cloud.microstrategy.com:2443/allusers?info_type=ADAttrs&badge_index_from=1&badge_id=55&target_badge_ids=55&ad_attr_list=lat,lon&access_token=POn5F2VXQdJRo9yUGTR4xIB8qnA1M-pP5EPNwkjRkLIcs--nfDi6FEBPIiDIsyXmzlY"
    r = requests.get(requestURL)
    jdata = r.json()
    lat = jdata['ad_attr_list'][0]['lat']
    lon = jdata['ad_attr_list'][0]['lon']
    UsherLocation = str(lat) + "," + str(lon)
    EchoLocation = "The Wondry".replace(" ", "+")
    API_KEY = "AIzaSyAJTw_aMHrgAt9uBBIOGoZnAjWtdKu_kVw"
    requestURL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + EchoLocation + "&destinations=" + UsherLocation + "&key=AIzaSyAJTw_aMHrgAt9uBBIOGoZnAjWtdKu_kVw"
    r = requests.get(requestURL)
    jdata = r.json()
    distanceBetween = jdata['rows'][0]['elements'][0]['distance']['text']
    if "ft" in distanceBetween:
        distanceBetween = float(distanceBetween.replace(" ft", "")) * 0.000189393939
    distanceBetween = str(distanceBetween).replace(" mi", "")
    if float(distanceBetween) < .5:
        return True
    else:
        return False

if  __name__ =='__main__':
    print locationVerify()
