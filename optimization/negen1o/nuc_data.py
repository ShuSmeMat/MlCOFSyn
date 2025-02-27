# -*- coding: utf-8 -*-
from batch_sub_cpp import PATH
import os
import glob

# 用户输入 theta1 和 theta2

with open("all.txt", 'w') as f:
    for i in range(len(PATH)):
        os.chdir(PATH[i])
        # print(os.getcwd())
        path = glob.glob(r'*.out')
        print(path[0])
        try:
            with open(path[0], 'r', encoding='gb18030') as f_1:
                line = f_1.readlines()
                it = line[0].split()[1]
                step_all = line[-4].split()[0]
                t_all = line[-4].split()[1]
                v = line[-4].split()[2]
                d_max = float(line[-4].split()[4])  # 将 d_max 转换为浮点数以用于计算

            with open('dia.txt', 'r') as f_2:
                line = f_2.readlines()
                d_adv = line[-2].split()[1]
                d_rsd = float(line[-1].split()[1])  # 将 d_rsd 转换为浮点数以用于计算

            with open('hei.txt', 'r') as f_3:
                line = f_3.readlines()
                h_adv = line[-2].split()[1]
                h_rsd = line[-1].split()[1]

            with open('dia_hei.txt', 'r') as f_4:
                line = f_4.readlines()
                dh_adv = line[-6].split()[1]
                dh_rsd = line[-1].split()[1]
                monomer_addition_mol = line[-2].split()[1]
                monomer_consumption_mol = line[-3].split()[1]
                total_nuclei_volume = line[-4].split()[2]
                total_addition_volume = line[-2].split()[2]

            # 计算 Q = d_max的theta1次 / d_rsd的theta2次
            if d_rsd != 0:  # 避免除以零的情况
                Q = d_max / d_rsd
            else:
                Q = 'inf'  # 如果 d_rsd 为0，则返回无穷大或其他适当的标记

            # 写入数据到 all.txt，包括新的 Q 列
            f.write(PATH[i] + '   ' + step_all + ' ' + it + ' ' + t_all + ' ' + v + ' ' +
                    str(d_max) + '   ' + d_adv + ' ' + str(d_rsd) + ' ' + h_adv + ' ' +
                    h_rsd + ' ' + dh_adv + ' ' + dh_rsd + '   ' +
                    monomer_addition_mol + '    ' + monomer_consumption_mol + '    ' +
                    total_nuclei_volume + '  ' + total_addition_volume + '   ' + str(Q) + '\n')

        except Exception as e:
            f.write(PATH[i] + ' waiting' + '\n')
            print(f"Exception occurred for {PATH[i]}: {e}")
        os.chdir("..")
