import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ConstantKernel, Matern, RBF
import pickle


class MGPR:
    """
    Class for multiple independent sklearn Gaussian Process Regression models.
    """

    def __init__(
        self, kernel_list: list, n_restarts_optimizer: int = 1
    ):  # TODO a list of what?
        self.models = [
            GaussianProcessRegressor(
                kernel=k, n_restarts_optimizer=n_restarts_optimizer
            )
            for k in kernel_list
        ]

    def fit(self, X: np.ndarray, y: np.ndarray):
        for i, model in enumerate(self.models):
            model.fit(X, y[:, i])

    # posterior mean for each measurable property
    def predict(self, X: np.ndarray):
        posterior_means = []
        posterior_stds = []
        for model in self.models:
            posterior_mean, posterior_std = model.predict(X, return_std=True)
            posterior_means.append(posterior_mean)
            posterior_stds.append(posterior_std)
            t1=np.array(posterior_means).T
            t2=np.array(posterior_means)
        return np.array(posterior_means).T, np.array(posterior_stds).T

    # generate posterior samples for each measurable property
    def sample_y(self, x_domain: np.ndarray, n_samples: int) -> np.ndarray:
        posterior_samples_list = []

        for model in self.models:
            posterior_samples = model.sample_y(x_domain, n_samples)
            posterior_samples_list.append(posterior_samples)

        posterior_samples_array = np.moveaxis(np.array(posterior_samples_list), 1, 0)

        return posterior_samples_array

    def save(self, filename):
        print(f"Saving class instance to {filename}...")
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
            print("Class instance saved successfully!")
        except Exception as e:
            print(f"Failed to save class instance: {e}")

    @classmethod
    def load(cls, filename):
        print(f"Loading class instance from {filename}...")
        try:
            with open(filename, "rb") as f:
                instance = pickle.load(f)
            print("Class instance loaded successfully!")
            return instance
        except Exception as e:
            print(f"Failed to load class instance: {e}")
            return None


def fit_matern_hypers(
    x_train: np.ndarray,
    y_train: np.ndarray,
    kernel_list: list,  # TODO list of what?
    n_restarts_optimizer: int = 30,
) -> list:  # TODO list of what?
    """GP hyperparameter fitting for a kernel of the form ConstantKernel() * Matern() + WhiteNoise()

    Args:
        x_train (np.ndarray): current collected x data
        y_train (np.ndarray): current collected y data
        kernel_list (list): list of kernels for different measured properties

    Returns:
        list: list of kernels with fitted hyperparameters
    """
    multi_gpr = MGPR(kernel_list=kernel_list, n_restarts_optimizer=n_restarts_optimizer)
    multi_gpr.fit(x_train, y_train)  # update posterior distribution and fit GP hypers

    kernels = []
    for model in multi_gpr.models:
        params = model.kernel_.get_params()
        alpha = params["k1__k1__constant_value"]  # kernel variance
        ls = params["k1__k2__length_scale"]  # anisotropic lengthscales
        noise = params["k2__noise_level"]  # likelihood variance

        # this is neccesary to force all posterior samples to have the same GP hyperparameters
        k = ConstantKernel(
            constant_value=alpha, constant_value_bounds="fixed"
        ) * Matern(
            nu=5 / 2, length_scale=ls, length_scale_bounds="fixed"
        ) + WhiteKernel(
            noise, noise_level_bounds="fixed"
        )
        kernels.append(k)

    def save_model(self, fname):
        pass

    return kernels

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle

class RandomForestOptimizer:
    """
    Class for optimizing multiple independent sklearn Random Forest models.
    """

    def __init__(self, n_jobs: int = -1):
        """
        Initialize the optimizer with a grid of parameters to search over.

        Args:
            param_grid (dict): The parameter grid to search over.
            n_jobs (int): Number of jobs to run in parallel (-1 means using all processors).
        """

        self.n_jobs = n_jobs
        self.best_models = None

    # def fit(self, X: np.ndarray, y: np.ndarray):
    #     """
    #     Fit the random forest models using grid search to find the best parameters.
    #
    #     Args:
    #         X (np.ndarray): The input features.
    #         y (np.ndarray): The target values. Each column represents one output dimension.
    #     """
    #     n_outputs = y.shape[1]
    #     self.best_models = []
    #
    #     for i in range(n_outputs):
    #         print(f"Optimizing output {i+1}/{n_outputs}")
    #         rf = RandomForestRegressor()
    #         gscv = GridSearchCV(
    #             rf,
    #             param_grid=self.param_grid,
    #             n_jobs=self.n_jobs,
    #             verbose=1,
    #             cv=2
    #         )
    #         gscv.fit(X, y[:, i])
    #         self.best_models.append(gscv.best_estimator_)
    #
    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit the random forest models without grid search, using specified parameters.

        Args:
            X (np.ndarray): The input features.
            y (np.ndarray): The target values. Each column represents one output dimension.
        """
        n_outputs = y.shape[1]
        self.best_models = []

        for i in range(n_outputs):

            # 手动设置参数或使用默认参数
            rf = RandomForestRegressor(
                n_estimators=100,  # 您可以根据需要调整参数
                max_depth=None,  # 您可以根据需要调整参数
                random_state=42  # 确保结果可重复
            )
            rf.fit(X, y[:, i])
            self.best_models.append(rf)
    def predict(self, X: np.ndarray):
        """
        Predict using the best models found in the grid search.

        Args:
            X (np.ndarray): The input features to predict for.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Predicted values and their associated uncertainties.
        """
        predictions = []
        uncertainties = []

        for model in self.best_models:
            # 收集所有子模型（树）的预测
            all_tree_predictions = np.array([tree.predict(X) for tree in model.estimators_])
            # 均值作为最终预测
            mean_prediction = all_tree_predictions.mean(axis=0)
            # 标准差作为不确定度
            std_dev_prediction = all_tree_predictions.std(axis=0)

            predictions.append(mean_prediction)
            uncertainties.append(std_dev_prediction)

        # 将结果转置使得每一行是一个样本的所有输出
        return np.array(predictions).T, np.array(uncertainties).T

    def sample_y(self, x_domain: np.ndarray, n_samples: int) -> np.ndarray:
        """
        Generate posterior samples for each measurable property using random forests.

        Args:
            x_domain (np.ndarray): The input features to sample for.
            n_samples (int): The number of samples to generate.

        Returns:
            np.ndarray: Generated samples, with shape (n_samples, n_outputs, n_samples).
        """
        posterior_samples_list = []

        for model in self.best_models:
            # Collect all tree predictions
            tree_predictions = np.array([tree.predict(x_domain) for tree in model.estimators_])

            # Draw samples for the input domain, each consisting of a random selection of these predictions
            samples = np.zeros((n_samples, x_domain.shape[0]))
            for i in range(n_samples):
                # Randomly choose predictions from the ensemble for each input
                sample_indices = np.random.choice(tree_predictions.shape[0], size=x_domain.shape[0], replace=True)
                samples[i, :] = tree_predictions[sample_indices, np.arange(x_domain.shape[0])]

            posterior_samples_list.append(samples)

        # Reorder dimensions to match the expected output shape
        posterior_samples_array = np.moveaxis(np.array(posterior_samples_list), 1, 0)

        return posterior_samples_array

    def save(self, filename):
        """
        Save the optimizer to a file.

        Args:
            filename (str): The path to the file where the optimizer should be saved.
        """
        print(f"Saving optimizer to {filename}...")
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
            print("Optimizer saved successfully!")
        except Exception as e:
            print(f"Failed to save optimizer: {e}")

    @classmethod
    def load(cls, filename):
        """
        Load the optimizer from a file.

        Args:
            filename (str): The path to the file from which the optimizer should be loaded.

        Returns:
            RandomForestOptimizer: The loaded optimizer instance.
        """
        print(f"Loading optimizer from {filename}...")
        try:
            with open(filename, "rb") as f:
                instance = pickle.load(f)
            print("Optimizer loaded successfully!")
            return instance
        except Exception as e:
            print(f"Failed to load optimizer: {e}")
            return None

