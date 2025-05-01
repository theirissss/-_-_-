import math

"""
round(,小数位):四舍五入/内置函数
abs()：绝对值
sqrt()：开根号
degrees()：转化为角度制
radians()：转化为弧度制
"""
class ZhuangHaoJiSuan:
    def __init__(self,R,L0,alpha_r,y_jd_zhu,x_jd_zhu,y_jd_fu,x_jd_fu,jd_zhu_zhuanghao):
        self.x_jd_zhu = x_jd_zhu
        self.y_jd_zhu = y_jd_zhu
        self.R=R
        self.L0=L0
        self.alpha_r_rad=math.radians(alpha_r)# alpha_r中的r表示right，右转
        self.jd_zhu_zhuanghao = jd_zhu_zhuanghao

        self.y_jd_fu = y_jd_fu
        self.x_jd_fu = x_jd_fu

    def quxian_yao_su_1(self): # 曲线要素
        """
        class形式的曲线要素计算
        :return: self，支持链式调用
        """
        # alpha_r=math.radians(alpha_r)
        # rad_180=math.radians(180)
        self.beita0=(self.L0/(2*self.R))
        self.beita0_shuchu=math.degrees(self.beita0)
        self.m=self.L0/2 - self.L0**3/(240*(self.R**2))
        self.p_yaosu=self.L0**2/(24*self.R)
        self.T=self.m+(self.p_yaosu+self.R)*math.tan(self.alpha_r_rad/2)
        self.L = self.R * (self.alpha_r_rad - 2 * self.beita0) + 2 * self.L0
        self.E=((self.R+self.p_yaosu)/math.cos(self.alpha_r_rad/2))-self.R
        self.q=2*self.T-self.L
        print(f"曲线要素：β₀={self.beita0_shuchu:.6f},m={self.m:.3f},p={self.p_yaosu:.3f},*T={self.T:.3f},L={self.L:.3f},*E={self.E:.3f},*q={self.q:.3f}")
        # print("基本正确，误差极小")
        return self


    def zhudianzhuanghao_2(self)->"ZhuangHaoJiSuan":

        self.zh_zhuanghao=self.jd_zhu_zhuanghao-self.T
        self.hy_zhuanghao=self.zh_zhuanghao+self.L0
        self.qz_zhuanghao=self.hy_zhuanghao+(self.L/2-self.L0)
        self.yh_zhuanghao=self.zh_zhuanghao+self.L-self.L0
        self.hz_zhuanghao= self.yh_zhuanghao+self.L0
        print(f"主点桩号：zh桩号：{self.zh_zhuanghao:.5f}，hy点桩号：{self.hy_zhuanghao:.5f}，qz点桩号：{self.qz_zhuanghao:.5f}，yh点桩号：{self.yh_zhuanghao:.5f}，hz点桩号：{self.hz_zhuanghao:.5f}")
        # print("全部正确")
        return self


    def alpha_jd_zh_and_hz_3(self)->"ZhuangHaoJiSuan": # 交点到直缓和缓直的方位角

        Δy=self.y_jd_fu-self.y_jd_zhu
        Δx=self.x_jd_fu-self.x_jd_zhu
        self.alpha_jd_hz_rad=(math.atan2(Δy,Δx))%(math.pi*2)#交点到缓直的方位角---------------------------------有修改
        alpha_jd_hz_shuchu=math.degrees(self.alpha_jd_hz_rad) # 用于查看的数值，专门转化为角度制
        """下面是alpha_jd_zh（这一步是有必要的，为什么不直接用hz到jd不加180，因为后面还要算hz和zh的坐标"""
        # zhuanxiangjiao_rad=math.radians(zhuanxiangjiao) # 把转向角转化为弧度制
        alpha_jd_zh= self.alpha_jd_hz_rad-self.alpha_r_rad+math.pi # 算出交点到直缓的方位角
        self.alpha_jd_zh_rad=alpha_jd_zh % (2*math.pi) # 限制在360度以内
        alpha_jd_zh_shuchu=math.degrees(self.alpha_jd_zh_rad) # 用于查看的数值，专门转化为角度制
        print(f"交点到缓直的方位角{alpha_jd_hz_shuchu},交点到直缓的方位角{alpha_jd_zh_shuchu}") # 用于查看
        # print("debug完成，无误差")
        return self


    def calculate_zh_coordinate_4a(self)-> "ZhuangHaoJiSuan":
        """
        直缓点坐标
        :return: self的直缓点的x，y坐标
        """

        self.x_zh = self.x_jd_zhu + self.T * math.cos(self.alpha_jd_zh_rad)
        self.y_zh = self.y_jd_zhu + self.T * math.sin(self.alpha_jd_zh_rad)
        print(f"zh点x坐标：{self.x_zh}，zh点y坐标：{self.y_zh}")
        # print("debug完成，有微小误差，0.002以内")
        return self


    def calculate_hz_coordinate_4b(self)-> "ZhuangHaoJiSuan":
        """
        缓直点坐标
        :return: self的缓直点的x，y坐标
        """

        self.x_hz = self.x_jd_zhu + self.T * math.cos(self.alpha_jd_hz_rad)
        self.y_hz = self.y_jd_zhu + self.T * math.sin(self.alpha_jd_hz_rad)
        print(f"hz点x坐标：{self.x_hz}，hz点y坐标：{self.y_hz}")
        # print("debug完成，有微小误差，0.002以内")
        return self

    def first_huanhe_p_5a(self, p_zhuanghao)-> tuple[float, float]:# 第一缓和曲线上p点坐标

        """
        第一缓和曲线上p点坐标
        :param p_zhuanghao: 所求点p的桩号
        :return: p点的x，y坐标
        """
        li = round(p_zhuanghao - self.zh_zhuanghao, 3)  # 直接修约 # 算li（zh和p的距离）
        li = abs(li) # 绝对值li防止zh桩号>p桩号
        c = round(self.R * self.L0, 3)  # 修约 # c的值
        """切线坐标"""
        xi = round(li - li ** 5 / (40 * c ** 2), 3)  # 修约 # 切线坐标xi
        yi = round(li ** 3 / (6 * c), 3)  # 修约 # 切线坐标yi
        """弦长"""
        d_zh_p = round(math.sqrt(xi ** 2 + yi ** 2), 3)  # 修约 ， sqrt开根号
        """方位角"""
        jiajiao = math.atan(yi/xi)#--------------------------------------------有修改

        fangweijiao_rad = self.alpha_jd_zh_rad +math.pi+jiajiao
        fangweijiao_shuchu=math.degrees(fangweijiao_rad) # 用于输出查看
        """最终计算p点的x坐标和y坐标"""
        p_x = round(self.x_zh + d_zh_p * math.cos(fangweijiao_rad), 3)  # 最终修约，三位小数
        p_y = round(self.y_zh + d_zh_p * math.sin(fangweijiao_rad), 3)  # 最终修约
        print(f"Li={li:.4f}, C={c:.3f}, Xi={xi:.3f}, Yi={yi:.3f}, ")
        print(f"D_zh_p={d_zh_p:.3f}, 方位角={fangweijiao_shuchu}")
        # print("debug完成，无误差")

        return p_x,p_y

    def yuanquxian_p_5bc(self, p_zhaunghao)-> tuple[float, float]: # 圆曲线上p点坐标
        """
        圆曲线上p点坐标
        :param p_zhaunghao: 所求点p的桩号
        :return: p点的x，y坐标
        """
        l_hy_p=abs(self.hy_zhuanghao - p_zhaunghao)
        φ = (self.beita0 + math.radians((180 * l_hy_p) / (math.pi * self.R))) % (math.pi * 2)
        φ_shuchu=math.degrees(φ)

        Xi=self.m+self.R*math.sin(φ)
        Yi=self.R*(1-math.cos(φ))+self.p_yaosu

        d_zh_p=math.sqrt(Xi**2+Yi**2)
        jiajiao=math.atan(Yi/Xi)
        jiajiao_shuchu=math.degrees(jiajiao)
        fangweijiao=((self.alpha_jd_zh_rad+math.pi)%(math.pi*2)+jiajiao)% (2 * math.pi)
        p_x=round(self.x_zh+d_zh_p*math.cos(fangweijiao),3)
        p_y=round(self.y_zh+d_zh_p*math.sin(fangweijiao),3)
        print(f"fai角度输出：{φ_shuchu},l的长度：{l_hy_p},Xi={Xi},Yi={Yi},d_zh_p={d_zh_p},夹角={jiajiao_shuchu},方位角={fangweijiao}")

        return p_x,p_y

    def second_huanhe_p_5d(self, p_zhuanghao)-> tuple[float, float]:# 第二缓和曲线上p点坐标
        """
        第二缓和曲线上p点坐标
        :param p_zhuanghao:所求点p的桩号
        :return: p点的x，y坐标
        """
        self.alpha_jd_hz_rad=math.radians(self.alpha_jd_hz_rad)
        li =abs (p_zhuanghao - self.hz_zhuanghao)  # 算li（zh和p的距离） # 绝对值li防止zh桩号>p桩号
        c = self.R * self.L0 # c的值
        """切线坐标"""
        xi =li - li ** 5 / (40 * c ** 2) # 切线坐标xi
        yi = li ** 3 / (6 * c)# 切线坐标yi
        """弦长"""
        d_zh_p =math.sqrt(xi ** 2 + yi ** 2)# sqrt开根号
        """夹角"""
        jiajiao= math.atan(yi/xi)
        """方位角（弧度）"""
        fangweijiao_rad=self.alpha_jd_hz_rad+math.pi-jiajiao #弧度制方位角
        fangweijiao_rad = fangweijiao_rad % (2 * math.pi)  # 限制在0~2π
        fangweijiao_shuchu=math.degrees(fangweijiao_rad) #转化为角度制方便查看
        """最终计算p点的x坐标和y坐标"""
        p_x = round(self.x_hz + d_zh_p * math.cos(fangweijiao_rad), 3)  # 最终修约，三位小数
        p_y = round(self.y_hz + d_zh_p * math.sin(fangweijiao_rad), 3)  # 最终修约
        print(f"Li={li:.3f}, C={c:.3f}, Xi={xi:.3f}, Yi={yi:.3f}, ")
        print(f"D_zh_p={d_zh_p:.3f}, 方位角={fangweijiao_shuchu}")

        return p_x,p_y


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
            return zhuanghao.strip().replace("K"," ").replace("k"," ").replace("+","")
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
        zuizhong_alpha = GeShiZhuanHuan(yuanshi_alpha)
        alpha_r=zuizhong_alpha.hanzi() # 两个都要赋值alpha_r        # 改。记得改
    params = {
        "x_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）X坐标: ")),
        "y_jd_zhu": float(input("请输入主交点（有R，L0的那个交点）Y坐标: ")),
        "R": float(input("请输入圆曲线半径R: ")),
        "L0": float(input("请输入缓和曲线长度L0: ")),
        "alpha_r": alpha_r,
        "jd_zhu_zhuanghao": float(input("请输入主交点桩号").replace("K"," ").replace("k"," ").replace("+","")),
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
        p1zhuanghao=input("请输入桩号")
        p_zhuanghao_float=float(p1zhuanghao.replace("K"," ").replace("k"," ").replace("+",""))
        if  qianzhijisuan.zh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hy_zhuanghao:
            p=zh.first_huanhe_p_5a(p_zhuanghao_float)
            print(f"第一缓和曲线上p点坐标为{p}")
        elif qianzhijisuan.hy_zhuanghao < p_zhuanghao_float <= qianzhijisuan.yh_zhuanghao:
            p = zh.yuanquxian_p_5bc(p_zhuanghao_float)
            print(f"圆曲线上p点坐标为{p}")
        elif qianzhijisuan.yh_zhuanghao < p_zhuanghao_float <= qianzhijisuan.hz_zhuanghao:
            p= zh.second_huanhe_p_5d(p_zhuanghao_float)
            print(f"第二缓和曲线上p点坐标为{p}")
        else:
            print("错误，桩号不能小于直缓点桩号！！！不能大于缓直点桩号！！！")
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
        ZhuangHaoJiSuan(**user_params)  # 字典解包传参
        .quxian_yao_su_1()
        .zhudianzhuanghao_2()
        .alpha_jd_zh_and_hz_3()
    )
    zh=qianzhijisuan.calculate_zh_coordinate_4a()
    hz=qianzhijisuan.calculate_hz_coordinate_4b()
    print(f"直缓点x{zh.x_zh},直缓y{zh.y_zh},缓直x{hz.x_hz},缓直y{hz.y_hz}")

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