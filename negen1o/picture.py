# -*- coding: utf-8 -*-
from batch_sub_cpp import PATH
import os
import numpy as np
import matplotlib.pyplot as plt
name = PATH
# print(name)
addition_number = name[0].split('_')[-1]

for i in range(len(PATH)):
    os.chdir(PATH[i])

    if os.path.exists('./dia.txt'):
        output_txt = PATH[i] + ".txt"
        output_png = PATH[i]+ ".png"

        with open(output_txt, 'w+') as f:
            x = []
            y = []
            xx = []
            yy = []
            z = []

            try:
                # 读取数据
                with open('dia.txt', 'r') as f_2:
                    lines = f_2.readlines()
                    for line in lines:
                        x.append(float(line.split()[-1]))

                with open('hei.txt', 'r') as f_3:
                    lines = f_3.readlines()
                    for line in lines:
                        y.append(float(line.split()[-1]))

                with open('Percentage(%).txt', 'r') as f_4:
                    lines = f_4.readlines()

                    x = x[:-2]  # 去掉最后两行
                    y = y[:-2]
                    k = len(x) - 1
                    v = 0
                    j = 0

                    for line in lines:
                        while True:
                            if x[k] > float(line.split()[0]) and x[k] <= float(line.split()[1]):
                                v = v + x[k] ** 2 * y[k]
                                j = j + 1
                                k = k - 1
                                continue
                            else:
                                if v != 0:
                                    xx.append(float(line.split()[0]))  # 第二列
                                    yy.append(float(line.split()[1]))  # 第二列的范围上界（可选）
                                    z.append(float(line.split()[2]) * v / j)  # 第四列
                                    v = 0
                                    j = 0
                                break
                    z_1 = sum(z)

                # 写入数据
                for o in range(len(z)):
                    f.write(f"{xx[o]}  {yy[o]}  {z[o]}  {z[o] / z_1}\n")

                # **绘图**
                plt.figure(figsize=(4, 3), dpi=100)
                plt.fill_between(xx, 0, np.array(z) / z_1, color='red', alpha=0.3)
                plt.xlabel("Diameter (nm)")
                plt.ylabel("Volume Proportion")
                # plt.title(f"Crystal Distribution")
                plt.grid(False)
                plt.xlim(min(xx) - 10, max(xx) + 10)
                plt.ylim(0, max(np.array(z) / z_1) * 1.2)

                # 保存图片
                plt.savefig(output_png, bbox_inches='tight')
                print(os.path.abspath(output_png))  # 输出完整路径

                plt.close()

            except Exception as e:
                f.write('wrong')
                # print(f"错误: {e}")

        # 复制文件到 RSD 目录
        os.system(f"cp ./{output_txt} ../RSD")

    os.chdir("..")
# print(output_png)


# output_png = os.path.abspath(os.path.join(os.getcwd(), PATH[i] + ".png"))
# print(output_png)