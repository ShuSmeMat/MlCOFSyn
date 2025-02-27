import csv
import pandas as pd
import sys

def get_number_of_columns(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.shape[1]  # 返回列数
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# 获取从命令行传递的 CSV 文件路径
csv_file_path = sys.argv[1]  # 假设UI传递CSV路径作为命令行参数

# 获取CSV的列数
num_columns = get_number_of_columns(csv_file_path)

if num_columns is None:
    print("Error: Could not determine the number of columns from the input file.")
    sys.exit(1)

# 读取 addition_squeue.txt 数据
with open('addition_squeue.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 存储处理后的数据
experiments = []

for line in lines:
    # 拆分行，获取反应条件部分
    parts = line.split(':')
    if len(parts) < 2:
        continue

    # 获取数值部分并去除多余空格
    values_str = parts[1].strip()

    # 按逗号分隔数值
    values = [float(v) for v in values_str.split(',')]

    # 如果实验数量不足列数，则填充0
    if len(values) < num_columns:
        values.extend([0] * (num_columns - len(values)))

    experiments.append(values)

# 读取 all.txt 数据
with open('all.txt', 'r', encoding='utf-8') as file:
    all_lines = file.readlines()

# 创建 reaction_Q.csv 并写入数据
with open('reaction_Q.csv', 'w', newline='', encoding='utf-8') as csvfile_q:
    writer_q = csv.writer(csvfile_q)

    # 写入标题行，根据列数动态生成标题
    header = [f'r{i + 1}' for i in range(num_columns)] + ['Q']
    writer_q.writerow(header)

    for i, experiment in enumerate(experiments):
        if i < len(all_lines):
            # 从 all.txt 中读取对应的 Q 值
            line_parts = all_lines[i].strip().split()
            q_value = line_parts[-1]  # 假设最后一列为 Q 值

            row = experiment + [q_value]  # 合并实验数据和Q值
            writer_q.writerow(row)

# 创建 reaction_space.csv 并写入数据（不含 Q 值）
with open('reaction_space.csv', 'w', newline='', encoding='utf-8') as csvfile_space:
    writer_space = csv.writer(csvfile_space)

    # 写入标题行，根据列数动态生成标题
    header_space = [f'r{i + 1}' for i in range(num_columns)]
    writer_space.writerow(header_space)

    for experiment in experiments:
        row_space = experiment  # 不包含 Q 值
        writer_space.writerow(row_space)

print("Data has been successfully written to reaction_Q.csv and reaction_space.csv")
