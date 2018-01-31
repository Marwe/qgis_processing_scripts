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
root = QgsProject.instance().layerTreeRoot()
lyr = root.findLayer(apoly)
print(lyr)

def run_script(iface):
    lyrl=QgsMapLayerRegistry.instance().mapLayers()

iter = lyr.getFeatures()
for feature in iter:
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    print attrs

    
