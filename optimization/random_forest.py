import numpy as np
from sklearn.ensemble import RandomForestRegressor

class Randomforest:
    def __init__(self, X, y):
        self.X = np.array(X)
        self.y = np.array(y)

        # 使用默认超参数初始化随机森林模型
        self.model = RandomForestRegressor()

    def fit(self):
        self.model.fit(self.X, self.y)

    def predict(self, points):
        points = np.array(points)
        pred = self.model.predict(points)
        var = self.variance(points)
        return pred, var

    def variance(self, points):
        samples = [tree.predict(points) for tree in self.model.estimators_]
        var = np.var(samples, axis=0)
        return var
