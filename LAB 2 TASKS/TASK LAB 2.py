from operator import mod
import pandas as p
from sklearn.linear_model import LinearRegression

data = p.read_excel('Student_Attendance_Dataset.xlsx')
print(data)
print(len(data))

c = ['Lab 1', 'Lab 2', 'Lab 3', 'Lab 4', 'Lab 5', 'Lab 6', 'Lab 7', 'Lab 8', 'Lab 9', 'Lab 10']
data[c] = data[c].replace({'P': 1, 'A': 0})

x = data[c]
y = data['Final Marks']
print(x, y)

model = LinearRegression()
print(f'{model} this is ')

m = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1]
df = p.DataFrame(m)
print(df)