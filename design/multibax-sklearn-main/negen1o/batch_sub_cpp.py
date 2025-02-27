import os
import shutil
import subprocess
import psutil
from multiprocessing import Process

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


def run_program(foldername, core_id):
    print(f"Compiling and running in {foldername} on core {core_id}...")

    os.chdir(foldername)

    # 编译
    compile_process = subprocess.run(["g++", 'NEgen1.cpp', "-o", 'NEgen1.exe'])
    if compile_process.returncode != 0:
        print(f"Compilation failed for {foldername}, please check the C++ configuration!")
    else:
        print(f"[{foldername}] Compilation successful, starting the program...")

        # 创建输出文件
        with open(f"{foldername}.out", "w", encoding="utf-8") as out_file:
            with subprocess.Popen(['NEgen1.exe'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True) as proc:
                # 获取当前进程的 psutil 进程对象
                p = psutil.Process(proc.pid)

                # 设置 CPU 亲和力为指定的核心（core_id）
                p.cpu_affinity([core_id])

                # 打印当前进程的 CPU 亲和性
                print(f"[{foldername}] CPU affinity: {p.cpu_affinity()}")

                for line in proc.stdout:
                    # 同时打印到控制台和文件
                    print(line, end="")
                    out_file.write(line)

        print(f"[{foldername}] is running, data saved to {foldername}.out")

    os.chdir("..")


def alter(tag, scale_factors, num, param):
    initial_condition = {}
    compile_folders = []  # 用来存储需要编译的文件夹

    # 获取系统可用的 CPU 核心数量
    total_cores = psutil.cpu_count(logical=False)  # 物理核心数量
    print(f"Total physical cores: {total_cores}")

    # 1) 先创建所有文件夹及文件，不进行编译
    for i in range(num):
        foldername = f'./{tag}_{str(w[i][0])}'
        PATH.append(foldername)

        if Create_folder(foldername):
            cofp_path = os.path.join(foldername, 'cof_parameter.h')
            with open('./cof_parameter.h', 'r', encoding='gbk') as f_in, open(cofp_path, 'w', encoding='gbk') as f_out:
                lines = f_in.readlines()
                for line in lines:
                    # 进行文件内容替换
                    # 1) V_initial
                    if "double V_initial =" in line:
                        old_part = line.split(';')[0].split()[-1]
                        new_part = param.get("V_initial", "0")
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

            # 复制相关的 C++ 文件
            shutil.copy2('NEgen1.cpp', foldername)
            shutil.copy2('cof_function.h', foldername)

            # 将文件夹添加到 compile_folders 列表中
            compile_folders.append(foldername)

    # 2) 使用 multiprocessing 并行启动每个程序，并为每个程序分配不同的核心
    processes = []
    for idx, foldername in enumerate(compile_folders):
        # 为每个进程分配一个核心，确保每个任务使用不同的核心
        core_id = idx % total_cores  # 如果任务数量超过核心数，使用取余操作循环分配核心
        p = Process(target=run_program, args=(foldername, core_id))
        p.start()
        processes.append(p)

    # 等待所有进程完成
    for p in processes:
        p.join()


# ============== 主程序入口 ===============

# 1) 读取 parameter.txt
param = read_parameters("parameter.txt")

# 2) 读取 addition_squeue.txt ->
w = {}
j = 0
with open('./addition_squeue.txt', 'r') as f:
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
