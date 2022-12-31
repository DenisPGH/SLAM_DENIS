
import numpy as np
# T=transponirane, change row to col , and back

t=     [[1,2,3],
        [4,5,6],
        [7,8,9]]

test_2=np.ones((3,3))

test_1=np.array(t)
transpose_=np.transpose(test_1)
#print(transpose_)
#print(test_2+test_1)
multiply_matrix=np.multiply(test_1,test_2) # po index umnojava
matrix_product=np.matmul(test_1, test_2) # umnojava no proizvodna
#print(multiply_matrix) # multi
#print(matrix_product)
determinate=np.linalg.det(test_1)
#print(determinate)
print('HERE')
print(test_1.dot(test_2))
print('HERE')
################################### EKF #############################
# 2n+3
points=[[0,1],[0,2]]
x_0,y_0,theta_0=0,0,0
size_dimensions= len(points) * 2 + 3
m_0=np.zeros((1, size_dimensions))
#print(m_0)
m_0_transpose=np.transpose(m_0)
#print(m_0_transpose)
E_0=np.zeros((size_dimensions, size_dimensions))
#print(E_0)

x_pred,y_pred,theta_pred= 0, 1, 0 # otiwa 1cm po (0,1)
prediction_step=[0,1,0]



F_x=np.zeros((3,size_dimensions))
#print(nz_ko_e)
F_x[0][0]=1
F_x[1][1]=1
F_x[2][2]=1
F_x_transpose=F_x.T
print(F_x_transpose)

#m_0_transpose_update=m_0_transpose+(np.multiply(nz_ko_e_transpose*prediction_step))
#funk_g=m_0_transpose+(nz_ko_e_transpose*prediction_step)
g=m_0_transpose+ np.multiply(F_x_transpose,prediction_step) # small g funk
print(g)
## step 1
m_t=g


