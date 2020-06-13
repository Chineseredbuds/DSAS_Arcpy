# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 
# Created on: 2018-10-10 13:49:21.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import glob

router=os.getcwd()
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 
# Created on: 2018-10-10 13:49:21.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import glob

router=os.getcwd()
# Create a Filegdb for the fds
arcpy.CreateFileGDB_management(router, "DSAS_Analysis.gdb")
years=list();


#idnum=0;
for root, dirs, files in os.walk(router):
	for filename in files:
		#idnum=idnum+1;
		if os.path.splitext(filename)[1] == '.shp':
			input_shp=os.path.join(root, filename)


			DSAS_gdb = router+"\\DSAS_Analysis.gdb"
			#FCName='fc'+os.path.splitext(filename)[0]
			file_year=os.path.splitext(filename)[0]
			#print file_year;
			FCName='fc'+file_year
			wholeYear='01/01/'+file_year;
			years.append(wholeYear)
			#ID.append(idnum)


			#define project
			#out_shp=router+'\\p'+filename   
			#outCS = arcpy.SpatialReference('WGS 1984 UTM Zone 49N')
			#arcpy.Project_management(input_shp, out_shp,outCS)

			#shpfile2featureclass

			arcpy.FeatureClassToFeatureClass_conversion(input_shp, DSAS_gdb,FCName)

Field_names=['OBJECTID','SHAPE','SHAPE_LENGTH','DATE_','UNCERTAINTY'];
Data_type=['Object ID','Geometry','DOUBLE','TEXT','FLOAT'];

if __name__=='__main__':    
	arcpy.env.workspace=DSAS_gdb
	#delet redundant field
	fcs = arcpy.ListFeatureClasses()#

	for fc in fcs:
		inFeatures=fc
		fieldObjList = arcpy.ListFields(inFeatures)
		for field in fieldObjList:
			if not field.required:
				for sField in Field_names:
					if field.name == sField:
						break;
					else:
						if sField == 'UNCERTAINTY':
							arcpy.DeleteField_management(inFeatures, field.name)
						else:
							continue;
		#add require fields
		for i in range(3,5):
			for field in fieldObjList:
				#if not field.required:
				if Field_names[i] == field.name:
					break
				else:
					if field.name == fieldObjList[-1].name:
						arcpy.AddField_management(inFeatures,Field_names[i], Data_type[i])
					else:
						continue																				

	try:
		Target = "analysisresults"
		template=fcs[0]
		# Execute CreateFeaturedataset
		arcpy.CreateFeatureclass_management(DSAS_gdb, Target,template,outCS)
		# Process: Append the feature classes into the empty feature class
		arcpy.Append_management(fcs,Target)
		
	except:
		# If an error occurred while running a tool print the messages
		print arcpy.GetMessages()
					
					
	# Create a feature class 

	# Set local variables
	outLocation = DSAS_gdb
	emptyFC = "shoreline"
	try:
		arcpy.env.workspace=DSAS_gdb
		# All polygon FCs in the workspace

		fcList = arcpy.ListFeatureClasses("","POLYLINE")


		arcpy.Merge_management(fcList, outLocation + os.sep + emptyFC)
		#arcpy.Delete_management(fcList)

	except:
		# If an error occurred while running a tool print the messages
		print arcpy.GetMessages()
	try:

		cursor = arcpy.UpdateCursor(outLocation + os.sep + emptyFC)
		filenum=0;
		for row in cursor:
			row.setValue("DATE_",years[filenum])
			row.setValue("UNCERTAINTY",0)
			cursor.updateRow(row)
			filenum=filenum+1
		for fc in fcList:
			arcpy.Delete_management(fc,"FeatureClass")
		print 'Finish!'
		
	except:
		# If an error occurred while running a tool print the messages
		print arcpy.GetMessages()
