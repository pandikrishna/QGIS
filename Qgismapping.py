##Points=group
##Mapa_de_rendimiento=vector
##Rendimiento=field Mapa_de_rendimiento

#limite_abajo= string 
#limite_arriba= string 

from qgis.utils import *
from qgis.core import *
from PyQt4.QtCore import * 
import numpy as np


vector = processing.getObject(Mapa_de_rendimiento)
var = []
iter = vector.getFeatures()
 
#adicion de valores de columna a lista y conversion de lista a array 
for feature in iter:
    idx = vector.fieldNameIndex(str(Rendimiento))
    var.append(feature.attributes()[idx])
var2 = np.asarray([float(i) for i in var])

#Primer metodo de limpieza
xmin = np.percentile(var2, 0)
q1 = np.percentile(var2, 25)
q2 = np.percentile(var2, 50)
q3 = np.percentile(var2, 75)
xmax = np.percentile(var2, 100)
intervalo_intercuartil = q3-q1
limite_abajo = q1-(intervalo_intercuartil)
limite_arriba = q3+(intervalo_intercuartil)

"""
#2do metodo de limpieza
promedio = np.mean(var2) 
desvest = np.std(var2) 
limite_abajo2 = promedio - (3* desvest) 
limite_arriba2 = promedio + (3* desvest) 
"""


expresion = str(Rendimiento +'<'+str(limite_abajo) or Rendimiento +'>'+str(limite_arriba))
#expresion2 = str(Rendimiento +'<'+str(limite_abajo2) and Rendimiento +'>'+str(limite_arriba2))
expr = QgsExpression(expresion)
#expr = QgsExpression(expresion and expresion2)
it =vector.getFeatures(QgsFeatureRequest(expr))
ids = [i.id() for i in it]
vector.setSelectedFeatures(ids)
