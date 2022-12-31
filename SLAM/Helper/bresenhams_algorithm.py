import  numpy as np
from matplotlib import pyplot as plt_
from matplotlib import colors
from matplotlib.colors import ListedColormap


class DrawLine:
    def __init__(self):
        self.plt=plt_
    def draw_matrix(self,rows,colls):
        mat=[]
        for row in range(1,rows+1):
            mat.append([0 for col in range(1,colls+1)])
        return mat

    def bresenhams_algorithm(self,start_x,start_y,end_x,end_y):
        """
        this function draw line between two cells in coordinate word frame
         return the coordiantes of the new cells
        """
        new_coord_holder=[]
        new_coord_holder.append((start_x,start_y))
        if start_x !=end_x and start_y !=end_y:
            new_x,new_y=0,0
            while new_x != end_x and new_y !=end_y:
                delta_x=end_x-start_x
                delta_y=end_y-start_y
                m=delta_y/delta_x # if <1 or not
                P_o=(2*delta_y) - delta_x
                if P_o<0:
                    new_x=start_x+1
                    new_y=start_y
                    P_o+=2*delta_y

                else:
                    new_x = start_x + 1
                    new_y = start_y+1
                    P_o += (2 * delta_y) - (2 * delta_x)

                start_x=new_x
                start_y=new_y

                new_coord_holder.append((new_x,new_y))
            new_coord_holder.append((end_x,end_y))
            return new_coord_holder
        elif start_x == end_x:
            small=min(start_y,end_y)
            big=max(start_y,end_y)
            for dist in range(small,big+1):
                new_coord_holder.append((start_x,dist))
            return new_coord_holder
        elif start_y == end_y:
            small=min(start_x,end_x)
            big=max(start_x,end_x)
            for dist in range(small,big+1):
                new_coord_holder.append((dist,start_y))
            return new_coord_holder




    def fill_matrix_after_bresenhams(self,mat,list_cells:list):
        """

        :param mat: matrix with all 0
        :param list_cells: coord with 1
        :return: new matrix with 0 and 1
        """
        new_mat=mat.copy()
        for y,x in list_cells:
            new_mat[x][y]=1
        return new_mat

    def show_data_in_grid(self,dim,start_x,start_y,end_x,end_y):
        coord = a.bresenhams_algorithm(start_x, start_y, end_x, end_y)
        mat = a.draw_matrix(dim, dim)
        grid_np = a.fill_matrix_after_bresenhams(mat, coord)
        self.plt.pcolor(np.arange(-0.5, dim), np.arange(-0.5, dim), grid_np, cmap=ListedColormap(['white', 'green']))
        self.plt.gca().set_aspect('equal')  # show square as square
        self.plt.xticks(range(dim))
        self.plt.yticks(range(dim))
        self.plt.show()


a=DrawLine()
dim=20
a.show_data_in_grid(dim,1,1,15,10)



