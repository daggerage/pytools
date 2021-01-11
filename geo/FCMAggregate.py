"""
对FCM生成的多个隶属度图层进行统计，出一个最后分类结果
"""

import geo.GdalBaseOperations as gb
import numpy as np


class AggOp(gb.RasterOperation):
    def op(self, y, x):
        values=np.array([
            i.array[y][x] for i in self.inputs
        ])
        return np.argmax(values)


inputs = [
    "D:/data-arcgis/pargo/fcm/solim/class1.asc",
    "D:/data-arcgis/pargo/fcm/solim/class2.asc",
    "D:/data-arcgis/pargo/fcm/solim/class3.asc",
    "D:/data-arcgis/pargo/fcm/solim/class4.asc",
    "D:/data-arcgis/pargo/fcm/solim/class5.asc",
]
outputPath = "D:/data-arcgis/pargo/fcm/solim/result.tif"

layers = [gb.initByPath(x) for x in inputs]
result = AggOp(layers)
result.run()

result.write(outputPath)
