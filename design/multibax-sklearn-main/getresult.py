import pandas as pd
import subprocess
import os

def simulate_experiment(proposed_experiments,csv_file_path):
    try:
        # 设置文件夹路径
        folder_path = 'negen1o'

        # 使用 subprocess 启动 C++ 程序（进入指定文件夹后执行）
        cpp_process = subprocess.Popen(['python', 'batch_sub_cpp.py'], cwd=folder_path)
        cpp_process.wait()

        # 启动 nuc_data.py 脚本
        nuc_process = subprocess.Popen(['python', 'nuc_data.py'], cwd=folder_path)
        nuc_process.wait()

        # 启动 data_process.py 脚本
        data_process_process = subprocess.Popen(['python', 'data_process.py',csv_file_path], cwd=folder_path)
        data_process_process.wait()

        # 在所有进程完成后，输出提示
        print("All processes have finished running.")
    except:
        print('stop')

    try:

        real_yield = pd.read_csv('negen1o/reaction_Q.csv')
        print("Proposed Experiment Details:")
        print(proposed_experiments)
    except:
        print('stop')
        return

    # 获取最后一列的倒数五行
    last_column = real_yield.columns[-1]  # 获取最后一列的列名
    result = real_yield[last_column].tail(5).values.reshape(-1,1)

    return result
