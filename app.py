import os
import topojson as tp
import geopandas as gpd
from os import listdir
from os.path import isfile, join

#get all original file names from ./originals
onlyfiles = [f for f in listdir('originals') if isfile(join('originals', f))]

#set simplify and quantize tolerance values
SIMPLIFY_TOLERANCE = .005
QUANTIZE_TOLERANCE = 1e10

#loop through files to simplify each
for f in onlyfiles:
    #read file
    path = gpd.read_file('./originals/'+f)

    #read og file size
    oldsz=os.stat('./originals/'+f).st_size
    print('\n\n#####################################\n'+f+'\n#####################################\n')
    print('ORGINAL SIZE:' + str(oldsz))

    #prepare topology of file and simplify
    r = tp.Topology(
    data=path, 
    topology=True,
    toposimplify=SIMPLIFY_TOLERANCE,
    ).topoquantize(QUANTIZE_TOLERANCE)

    #declare new file path of simplified topojson
    NEW_FILE_PATH = "simps/s" + str(SIMPLIFY_TOLERANCE).replace(".", "_") + "q" + str(QUANTIZE_TOLERANCE).replace(".", "_") + "-" + f
    
    #write simplified topojson to file in ./simps directory
    r.to_json(NEW_FILE_PATH)

    #read new file size
    newsz=os.stat(NEW_FILE_PATH).st_size
    print('NEW SIZE:' + str(newsz))

    #print percent reduction of new topojson in size bytes
    print("% OF ORIGNAL SIZE: " + str(newsz/oldsz))
