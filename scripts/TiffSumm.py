from osgeo import gdal
import numpy as np
import sys
from scipy import stats

"""
This script is to make a summary of a tiff image, especially to find the peculiar(s).

usage:
python NoDataCount.py <tiff file path>
"""


def largest_indices(ary, n):
    """Returns the n largest indices from a numpy array. (src: Internet.)"""
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, ary.shape)


def RasterSummary(filename):
    np.set_printoptions(threshold=np.inf)
    dataset = gdal.Open(filename)
    cols=dataset.RasterXSize
    rows=dataset.RasterYSize

    band = dataset.GetRasterBand(1)

    arr=band.ReadAsArray(0, 0, cols, rows)
    print(filename)
    print(rows,'x',cols)
    print('avg:',np.mean(arr))
    mode=stats.mode(arr.reshape(-1))
    print('mode:',mode.mode[0],'[*',mode.count[0],'times]')
    print('median:',np.median(arr))
    for i in range(1,5):
        print(str(i*20)+'% percentile',np.percentile(arr, i*20))
    print('99.999% percentile',np.percentile(arr, 99.999))
    k=10
    index=largest_indices(arr,k)
    for i in range(k):
        x=index[0][i]
        y=index[1][i]
        print('%dth largest at (%d,%d)-> %f' % (i+1,x,y,arr[x][y]))

    del dataset


if __name__=='__main__':
    RasterSummary(sys.argv[1])
