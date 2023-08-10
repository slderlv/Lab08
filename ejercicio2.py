import pandas as pd
import random
from math import sqrt

file = pd.read_csv("UNI_CORR_500_01.txt",skiprows=3,sep="\t")
dataFrame = file.rename(columns={
  "# PersID": "PersID",
})
randomNum = random.randint(dataFrame["PersID"].min(),dataFrame["PersID"].max())
# print(randomNum)
randomFrames = dataFrame[dataFrame["PersID"]==randomNum]
# print(randomFrames)
dataFrameOrdenado = dataFrame.sort_values(by=["PersID","Frame"])

def calcular_distancia(x2,x1,y2,y1):
  return sqrt((x2-x1)**2+(y2-y1)**2)

def calcular_velocidad(row):
  id = int(row["PersID"])
  frame = int(row["Frame"])
  if dataFrame[dataFrame["PersID"]==id]["Frame"].min()==frame:
    return 0
  prev_data = dataFrame[dataFrame["Frame"]==frame-1]
  prev_x = prev_data["X"].iloc[0]
  prev_y = prev_data["Y"].iloc[0]
  distancia = calcular_distancia(row["X"],prev_x,row["Y"],prev_y)
  
  return distancia/0.04
  
dataFrame["Velocidad"] = dataFrame[["PersID","Frame","X","Y"]].apply(calcular_velocidad,axis=1)
dataFrame.to_csv("dataframe-with-velocity.txt",sep="\t",index=False)