# coding=utf-8

class RegressionTree:
    def __init__(self, data_series):
        self.train_data_x = []
        for i in range(len(data_series) - 6):
            item = data_series[i:i + 6]
            self.train_data_x.append(item)

    def get_train_data_x(self):
        return self.train_data_x


if __name__ == "__main__":
    data_series = [2.0534333854284, 0.0012215188329604634, 0.01743939470890965, 1.8931332291432006, 0.135263434807194,
                   1.793645135739508, 2.5864545980184457, 2.2490174778885046, 3.870902260071695, 11.36666494343233,
                   0.08747952619021486, 0.0, 0.008719697354454825, 0.9465666145716003, 0.04471368807394504,
                   4.964032379359032e-06,
                   0.3670142276422695, 1.2144074850195377, 16.079797910366793, 5.622949754149927, 13.68605814397561,
                   12.593995925074665, 6.253461987473333, 9.167978051984235, 4.009842067939814]

    rt = RegressionTree(data_series)
    print rt.get_train_data_x()