# -*-coding:utf-8-*-

"""
文件：非等间隔数据的等高线图绘制的两种实现.py
描述：matplotlib 3.0.3 文档
    1.采用先在规则网格上插值，然后规则网格数据绘图的方式实现
        ir_contour_plot_by_interpolation(fig, ax1, x, y, z, npts)
    2.直接使用tricontour或tricontourf的方式实现
        ir_contour_plot_by_tricontour(fig, ax2, x, y, z, npts)
作者：官方文档人员
编辑：独行的旅人
时间：2019-04-14
"""


import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np


def ir_contour_plot_by_interpolation(fig, ax1, x, y, z, npts):
    """
    绘制非等间隔数据的等高线图
    采用现在规则网格上插值，然后采用传统方式绘制等高线的方法实现
    插值的方式为线性插值
    --------------
    参数:
        fig:画布对象
        ax1:子图对象
        x,y,z:已知点坐标
        npts:已知点个数
    返回值:
        fig, ax1
        将画布和子图对象返回
        
        参数和返回值这样设计是为了符合封闭性原则
    
    使用示例
        # 播下随机数种子
        np.random.seed(19680801)
        npts = 200

        # 生成范围-2到2的随机数，数量为npts
        x = np.random.uniform(-2, 2, npts)
        y = np.random.uniform(-2, 2, npts)
        # 类高斯曲线(正态分布中的一条标准曲线)?
        z = x * np.exp(-x**2 - y**2)

        # 创建画布对象，画布对象中包含2个上下分布的子画布
        fig, (ax1, ax2) = plt.subplots(nrows=2)

        # 调用函数进行绘图
        fig, ax1 = ir_contour_plot_by_interpolation(fig, ax1, x, y, z, npts)

        # 子图间预留的空间高度
        plt.subplots_adjust(hspace=0.5)

        plt.show()
    """

    # 要进行空间插值的网格的分割数, 这两个值不要最好不要超过10000，因为运行会很慢
    # 百的量级和千的量级差异不大
    ngridx = 100
    ngridy = 200

    # 创建网格数据
    xi = np.linspace(-2.1, 2.1, ngridx)
    yi = np.linspace(-2.1, 2.1, ngridy)

    # ********采用模块内的方法插值************
    # 通过(xi, yi)线性插值得到data(x, y)
    # 得到非结构化的三角形网络
    triang = tri.Triangulation(x, y)
    # 在三角形网络上执行线性插值
    interpolator = tri.LinearTriInterpolator(triang, z)
    # 从坐标向量返回坐标矩阵
    Xi, Yi = np.meshgrid(xi, yi)
    # 执行插值
    zi = interpolator(Xi, Yi)
    # *****************************************

    # ********采用外部模块插值(这里提供方法,但该函数不使用该方法)**********
    # 采用scipy.interpolate提供的方法进行插值
    # 
    # from scipy.interpolate import gridata
    # 
    # zi = griddata((x, y), z, (xi[None, :], yi[:, None], method='linear))

    # 绘制等高线并上色
    ax1.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
    cntr1 = ax1.contourf(xi ,yi, zi, levels=14, cmap="RdBu_r")
    fig.colorbar(cntr1, ax=ax1)
    ax1.plot(x, y, 'ko', ms=3)
    # 坐标范围
    ax1.axis((-2, 2, -2, 2))
    ax1.set_title('grid and contour (%d points, %d grid points)' %
              (npts, ngridx * ngridy))

    return fig, ax1


def ir_contour_plot_by_tricontour(fig, ax2, x, y, z, npts):
    """
    绘制非等间隔数据的等高线图
    直接提供非等间距的数据的绘图方式:tricontour
    --------------
    参数:
        fig:画布对象
        ax2:子图对象
        x,y,z:已知点坐标
        npts:已知点个数

    返回值:
        fig, ax1
        将画布和子图对象返回
        
        参数和返回值这样设计是为了符合封闭性原则
    
    使用示例:
        # 播下随机数种子
        np.random.seed(19680801)
        npts = 200

        # 生成范围-2到2的随机数，数量为npts
        x = np.random.uniform(-2, 2, npts)
        y = np.random.uniform(-2, 2, npts)
        # 类高斯曲线(正态分布中的一条标准曲线)?
        z = x * np.exp(-x**2 - y**2)

        # 创建画布对象，画布对象中包含2个上下分布的子画布
        fig, (ax1, ax2) = plt.subplots(nrows=2)

        # 调用函数进行绘图
        fig, ax2 = ir_contour_plot_by_tricontour(fig, ax2, x, y, z, npts)

        # 子图间预留的空间高度
        plt.subplots_adjust(hspace=0.5)

        plt.show()
    """

    ax2.tricontour(x, y,z, levels=14, linewidths=0.5, colors='k')
    cntr2 = ax2.tricontourf(x, y,z, levels=14, cmap="RdBu_r")

    fig.colorbar(cntr2, ax=ax2)
    ax2.plot(x, y, 'ko', ms=3)
    ax2.axis((-2, 2, -2, 2))
    ax2.set_title('tricontour (%d points)' % npts)

    return fig, ax2
    

if __name__ == '__main__':
    # 播下随机数种子
    np.random.seed(19680801)
    npts = 200

    # 生成范围-2到2的随机数，数量为npts
    x = np.random.uniform(-2, 2, npts)
    y = np.random.uniform(-2, 2, npts)
    # 类高斯曲线(正态分布中的一条标准曲线)?
    z = x * np.exp(-x**2 - y**2)

    # 创建画布对象，画布对象中包含2个上下分布的子画布
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    # 调用函数进行绘图
    fig, ax1 = ir_contour_plot_by_interpolation(fig, ax1, x, y, z, npts)
    fig, ax2 = ir_contour_plot_by_tricontour(fig, ax2, x, y, z, npts)

    # 子图间预留的空间高度
    plt.subplots_adjust(hspace=0.5)

    plt.show()





