from numpy import *
import numpy as np
from math import *


class bCurveRec():
    def __init__(self,q):
        '''
        :param q: 采样点，为n*3的矩阵
        '''
        self.q=q#q为数据点，n*3的矩阵


    def controlPoint(self):
        '''
        该方法是根据采样点反求控制顶点
        :return: 控制顶点
        '''
        count=self.q.shape[0]#数据点的个数
        u=list([0]*count)#对数据点参数化之后的节点序列，令其初始值全为0
        u[count-1]=1
        chordlength=list([0]*(count-1))
        sum=0
        for i in range(count-1):
            chordlength[i]=sqrt(pow(self.q[i,0]-self.q[i+1,0],2)+pow(self.q[i,1]-self.q[i+1,1],2)+pow(self.q[i,2]-self.q[i+1,2],2))#两相邻数据点的距离
            sum+=chordlength[i]#距离之和
            pass
        for i in range(1,count-1):
            u[i]=u[i-1]+sqrt(pow(self.q[i,0]-self.q[i+1,0],2)+pow(self.q[i,1]-self.q[i+1,1],2)+pow(self.q[i,2]-self.q[i+1,2],2))/sum#积累弦长参数法
            pass
        nodeu=list([0]*(count+4))#节点矢量
        nodeu[count:count+4]=[1,1,1,1]#3次b样条曲线，节点矢量前四个为0，后四个为1
        for i in range(4,count):
            nodeu[i]=(u[i-1]+u[i-2]+u[i-3])/3#见计算机辅助几何设计304页


        coeff_matrix=np.zeros((count,count))#系数矩阵，求控制顶点
        for i in range(1,count-1):
            coeff_matrix[i,i-1]=1
            coeff_matrix[i,i]=4
            coeff_matrix[i,i+1]=1
            pass
        coeff_matrix[0,0]=-1
        coeff_matrix[0,1]=1
        coeff_matrix[count-1,count-2]=1
        coeff_matrix[count-1,count-1] =-1


        e=np.zeros((count,3))
        e[0,:]=[0,0,0]
        e[count-1,:]=[0,0,0]
        e[1:count-1,:]=self.q[1:count-1,:]
        d=6*np.dot(np.linalg.inv(coeff_matrix),e)#控制顶点，数目和数据点一样，n*3的矩阵
        return d


    def cNodeSeq(self):
        '''
         反求出控制顶点后，接下来要正求拟合曲线，首先对控制节点参数化，然后利用德布尔算法递推出B样条曲线上的点
        :return: 控制顶点节点序列
        '''
        count = self.q.shape[0]
        contu = list([0] * (count + 4))  # 控制节点的节点矢量
        contu[count:count + 4] = [1, 1, 1, 1]
        controlLength = list([0] * (count - 1))
        sum2 = 0
        d=self.controlPoint()
        for i in range(count - 1):
            controlLength[i] = sqrt(
                pow(d[i, 0] - d[i + 1, 0], 2) + pow(d[i, 1] - d[i + 1, 1], 2) + pow(d[i, 2] - d[i + 1, 2], 2))
            sum2 += controlLength[i]
        contu[4] = (controlLength[0] + controlLength[1]) / sum2
        for i in range(5, count):
            contu[i] = contu[i - 1] + controlLength[i - 3] / sum2
        return contu


    def deBoorDv(self,d,nodeSequence,i,u_i,l):
        '''
        该方法是输入一个u,0<u<1,利用德布尔算法求其三维坐标值，直接调用输入参数较多，请使用uTo3Dimen方法
        :param d: 控制顶点
        :param nodeSequence:控制顶点节点序列
        :param i: u在节点序列中区间较小值
        :param u_i: 0,1之间的值
        :param l: 迭代次数,初始值为3
        :return:返回三维坐标值
        '''
        k=3
        if l==0:
            return d[i,:]
        temp=nodeSequence[i+k+1]-nodeSequence[i+l]
        if temp==0:
            return 0
        else:
            temp2=(u_i-nodeSequence[i+l])/temp
            temp3=(1-temp2)*self.deBoorDv(d,nodeSequence,i,u_i,l-1)+temp2*self.deBoorDv(d,nodeSequence,i+1,u_i,l-1)
            return temp3


    def findspan(self,count,k,u_i,nodeSequence):
        '''
        该方法是找一个u在控制顶点节点序列中的区间，取区间较小值
        :param count: 节点序列长度
        :param k: B样条次数
        :param u_i: 0到1之间的参数值
        :param nodeSequence: 控制顶点节点序列
        :return: 区间坐标较小值
        '''
        if u_i==nodeSequence[count+1]:
            return count
        low=k
        high=count
        mid=(low+high)//2
        while u_i<nodeSequence[mid] or u_i>nodeSequence[mid+1]:
            if u_i<nodeSequence[mid]:
                high=mid
            else:
                low=mid
            mid=(low+high)//2
        return mid


    def uTo3Dimen(self,u_i):
        '''
        使用该方法返回三维坐标值
        :param u_i: 0到1之间的参数值
        :return: u对应的三维坐标值
        '''
        temp=self.deBoorDv(self.controlPoint(),self.cNodeSeq(),self.findspan(self.q.shape[0],3,u_i,self.cNodeSeq())-3,u_i,3)
        return temp


q=np.array([[1,1,1],[2,3,2],[3,4,3],[4,4,4],[5,3,5],[6,2,6],[7,0,7]])
a=bCurveRec(q)
print(a.uTo3Dimen(0.5))


