import csv
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
from src.acquisition import run_acquisition
from src.algorithms import MultibandIntersection
from src.models import RandomForestOptimizer
from getresult import simulate_experiment

def run_design(n_initial, n_iters, design_sequence_count, data_path, threshold_lower, threshold_upper,update_signal):
    # 读取 CSV 文件
    data = pd.read_csv(data_path)

    # 假设特征在 DataFrame 的所有列，目标变量在最后一列
    X = data.iloc[:, :].to_numpy()  # 转换特征为 NumPy 数组
    all_ids = list(np.arange(0, len(X)))

    x_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaler = MinMaxScaler(feature_range=(-1, 1))

    scalers = [x_scaler, y_scaler]

    algorithms = {
        'Multiband': MultibandIntersection(user_algo_params={'scalers': scalers, 'threshold_bounds': [[threshold_lower, threshold_upper]]}),
    }
    algorithm = algorithms['Multiband']
    n_posterior_samples = 20


    metrics = {
        "MeanBAX": {"n_obtained": [], "jaccard_posterior_index": [], "switch_strategy": []},
    }

    strategy = "MeanBAX"

    # 终止条件：design_sequence_count
    np.random.seed(0)
    train_indices = list(np.random.choice(all_ids, n_initial))
    x_train = X[train_indices]

    update_signal.emit('Initial sequence:')
    ##################### NEgen1o 获取 x 对应 y 值 train
    with open("./negen1o/addition_squeue.txt", "w") as f:
        for idx in train_indices:
            sequence = X[idx]  # 除去 'Q' 列
            non_zero_values = sequence[sequence != 0]  # 获取非零数值
            non_zero_count = len(non_zero_values)  # 计算非零数值的个数
            values_str = ",".join(map(str, non_zero_values))  # 将非零数值转换为字符串，并用逗号连接
            f.write(f"1_{idx}_{non_zero_count} : {values_str}\n")

    y_train = simulate_experiment(train_indices,data_path)
    Y = None
    collected_ids = list(train_indices)
    n_obtained_list = []

    n_obtained_set = set()
    valid_sequences = []
    for idx in range(len(x_train)):
        q_value = y_train[idx]
        if threshold_lower <= q_value <= threshold_upper:
            valid_sequences.append((x_train[idx], q_value))

    # 如果有符合条件的序列，输出它们
    if valid_sequences:
        for sequence, q_value in valid_sequences:
            update_signal.emit(f"Sequence: {sequence}, Q value: {q_value}")
    else:
        update_signal.emit("The current iteration did not find a match for monomer addition sequence\n")

    for i in tqdm(range(n_iters)):
        random_forest = RandomForestOptimizer(n_jobs=1)
        if len(valid_sequences) >= design_sequence_count:
            update_signal.emit(
                f"Reached design sequence count of {design_sequence_count}. Terminating optimization.")  # 发出终止信息
            break  # Terminate optimization process
        update_signal.emit(f'Iteration {i+1} already started:')

        # Acquire next index
        x_train, y_train, model, collected_ids, acquisition_function, switch_strategy = run_acquisition(
            x_train, y_train, X, Y, strategy, algorithm, random_forest, collected_ids, n_posterior_samples,n_initial,data_path
        )

        # Calculate metrics
        n_obtained_list.append(collected_ids)
        n_obtained_set.update(collected_ids)

        # Filter the last n_initial samples that satisfy the condition
        valid_indices = []
        for idx in range(max(0, len(x_train) - n_initial), len(x_train)):  # Get the last n_initial samples
            if threshold_lower <= y_train[idx] <= threshold_upper:
                valid_indices.append(idx)
                valid_sequences.append((x_train[idx], y_train[idx]))



        # Output the corresponding x_train and y_train values that satisfy the condition
        if valid_indices:
            update_signal.emit(f"Iteration {i+1}: Satisfying points in addition sequence, Q value:")
            for idx in valid_indices:
                update_signal.emit(f"Sequence: {x_train[idx]}, Q: {y_train[idx]}")
        else:
            update_signal.emit("The current iteration did not find a match for monomer addition sequence\n")

        update_signal.emit('\n')  # 换行

    max_q_value = np.max([q_value for _, q_value in valid_sequences], initial=-np.inf)
    result_df = pd.DataFrame(x_train, columns=[f"r_{i + 1}" for i in range(x_train.shape[1])])
    result_df['Q'] = y_train  # Add Q values as the last column
    result_df.to_csv('result.csv', index=False)
    update_signal.emit(f'The monomer addition sequences and their corresponding Q values are saved in `result.csv')
    return len(valid_sequences), max_q_value


