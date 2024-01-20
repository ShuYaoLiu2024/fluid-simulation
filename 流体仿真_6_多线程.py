import math
import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.animation import FuncAnimation #画动图

mplstyle.use('fast')

from threading import Thread #多线程

import time
import copy

#参数
dt=0.01
mu=0.5#粘度
rho=1#即每个微团的质量
k_attraction=1000#分子间吸引力常数

area=[10,15]#区域长宽
k_area=0.1

thread_number=40

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
		self.contral=0
		self.incontral=0

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
	Fp_a=0
	Fp_b=0
	if fluidcell_b.contral==0:
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
	elif fluidcell_b.incontral==1:
		if r1<4:
			r=math.sqrt(sum(np.multiply(R,R)))+0.00001
			if r<2:
				
				
				fp=k_attraction*(2/(r)-1)

				V=fluidcell_a.V-fluidcell_b.V
				a=sum(np.multiply(R,V))
				if a>0:
					fp=fp*mu
	

		Fp_a=np.multiply(R,[fp/r])
		Fp_b=0

	return Fp_a,Fp_b

def renew_fpfv_one(fluidcell_all,tasks_one):

	'''
	if fluidcell_all[-1].incontral==0:
		fluidcell_all_1=fluidcell_all[0:-1]

	else:
		fluidcell_all_1=fluidcell_all
	
	for i in range(len(fluidcell_all_1)):
		fluidcell_all_1[i].Fp=0
	
	for i in range(len(fluidcell_all_1)):
		for j in range(i+1,len(fluidcell_all_1)):
			Fp_a,Fp_b=get_FpFv(fluidcell_all_1[i],fluidcell_all_1[j])
			fluidcell_all_1[i].Fp+=Fp_a
			fluidcell_all_1[j].Fp+=Fp_b
		#fluidcell_all_1[i].Fp=np.multiply(fluidcell_all_1[i].Fp,[len(fluidcell_all_1)])什么东西
	'''
	for task in tasks_one:
		Fp_a,Fp_b=get_FpFv(fluidcell_all[task[0]],fluidcell_all[task[1]])
		fluidcell_all[task[0]].Fp.append(Fp_a)
		fluidcell_all[task[1]].Fp.append(Fp_b)

	


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
	for i in range(1000):
		fluidcell=Fluidcell(i)
		fluidcell.R=np.array([random.random()*area[0],random.random()*area[1]*0.6])
		fluidcell_all.append(copy.deepcopy(fluidcell))
	#交互
	fluidcell=Fluidcell(i+1)
	fluidcell.contral=1
	fluidcell.F=np.array([0,0])
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
			if fluidcell.contral==0:
				fluidcell.F=F_all

#------------------------------------多线程
def thread_manage_ini(fluidcell_all_len):
	tasks=[]
	thread_plan=[]
	for i in range(fluidcell_all_len):
		for j in range(i+1,fluidcell_all_len):
			tasks.append([i,j])
	a=math.floor(len(tasks)/thread_number)#向下取整
	
	tasks_one=[]
	for i in range(len(tasks)):
		
		if i%a==0:
			thread_plan.append(copy.deepcopy(tasks_one) )
			tasks_one=[]
		tasks_one.append(copy.deepcopy(tasks[i]))
	thread_plan=thread_plan[1:]
	thread_plan.append(copy.deepcopy(tasks_one))

	return thread_plan

def thread_manage(fluidcell_all,thread_plan):
	for i in range(len(fluidcell_all)):
		fluidcell_all[i].Fp=[]

	threads=[]
	for i in range(thread_number):
		thread_one=Thread(target=renew_fpfv_one, args=(fluidcell_all,thread_plan[i]))
		threads.append(thread_one)
	for i in range(thread_number):
		threads[i].start()
	for i in range(thread_number):
		threads[i].join()

	for i in range(len(fluidcell_all)):
		fluidcell_all[i].Fp=sum(fluidcell_all[i].Fp)
		

#------------------------------------画图及update
def draw(area):

	fig = plt.figure(dpi=100)
	plt.grid(ls='--')
	
	points_ani = plt.plot([],[],'o')[0]
	ctrl_ani = plt.plot([],[],'o',20,color="pink",markersize=20)[0]
	fps_ani = plt.text(area[0]*0.9,-area[1]*0.1,'',fontsize=10)

	ax = plt.gca()
	ax.set_aspect(1)
	plt.xlim((-area[0]*0.2, area[0]*1.2))
	plt.ylim((-area[1]*0.2, area[1]*1.2))

	def draw_update(frame):
		global gen
		global fluidcell_all
		global time0
		global thread_plan
		dtime_real=time.time()-time0
		time0=time.time()
		fps=1/dtime_real
		
		

		fluidcell_all,gen=main_update(fluidcell_all,gen,thread_plan)

		

		xdata, ydata = [], []
		for fluidcell in fluidcell_all[:-1]:

			xdata.append(fluidcell.R[0])
			ydata.append(fluidcell.R[1])

		points_ani.set_data(xdata, ydata)

		


		if fluidcell_all[-1].incontral==1:
			ctrl_ani.set_data([fluidcell_all[-1].R[0]], [fluidcell_all[-1].R[1]])
			ctrl_ani.set_visible(True)
		else:
			ctrl_ani.set_visible(False)
		fps_ani.set_text(str(round(fps,1)))
		return 1

	

	#交互
	def mouse_move(event):
		global Mouse_Down
		global fluidcell_all
		if Mouse_Down==1:
			fluidcell_all[-1].incontral=1
			fluidcell_all[-1].R=np.array([event.xdata,event.ydata])
		else:

			fluidcell_all[-1].incontral=0

	def mouse_down(event):
		global Mouse_Down
		Mouse_Down=1
	def mouse_up(event):
		global Mouse_Down
		Mouse_Down=0

	fig.canvas.mpl_connect('motion_notify_event', mouse_move)
	fig.canvas.mpl_connect('button_press_event', mouse_down)
	fig.canvas.mpl_connect('button_release_event', mouse_up)


	ani = FuncAnimation(fig, draw_update, frames=None,interval=0)
	plt.show()


def main_update(fluidcell_all,gen,thread_plan):
	gen+=1

	thread_manage(fluidcell_all,thread_plan)
	renew_R(fluidcell_all)
	in_area(fluidcell_all)
	
	return fluidcell_all,gen


#-------------------------------------名存实亡的主函数

if __name__ == '__main__':
	
	fluidcell_all=ini()
	thread_plan=thread_manage_ini(len(fluidcell_all))
	gen=0
	time0=time.time()
	Mouse_Down=0
	draw(area)

	