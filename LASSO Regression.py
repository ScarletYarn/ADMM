#LASSO Regression

import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
#from scipy.interpolate import spline


def PGM(x, alpha, landa, A, b, error):
    k = 0
    print("x的取值的迭代过程：")
    print(x)
    obj = []
    while (1):
        z = x - alpha * landa * np.dot(A.T, np.dot(A, x) - b)
        xx = np.copy(x)
        xx = np.sign(z) * np.maximum(np.linalg.norm(z) - alpha, 0)

        red = np.linalg.norm(
            xx, ord=1) + (alpha / 2) * np.linalg.norm(A @ xx - b)**2
        obj.append(red)
        print('The %dth iteration, target value is %f' % (k, red))

        e = np.linalg.norm(xx - x)
        if e < error:
            break
        else:
            x = np.copy(xx)
            print('The current x is: ', x)
        k += 1
    return xx, k, obj


def ADMM(x, alpha, landa, A, b, error, beta, z):
    k = 0
    print("x的取值的迭代过程：")
    print(x)
    obj = []
    while (1):
        I = np.identity(len(A[0]))
        #print(I)
        #此处的landa是向量
        temp1 = np.linalg.inv(alpha * (A.T @ A) + beta * I)
        #print(temp1)
        temp2 = alpha * (A.T @ b) + beta * z - landa

        xx = temp1 @ temp2
        #print(xx)
        zz = np.copy(z)

        zz = np.sign(xx + landa / beta) * np.maximum(
            np.abs(xx + landa / beta) - 1 / beta, 0)

        landalanda = landa + beta * (xx - zz)

        xzk = np.vstack((x, z))
        xzkp = np.vstack((xx, zz))

        red = np.linalg.norm(
            xx, ord=1) + (alpha / 2) * np.linalg.norm(A @ xx - b)**2
        obj.append(red)
        print('The %dth iteration, target value is %f' % (k, red))

        e = np.linalg.norm(xzk - xzkp)

        if e <= error:
            break
        else:
            x = np.copy(xx)
            z = np.copy(zz)
            landa = np.copy(landalanda)
            print('The current x is: ', x)
        k += 1
    return xx, k, obj


def draw(obj):
    x = np.zeros(len(obj))
    for i in range(len(obj)):
        x[i] = i * 0.1
    '''
    x_new=np.linspace(x.min(),x.max(),300)
    obj_smooth=spline(x,obj,x_new)
    '''
    plt.scatter(x, obj, c='black')
    plt.plot(x, obj, linewidth=1)
    #plt.plot(x_new,obj_smooth,c='red')
    plt.ylabel('obj')
    plt.show()


def main():
    #PGM:
    # x = np.array([[1.]])
    # landa = 0.5
    # alpha = 0.1
    # A = np.array([[1.]])
    # b = np.array([[.2]])
    # error = 0.001
    # xx, count, obj = PGM(x, alpha, landa, A, b, error)
    # print(obj)
    # draw(obj)

    #ADMM
    x = np.reshape(np.array(([1., 1., 1.])), (-1, 1))
    z = np.reshape(np.array(([1., 1., 1.])), (-1, 1))
    landa = np.reshape(np.array(([1., 1., 1.])), (-1, 1))
    A = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
    b = np.reshape(np.array(([2., 2., 2.])), (-1, 1))
    alpha=0.1
    error=0.01
    beta=0.01
    xx,count,obj=ADMM(x,alpha,landa,A,b,error,beta,z)
    draw(obj)
    print("最终迭代结果: x：", xx)
    print("共进行了", count, "次迭代")


main()
