import numpy as np


def input_information ():
         row = int(input("Enter the number of rows:")) 
         column = int(input("Enter the number of columns:")) 
         print("Enter the entries in a single line (separated by space) for Input 1: ")
         entries = []
         entries = map(int, raw_input().split())
         matrix_x = np.array(entries).reshape(row, column)
         print("Enter the entries in a single line (separated by space) for Input 2: ")
         entries = map(int, raw_input().split())
         matrix_y = np.array(entries).reshape(row, column)
         print (matrix_x)
         print ("\n")
         print (matrix_y)
         print ("\n")
         return matrix_x, matrix_y ,row ,column
       

def input_single_matrix ():
         row = int(input("Enter the number of rows:")) 
         column = int(input("Enter the number of columns:")) 
         print("Enter the entries in a single line (separated by space) for Input 1: ")
         entries = []
         entries = map(int, raw_input().split())
         matrix_x = np.array(entries).reshape(row, column)
         return matrix_x ,row ,column


def transpose(matrix_x,row ,column ):
    for i in range (0 , row):
        for j  in range (i+1 ,column):
            matrix_x[i][j], matrix_x[j][i] = matrix_x[j][i], matrix_x[i][j] 
    print (matrix_x) 

def rotate(matrix_x,row ,column):
    lista = []
    if ( row == column):
      for j  in range (0, column ):
          for i in range (row-1 , -1, -1):
             lista.append(matrix_x[i][j])
      matrix_x = np.array(lista).reshape(row, column)
    #for i in range ( 0 , len(lista) , row ):
         #listb.append(lista[i:i+row])
    return matrix_x
          
   
if __name__ == '__main__':
   while True:
      operation =  raw_input("Enter the operation to be done")
      if (operation == "break"):
         break
      if ( operation == "Add"):  
         matrix_x, matrix_y, row ,column = input_information()
         print (np.add(matrix_x,matrix_y))
      if ( operation == "Sub"):  
         matrix_x, matrix_y, row ,column  = input_information()
         print (np.subtract(matrix_x,matrix_y))
      if ( operation == "Mul"):  
         matrix_x, matrix_y, row ,column  = input_information()
         print (np.multiply(matrix_x,matrix_y))
      if ( operation == "Div"):  
         matrix_x, matrix_y, row ,column  = input_information()
         print (np.divide(matrix_x,matrix_y))
      if ( operation == "pose"):  
         matrix_x, row ,column  = input_single_matrix()
         print (transpose(matrix_x,row ,column ))
      if ( operation == "rotate"):  
         matrix_x, row ,column = input_single_matrix()
         print (rotate(matrix_x))    
         


 
