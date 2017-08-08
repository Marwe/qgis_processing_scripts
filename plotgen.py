# based on tutorial 
# https://howtoinqgis.wordpress.com/2016/11/26/how-to-generate-a-vector-grid-of-polygons-in-qgis-using-python/
# TODO
# get line points for corner point and direction from drawn line
# adapt code from chapter 7.4 Writing Custom Map Tools
# http://docs.qgis.org/2.2/pdf/en/QGIS-2.2-PyQGISDeveloperCookbook-en.pdf

##Custom=group
##plotgen=name

##result_name=string plotgen_result
# A bounding vector geometry
#bounding_polygon=vector polygon
#ab_line=vector line
##Grid_extent=extent
#upper_left=vector

# parcel size defs 
##parcel_width=number 12
##parcel_length=number 12

# gaps
##gap_w=number 0
##gap_l=number 2

# number of rows, cols
##num_rows=number 100
##num_cols=number 50


# The vector output
#plot_poly=output vector polygon
#plot_tracks=output vector line


from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface

extent = Grid_extent.split(',')
(xmin, xmax, ymin, ymax) = (float(extent[0]), float(extent[1]), float(extent[2]), float(extent[3]))

hspacing = parcel_width
vspacing = parcel_length

attnames_area=["DATE","TIME","VERSION","ID","NAME","AREA","PERIMETER","SWATHSIN","DIST1","DIST2","PREFWEIGHT"]
attnames_line=["DATE","TIME","VERSION","ID","NAME","LENGTH","DIST1","DIST2","PREFWEIGHT"]

# Create the grid and line layer
crs = iface.mapCanvas().mapSettings().destinationCrs().toWkt()
vector_grid = QgsVectorLayer('Polygon?crs='+ crs, result_name , 'memory')
prov = vector_grid.dataProvider()
vector_lines = QgsVectorLayer('Polygon?crs='+ crs, result_name + '=' , 'memory')
provl = vector_lines.dataProvider()

# Add ids and coordinates fields
fields = QgsFields()
fields.append(QgsField('plotid', QVariant.Int, '', 10, 0))
fields.append(QgsField('rowid', QVariant.Int, '', 10, 0))
fields.append(QgsField('colid', QVariant.Int, '', 10, 0))
for an in attnames_area:
    fields.append(QgsField(an, QVariant.String, '', 100, 0))
prov.addAttributes(fields)

fieldsl = QgsFields()
fieldsl.append(QgsField('trackid', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('lineno', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('ori', QVariant.Int, '', 10, 0))
for an in attnames_line:
    fieldsl.append(QgsField(an, QVariant.String, '', 100, 0))
provl.addAttributes(fields)


# Generate the features for the vector grid
plotid = 0
rowid=0
colid=0
y = ymax
lineystart=ymax+vspacing
lineyend=ymax - vspacing * num_rows - gap_l * num_rows - vspacing
#while y >= ymin:
while colid<num_cols:
    colid+=1
    x = xmin
    rowid=0
#    while x <= xmax:
    while rowid <= num_rows:
        rowid+=1
        point1 = QgsPoint(x, y)
        point2 = QgsPoint(x + hspacing, y)
        point3 = QgsPoint(x + hspacing, y - vspacing)
        point4 = QgsPoint(x, y - vspacing)
        vertices = [point1, point2, point3, point4] # Vertices of the polygon for the current id
        inAttr = [plotid, rowid, colid]
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry().fromPolygon([vertices])) # Set geometry for the current id
        feat.setAttributes(inAttr) # Set attributes for the current id
        prov.addFeatures([feat])
        lpoint1 = QgsPoint(x+hspacing/2, lineystart)
        lpoint2 = QgsPoint(x+hspacing/2, lineyend)
        lvertices = [lpoint1, lpoint2]
        lfeat = QgsFeature()
        lfeat.setGeometry(QgsGeometry().fromPolyline([lvertices])) # Set geometry for the current id
        lfeat.setAttributes(inAttr) # Set attributes for the current id
        provl.addFeatures([lfeat])
        x = x + hspacing + gap_w
        plotid += 1
    y = y - vspacing - gap_l

# Update fields for the vector grid
vector_grid.updateFields()
vector_lines.updateFields()

# Add the layer to the Layers panel
QgsMapLayerRegistry.instance().addMapLayers([vector_grid])
QgsMapLayerRegistry.instance().addMapLayers([vector_lines])
