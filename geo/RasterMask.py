import geo.GdalBaseOperations as gb

thres = [
    [280, 360],
    [290, 360],
    [300, 360],
    [310, 360],
]
maskOutputs = [
    "D:/data-arcgis/pargo/fcm/with_mask/dem_nenjiang_10-%s-%sm.tif" % (thres[i][0], thres[i][1])
    for i in range(len(thres))
]
maskees = [
    r"D:\data-arcgis\pargo\fcm\normalized\slp_1.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\plan_1.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\prof_1.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\twi_1.tif",
]
maskees10 = [
    r"D:\data-arcgis\pargo\fcm\normalized\slp_10.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\plan_10.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\prof_10.tif",
    r"D:\data-arcgis\pargo\fcm\normalized\twi_10.tif",
]
maskeeOutputs = [
    r"D:\data-arcgis\pargo\fcm\with_mask\slp1.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\prof1.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\plan1.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\twi1.tif",
]
maskee10Outputs = [
    r"D:\data-arcgis\pargo\fcm\with_mask\slp10.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\prof10.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\plan10.tif",
    r"D:\data-arcgis\pargo\fcm\with_mask\twi10.tif",
]
for i in range(len(thres)):
    mask = gb.initByPath(r"D:\data-arcgis\pargo\fcm\dem_nenjiang_10.tif")
    mask.valueMask(thres[i][0], thres[i][1], False)
    mask.write(maskOutputs[i])

    maskee = gb.initByPath(maskees10[i])
    maskee.datasetMask(mask)
    # maskee.rectangularMask((i * maskee.Y // len(thres), 0), ((i + 1) * maskee.Y // len(thres), maskee.X))
    maskee.write(maskee10Outputs[i])
