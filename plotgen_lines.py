# based on tutorial 
# https://howtoinqgis.wordpress.com/2016/11/26/how-to-generate-a-vector-grid-of-polygons-in-qgis-using-python/
# TODO
# get line points for corner point and direction from drawn line
# adapt code from chapter 7.4 Writing Custom Map Tools
# http://docs.qgis.org/2.2/pdf/en/QGIS-2.2-PyQGISDeveloperCookbook-en.pdf

##LTZ=group
##plotgen_lines=name

##result_name=string plotgen_lines
# A bounding vector geometry
#bounding_polygon=vector polygon
#ab_line=vector line
#Grid_extent=extent
#upper_left=vector point extent.center()


# parcel size defs 
##parcel_width=number 1.5
##parcel_length=number 6

# gaps
##gap_w=number 0
##gap_l=number 2

# number of rows, cols
##num_rows=number 10
##num_cols=number 20

##add_brutto_parcels=boolean

#map_unit=number iface.mapCanvas().mapUnits()

# The vector output
#plot_poly=output vector polygon
#plot_tracks=output vector line


from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface
import uuid

#if add_brutto_parcels is True:
#    # check for gaps
#    if !((gap_w > 0) || (gap_l > 0)):
#        # no gaps, brutto==netto
#        add_brutto_parcels=False

#extent = Grid_extent.split(',')
#(xmin, xmax, ymin, ymax) = (float(extent[0]), float(extent[1]), float(extent[2]), float(extent[3]))
(xmin,ymax)=iface.mapCanvas().extent().center()

hspacing = parcel_width
vspacing = parcel_length

attnames_area=["DATE","TIME","VERSION","ID","NAME","AREA","PERIMETER","SWATHSIN","DIST1","DIST2","PREFWEIGHT"]
attnames_line=["DATE","TIME","VERSION","ID","NAME","LENGTH","DIST1","DIST2","PREFWEIGHT"]
attnames_all =["DATE","TIME","VERSION","ID","NAME","LENGTH","AREA","PERIMETER","SWATHSIN","DIST1","DIST2","PREFWEIGHT"]


# Create the grid and line layer
crs = iface.mapCanvas().mapSettings().destinationCrs().toWkt()

#vector_grid = QgsVectorLayer('Polygon?crs='+ crs, result_name , 'memory')
#prov = vector_grid.dataProvider()
vector_lines = QgsVectorLayer('LineString?crs='+ crs, result_name , 'memory')
provl = vector_lines.dataProvider()

# Add ids and coordinates fields
#fields = QgsFields()
#fields.append(QgsField('plotid', QVariant.Int, '', 10, 0))
# # fields.append(QgsField('trackid', QVariant.Int, '', 10, 0))
#fields.append(QgsField('rowid', QVariant.Int, '', 10, 0))
#fields.append(QgsField('colid', QVariant.Int, '', 10, 0))
#fields.append(QgsField('uuid4', QVariant.String, '', 36, 0))
#for an in attnames_area:
#for an in attnames_all:
#    fields.append(QgsField(an, QVariant.String, '', 100, 0))
#prov.addAttributes(fields)

# add all possible attributes
fieldsl = QgsFields()
fieldsl.append(QgsField('plotid', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('trackid', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('rowid', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('colid', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('gtype', QVariant.Int, '', 10, 0))
fieldsl.append(QgsField('uuid4', QVariant.String, '', 36, 0))
for an in attnames_all:
    fieldsl.append(QgsField(an, QVariant.String, '', 100, 0))
provl.addAttributes(fieldsl)


# Generate the features for the vector grid, now lines
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
        inAttr = [plotid, -1, rowid, colid, 'netto', str(uuid.uuid4())]
        feat = QgsFeature()
        #feat.setGeometry(QgsGeometry().fromPolygon([[point1, point2, point3, point4]])) # Set geometry for the current id
        feat.setGeometry(QgsGeometry().fromPolyline([point1, point2, point3, point4, point1])) # Set geometry for the current id
        feat.setAttributes(inAttr) # Set attributes for the current id
        # prov.addFeatures([feat])
        # add to the line layer
        provl.addFeatures([feat])
        if add_brutto_parcels:
            xb=x-gap_w/2
            yb=y-gap_l/2
            point1 = QgsPoint(xb,yb)
            point2 = QgsPoint(xb + hspacing + gap_w, yb)
            point3 = QgsPoint(xb + hspacing + gap_w, yb + vspacing + gap_l)
            point4 = QgsPoint(xb, yb + vspacing + gap_l)
            inAttr = [plotid, -1, rowid, colid, 'brutto', str(uuid.uuid4())]
            feat = QgsFeature()
            #feat.setGeometry(QgsGeometry().fromPolygon([[point1, point2, point3, point4]])) # Set geometry for the current id
            feat.setGeometry(QgsGeometry().fromPolyline([point1, point2, point3, point4, point1])) # Set geometry for the current id
            feat.setAttributes(inAttr) # Set attributes for the current id
            provl.addFeatures([feat])
        
            
    # generate the line features 
    lpoint1 = QgsPoint(x + hspacing/2, lineystart)
    lpoint2 = QgsPoint(x + hspacing/2, lineyend)
    lfeat = QgsFeature()
    lfeat.setGeometry(QgsGeometry().fromPolyline([lpoint1, lpoint2])) # Set line geometry for the current id
    inAttr = [ -1, colid, -1, colid, str(uuid.uuid4()) ]
    lfeat.setAttributes(inAttr) # Set attributes for the current id
    provl.addFeatures([lfeat])
    # add to the common line vector layer
    # disabled for lines only
    #prov.addFeatures([lfeat])

# Update fields for the vector
#vector_grid.updateFields()
vector_lines.updateFields()

# Add the layer to the Layers panel
#QgsMapLayerRegistry.instance().addMapLayers([vector_grid])
QgsMapLayerRegistry.instance().addMapLayers([vector_lines])
