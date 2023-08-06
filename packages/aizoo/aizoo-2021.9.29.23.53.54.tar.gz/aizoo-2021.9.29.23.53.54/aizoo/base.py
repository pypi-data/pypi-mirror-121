#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : aizoo.
# @File         : oof
# @Time         : 2021/9/14 下午3:42
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : todo: 增加nn模型


from meutils.pipe import *
from sklearn.model_selection import ShuffleSplit, StratifiedKFold


class OOF(object):

    def __init__(self, params=None, fit_params=None, weight_func=None, task='Classifier', importance_type='split'):
        """

        @param params:
        @param fit_params:
        @param weight_func:
        @param task: Classifier or Regressor
        """
        self.params = params if params is not None else {}
        self.fit_params = fit_params if fit_params is not None else {}
        self.weight_func = weight_func

        self.task = task.title()

        self._estimators = []  # 每一折的模型
        self._importance_type = importance_type
        self.feature_importances_ = None

    @abstractmethod
    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        raise NotImplementedError

    def predict(self, X):
        preds = []

        for estimator in self._estimators:
            if hasattr(estimator, 'predict_proba'):
                preds.append(estimator.predict_proba(X))
            else:
                preds.append(estimator.predict(X))

        return np.array(preds).mean(0)

    def fit(self, X, y, X_test=None, feval=None, cv=5, split_seed=777, oof_file=None):

        X_test = X_test if X_test is not None else X[:66]

        self.feature_importances_ = np.zeros((cv, X.shape[1]))

        if self.task == 'Regressor':  # 目标值多于128个就认为是回归问题 len(set(y)) > 128
            self.oof_train_proba = np.zeros(len(X))
            self.oof_test_proba = np.zeros(len(X_test))
            _ = enumerate(ShuffleSplit(cv, random_state=split_seed).split(X, y))

        elif self.task == 'Classifier':
            num_classes = len(set(y))
            assert num_classes < 128, "是否是分类问题"
            self.oof_train_proba = np.zeros([len(X), num_classes])
            self.oof_test_proba = np.zeros([len(X_test), num_classes])
            _ = enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_seed).split(X, y))
        else:
            raise ValueError("TaskTypeError⚠️")

        valid_metrics = []
        for n_fold, (train_index, valid_index) in _:
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]

            ##############################################################
            valid_predict, test_predict = self.fit_predict(X_train, y_train, X_valid, y_valid, X_test)
            ##############################################################

            self.oof_train_proba[valid_index] = valid_predict
            self.oof_test_proba += test_predict / cv

            # 记录特征重要性
            self.feature_importances_[n_fold] = self._get_imp(self._estimators[-1], X_train, self._importance_type)

            if feval is not None:
                if self.oof_test_proba.shape[1] == 2:  # todo: 目前不支持多分类
                    valid_metrics.append(feval(y_valid, valid_predict[:, 1]))  # 二分类
                else:
                    valid_metrics.append(feval(y_valid, valid_predict))  # 回归

        if self.oof_test_proba.shape[1] == 2:
            self.oof_train_proba = self.oof_train_proba[:, 1]
            self.oof_test_proba = self.oof_test_proba[:, 1]

        self.oof_train_test = np.r_[self.oof_train_proba, self.oof_test_proba]  # 方便后续stacking

        if feval is not None:
            self.oof_score = feval(y, self.oof_train_proba)

            print("\n\033[94mScore Info:\033[0m")
            print(f"\033[94m     {cv:>2} CV: {self.oof_score:.6f}\033[0m")

            _ = np.array(valid_metrics)
            print(f"\033[94m     Valid: {_.mean():.6f} +/- {_.std():.6f} \033[0m\n")

            return self.oof_score

        if oof_file is not None:
            pd.DataFrame({'oof': self.oof_train_test}).to_csv(oof_file, index=False)

    @classmethod
    def opt_cv(cls, X, y, X_test=None, cv_list=range(3, 16), params=None, **run_kwargs):
        """todo: 折数优化"""

        scores = []
        for cv in tqdm(cv_list, desc='opt cv'):  # range(3, 16):
            oof = cls(params)
            oof.run(X, y, X_test, **run_kwargs)
            scores.append((oof.oof_score, cv, oof))

        return sorted(scores)[::-1]

    def plot_feature_importances(self, feature_names=None, topk=20, figsize=None, pic_name=None):
        import seaborn as sns
        import matplotlib.pyplot as plt

        columns = ['Importances', 'Features']
        importances = self.feature_importances_.mean(0)

        if feature_names is None:
            feature_names = list(map(lambda x: f'F_{x}', range(len(importances))))

        _ = sorted(zip(importances, feature_names), reverse=True)
        self.df_feature_importances = pd.DataFrame(_, columns=columns)

        plt.figure(figsize=(14, topk // 5) if figsize is None else figsize)
        sns.barplot(*columns, data=self.df_feature_importances[:topk])
        plt.title('Features Importances\n')
        plt.tight_layout()
        if pic_name is not None:
            plt.savefig(f'importances_{self.oof_score}.png')

    @staticmethod
    def _get_imp(estimator, X=None, importance_type=None):

        if importance_type in (None, 'tree', 'gini', 'split', 'gain'):
            imp = estimator.feature_importances_

        elif importance_type in ('shap', 'Shap'):
            imp = ...

        else:
            imp = ...

        return imp
