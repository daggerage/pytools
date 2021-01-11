"""
将一个一维数组均匀划分，使得每一份的元素之和的最大值最小
DP方法
"""
import numpy as np


def range_close(start=1, end=0):  # 修改循环为闭区间，且下标从1开始，与文章伪代码一致
    return range(start, end + 1)


def partition(W, N, P):
    B = np.zeros((P + 1, N + 1))  # Bottleneck
    for i in range_close(end=N):
        B[1, i] = W[i]
    for p in range_close(2, P):
        j = p - 1
        for i in range_close(p, N - P + p):
            if W[i] - W[j] > B[p - 1, j]:
                while W[i] - W[j] > B[p - 1, j]:
                    j += 1
                if W[i] - W[j - 1] < B[p - 1, j]:
                    j -= 1
                    B[p][i] = W[i] - W[j]
                else:
                    B[p][i] = B[p - 1][j]
            else:
                B[p][i] = B[p - 1][j]
    return B[P][N]


if __name__ == '__main__':
    P = 3  # number of Processors
    weights = [10, 8, 5, 1, 11, 7, 20, 3, 8, 9] # weights of items
    # weights = [10,10,10,10,10,10,10,10,10,10,]
    N = len(weights) # number of items
    W = np.zeros(N + 1) # sum of the first i weights
    for i in range_close(end=N):
        for j in range(i):
            W[i] += weights[j]
    partition(W, N, P)
