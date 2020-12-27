import numpy
import random
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread

class TSP(QThread):
    draw_dlg = pyqtSignal(numpy.ndarray)
    def __init__(self, epoch = 500, size_of_population = 50, init_size = 6, p_mutation = 0.05):
        
        '''
            size_of_population:最大个体数
            init_size:初始个体数
            p_mutation:个体变异概率
        '''
        super(TSP,self).__init__()
        self.epoch = epoch
        self.go_on_calc = True
        # 1. 初始化地图
        # 初始节点坐标信息
        '''
        node_position = [
            [76,56],
            [144,48],
            [255,8],
            [288,293],
            [69,393],
            [142,255],
            [360,383],
            [455,260],
            [347,528],
            [206,402],
            ]
        '''
        node_position = [
            [76,56],
            [144,48],
            [255,8],
            [288,293],
            [69,393],
            [142,255],
            [360,383],
            [455,260],
            [347,528],
            [206,402],
            [150,343],
            [15,50],
            [750,241],
            [343,121],
            [56,139],
            [25,776],
            [131,232],
            [76,330],
            [15,670],
            [521,144]
            ]
        # 创建距离矩阵
        # print(len(node_position))
        self.size_of_map = len(node_position) # 地图大小
        self.map = [[0]*self.size_of_map for i in range(self.size_of_map)]
        for x in range(self.size_of_map):
            for y in range(x+1,self.size_of_map):
                self.map[x][y] = ((node_position[x][0]-node_position[y][0])**2 + (node_position[x][1] - node_position[y][1])**2)**0.5
                self.map[y][x] =  self.map[x][y]


        self.map = numpy.array(self.map)
        # print("初始地图距离矩阵：",self.map)

        # 2. 定义编码：int
        self.node = [i for i in range(1, self.size_of_map + 1)] 
        # 3. 初始化种群
        self.size_of_population = size_of_population # 种群总大小，当个体过多则淘汰
        self.init_size = init_size # 初始化个体数
        self.current_size = self.init_size # 当前个体数
        self.all_route = [[0]*self.size_of_map for i in range(self.size_of_population)] # 所有种群
        self.all_route = numpy.array(self.all_route)

        # 根据种群大小循环生成初始个体
        for x in range(self.init_size):
            random.shuffle(self.node) # 随机打乱顺序
            for y in range(self.size_of_map):                
                self.all_route[x][y] = self.node[y]
            
        # print("初始种群：\n", self.all_route) 

        # 4. 定义变异率
        self.p_mutation = p_mutation

        # 最佳个体
        self.best_route = [0 for i in range(self.size_of_map)]
        self.best_score = 9999
        self.best_no = -1
        print("epoch:",self.epoch)
        

    def test(self):
        # 测试函数，验证map是否赋值正确
        count = 0
        for x in range(self.size_of_map):
            for y in range(self.size_of_map):
                if self.map[x][y] != self.map[y][x]:
                    print("error    ",x, y)
                count += 1
        print(count)

    def get_dist(self,route):
        # 获取输入路径的长度
        sum_result = 0
        for i in range(self.size_of_map - 1):
            sum_result += self.map[route[i] - 1][route[i+1] - 1]
        return sum_result

    def calc_f(self, route):
        # 输入一个路径，返回适应值，其值为总路程倒数
        # 适应值越大越好
        # print(F"输入路径为：{route}")
        sum_result = 0
        for i in range(self.size_of_map - 1):
            sum_result += self.map[route[i] - 1][route[i+1] - 1]
        # print(F"总路程为:{sum}")
        # print(F"返回值：{1/sum}")
        return 1/sum_result

    def chooseParent(self):
        # 选择用于交配的个体
        # 采用轮盘赌方式
        individual = [0] * self.current_size # 个体列表
        p_individual = [0] * self.current_size # 个体被选上的概率
        sum_f = 0 # 适应值总和
        for i in range(self.current_size):
            # print(i)
            individual[i] = i
            sum_f += self.calc_f(self.all_route[i])
            p_individual[i] = self.calc_f(self.all_route[i])
        for i in range(self.current_size):
            # print(i)
            p_individual[i] /= sum_f 
            # print(p_individual[i])
        # print(p_individual)
        parents = numpy.random.choice(individual, size = 2,replace=False, p=p_individual)
        return parents[0], parents[1]

    def deleteLoser(self):
        # 淘汰个体
        # 同样采用轮盘赌

        # 新增最优个体保护规则
        individual = [0] * self.current_size # 个体列表
        p_individual = [0] * self.current_size # 个体被淘汰的概率
        sum_d = 0.0 # 不适应值总和
        for i in range(self.current_size):
            individual[i] = i
            sum_d += 1/self.calc_f(self.all_route[i])
            p_individual[i] = 1/self.calc_f(self.all_route[i])
        for i in range(self.current_size):
            # print(i)
            p_individual[i] /= sum_d 
            # print(p_individual[i])
        loser = numpy.random.choice(individual, size = 1,replace=False, p=p_individual)
        ctr = True # 用于控制下面的最优保护循环 
        while True:  
             
            for i in range(self.size_of_map):
                if self.best_no != loser[0]:
                    ctr = False
                    break
            if ctr == False:
                break
            loser = numpy.random.choice(individual, size = 1,replace=False, p=p_individual) 
            
        self.all_route = numpy.delete(self.all_route, loser, 0) # 直接删去淘汰个体
        self.current_size -= 1
        self.all_route = numpy.insert(self.all_route, self.current_size,values=[0]*self.size_of_map, axis=0)

    def cross_single(self, dad, mom):
         # 交叉
        # dad和mom给的是all_route中的索引号

        # 获取实际的路径基因
        dad_route = self.all_route[dad]
        mom_route = self.all_route[mom]
        # 1. 随机选取两个交叉点
        n1 = random.randint(0,self.size_of_map-2)
        n2 = self.size_of_map-1
        # 选择交叉点中间的基因进行交叉
        # print(n1,n2)
        dad_piece = dad_route[n1:n2 + 1]
        mom_piece = mom_route[n1:n2 + 1]
        mapping_tab = [] # 映射表，防止不合法路径
        # 2. 建立映射
        for i in range(n2 - n1 + 1):
            if dad_piece[i] not in mom_piece and dad_piece[i] not in mapping_tab:
                mapping_tab.append(dad_piece[i])
                for j in range(n2 - n1 + 1):
                    if mom_piece[j] not in dad_piece and mom_piece[j] not in mapping_tab:
                        mapping_tab.append(mom_piece[j])
                        break
                     
        # 3. 开始交叉
        dad_route = numpy.delete(dad_route, range(n1,n2 + 1)) # 删去交叉片段
        mom_route = numpy.delete(mom_route, range(n1,n2 + 1))
        # 进行映射
        for i in range(len(dad_route) ):
            if dad_route[i] in mapping_tab:
                for m in range(len(mapping_tab)):
                    if dad_route[i] == mapping_tab[m]:
                        if m == len(mapping_tab)-1:
                            dad_route[i] = mapping_tab[0]
                        else:
                            dad_route[i] = mapping_tab[m+1]
                        break
                
            if mom_route[i] in mapping_tab:
                for m in range(len(mapping_tab)):
                    if mom_route[i] == mapping_tab[m]:
                        if m == len(mapping_tab)-1:
                            mom_route[i] = mapping_tab[0]
                        else:
                            mom_route[i] = mapping_tab[m+1]
                        break
        # 完成交换
        son_route_1 = numpy.insert(dad_route, n1, values=mom_piece, axis=0)
        son_route_2 = numpy.insert(mom_route, n1, values=dad_piece, axis=0)     
        return son_route_1, son_route_2

    def cross(self, dad, mom):
        # 交叉
        # dad和mom给的是all_route中的索引号

        # 获取实际的路径基因
        dad_route = self.all_route[dad]
        mom_route = self.all_route[mom]
        # 1. 随机选取两个交叉点
        n1 = random.randint(0,self.size_of_map-2)
        n2 = random.randint(n1, self.size_of_map-1)
        # 选择交叉点中间的基因进行交叉
        # print(n1,n2)
        dad_piece = dad_route[n1:n2 + 1]
        mom_piece = mom_route[n1:n2 + 1]
        mapping_tab = [] # 映射表，防止不合法路径
        # 2. 建立映射
        for i in range(n2 - n1 + 1):
            if dad_piece[i] not in mom_piece and dad_piece[i] not in mapping_tab:
                mapping_tab.append(dad_piece[i])
                for j in range(n2 - n1 + 1):
                    if mom_piece[j] not in dad_piece and mom_piece[j] not in mapping_tab:
                        mapping_tab.append(mom_piece[j])
                        break
                     
        # 3. 开始交叉
        dad_route = numpy.delete(dad_route, range(n1,n2 + 1)) # 删去交叉片段
        mom_route = numpy.delete(mom_route, range(n1,n2 + 1))
        # 进行映射
        for i in range(len(dad_route) ):
            if dad_route[i] in mapping_tab:
                for m in range(len(mapping_tab)):
                    if dad_route[i] == mapping_tab[m]:
                        if m == len(mapping_tab)-1:
                            dad_route[i] = mapping_tab[0]
                        else:
                            dad_route[i] = mapping_tab[m+1]
                        break
                
            if mom_route[i] in mapping_tab:
                for m in range(len(mapping_tab)):
                    if mom_route[i] == mapping_tab[m]:
                        if m == len(mapping_tab)-1:
                            mom_route[i] = mapping_tab[0]
                        else:
                            mom_route[i] = mapping_tab[m+1]
                        break
        # 完成交换
        son_route_1 = numpy.insert(dad_route, n1, values=mom_piece, axis=0)
        son_route_2 = numpy.insert(mom_route, n1, values=dad_piece, axis=0)     
        return son_route_1, son_route_2

    def mutate(self,route):
        # 以一定的概率变异
        if random.random() <= self.p_mutation:           
            n1 = random.randint(0,self.size_of_map-2)
            n2 = random.randint(n1+1, self.size_of_map-1)
            temp = route[n1]
            route[n1] = route[n2]
            route[n2] = temp
        return route

    def output_result(self):
        # 结果输出
        best = 0
        score = 0.0
        for i in range(self.current_size):
            if score < self.calc_f(self.all_route[i]):
                best = i
                score = self.calc_f(self.all_route[i])
        self.best_no = best
        # print(F"最好结果是第{best}条")
        # print(self.all_route[best])
        # print(F"长度为：{int(1/score)}")
        self.write_down_best_result(self.all_route[best],int(1/score))


    def write_down_best_result(self,best_route,best_score):
        if best_score < self.best_score:
            # print(best_score)
            self.best_route = best_route
            self.best_score = best_score


    def run_one(self):
        dad, mom = self.chooseParent()
        son_1, son_2 = self.cross_single(dad, mom) # 单点交叉       
        # son_1, son_2 = self.cross(dad, mom) # 两点交叉
        
        son_1 = self.mutate(son_1) # 变异
        son_2 = self.mutate(son_2)
        while self.current_size > (self.size_of_population - 5):
            self.deleteLoser()

        for i in range(self.size_of_map):
                self.all_route[self.current_size][i] = son_1[i]
                self.all_route[self.current_size+1][i] = son_2[i]
        self.current_size += 2

    def run(self):
        
            for i in range (self.epoch):
                self.run_one()
                if i % 100 ==0:
                    print(i)
                self.output_result()
                # if i %  == 0:
                self.draw_dlg.emit(self.best_route)
                
            for i in range(self.current_size):
                print(self.all_route[i])
                a = self.get_dist(self.all_route[i])
                print(a)
                
            self.output_result()
            print(F"best_route:{self.best_route},best_dst:{self.best_score}") 
            self.draw_dlg.emit(self.best_route)       




# 调试使用，无实际作用
if __name__ == "__main__":


    tsp =TSP(epoch = 2000,init_size=50,p_mutation=0.5,size_of_population=70)



    epoch = 2000
    for i in range (epoch):
        tsp.run_one()
        print(i)
        tsp.output_result()
        
    for i in range(tsp.current_size):
        print(tsp.all_route[i])
        a = tsp.get_dist(tsp.all_route[i])
        print(a)
        
    tsp.output_result()

    print(F"best_route:{tsp.best_route},best_dst:{tsp.best_score}")



