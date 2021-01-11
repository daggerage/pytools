from typing import List

import geo.GdalBaseOperations as gb
import os.path


class SegmentalSum(gb.RasterOperation):
    def __init__(self, layers: List[gb.RasterLayer]):
        super().__init__(layers)
        self.segs = [
            0, 500, 2500, 5000, 8000, 15000
        ]
        self.resultList = [0 for i in range(len(self.segs))]

    def op(self, row, col):
        v = self.inputs[0].array[row][col]
        for i in range(1, 2):
            # for i in range(len(self.segs) - 1):
            if self.segs[i] <= v <= self.segs[i + 1]:
                self.resultList[i] += v
                print("(%i,%i):%f" % (row, col, v))


inputs = [
    "../data/test.tif",
]

for x in inputs:
    if not os.path.isfile(x):
        print("file does not exist:", x)
        exit()
layers = [gb.initByPath(x) for x in inputs]
result = SegmentalSum(layers)
result.run()
# for item in result.resultList:
#     print("%s\n" % item)
