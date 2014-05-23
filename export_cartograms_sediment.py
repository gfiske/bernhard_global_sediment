#export_cartograms_sediment.py
#written by Greg Fiske July 2012
#rewritten in Apr 2014 for use with the sediment cartogram animation
#references an MXD map, exports the map to a jpg, changes the layer data link to the next cartogram in a list, exports again
#written to export the weekly discharge cartogram maps

#note: this script doesn't work with the input replaceDataSources in a Feature Dataset.  I've had to copy them to their own FGD.  Not sure why.

import arcpy, os
arcpy.OverwriteOutput = True


#reference basemap
mxdPath = '\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\week_automation_sediment.mxd'
mxd = arcpy.mapping.MapDocument(mxdPath)
#df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#list the cartogram vectors
arcpy.env.workspace = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output1.gdb"
fcs = arcpy.ListFeatureClasses("*", "Polygon")
for i in fcs:
    if not "cntry" in i:
        for lyr in arcpy.mapping.ListLayers(mxd, "*"):
            #update each layer with weekly cartogram
            if lyr.name.lower() == "watersheds":
                lyr.replaceDataSource("\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output1.gdb", "FILEGDB_WORKSPACE", i, True)
                lyr.symbology.valueField = i
            ##if lyr.name.lower() == "cntry":
            ##    lyr.replaceDataSource("c:\\Data\\Global\\CarbonRivers\\Cartograms\\vector\\test2.gdb", "FILEGDB_WORKSPACE", "cntry_" + i, True)
            if lyr.name.lower() == "img":
                i2 = i.replace("week", "")
                lyr.replaceDataSource("\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output1.gdb", "FILEGDB_WORKSPACE", "img_" + i2, True)
            #refresh map
            ##arcpy.RefreshActiveView()
            #export to jpg
            arcpy.mapping.ExportToJPEG(mxd, "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\images\\by_week\\" + i + ".jpg", resolution = 150, color_mode = "24-BIT_TRUE_COLOR", jpeg_quality = 100)
            ##arcpy.mapping.ExportToPNG(mxd, "C:\\Data\\Global\\CarbonRivers\\Cartograms\\images\\by_week\\" + i + ".png", resolution = 150, color_mode = "24-BIT_TRUE_COLOR")
            ##arcpy.mapping.ExportToAI(mxd, "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\images\\by_week\\" + i + ".ai")
            ##arcpy.mapping.ExportToTIFF(mxd, "C:\\Data\\Global\\CarbonRivers\\Cartograms\\images\\by_week\\" + i + ".tif", resolution = 150, color_mode = "24-BIT_TRUE_COLOR", tiff_compression = "NONE")



del mxd
