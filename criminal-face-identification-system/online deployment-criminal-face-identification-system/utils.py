from encoding import Encode
from recognition import Recognition
import numpy as np
import json
from urllib.request import urlopen
        
        
def encode_folder():
    enc = Encode('./database/missing_persons/')
    enc.names()
    enc.findEncodings()
    enc.save()
    
    
def detect():
    with open('./database/encodings.json') as f:
        data = json.load(f)
        
    eList = []
    cNames = data['classNames']
    for i in range(len(cNames)):
        eList.append(np.array(data['encodeList'][i]))
            
    
    rec = Recognition(eList, cNames)
    status, name = rec.recog()
    return status, name
    
    
def get_coordinates():
    urlopen("http://ipinfo.io/json")
    data = json.load(urlopen("http://ipinfo.io/json"))
    lat = data['loc'].split(',')[0]
    lon = data['loc'].split(',')[1]

    return lat, lon
    
    
    
    
    