import torch
import torchvision
import numpy as np
flag = torch.cuda.is_available()
print(flag)
'''
device= torch.device("cpu")

GTensor2 = torch.randn(4, 4)
GTensor2=GTensor2.to(device)

for i in range(10000000):
	GTensor1 = torch.randn(4, 4)

	#GTensor1 = torch.as_tensor(Gnp)
	GTensor1=GTensor1.to(device)
	GTensor2=GTensor2+GTensor1
print(GTensor2)
print(GTensor1)


exit()
'''