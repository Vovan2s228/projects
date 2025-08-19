class PIDcontroller:
    def __init__(self):
        self.p_p = 0.02
        self.p_i = 0.00005
        self.p_d = 0.5
        self.CTE_list = [0]

    def process(self, CTE):
        self.CTE_list.append(CTE)
        return -self.p_p * CTE - self.p_d * (self.CTE_list[-1]-self.CTE_list[-2]) - self.p_i * sum(self.CTE_list)

