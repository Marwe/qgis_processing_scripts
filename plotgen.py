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
##parcel_width=number 1.5
##parcel_length=number 6

# gaps
##gap_w=number 0
##gap_l=number 2

# number of rows, cols
##num_rows=number 10
##num_cols=number 20


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
vector_lines = QgsVectorLayer('LineString?crs='+ crs, result_name + '=' , 'memory')
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
for an in attnames_line:
    fieldsl.append(QgsField(an, QVariant.String, '', 100, 0))
provl.addAttributes(fields)


# Generate the features for the vector grid
plotid = 0
# recompute ymin for the final geom
ymin = ymax - (vspacing+gap_l)*num_rows
lineystart = ymin - vspacing
lineyend   = ymin + vspacing * num_rows + vspacing + gap_l * num_rows 
linexstart = xmin - hspacing
linexend   = xmin + hspacing * num_cols + hspacing + gap_w * num_cols
for colid in range(num_cols):
    x = xmin + (hspacing + gap_w)*colid
    for rowid in range(num_rows):
        y = ymin + (vspacing + gap_l)*rowid
        plotid += 1
        point1 = QgsPoint(x, y)
        point2 = QgsPoint(x + hspacing, y)
        point3 = QgsPoint(x + hspacing, y + vspacing)
        point4 = QgsPoint(x, y + vspacing)
        inAttr = [plotid, rowid, colid]
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry().fromPolygon([[point1, point2, point3, point4]])) # Set geometry for the current id
        feat.setAttributes(inAttr) # Set attributes for the current id
        prov.addFeatures([feat])
    # generate the line features 
    lpoint1 = QgsPoint(x + hspacing/2, lineystart)
    lpoint2 = QgsPoint(x + hspacing/2, lineyend)
    lfeat = QgsFeature()
    lfeat.setGeometry(QgsGeometry().fromPolyline([lpoint1, lpoint2])) # Set line geometry for the current id
    lfeat.setAttributes(inAttr) # Set attributes for the current id
    inAttr = [colid]
    provl.addFeatures([lfeat])


# Update fields for the vector
vector_grid.updateFields()
vector_lines.updateFields()

# Add the layer to the Layers panel
QgsMapLayerRegistry.instance().addMapLayers([vector_grid])
QgsMapLayerRegistry.instance().addMapLayers([vector_lines])
