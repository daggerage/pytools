from abc import abstractmethod

from osgeo import gdal
import numpy as np
import re
from typing import List
import copy


class RasterLayer:
    def __init__(self, dataset):
        self.dataset: 'gdal.Dataset' = dataset
        self.cols = dataset.RasterXSize
        self.rows = dataset.RasterYSize
        self.array = dataset.GetRasterBand(1).ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize)
        self.noData = dataset.GetRasterBand(1).GetNoDataValue()
        self.path = ''

    def __del__(self):
        del self.dataset


    def write(self, path):
        datasetOut = gdal.GetDriverByName("GTiff").CreateCopy(path, self.dataset)
        datasetOut.GetRasterBand(1).WriteArray(self.array)

    def valueMask(self, low, high, isSetNull):
        a = self.array
        if isSetNull:
            self.array = np.where((a > low) & (a < high), self.noData, a)
        else:
            self.array = np.where((a > low) & (a < high), a, self.noData)

    def datasetMask(self, mask: 'RasterLayer'):
        self.array[mask.array == mask.noData] = self.noData

    def rectangularMask(self, leftTop, rightDown):
        self.array[leftTop[0]:rightDown[0]][leftTop[1]:rightDown[1]] = self.noData

    def clearLayer(self):
        self.array = np.full((self.rows, self.cols), self.noData)

    def expandNoData(self, up, down, left, right):
        for i in range(down):
            self.array = np.insert(arr=self.array, obj=self.rows, values=[self.noData for i in range(self.cols)], axis=0)
            self.rows += down
        for i in range(up):
            self.array = np.insert(arr=self.array, obj=0, values=[self.noData for i in range(self.cols)], axis=0)
            self.rows += up
        for i in range(right):
            self.array = np.insert(arr=self.array, obj=self.cols, values=[self.noData for i in range(self.rows)], axis=1)
            self.rows += right
        for i in range(left):
            self.array = np.insert(arr=self.array, obj=0, values=[self.noData for i in range(self.rows)], axis=1)
            self.rows += left
        self.dataset.SetMetadata()

    def iterate(self, op):
        for row in range(self.rows):
            for col in range(self.cols):
                self.array[row][col] = op(row, col)

    def createNoDataCopy(self) -> 'RasterLayer':
        dataset = gdal.GetDriverByName("GTiff").CreateCopy(self.path, self.dataset)
        cp = RasterLayer(dataset)
        cp.clearLayer()
        return cp



def initByPath(inputFile):
    dataset = gdal.Open(inputFile)
    g = RasterLayer(dataset)
    g.path = inputFile
    return g


class RasterOperation:
    def __init__(self, layers: List[RasterLayer]):
        self.inputs = layers
        self.outputArray = copy.deepcopy(self.inputs[0].array)
        self.cols = self.inputs[0].cols
        self.rows = self.inputs[0].rows

    def run(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.outputArray[row][col] = self.op(row, col)

    def write(self, path):
        driver = gdal.GetDriverByName("GTiff")
        ds = driver.Create(path, self.cols, self.rows, 1, gdal.GDT_Float64)
        ds.SetProjection(self.inputs[0].dataset.GetProjection())
        ds.SetGeoTransform(self.inputs[0].dataset.GetGeoTransform())
        ds.GetRasterBand(1).SetNoDataValue(self.inputs[0].noData)
        ds.GetRasterBand(1).WriteArray(self.outputArray)
        del ds

    @abstractmethod
    def op(self, row, col):
        pass
