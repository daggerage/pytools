import scripts.GdalBaseOperations as gb
import numpy as np

inputPath = r"D:\data-arcgis\pargo\idw\idw_bounding_mask_100m.tif"
outputPath = r"D:\data-arcgis\pargo\idw\idw_bounding_mask_100m_expand.tif"

dataset = gb.initByPath(inputPath)
dataset.expandNoData(0, 1, 0, 1)
# dataset.test()
dataset.write(outputPath)
