from sklearn.naive_bayes import CategoricalNB
X=[[1],[1],[0],[1],[0],[1],[0],[0],[0],[1]]
Y=["Spam","Spam","Spam","Spam","Spam","No Spam","No Spam","No Spam","No Spam","No Spam"]
M= CategoricalNB()
M.fit(X,Y)
N=[[1]]
p=M.prediction(N)
print(p)
