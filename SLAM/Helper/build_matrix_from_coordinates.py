

class WorldMatrix:
    def __init__(self,dim):
        self.matrix=[]
        self.dim=dim

    def print_matrix(self):
        """
        print the matrix ordently

        :param matrix:
        :return:
        """
        for a in range(len(self.matrix)):
            print(self.matrix[a])

    def create_empty_matrix_worldframe(self):
        """
        build empty matrix, with 0
        x=col, y=row
        :param dim: size of the world from -dim durch 0 to +dim
        :return:
        """
        word_dim=(self.dim*2)+1
        for y in range(word_dim):
            self.matrix.append([0]*(word_dim))
        return self.matrix


    def mark_cells(self,x,y,value):
        """
        mark the cells with given coordinates, with given 'name'
        :param x: act x
        :param y: act y
        :param value: what kind of value
        :return: nothing
        """
        mid=len(self.matrix)//2
        col = mid + x
        row = mid - y
        if not 0<=row<len(self.matrix):
            print(f"Y:{y} not in range of our world!!")
            return
        if not 0<= col < len(self.matrix[row]):
            print(f"X:{x} not in range of our world!!")
            return
        self.matrix[row][col]=value






h=WorldMatrix(2)
res=h.create_empty_matrix_worldframe()
h.mark_cells(-2,-2,1)
h.mark_cells(2,2,1)
h.mark_cells(-2,2,1)
h.mark_cells(2,-2,1)
h.mark_cells(0,0,1)
h.print_matrix()

