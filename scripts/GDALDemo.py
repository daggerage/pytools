from osgeo import gdal
import numpy as np
from functools import reduce


def RasterProcess():
    file = "D:/arcgis-data/pargo/idw_load_space_300m_72c.tif"
    out = "D:/arcgis-data/pargo/idw_load_space_300m_72c_change.tif"

    np.set_printoptions(threshold=np.inf)  # 使print大量数据不用符号...代替而显示所有

    dataset = gdal.Open(file)

    print(dataset.GetDescription())  # 数据描述
    print(dataset.RasterCount)  # 波段数

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    band = dataset.GetRasterBand(1)

    driver = gdal.GetDriverByName("GTiff")
    datasetOut = driver.CreateCopy(out, dataset)
    srcArray = band.ReadAsArray(0, 0, cols, rows)

    for i in range(rows):
        if 200 < i < 300:
            srcArray[i][200:500] = 0.1
    datasetOut.WriteRaster(0, 0, cols, rows, srcArray.tostring(), cols, rows)

    del dataset

class A:
    def __init__(self):
        self.z=1

if __name__ == '__main__':
    a=A()
    print(a.z)
    # RasterProcess()
