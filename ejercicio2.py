import pandas as pd
import random
from math import sqrt
import psutil,time
def get_resource_info(code_to_measure):
    resources_save_data = get_resource_usage(code_to_measure=code_to_measure)
    print(f"Tiempo de CPU: {resources_save_data['tiempo_cpu']} segundos")
    print(f"Uso de memoria virtual: {resources_save_data['memoria_virtual']} MB")
    print(f"Uso de memoria residente: {resources_save_data['memoria_residente']} MB")
    print(f"Porcentaje de uso de CPU: {resources_save_data['%_cpu']} %")

# Función que devuelve el tiempo de CPU y el uso de memoria para un código dado
def get_resource_usage(code_to_measure):
    process = psutil.Process()
    #get cpu status before running the code
    cpu_percent = psutil.cpu_percent()
    start_time = time.time()
    code_to_measure()
    end_time = time.time()
    end_cpu_percent = psutil.cpu_percent() 
    cpu_percent = end_cpu_percent - cpu_percent
    cpu_percent = cpu_percent / psutil.cpu_count()
    
    return {
        'tiempo_cpu': end_time - start_time,
        'memoria_virtual': process.memory_info().vms / (1024 * 1024),  # Convertir a MB
        'memoria_residente': process.memory_info().rss / (1024 * 1024),  # Convertir a MB
        '%_cpu': cpu_percent # Porcentaje de uso de CPU
    }

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
    prev_data = dataFrame[(dataFrame["PersID"] == id) & (dataFrame["Frame"] == frame - 1)]
    prev_x = prev_data["X"].iloc[0]
    prev_y = prev_data["Y"].iloc[0]
    distancia = calcular_distancia(row["X"],prev_x,row["Y"],prev_y)
    return distancia/0.04

def main():
    dataFrame["Velocidad"] = dataFrame[["PersID","Frame","X","Y"]].apply(calcular_velocidad,axis=1)
get_resource_info(main)
dataFrame.to_csv("dataframe-with-velocity.txt",sep="\t",index=False)