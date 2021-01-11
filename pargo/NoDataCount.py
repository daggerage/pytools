"""
输入栅格进行分片，对每片的NoData栅格计数
用于pargo文章对比不同划分方式
"""

from osgeo import gdal
import numpy as np
import sys
from scipy import stats


def divRow(rows, div):
    result = [1]
    for i in range(1,div + 1):
        result.append(i * (rows // div))
    return result


def RasterSummary(filename):
    np.set_printoptions(threshold=np.inf)
    dataset = gdal.Open(filename)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    band = dataset.GetRasterBand(1)

    arr = band.ReadAsArray(0, 0, cols, rows)
    print(filename)
    print(rows, '*', cols)
    # print('avg:',np.mean(arr))
    # mode=stats.mode(arr.reshape(-1))
    # print('mode:',mode.mode[0],'[*',mode.count[0],'times]')
    # print('median:',np.median(arr))
    # for i in range(1,5):
    #     print(str(i*20)+'% percentile',np.percentile(arr, i*20))
    # print('99.999% percentile',np.percentile(arr, 99.999))
    # k=10
    # index=largest_indices(arr,k)
    # for i in range(k):
    #     x=index[0][i]
    #     y=index[1][i]
    #     print('%dth largest at (%d,%d)-> %f' % (i+1,x,y,arr[x][y]))

    div = 72

    # 等面积划分
    divs_area = divRow(rows, div)

    # equal-quantity策略
    divs_quantity = [
        1,
        1001,
        1501,
        1841,
        2051,
        2221,
        2381,
        2541,
        2701,
        2871,
        3031,
        3191,
        3341,
        3491,
        3621,
        3751,
        3881,
        4011,
        4131,
        4251,
        4361,
        4461,
        4561,
        4661,
        4761,
        4861,
        4961,
        5061,
        5161,
        5261,
        5361,
        5461,
        5561,
        5661,
        5761,
        5861,
        5961,
        6061,
        6161,
        6261,
        6361,
        6461,
        6561,
        6661,
        6771,
        6871,
        6971,
        7071,
        7171,
        7281,
        7391,
        7501,
        7611,
        7721,
        7831,
        7941,
        8051,
        8161,
        8271,
        8391,
        8511,
        8641,
        8771,
        8911,
        9061,
        9231,
        9411,
        9591,
        9771,
        9961,
        10161,
        10391,
        11128
    ]

    #所提出的策略
    divs_balance=[
        1,
        731,
        1181,
        1561,
        1851,
        2051,
        2221,
        2381,
        2541,
        2691,
        2861,
        3021,
        3181,
        3331,
        3481,
        3611,
        3741,
        3871,
        4001,
        4131,
        4251,
        4361,
        4471,
        4581,
        4681,
        4781,
        4881,
        4981,
        5081,
        5181,
        5281,
        5381,
        5481,
        5581,
        5681,
        5781,
        5881,
        5981,
        6091,
        6201,
        6301,
        6401,
        6501,
        6601,
        6711,
        6821,
        6931,
        7041,
        7151,
        7261,
        7371,
        7481,
        7591,
        7701,
        7811,
        7931,
        8051,
        8171,
        8291,
        8411,
        8541,
        8671,
        8811,
        8951,
        9111,
        9281,
        9461,
        9641,
        9831,
        10021,
        10231,
        10491,
        11128
    ]

    divs=divs_balance

    for i in range(len(divs) - 1):
        start = divs[i]
        end = divs[i + 1] - 1
        print('row %i-%i' % (start, end))
        invalid = np.sum(arr[start:end] == -9999)
        valid = (end - start) * cols - invalid

        # for row in range(start, end):
        #     for col in range(cols):
        #         if arr[row][col] == -9999:
        #             invalid += 1
        #         else:
        #             valid += 1
        print('valid: %i' % valid)
        print('invalid: %i' % invalid)
        print()
    del dataset


if __name__ == '__main__':
    RasterSummary(sys.argv[1])
