import os
import shutil
import subprocess
import sys
PATH = []

def Create_folder(foldername):
    foldername = foldername.strip().rstrip("\\")
    if not os.path.exists(foldername):
        os.makedirs(foldername)
        return True
    else:
        return False

def read_parameters(param_file):
    """
    读取 parameter.txt，将其中 'key=value' 形式的行解析成字典。
    注释行（以 # 开头）和空行会跳过。
    """
    param = {}
    with open(param_file, 'r', encoding='utf-8') as pf:
        for line in pf:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                param[k] = v
    return param

def alter(tag, scale_factors, num, param):
    initial_condition = {}
    processes = []  # 用于保存所有启动的进程对象
    for i in range(num):
        foldername = f'./{tag}_{str(w[i][0])}'
        PATH.append(foldername)

        if Create_folder(foldername):
            cofp_path = os.path.join(foldername, 'cof_parameter.h')
            with open('./cof_parameter.h', 'r', encoding='gbk') as f_in, open(cofp_path, 'w', encoding='gbk') as f_out:
                lines = f_in.readlines()
                for line in lines:
                    # 先检查是否包含我们要替换的关键词

                    # 1) V_initial
                    if "double V_initial =" in line:
                        old_part = line.split(';')[0].split()[-1]  # 取到"0"这样的旧值
                        new_part = param.get("V_initial", "0")     # 如果 param 中没写，就用 "0" 作为默认
                        line = line.replace(old_part, new_part)
                        initial_condition["V_initial"] = new_part

                    # 2) con_initial
                    if "double con_initial =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("con_initial", "0")
                        line = line.replace(old_part, new_part)
                        initial_condition["con_initial"] = new_part

                    # 3) hei_initial
                    if "double hei_initial =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("hei_initial", "0")
                        line = line.replace(old_part, new_part)
                        initial_condition["hei_initial"] = new_part

                    # 4) dia_initial
                    if "double dia_initial =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("dia_initial", "0")
                        line = line.replace(old_part, new_part)
                        initial_condition["dia_initial"] = new_part

                    # 5) addition_interval
                    if "addition_interval =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("addition_interval", "1200")
                        line = line.replace(old_part, new_part)
                        initial_condition["addition_interval"] = new_part

                    # 同时保留你原先对 addition_number / C_hhtp_add 等的逻辑
                    # 6) addition_number
                    if "addition_number =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = scale_factors[i][2]
                        line = line.replace(old_part, new_part)
                        initial_condition["addition_number"] = new_part

                    # 7) C_hhtp_add
                    if "C_hhtp_add =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("C_hhtp_add", "0.002")  # 读取param字典中的值，默认值为0.002
                        line = line.replace(old_part, new_part)  # 用新值替换
                        initial_condition["C_hhtp_add"] = new_part  # 保存修改值

                    # 8) double V_add[]
                    if "double V_add[] " in line:
                        old_vals = line.split('{')[1].split('}')[0]
                        new_vals = scale_factors[i][1]
                        line = line.replace(old_vals, str(new_vals))
                        initial_condition["V_add"] = str(new_vals)

                    f_out.write(line)

            # run job（在 HPC 上用 slurm）
            for key, value in initial_condition.items():
                print(f"{key}: {value}")
            shutil.copy2('NEgen1.cpp', foldername)
            shutil.copy2('cof_function.h', foldername)

            os.chdir(foldername)
            compile_process = subprocess.run(["g++", 'NEgen1.cpp', "-o", 'NEgen1.exe'])
            if compile_process.returncode != 0:
                print("Compilation failed, please check the c++ configuration！")
            else:
                print(f"[{foldername}]Compilation is successful, start running the program...")

                # 创建并启动进程
                proc = subprocess.Popen(['NEgen1.exe'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
                processes.append(proc)  # 保存进程对象

                # 输出处理
                with open(f"{foldername}.out", "w", encoding="utf-8") as out_file:
                    for line in proc.stdout:
                        print(line, end="")
                        out_file.write(line)

                print(f"[{foldername}]is running，data saved to {foldername}.out")
            os.chdir("..")
        return processes  # 返回所有进程对

# ============== 主程序入口 ===============

# 1) 读取 parameter.txt
param = read_parameters("parameter.txt")

# 2) 读取 addition_squeue.txt -> w
w = {}
j = 0
with open('./addition_squeue.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        try:
            w[j] = []
            w[j].append(line.split()[0])  # e.g. "1_1_1"
            w[j].append(line.split()[2])  # e.g. "0.002,0.002,0.003" (V_add)
            line_name = line.split()[0]
            line_name = line_name.split('_')[-1]
            w[j].append(line_name)
            j = j + 1
        except:
            break
num = j

# 3) 调用 alter
alter("nuc", w, num, param)
