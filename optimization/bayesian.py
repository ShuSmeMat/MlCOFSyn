import pandas as pd
import numpy as np
import os
from getresult import simulate_experiment
from random_forest import Randomforest
from acquisition import expected_improvement
import joblib

np.random.seed(1)
pd.set_option('display.max_columns', None)
# 设置最大行数为 None，表示显示所有行
pd.set_option('display.max_rows', None)

class Objective:
    def __init__(self, results, target=-1):
        self.results = results
        self.target = target
        self.domain = None


def bayesian_optimization(conditions,conditions_file_path,csv_file_path='pre_data.csv', max_iterations=30, stability_threshold=5,
                          num_best_conditions=5, update_result_text=None, update_max_value_text=None, send_sequence=None):
    # 检查 conditions
    update_result_text('--------------------Optimization started--------------------\n')
    if conditions is None or conditions.empty:
        raise ValueError("The conditions parameter cannot be None or empty.")

    if os.path.exists(csv_file_path):
        selected_conditions = pd.read_csv(csv_file_path, index_col=0)
        x = selected_conditions.iloc[:, :-1].values
        y = selected_conditions['Q'].values
        rf_model = Randomforest(x, y)
        rf_model.fit()
    else:
        n_initial_conditions = num_best_conditions  # 初始选择的条件个数
        random_indices = np.random.choice(conditions.index, size=n_initial_conditions, replace=False)
        selected_conditions = conditions.loc[random_indices].copy()

        # 写入初始条件到文件
        with open("./negen1o/addition_squeue.txt", "w") as f:
            for idx, row in selected_conditions.iterrows():
                sequence = row.values[:]  # 除去 'Q' 列
                non_zero_values = sequence[sequence != 0]  # 获取非零数值
                non_zero_count = len(non_zero_values)  # 计算非零数值的个数
                values_str = ",".join(map(str, non_zero_values))  # 将非零数值转换为字符串，并用逗号连接
                f.write(f"1_{idx}_{non_zero_count} : {values_str}\n")

        first_result = simulate_experiment(selected_conditions,conditions_file_path)
        x = selected_conditions.values
        y = first_result
        first_condition = conditions.loc[random_indices].copy()
        first_condition.loc[:, 'Q'] = first_result

        update_result_text('-------------------------------initial sequence-------------------------------')
        update_result_text(f'{first_condition}\n')
        rf_model = Randomforest(x, y)
        rf_model.fit()

    all_selected_indices = set(selected_conditions.index)
    selected_conditions['Q'] = y

    objective = Objective(selected_conditions)

    previous_max_value = -np.inf
    stability_count = 0

    all_results = []

    for iteration in range(max_iterations):
        remaining_conditions = conditions[~conditions.index.isin(all_selected_indices)]
        candidate_conditions = remaining_conditions

        # 更新目标对象的 domain 属性
        objective.domain = candidate_conditions
        # 计算 EI
        ei_values = expected_improvement(rf_model, objective)

        # 选择 EI 最高的前 num_best_conditions 个条件
        next_experiment_indices = np.argsort(ei_values)[-num_best_conditions:]
        next_experiment_conditions = candidate_conditions.iloc[next_experiment_indices]
        next_conditions = next_experiment_conditions.copy()

        # 写入选择的条件到文件
        with open("./negen1o/addition_squeue.txt", "w") as f:
            for idx, row in next_conditions.iterrows():
                sequence = row.values[:]  # 除去 'Q' 列
                non_zero_values = sequence[sequence != 0]  # 获取非零数值
                non_zero_count = len(non_zero_values)  # 计算非零数值的个数
                values_str = ",".join(map(str, non_zero_values))  # 将非零数值转换为字符串，并用逗号连接
                f.write(f"1_{idx}_{non_zero_count} : {values_str}\n")

        next_results = simulate_experiment(next_conditions,conditions_file_path)
        next_experiment_conditions = candidate_conditions.iloc[next_experiment_indices].copy()
        next_experiment_conditions.loc[:, 'Q'] = next_results

        combined_conditions = pd.concat([selected_conditions, next_experiment_conditions])
        combined_results = np.concatenate([y, next_results])
        objective.results = combined_conditions

        rf_model = Randomforest(combined_conditions.iloc[:, :-1], combined_results)
        rf_model.fit()

        max_result_index = np.argmax(next_results)
        max_value = next_results[max_result_index]


        # 如果提供了回调函数，调用它来更新 UI 中的文本框
        if update_result_text:
            update_result_text(f"--------------------------------- Iteration {iteration + 1}---------------------------------:\n")
            update_result_text(f"Max Result: {max_value}\n")
            update_result_text(f"Optimal Conditions: {next_experiment_conditions}\n")

        selected_conditions = combined_conditions
        y = combined_results
        all_selected_indices.update(combined_conditions.index)

        all_results.extend(next_results)

        if max_value < previous_max_value:
            stability_count += 1
        elif max_value + 50 > previous_max_value:
            stability_count = 0
            previous_max_value = max_value

        if stability_count >= stability_threshold:
            print("Stopping criterion met: maximum value has stabilized.")
            break

    selected_conditions['Q'] = y
    selected_conditions.to_csv(csv_file_path, index=True)

    print(f"Save all conditions to {csv_file_path}")
    max_q_index = np.argmax(y)  # y 是最后的目标值数组，即 'Q'
    max_q_value = y[max_q_index]  # 最大 Q 值
    max_q_condition = selected_conditions.iloc[max_q_index, :-1]  # 找到最大 Q 值对应的条件（去除 Q 列）

    # 获取非零项
    non_zero_values = max_q_condition[max_q_condition != 0].values  # 仅保留非零项
    non_zero_values_str = ",".join(map(str, non_zero_values))  # 转换成逗号分隔的字符串

    # 输出最大 Q 值对应的条件
    if update_result_text:
        update_result_text(f"Max Q value: {max_q_value}\n")
        update_result_text(f"monomer addition sequence  (Max Q value): {non_zero_values_str}\n")

    # 将最大值传递给 update_max_value_text
    if update_max_value_text:
        update_max_value_text(max_q_value)
    if send_sequence:
        send_sequence(non_zero_values_str)
    selected_conditions.to_csv('result.csv', index=False)
    update_result_text(f'The monomer addition sequences and their corresponding Q values are saved in `result.csv`')
