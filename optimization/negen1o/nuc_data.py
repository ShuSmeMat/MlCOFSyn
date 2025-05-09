# -*- coding: utf-8 -*-
import os
import glob
import time
from batch_sub_cpp import PATH  # 假设由 batch 脚本动态生成的路径列表
theta1 = 1
theta2 = 2

with open("all.txt", 'w') as f:
    for i in range(len(PATH)):
        os.chdir(PATH[i])
        path = glob.glob(r'*.out')
        print(path[0])
        x = []
        y = []
        try:
            with open(path[0], 'r', encoding='gb18030') as f_1:
                line = f_1.readlines()
                it = line[0].split()[1]
                step_all = line[-4].split()[0]
                t_all = line[-4].split()[1]
                v = line[-4].split()[2]
                d_max = line[-4].split()[4]

            with open('dia.txt', 'r') as f_2:
                lines = f_2.readlines()
                d_adv = lines[-2].split()[1]
                for line in lines:
                    x.append(float(line.split()[-1]))
                dia_max = lines[0].split()[1]
                rsd = lines[-1].split()[1]

            with open('hei.txt', 'r') as f_3:
                lines = f_3.readlines()
                h_adv = lines[-2].split()[1]
                h_rsd = lines[-1].split()[1]
                for line in lines:
                    y.append(float(line.split()[-1]))

            # 使用第二个脚本中的方式计算 d_rsd
            with open('Percentage(%).txt', 'r') as f_4:
                lines = f_4.readlines()
                z = []
                x = x[:-2]
                y = y[:-2]
                dia = []
                p = []
                k = len(x) - 1
                # print(len(x))
                v = 0
                j = 0
                dia_0 = 0
                for line in lines:
                    while True:
                        if x[k] > float(line.split()[0]) and x[k] <= float(line.split()[1]):
                            dia_0 = dia_0 + x[k]
                            v = v + x[k] ** 2 * y[k]
                            j = j + 1
                            k = k - 1
                            continue
                        else:
                            if v != 0:
                                dia.append(dia_0 / j)
                                z.append(float(line.split()[2]) * (v) * (dia_0 / j))
                                p.append(float(line.split()[2]) * (v))
                                # f.write(PATH[i]+'  '+str(v/j)+' '+line.split()[2]+' '+str(float(line.split()[2])*v/j)+'\n')
                                v = 0
                                j = 0
                                dia_0 = 0
                            break
                z_1 = sum(z) / sum(p)
                asw = 0
                for bb in range(len(z)):
                    asw = asw + p[bb] * (dia[bb] - z_1) ** 2
                z_f = (asw / sum(p)) ** 0.5

                print(str(z_f / z_1 ))
                d_rsd = z_f / z_1  # 使用第二个脚本精确的计算方式

            with open('dia_hei.txt', 'r') as f_5:
                line = f_5.readlines()
                dh_adv = line[-6].split()[1]
                dh_rsd = line[-1].split()[1]
                monomer_addition_mol = line[-2].split()[1]
                monomer_consumption_mol = line[-3].split()[1]
                total_nuclei_volume = line[-4].split()[2]
                total_addition_volume = line[-2].split()[2]
            dia_max_3 = round(float(dia_max), 4)
            if z_f / z_1 != 0:
                Q = (dia_max_3)**theta1 / (z_f / z_1)**theta2
            else:
                Q = 'inf'

            f.write(
                str(PATH[i]) + '   ' +
                str(step_all) + ' ' + str(it) + ' ' + str(t_all) + ' ' + str(v) + ' ' +
                dia_max + '   ' + str(d_adv) + ' ' + str(z_f / z_1) + ' ' + str(h_adv) + ' ' +
                str(h_rsd) + ' ' + str(dh_adv) + ' ' + str(dh_rsd) + '   ' +
                str(monomer_addition_mol) + '    ' + str(monomer_consumption_mol) + '    ' +
                str(total_nuclei_volume) + '  ' + str(total_addition_volume) + '   ' + str(Q) + '\n'
            )

            print(dia_max)
            print(z_f / z_1)
            print(dh_rsd)

        except Exception as e:
            f.write(PATH[i] + ' waiting' + '\n')
            print(f"Exception occurred for {PATH[i]}: {e}")
        os.chdir("..")
