import numpy as np

t=     [[1,2,3],
        [4,5,6],
        ]

t_2=[[1,2],
     [4,5],
     [7,8]]
test_1=np.array(t)
test_2=np.array(t_2)
# multiplication matrices
res=np.matmul(test_1,test_2)
res_2=np.matmul(test_2,test_1)
print(res)
print(res_2)

#identiti matrix n*n
idenity_=np.identity(4)
print(idenity_)

#inverse
a=[[1,2],
   [2,2]]
b=[[1,-2],
   [-2,2]]

a=[[1, 2 ,1],
[4 ,4 ,5],
[6 ,7, 7]]
b=[[-7 ,-7, 6],
[2, 1, -1],
[4 ,5, -4]]
aa=np.array(a)
bb=np.array(b)

res_1=np.multiply(aa,bb)
res_2=np.multiply(bb,aa)
print(res_1)
print(res_2)

########### linear equation
print('linear')
"""
2x1 + 3x2 + 5x3 = 1
4x1 􀀀 2x2 􀀀 7x3 = 8
9x1 + 5x2 􀀀 3x3 = 2
"""
a=[[2, 3, 5],
[4, -2, -7],
[9 ,5, -3]]

x=[[1],
   [8],
   [2]]
a=[     [1, 0 ,8, -4],
        [0 ,1, 2, 12]]
x=[[42],[8]]
aa=np.array(a)
xx=np.array(x)

f=np.multiply(xx[0],aa[:,0])
e=np.multiply(xx[1],aa[:,1])
#h=np.multiply(xx[2],aa[:,2])
print(f)
print(e)
# print(h)
res=f+e
print(np.transpose(res))
# div=np.matmul(xx,aa)
# print(div)

