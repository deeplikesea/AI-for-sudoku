import numpy as np
import copy as cp
import time

class sudoku_solution(object):
    def __init__(self, sd):
        row = []
        col = []
        for i in range(9):
            for j in range(9):
                if sd[i][j] == 0:
                    row.append(i)
                    col.append(j)
        #first, we need to find all empty positions and mark them
        self.row = row
        self.col = col
        self.sd = sd

    def order(self):# this function just help you accelerate your speed, just shrink the search tree, you can ignore it.
        small_sudoku = [[],[],[], [],[],[], [],[],[]]
        for n in range(9):
            for m in range(9):
                small_n = (m//3) + (n//3)*3
                small_m = (m%3) + (n%3)*3
                small_sudoku[n].append(self.sd[small_n][small_m])
        #seond, we find 9 small sudokus to constrain available elements
        sdt = np.transpose(self.sd) # sd transpose
        weight_value = []
        for i in range(len(self.row)):
            count = 0
            for val in [1,2,3,4,5,6,7,8,9]:
                if (val not in self.sd[self.row[i]]) and (val not in sdt[self.col[i]]) and (val not in small_sudoku[(self.row[i]//3)*3 + (self.col[i]//3)]):
                    count += 1
            weight_value.append(count)
        order_row = []
        order_col = []
        for i in range(min(weight_value),max(weight_value)+1):
            for n in range(len(self.row)):
                if weight_value[n] == i:
                    order_row.append(self.row[n])
                    order_col.append(self.col[n])
        self.row = order_row
        self.col = order_col

    def available(self, i):# find the available digits for the current empty box.
        small_sudoku = [[],[],[], [],[],[], [],[],[]]
        for n in range(9):
            for m in range(9):
                small_n = (m//3) + (n//3)*3
                small_m = (m%3) + (n%3)*3
                small_sudoku[n].append(self.sd[small_n][small_m])
        #seond, we find 9 small sudokus to constrain available elements
        sdt = np.transpose(self.sd) # sd transpose
        available = []
        for val in [1,2,3,4,5,6,7,8,9]:
            if (val not in self.sd[self.row[i]]) and (val not in sdt[self.col[i]]) and (val not in small_sudoku[(self.row[i]//3)*3 + (self.col[i]//3)]):
                available.append(val)
        #print(i)
        #print(self.sd[self.row[i]])
        #print(sdt[self.col[i]])
        #print(small_sudoku[(self.row[i]//3)*3 + (self.col[i]//3)])
        #print(available)
        return available
        # judge if elements are qualified before taking


    def fill(self, list):# fill the current state to check if it's right.
        count = 0
        for i in range(len(list)):
            if list[i] != 0:
                count += 1
            self.sd[self.row[i]][self.col[i]] = list[i]
        #print(count)
        #print(list)
        #print(self.sd)
        return count # how many elements it fill in

    def depth_search(self):
        self.order()#you know you can ignore this functioin,it's all right to delete this. 
        visited = 0
        L = []# L is to store states.
        space = 0

        exist = [0 for i in range(len(self.row))]# it will help us reset soduku back to original state if it's already calculated
        L.append(exist)
        while True:
            if space < len(L):
                space = len(L)
            if len(L) != 0:
                exist = L[-1]
                i = self.fill(exist)
                if i == len(self.row):
                    break
            else:
                print("This sudoku is wrong.")
                break
            # judge the current situation
            choice = self.available(i)
            # find available value for the next
            L.pop()
            visited += 1
            if len(choice) == 0:
                #print(L)
                continue

            for val in choice:
                exist[i] = val
                #print(exist)
                L.append(cp.deepcopy(exist))
        return self.sd, visited, space
#visited is a value to display how many nodes we've visited during the whole process
#space is a value to display how many memory we used but keep in mind, here the unit is a sudoku

    def breadth_search(self):
        self.order()
        visited = 0
        L = []
        space = 0

        exist = [0 for i in range(len(self.row))]
        L.append(exist)
        while True:
            if space < len(L):
                space = len(L)
            if len(L) != 0:
                exist = L[0]
                i = self.fill(exist)
                if i == len(self.row):
                    break
            else:
                print("This sudoku is wrong.")
                break
            # judge the current situation
            choice = self.available(i)
            # find available value for the next
            L.pop(0)
            visited += 1
            if len(choice) == 0:
                #print(L)
                continue

            for val in choice:
                exist[i] = val
                #print(exist)
                L.append(cp.deepcopy(exist))
        return self.sd, visited, space

    def iterative_deepening(self):
        self.order()
        temp = []
        j = 1
        space = 0

        while j <= len(self.row):
            count = 0
            L = []
            exist = [0 for i in range(j)]
            L.append(exist)
            while True:
                if space < len(L):
                    space = len(L)
                if len(L) != 0:
                    exist = L[-1]
                    i = self.fill(exist)
                    if i == len(self.row):
                        break
                else:
                    if j == len(self.row):
                        print("This sudoku is wrong.")
                        break
                    else:
                        break
                # judge the current situation
                choice = self.available(i)
                # find available value for the next
                L.pop()
                count += 1
                if len(choice) == 0:
                    #print(L)
                    continue
                for val in choice:
                    exist[i] = val
                    #print(exist)
                    L.append(cp.deepcopy(exist))
            temp.append(count)
            j += 1
        visited = 0
        for val in temp:
            visited += val
        return self.sd, visited, space

'''
sd = [[5,3,0, 0,7,0, 0,0,0],
      [6,0,0, 1,9,5, 0,0,0],
      [0,9,8, 0,0,0, 0,6,0],
      [8,0,0, 0,6,0, 0,0,3],
      [4,0,0, 8,0,3, 0,0,1],
      [7,0,0, 0,2,0, 0,0,6],
      [0,6,0, 0,0,0, 2,8,0],
      [0,0,0, 4,1,9, 0,0,5],
      [0,0,0, 0,8,0, 0,7,9]]

[5, 3, 4, 6, 7, 8, 9, 1, 2]
[6, 7, 2, 1, 9, 5, 3, 4, 8]
[1, 9, 8, 3, 4, 2, 5, 6, 7]
[8, 5, 9, 7, 6, 1, 4, 2, 3]
[4, 2, 6, 8, 5, 3, 7, 9, 1]
[7, 1, 3, 9, 2, 4, 8, 5, 6]
[9, 6, 1, 5, 3, 7, 2, 8, 4]
[2, 8, 7, 4, 1, 9, 6, 3, 5]
[3, 4, 5, 2, 8, 6, 1, 7, 9]
'''

sd_diff = [[4,0,0, 0,0,0, 0,7,5],
           [0,3,0, 0,0,0, 1,6,0],
           [0,0,0, 0,0,2, 0,0,0],
           [0,0,3, 7,0,0, 8,0,0],
           [0,0,0, 1,0,8, 0,2,0],
           [0,0,0, 0,3,0, 0,0,0],
           [0,0,0, 9,0,0, 7,1,4],
           [1,0,0, 0,0,6, 0,9,0],
           [0,4,9, 0,0,3, 0,0,0]]

if __name__ == '__main__':
#below is what we trying to test the speed of each algorithms
    sudoku = sudoku_solution(sd_diff)
    begin = time.clock()
    result, visited, space = sudoku.depth_search()
    end = time.clock()
    print("Execution Time in seconds for depth_first:",end-begin)
    print(visited)
    print(space)
    for i in range(9):
        print(result[i])
    print("----------------------")

    begin = time.clock()
    result, visited, space = sudoku.breadth_search()
    end = time.clock()
    print("Execution Time in seconds for breadth_first:",end-begin)
    print(visited)
    print(space)
    for i in range(9):
        print(result[i])
    print("----------------------")

    begin = time.clock()
    result, visited, space = sudoku.iterative_deepening()
    end = time.clock()
    print("Execution Time in seconds for iterative_deepening:",end-begin)
    print(visited)
    print(space)
    for i in range(9):
        print(result[i])
