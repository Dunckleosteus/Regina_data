import pandas as pd
from shapely.geometry import LineString
import shapely.wkt
import geopandas 
import os 
import matplotlib.pyplot as plt
import pyproj
import glob


#name = os.path.join("N3495D03_Export.TXT")
for name in glob.glob("/home/d/Ginger/mission/Strassbourg/Regina_data/INPUT/*"):
    df = pd.read_csv(name, encoding = "iso8859_15", sep = "\t")
    for i in range (0, len(df.columns)):
        print(f"{str(i)} => {df.columns[i]}")
    #print (df.WGS_LAT_ST)
    df["geometry"] = LineString([[0, 0], [0, 0]])# initialize a default geometry field 

    for field in [df.columns[103], df.columns[104], df.columns[105], df.columns[106]]:
        df[field] = df[field].str.replace(",", ".")
        df[field] = df[field].astype(float)

    for row in range(0, len(df.index)):
        df.at[row, "geometry"] = LineString([[df.at[row, "WGS_LON_ST"], df.at[row, "WGS_LAT_ST"]], [df.at[row, "WGS_LON_EN"], df.at[row, "WGS_LAT_EN"]]])

    output = geopandas.GeoDataFrame(df, geometry = df["geometry"])
    output.set_crs('epsg:4326', allow_override=True, inplace = True)

    output.to_file(("/home/d/Ginger/mission/Strassbourg/Regina_data/OUTPUT/"+ name[-20:-4]+".shp"))