import pandas as pd
dataFrame = pd.read_csv("NombreEdadPtos.txt",sep="\t")
def calcular_nota(puntaje):
  if 0<=puntaje<=60:
    return 0.05 * puntaje + 1
  elif 60<puntaje<=100:
    return 0.075 * puntaje - 0.5
  
dataFrame["Nota"] = dataFrame["Puntuación"].apply(calcular_nota)
print(dataFrame)

filtroNotas = dataFrame["Nota"]>5.5
filtroNombre = dataFrame["Nombre"].str.lower().str.contains("r")
dataFrameFiltrado = dataFrame[filtroNotas & filtroNombre]
print(dataFrameFiltrado)

dataFrameOrdenado = dataFrame.sort_values(by=["Nota"],ascending=False)
print(dataFrameOrdenado)