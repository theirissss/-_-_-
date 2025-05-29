import math
from abc import ABC,abstractmethod

"""
计划：
补全或改造后续的逻辑
把第一第二缓和曲线整合为一个缓和曲线的函数（总共四份逻辑：第一左/第一右/第二左/第二右）其他逻辑复用，把这个改造成四个策略或两两嵌套（第一左/右，第二左/右）
定义/解耦为三个大类，基类（算要素/主点），zh/hz类（计算zh/hz方位角），p点类（计算缓和/圆曲线上某一点坐标）
把一些动态切换的逻辑封包（例如左右前后选择直接获取输入/根据桩号计算）
"""
# 第一个抽象类，选择左右转，交点前后位置的不同zh和hz计算方法

class FangWeiShunXu(ABC):
    @abstractmethod
    def zh_hz_fangweijiao(self,calculator:"ZhuangHaoJiSuanBase"):pass # 左主后，左主前，右主后，右主前


"""思路：父类，策略类，子类继承并调用"""
class LeftMainAfter(FangWeiShunXu):# 左转曲线
    def zh_hz_fangweijiao(self,calculator): # 左转曲线，主交点在副交点后
        left_mainafter_alpha_zh=(math.atan2(calculator.Δy,calculator.Δx))% (2*math.pi)
        left_mainafter_alpha_hz=(left_mainafter_alpha_zh+(math.pi-calculator.alpha_rad))% (2*math.pi)
        return left_mainafter_alpha_zh,left_mainafter_alpha_hz

class LeftMainBefore(FangWeiShunXu):# 左转曲线
    def zh_hz_fangweijiao(self,calculator): # 左转曲线，主交点在副交点前
        left_mainbefore_alpha_hz = (math.atan2(calculator.Δy, calculator.Δx))% (2*math.pi)
        left_mainbefore_alpha_zh = (left_mainbefore_alpha_hz-(math.pi-calculator.alpha_rad))% (2*math.pi)
        return left_mainbefore_alpha_zh, left_mainbefore_alpha_hz

class RightMainAfter(FangWeiShunXu):# 右转曲线
    def zh_hz_fangweijiao(self,calculator): # 右转曲线，主交点在副交点后
        right_mainafter_alpha_zh = (math.atan2(calculator.Δy, calculator.Δx))% (2*math.pi)
        right_mainafter_alpha_hz=(right_mainafter_alpha_zh-(math.pi-calculator.alpha_rad))% (2*math.pi)
        return right_mainafter_alpha_zh,right_mainafter_alpha_hz

class RightMainBefore(FangWeiShunXu):  # 右转曲线
    def zh_hz_fangweijiao(self,calculator): # 右转曲线，主交点在副交点前
        right_mainbefore_alpha_hz=(math.atan2(calculator.Δy,calculator.Δx))% (2*math.pi)
        right_mainbefore_alpha_zh=(right_mainbefore_alpha_hz+(math.pi-calculator.alpha_rad))% (2*math.pi)
        return right_mainbefore_alpha_zh,right_mainbefore_alpha_hz


"""我算是看懂了，函数/方法不关心calculator（参数）从哪来的，只要他在方法/函数名后面的括号里作为形参传进函数了，那就能运转，形参的意义就在这里"""
"""反正到了运行zh_hz_fangweijiao的时候，这个calculator早都实例化了"""

# 第二个抽象类，定义左右转曲线在计算p点时的区别

class LeftRightDelta(ABC):
    @abstractmethod
    def left_right_delta(self,calculator):pass

class LeftDelta(LeftRightDelta):
    def left_right_delta(self,calculator):pass
        # fangweijiao_rad = calculator.alpha_jd_zh_rad + math.pi + delta # 可以试试把delta存进self，方便直接calculator.delta调用


class RightDelta(LeftRightDelta):
    def left_right_delta(self,calculator):pass

# 第三个抽象类，选择不同位置的p点的计算方法

class ZhuangHaoZuoBiao(ABC):
    @abstractmethod
    def zuobiao_jisuan(self,calculator,p_zhuanghao):
        pass

class FirstHuanheP(ZhuangHaoZuoBiao): # 第一缓和曲线

    def zuobiao_jisuan(self,calculator, p_zhuanghao)-> tuple[float, float]:# 第一缓和曲线上p点坐标

        """
        第一缓和曲线p点计算策略
        :param calculator: 形参，来自于下面ZhuangHaoJiSuanBase的实例化
        :param p_zhuanghao: p点桩号
        :return: p点的x，y坐标
        """
        li = round(p_zhuanghao - calculator.zh_zhuanghao, 3)  # 直接修约 # 算li（zh和p的距离）
        li = abs(li) # 绝对值li防止zh桩号>p桩号
        c = round(calculator.R * calculator.L0, 3)  # 修约 # c的值
        """切线坐标"""
        xi = round(li - li ** 5 / (40 * c ** 2), 3)  # 修约 # 切线坐标xi
        yi = round(li ** 3 / (6 * c), 3)  # 修约 # 切线坐标yi
        """弦长"""
        d_zh_p = round(math.sqrt(xi ** 2 + yi ** 2), 3)  # 修约 ， sqrt开根号
        """方位角"""
        delta = math.atan(yi/xi)#--------------------------------------------有修改

        fangweijiao_rad = calculator.alpha_jd_zh_rad +math.pi+delta # 这句准备换
        fangweijiao_shuchu=math.degrees(fangweijiao_rad) # 用于输出查看
        """最终计算p点的x坐标和y坐标"""
        p_x = round(calculator.x_zh + d_zh_p * math.cos(fangweijiao_rad), 3)  # 最终修约，三位小数
        p_y = round(calculator.y_zh + d_zh_p * math.sin(fangweijiao_rad), 3)  # 最终修约
        print(f"Li={li:.4f}, C={c:.3f}, Xi={xi:.3f}, Yi={yi:.3f}, ")
        print(f"D_zh_p={d_zh_p:.3f}, 方位角={fangweijiao_shuchu}")
        # print("debug完成，无误差")

        return p_x,p_y

class YuanQuXianP(ZhuangHaoZuoBiao): # 圆曲线

    def zuobiao_jisuan(self,calculator, p_zhaunghao)-> tuple[float, float]: # 圆曲线上p点坐标
        """
        圆曲线p点计算策略
        :param calculator: 形参，来自于下面ZhuangHaoJiSuanBase的实例化
        :param p_zhaunghao:  p点桩号
        :return: p点的x，y坐标
        """
        l_hy_p=abs(calculator.hy_zhuanghao - p_zhaunghao)
        φ = (calculator.beita0 + math.radians((180 * l_hy_p) / (math.pi * calculator.R))) % (math.pi * 2)
        φ_shuchu=math.degrees(φ)

        Xi=calculator.m+calculator.R*math.sin(φ)
        Yi=calculator.R*(1-math.cos(φ))+calculator.p_yaosu

        d_zh_p=math.sqrt(Xi**2+Yi**2)
        delta=math.atan(Yi/Xi)
        delta_shuchu=math.degrees(delta)
        fangweijiao=((calculator.alpha_jd_zh_rad+math.pi)%(math.pi*2)+delta)% (2 * math.pi)
        p_x=round(calculator.x_zh+d_zh_p*math.cos(fangweijiao),3)
        p_y=round(calculator.y_zh+d_zh_p*math.sin(fangweijiao),3)
        print(f"fai角度输出：{φ_shuchu},l的长度：{l_hy_p},Xi={Xi},Yi={Yi},d_zh_p={d_zh_p},夹角={delta_shuchu},方位角={fangweijiao}")

        return p_x,p_y

class SecondHuanHeP(ZhuangHaoZuoBiao): # 第二缓和曲线

    def zuobiao_jisuan(self,calculator, p_zhuanghao)-> tuple[float, float]:# 第二缓和曲线上p点坐标
        """
        第二缓和曲线p点计算策略
        :param calculator: 形参，来自于下面ZhuangHaoJiSuanBase的实例化
        :param p_zhuanghao: p点桩号
        :return: p点的x，y坐标
        """
        calculator.alpha_jd_hz_rad=math.radians(calculator.alpha_jd_hz_rad)
        li =abs (p_zhuanghao - calculator.hz_zhuanghao)  # 算li（zh和p的距离） # 绝对值li防止zh桩号>p桩号
        c = calculator.R *calculator.L0 # c的值
        """切线坐标"""
        xi =li - li ** 5 / (40 * c ** 2) # 切线坐标xi
        yi = li ** 3 / (6 * c)# 切线坐标yi
        """弦长"""
        d_zh_p =math.sqrt(xi ** 2 + yi ** 2)# sqrt开根号
        """夹角"""
        delta= math.atan(yi/xi)
        """方位角（弧度）"""
        fangweijiao_rad=calculator.alpha_jd_hz_rad+math.pi-delta #弧度制方位角
        fangweijiao_rad = fangweijiao_rad % (2 * math.pi)  # 限制在0~2π
        fangweijiao_shuchu=math.degrees(fangweijiao_rad) #转化为角度制方便查看
        """最终计算p点的x坐标和y坐标"""
        p_x = round(calculator.x_hz + d_zh_p * math.cos(fangweijiao_rad), 3)  # 最终修约，三位小数
        p_y = round(calculator.y_hz + d_zh_p * math.sin(fangweijiao_rad), 3)  # 最终修约
        print(f"Li={li:.3f}, C={c:.3f}, Xi={xi:.3f}, Yi={yi:.3f}, ")
        print(f"D_zh_p={d_zh_p:.3f}, 方位角={fangweijiao_shuchu}")

        return p_x,p_y


"""——————————————————————————————————————————————————————————————————————————————————————————————————————————————————"""

class ZhuangHaoJiSuanBase:
    def __init__(self,R: float, L0: float, alpha_r: float, y_jd_zhu: float,
                 x_jd_zhu: float, y_jd_fu: float, x_jd_fu: float, jd_zhu_zhuanghao: float):
        # self.__dict__.update(params)

        self.x_jd_zhu = x_jd_zhu # 这里是否可以暂时去掉
        self.y_jd_zhu = y_jd_zhu # 这里是否可以暂时去掉

        self.R=R # 基础计算要用的参数，左右转不影响**
        self.L0=L0 # 基础计算要用的参数，左右转不影响**
        self.alpha_rad=math.radians(alpha_r) # 基础计算要用的参数，左右转不影响**
        self.jd_zhu_zhuanghao = jd_zhu_zhuanghao # 基础计算要用的参数，左右转不影响**

        self.y_jd_fu = y_jd_fu # 这里是否可以暂时去掉
        self.x_jd_fu = x_jd_fu # 这里是否可以暂时去掉
        #
        self.Δy = self.y_jd_fu - self.y_jd_zhu
        self.Δx = self.x_jd_fu - self.x_jd_zhu
        # self.main_alpha=(math.atan2(self.Δy,self.Δx))% (2*math.pi)

    def quxian_yao_su_1(self): # 曲线要素
        """
        class形式的曲线要素计算
        :return: self，支持链式调用
        """
        self.beita0=(self.L0/(2*self.R))
        self.beita0_shuchu=math.degrees(self.beita0)
        self.m=self.L0/2 - self.L0**3/(240*(self.R**2))
        self.p_yaosu=self.L0**2/(24*self.R)
        self.T=self.m+(self.p_yaosu+self.R)*math.tan(self.alpha_rad / 2)
        self.L = self.R * (self.alpha_rad - 2 * self.beita0) + 2 * self.L0
        self.E= ((self.R+self.p_yaosu) / math.cos(self.alpha_rad / 2)) - self.R
        self.q=2*self.T-self.L
        print(f"曲线要素：β₀={self.beita0_shuchu:.6f},m={self.m:.3f},p={self.p_yaosu:.3f},*T={self.T:.3f},L={self.L:.3f},*E={self.E:.3f},*q={self.q:.3f}")
        # print("基本正确，误差极小")
        return self


    def zhudianzhuanghao_2(self)-> "ZhuangHaoJiSuanBase": # 主点桩号

        self.zh_zhuanghao=self.jd_zhu_zhuanghao-self.T
        self.hy_zhuanghao=self.zh_zhuanghao+self.L0
        self.qz_zhuanghao=self.hy_zhuanghao+(self.L/2-self.L0)
        self.yh_zhuanghao=self.zh_zhuanghao+self.L-self.L0
        self.hz_zhuanghao= self.yh_zhuanghao+self.L0
        print(f"主点桩号：zh桩号：{self.zh_zhuanghao:.5f}，hy点桩号：{self.hy_zhuanghao:.5f}，qz点桩号：{self.qz_zhuanghao:.5f}，yh点桩号：{self.yh_zhuanghao:.5f}，hz点桩号：{self.hz_zhuanghao:.5f}")
        # print("全部正确")
        return self


class ZhuanXiangFangWeiJiao:
    def __init__(self,calculator:ZhuangHaoJiSuanBase, direction:str, position:str):
        self.calculator=calculator
        self.direction=direction
        self.position=position

    def _init_strategy(self):
        # 判断左右前后是不是放在一个小模块/抽象类里面比较好？无论是用户输入还是以后通过计算得出都方便改
        """
        工厂方法替换原alpha_jd_zh_and_hz_3，选择适用策略类
        :return:某个适用策略类，例LeftMainBefore()，这里返回策略类，但是并不调用，只是进行筛选
        """
        strategies = {
            ("左", "后"): LeftMainAfter(),
            ("左", "前"): LeftMainBefore(),
            ("右", "后"): RightMainAfter(),
            ("右", "前"): RightMainBefore() # 这里都是类的实例
        } # LeftMainAfter() 会立即创建一个实例，并作为字典的值存储。就像main()一样，检测到括号直接实例化，不需要a=B()起手
          # 甚至a=B()起手只是把B()赋值给a而已，他什么都不是
        return strategies[(self.direction, self.position)]# 例如索引["左","前"]，返回LeftMainBefore()

    def diaoyong_celue1(self):
        self.strategy=self._init_strategy() # 这一步可以搬到__init__里面
        return self

    def zh_hz_zuobiao(self):
        self.zh_fangweijiao,self.hz_fangweijiao=self.strategy.zh_hz_fangweijiao(self.calculator) # 根据上面的策略这里会返回一个直缓和缓直方位角
        return self

class ZhuanXiangZuoBiao: # 说人话就是zh和hz点的坐标

    def __init__(self,calculator:ZhuangHaoJiSuanBase,zhhzfangweijiao:ZhuanXiangFangWeiJiao): # param分别是前两个类的实例
        self.calculator=calculator
        self.zhhzfangweijiao=zhhzfangweijiao

    def calculate_zh_coordinate_4a(self):
        """
        zh坐标
        :return: self的直缓点的x，y坐标
        """
        self.x_zh = self.calculator.x_jd_zhu + self.calculator.T * math.cos(self.zhhzfangweijiao.zh_fangweijiao)
        self.y_zh = self.calculator.y_jd_zhu + self.calculator.T * math.sin(self.zhhzfangweijiao.zh_fangweijiao)
        print(f"zh点x坐标：{self.x_zh}，zh点y坐标：{self.y_zh}")
        return self

    def calculate_hz_coordinate_4b(self):
        """
        hz坐标
        :return: self的缓直点的x，y坐标
        """

        self.x_hz = self.calculator.x_jd_zhu + self.calculator.T * math.cos(self.zhhzfangweijiao.hz_fangweijiao)
        self.y_hz = self.calculator.y_jd_zhu + self.calculator.T * math.sin(self.zhhzfangweijiao.hz_fangweijiao)
        print(f"hz点x坐标：{self.x_hz}，hz点y坐标：{self.y_hz}")
        return self

class PDianZuoBiao: # 最后再把LeftRightDelta(ABC)的这几个工厂一下就好了
    def __init__(self,calculator:ZhuangHaoJiSuanBase,zhhzfangweijiao:ZhuanXiangFangWeiJiao,zh_hzzuobiao:ZhuangHaoZuoBiao,p):# 参数分别是前三个类的实例
        self.calculator=calculator
        self.zhhzfangweijiao=zhhzfangweijiao
        self.zh_hzzuobiao=zh_hzzuobiao

    def _init_quxianshang(self):pass



"""左转右转影响圆曲线上p点坐标计算吗"""













"""此行向后待解除注释"""
# def get_curve_params() -> dict:
#     print("****************************【道路曲线参数输入】*******************************")
#     params = {
#         "x_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）X坐标: ")),
#         "y_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）Y坐标: ")),
#         "R": float(input("请输入圆曲线半径R: ")),
#         "L0": float(input("请输入缓和曲线长度L0: ")),
#         "alpha_r": float(input("请输入转向角(**转化为小数形式,例如10°20'30''转化为10.341666保留六位小数**): ")),
#         "jd_zhu_zhuanghao": float(input("请输入主交点桩号").replace("K"," ").replace("k"," ").replace("+","")),
#         "x_jd_fu": float(input("请输入副交点（只有两个坐标值的那个交点）X坐标: ")),
#         "y_jd_fu": float(input("请输入副交点（只有两个坐标值的那个交点）Y坐标: "))
#     }
#     return params


class GeShiZhuanHuan:
    """
    负责输入输出的格式转换，例如，dms转换十进制，桩号转换浮点数
    调用格式：类名称.方法名(参数)   eg：GeShiZhuanHuan.hanzijiaodu(10度20分30秒)
    """
    @staticmethod
    def jiaodu(jiaodu): # 汉字解为浮点数
        # 需要学习正则表达式匹配汉字，符号
        if isinstance(jiaodu,str):
            hanzi_1=jiaodu.strip("秒") # 1度2分3
            hanzi_list=hanzi_1.split("度") # ["1","2分3"]
            hanzi_list2=hanzi_list[1].split("分") # ["2","3"]
            dd=abs(float(hanzi_list[0]))+float(hanzi_list2[0])/60+float(hanzi_list2[1])/3600
            return -dd if float(hanzi_list[0])<0 else dd
        elif isinstance(jiaodu,(int,float)):
            pass     # 记得添加逻辑


    @staticmethod
    def zhuanghao(zhuanghao):
        if isinstance(zhuanghao,str):
            return float(zhuanghao.strip().replace("K"," ").replace("k"," ").replace("+",""))
        elif isinstance(zhuanghao,(int,float)):
            return f"K{zhuanghao // 1000}+{zhuanghao % 1000}"




def get_curve_params() -> dict:
    """
    获取用户输入计算参数
    :return: 返回字典
    """
    print("****************************【道路曲线参数输入】*******************************")
    yuanshi_alpha=input("请输入转向角（10度20分30秒，汉字单位形式/或10.341666，十进制形式）")

    try:
        alpha_r=float(yuanshi_alpha) # 两个都要赋值alpha_r
    except ValueError:
        alpha_r = GeShiZhuanHuan.jiaodu(yuanshi_alpha) # 转向角转换格式
    params = {
        "x_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）X坐标: ")),
        "y_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）Y坐标: ")),
        "R": float(input("请输入圆曲线半径R: ")),
        "L0": float(input("请输入缓和曲线长度L0: ")),
        "alpha_r": alpha_r,
        "jd_zhu_zhuanghao": GeShiZhuanHuan.zhuanghao(input("请输入主交点桩号")),
        "x_jd_fu": float(input("请输入副交点（只有两个坐标值的那个交点）X坐标: ")),
        "y_jd_fu": float(input("请输入副交点（只有两个坐标值的那个交点）Y坐标: "))
    }
    return params


def main(show_huoqu):
    """
    主程序
    :param show_huoqu: 决定print("*************************平曲线上任一桩号坐标计算*************************)")有无显示必要
    :return: 无
    """
    try:
        if show_huoqu:
            print("*************************平曲线上任一桩号坐标计算*************************)")
        p_zhuanghao=input("请输入桩号")
        p_zhuanghao_float=GeShiZhuanHuan.zhuanghao(p_zhuanghao)
        if  qianzhijisuan.zh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hy_zhuanghao:
            p=zh.first_huanhe_p_5a(p_zhuanghao_float)
            print(f"第一缓和曲线上p点坐标为{p}")
        elif qianzhijisuan.hy_zhuanghao < p_zhuanghao_float <= qianzhijisuan.yh_zhuanghao:
            p = zh.yuanquxian_p_5bc(p_zhuanghao_float)
            print(f"圆曲线上p点坐标为{p}")
        elif qianzhijisuan.yh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hz_zhuanghao:
            p= zh.second_huanhe_p_5d(p_zhuanghao_float)
            print(f"第二缓和曲线上p点坐标为{p}")
        elif p_zhuanghao_float < qianzhijisuan.zh_zhuanghao:
            print("错误，桩号不能小于直缓点桩号！！！")
        elif p_zhuanghao_float > qianzhijisuan.hz_zhuanghao:
            print("错误，桩号不能大于缓直点桩号！！！")
        else:
            print("错误，请输入有效桩号格式，例如K12+345或k12+345")
    except:
        print("错误，请输入有效桩号！！！")


if __name__ == "__main__":
    # 1. 获取参数


    user_params = get_curve_params()
    # user_params={
    #     "R": 9000,
    #     "L0": 530,
    #     "alpha_r": 37.29225,
    #     "x_jd_zhu": 2798759.333,
    #     "y_jd_zhu": 493981.198,
    #     "x_jd_fu": 2793009.023,
    #     "y_jd_fu": 481696.391,
    #     "jd_zhu_zhuanghao": 95054.204
    # }      # 临时试验参数

    # 2. 直接实例化并计算（暴力链式）
    qianzhijisuan = (
        ZhuangHaoJiSuanBase("qian","zuo",**user_params)  # 字典解包传参
        .quxian_yao_su_1()
        .zhudianzhuanghao_2()
        .alpha_jd_zh_and_hz_3()
    )
    zh=qianzhijisuan.calculate_zh_coordinate_4a()
    hz=qianzhijisuan.calculate_hz_coordinate_4b()
    print(f"直缓点x{zh.x_zh},直缓y{zh.y_zh},缓直x{hz.x_hz},缓直y{hz.y_hz}")
#这一步很关键
    # shiyan_gongchang = jisuan_gongchang("左", "后",**user_params)
# strategy_class(**params)：带参数的抽象方法，需要调用


    main(True) # 首次调用显示首行提示

    while True:
        try:
            wenwen =(input("是否继续计算（选择“是”或“否”）")).strip()
            if wenwen=="是":
                main(False)# 后续调用不显示首行提示
            else:
                print("计算结束")
                break
        except:
            print("请输入“是”或“否”")

    print("已完成全部计算任务")
    input("按回车键退出...")



























    # try:
    #     print("*************************平曲线上任一桩号坐标计算*************************)")
    #     p1zhuanghao=input("请输入桩号")
    #     p_zhuanghao_float=float(p1zhuanghao.replace("K"," ").replace("k"," ").replace("+",""))
    #     if  qianzhijisuan.zh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hy_zhuanghao:
    #         p=zh.first_huanhe_p_5a(p_zhuanghao_float)
    #         print(f"第一缓和曲线上p点坐标为{p}")
    #     elif qianzhijisuan.hy_zhuanghao < p_zhuanghao_float <= qianzhijisuan.yh_zhuanghao:
    #         p = zh.yuanquxian_p_5bc(p_zhuanghao_float)
    #         print(f"圆曲线上p点坐标为{p}")
    #     elif qianzhijisuan.yh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hz_zhuanghao:
    #         p= zh.second_huanhe_p_5d(p_zhuanghao_float)
    #         print(f"第二缓和曲线上p点坐标为{p}")
    #     else:
    #         print("错误，桩号不能小于直缓点桩号！！！不能大于缓直点桩号！！！")
    # except:
    #     print("错误，请输入有效桩号！！！")
# print("已完成全部计算任务")
# input("按回车键退出...")



#     p1=zh.first_huanhe_p_5a(int(input("请输入第一缓和曲线桩号")))
#     print(f"p1坐标为{p1}")
#     p2=zh.yuanquxian_p_5bc(int(input("请输入圆曲线桩号")))
#     print(f"p2坐标为{p2}")
#     p3=zh.yuanquxian_p_5bc(int(input("请输入圆曲线桩号")))
#     print(f"p3坐标为{p3}")
#     p4=hz.second_huanhe_p_5d(int(input("请输入第二缓和曲线桩号")))
#     print(f"p4坐标为{p4}")
# print("已完成全部计算任务")
# input("按回车键退出...")