#cart_all_weeks_sediment.py
#produces a cartogram for all weeks of Albert's sediment data
#written by Greg Fiske Apr 2014
#rewrite of cart_all_weeks.py from discharge cartogram
#expects and input shapefile with weekly sediment attribute data prepared by the weekly_sum_sediment_April_14_2014.R script

#make sure input shapefile is in the same projection as the extra featureclasses

import arcpy, os
arcpy.OverwriteOutput = True
#import the custom toolbox
arcpy.ImportToolbox("C:\\ArcGIS\\Cartograms\\Cartogram.tbx", "Cartograms")


# Set Geoprocessing environments
arcpy.env.scratchWorkspace = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb"
arcpy.env.workspace = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb"
input_wspace = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\"
output_wspace = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb\\output1\\"
cntry_fc = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb\\cntry05"
image_fc = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb\\hyp_50m_sr_w"
image_fc2 = "\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\vector\\cartogram_output.gdb\\hyp_hr_sr_w_no_land"

#build a list of weeks
weeklist = range(1,53)
#weeklist = [1]


try:

    for i in weeklist:
        myWeek = "week" + str(i)
        myWeek = myWeek.replace("\"", "")
        arcpy.MakeFeatureLayer_management (input_wspace + "watersheds_rob.shp", "mylyr")
        arcpy.SelectLayerByAttribute_management("mylyr", "NEW_SELECTION", "\"" + myWeek + "\" >= 0")
        # run cartogram tool. Choose one line or the other depending on desired background
        ##arcpy.Cartogram_Cartograms("mylyr",myWeek,output_wspace + myWeek,"FID","AREA_CALC","1","512","true", cntry_fc + " cntry_" + myWeek,"true")
        ##arcpy.Cartogram_Cartograms("mylyr",myWeek,output_wspace + myWeek,"FID","AREA_CALC","1","512","true", image_fc + " img_" + str(i) + ";" + image_fc2 + " img2_" + str(i), "true")
        arcpy.Cartogram_Cartograms("mylyr",myWeek,output_wspace + myWeek,"FID","AREA_CALC","1","512","true", image_fc + " img_" + str(i), "true")
        arcpy.Delete_management("mylyr")

except Exception,msg:
    err = arcpy.GetMessages(2)
    arcpy.AddError(err)
    #print msg

