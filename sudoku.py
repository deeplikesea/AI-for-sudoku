import numpy as np
import copy as cp
import queue

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

    def available(self, i):
        small_sudoku = [[],[],[], [],[],[], [],[],[]]
        for n in range(9):
            for m in range(9):
                small_n = (m//3) + (n//3)*3
                small_m = (m%3) + (n%3)*3
                small_sudoku[n].append(sd[small_n][small_m])
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


    def fill(self, list):
        count = 0
        for i in range(len(list)):
            if list[i] != 0:
                count += 1
            self.sd[self.row[i]][self.col[i]] = list[i]
            i += 1
        #print(count)
        #print(list)
        #print(self.sd)
        return count # how many elements it fill in

    def depth_search(self):
        L = []
        exist = [0 for i in range(len(self.row))]
        L.append(exist)
        while True:
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
            if len(choice) == 0:
                #print(L)
                continue

            for val in choice:
                exist[i] = val
                #print(exist)
                L.append(cp.deepcopy(exist))
        return self.sd

    def breadth_search(self):
        L = queue.Queue()
        exist = [0 for i in range(len(self.row))]
        L.put(exist)
        while True:
            if L.empty() == False:
                exist = L.get()
                i = self.fill(exist)
                if i == len(self.row):
                    break
            else:
                print("This sudoku is wrong.")
                break
            # judge the current situation
            choice = self.available(i)
            # find available value for the next
            if len(choice) == 0:
                #print(L)
                continue

            for val in choice:
                exist[i] = val
                #print(exist)
                L.put(cp.deepcopy(exist))
            #print(L)
        return self.sd

    def iterative_deepening(self):
        j = 1
        while j <= len(self.row):
            L = []
            exist = [0 for i in range(j)]
            L.append(exist)
            while True:
                if len(L) != 0:
                    exist = L[-1]
                    i = self.fill(exist)
                    if i == j:
                        break
                else:
                    print("This sudoku is wrong.")
                    break
                # judge the current situation
                choice = self.available(i)
                # find available value for the next
                L.pop()
                if len(choice) == 0:
                    #print(L)
                    continue
                for val in choice:
                    exist[i] = val
                    #print(exist)
                    L.append(cp.deepcopy(exist))
            j += 1
        return self.sd
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

sd_diff = [[0,0,5, 3,0,0, 0,0,0],
           [8,0,0, 0,0,0, 0,2,0],
           [0,7,0, 0,1,0, 5,0,0],
           [4,0,0, 0,0,5, 3,0,0],
           [0,1,0, 0,7,0, 0,0,6],
           [0,0,3, 2,0,0, 0,8,0],
           [0,6,0, 5,0,0, 0,0,9],
           [0,0,4, 0,0,0, 0,3,0],
           [0,0,0, 0,0,9, 7,0,0]]


sudoku = sudoku_solution(sd_diff)
result = sudoku.iterative_deepening()
for i in range(9):
    print(result[i])
