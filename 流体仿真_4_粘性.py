import math
import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.animation import FuncAnimation #画动图

mplstyle.use('fast')

import time
import copy

#参数
dt=0.01
mu=0.5#动力粘度
rho=1#即每个微团的质量
k_attraction=10#分子间吸引力常数

area=[10,15]#区域长宽
k_area=0.1


F_all=np.array([0,-20])


#流体微团
class Fluidcell:
	def __init__(self,number):
		self.number=number
		self.R=np.array([0,0])
		self.V=np.array([0,0])
		self.F=F_all
		self.Fp=np.array([0,0])
		self.Fv=np.array([0,0])

#---------------------------------牛顿第二定律更新位置
#计算加速度
def get_A(fluidcell):
	A=np.multiply(fluidcell.F+fluidcell.Fp+fluidcell.Fv,[1/rho])
	return A

#计算速度
def renew_V(fluidcell):
	A=get_A(fluidcell)
	V=fluidcell.V+np.multiply(A,[dt])
	fluidcell.V=V

#计算位置
def renew_R(fluidcell):
	for fluidcell in fluidcell_all:
		renew_V(fluidcell)
		R=fluidcell.R+np.multiply(fluidcell.V,[dt])
		fluidcell.R=R


#-----------------------------------计算分布密度得到压强梯度✕直接算分子间作用力合力✓+通过控制作用力实现粘性
def get_FpFv(fluidcell_a,fluidcell_b):
	R=fluidcell_a.R-fluidcell_b.R
	r1=abs(R[0])+abs(R[1])
	r=r1
	fp=0
	if r1<2:
		r=math.sqrt(sum(np.multiply(R,R)))+0.00001
		if r<1:
			#fp=k_attraction*(1/math.pow(r+0.00001,3)-1/(r+0.00001))#排斥为正 当初是你引我而来，现在又是你将我推走
			fp=k_attraction*(1/(r)-1)
			V=fluidcell_a.V-fluidcell_b.V
			a=sum(np.multiply(R,V))
			if a>0:
				fp=fp*mu

	Fp_a=np.multiply(R,[fp/r])
	Fp_b=np.multiply(Fp_a,[-1])

	return Fp_a,Fp_b

def renew_fpfv(fluidcell_all):
	for i in range(len(fluidcell_all)):
		fluidcell_all[i].Fp=0

	for i in range(len(fluidcell_all)):
		for j in range(i+1,len(fluidcell_all)):
			Fp_a,Fp_b=get_FpFv(fluidcell_all[i],fluidcell_all[j])
			fluidcell_all[i].Fp+=Fp_a
			fluidcell_all[j].Fp+=Fp_b
		fluidcell_all[i].Fp=np.multiply(fluidcell_all[i].Fp,[len(fluidcell_all)])



#-----------------------------------画图
'''
def draw(fluidcell_all,area,time):

	plt.clf()
	plt.ion()
	
	plt.xlim((-area[0]*0.2, area[0]*1.2))
	plt.ylim((-area[1]*0.2, area[1]*1.2))
	plt.text(area[0],-area[1]*0.1,str(time),fontsize=5,verticalalignment="top",horizontalalignment="left")
	for fluidcell in fluidcell_all:

		plt.scatter([fluidcell.R[0]],[fluidcell.R[1]],s=100,c=str(0))

	ax = plt.gca()
	ax.set_aspect(1)
	plt.pause(0.01)
	plt.ioff()
'''


#------------------------------------初始化
def ini():
	fluidcell_all=[]
	for i in range(80):
		fluidcell=Fluidcell(i)
		fluidcell.R=np.array([random.random()*area[0],random.random()*area[1]*0.6])
		fluidcell_all.append(copy.deepcopy(fluidcell))
	return fluidcell_all

#------------------------------------区域限制

def in_area(fluidcell_all):
	
	for fluidcell in fluidcell_all:
		
		i=0
		if fluidcell.R[0]<0:
			fluidcell.V[0]=abs(fluidcell.V[0])*k_area
			fluidcell.R[0]=0+0.0001
			i=1
		if fluidcell.R[0]>area[0]:
			fluidcell.V[0]=-abs(fluidcell.V[0])*k_area
			fluidcell.R[0]=area[0]-0.0001
			i=1
		if fluidcell.R[1]<0:
			fluidcell.V[1]=abs(fluidcell.V[1])*k_area
			fluidcell.R[1]=0+0.0001
			i=1
		if fluidcell.R[1]>area[1]:
			fluidcell.V[1]=-abs(fluidcell.V[1])*k_area
			fluidcell.R[1]=area[1]-0.0001
			i=1
		if i==1:
			fluidcell.F=np.array([0,0])
		else:
			fluidcell.F=F_all


#------------------------------------画图及update
def draw(area):

	fig = plt.figure()
	plt.grid(ls='--')
	
	points_ani = plt.plot([],[],'o')[0]
	fps_ani = plt.text(area[0]*0.9,-area[1]*0.1,'',fontsize=10)

	ax = plt.gca()
	ax.set_aspect(1)
	plt.xlim((-area[0]*0.2, area[0]*1.2))
	plt.ylim((-area[1]*0.2, area[1]*1.2))

	def draw_update(frame):
		global gen
		global fluidcell_all
		global time0
		dtime_real=time.time()-time0
		time0=time.time()
		fps=1/dtime_real

		fluidcell_all,gen=main_update(fluidcell_all,gen)
		xdata, ydata = [], []
		for fluidcell in fluidcell_all:

			xdata.append(fluidcell.R[0])
			ydata.append(fluidcell.R[1])

		points_ani.set_data(xdata, ydata)
		fps_ani.set_text(str(round(fps,1)))
		return 1


	ani = FuncAnimation(fig, draw_update, frames=None,interval=0)
	plt.show()


def main_update(fluidcell_all,gen):
	gen+=1
	renew_fpfv(fluidcell_all)
	renew_R(fluidcell_all)
	in_area(fluidcell_all)
	
	return fluidcell_all,gen


#-------------------------------------名存实亡的主函数

if __name__ == '__main__':
	
	fluidcell_all=ini()
	gen=0
	time0=time.time()
	draw(area)

	