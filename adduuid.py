# Customize this starter script by adding code
# to the run_script function. See the Help for
# complete information on how to create a script
# and use Script Runner.


##LTZ=group
##adduuid=name

##vector_layer=vector 

""" add a uuid attribute """

# Some commonly used imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from uuid import uuid4

print(vector_layer)
print(type(vector_layer))
#QMessageBox.information(None, "Vector layer", vector_layer)
lyrs=self.iface.legendInterface().layers()

uuid_exists=False
for c in f.fields().toList():
    print(c.name())
    if "uuid" == c.name():
        uuid_exists=True
        QMessageBox.information(None, "Attribute uuid exists", "leaving unchanged")
    else:
        QMessageBox.information(None, "Attribute uuid does not exist", "adding")





#root = QgsProject.instance().layerTreeRoot()
#lyr = root.findLayer(vector_layer)
#print(lyr)


#def run_script(iface):
    #lyrl=QgsMapLayerRegistry.instance().mapLayers()

#iter = lyr.getFeatures()
#for feature in iter:
    ## fetch attributes
    #attrs = feature.attributes()
    ## attrs is a list. It contains all the attribute values of this feature
    #print attrs
  
#lyr=QgsVectorLayer('/media/martin/data700/martin/ltz-data/maxau-data/Hofgut_Maxau/gisdaten2018/grids/mx18_s16_soil.shp','addauuidhere','ogr') 
#lf=lyr.getFeatures()
#for c in f.fields().toList():
#    print(c.name())
# lp=lyr.dataProvider()
# lp.addAttributes([QgsField("uuid",QVariant.String)])
# lp.changeAttributeValues({1: uuid.uuid4()})
# lyr.updateFields()
# QgsFileWriter.writeAsVectorFormat(lyr,'out_uuid.shp',"utf-8",None,"ESRI Shapefile")

