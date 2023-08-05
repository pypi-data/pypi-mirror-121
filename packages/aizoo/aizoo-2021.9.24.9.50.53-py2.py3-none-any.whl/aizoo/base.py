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

    def __init__(self, params=None, fit_params=None, weight_func=None):
        self.params = params
        self.fit_params = fit_params if fit_params is not None else {}
        self.weight_func = weight_func

    @abstractmethod
    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        """
        valid_predict, test_predict

        hasattr(clf, 'predict')

        train_weights = 1 / np.square(y_train)
        val_weights = 1 / np.square(y_val)
        """
        raise NotImplementedError

    def run(self, X, y, X_test=None, feval=None, cv=5, split_seed=777, oof_file=None):
        num_classes = len(set(y))
        logger.info(f'nunique(y): {num_classes}')

        X_test = X_test if X_test is not None else X[:66]

        if num_classes > 128:  # 目标值多于128个就认为是回归问题
            self.oof_train_proba = np.zeros(len(X))
            self.oof_test_proba = np.zeros(len(X_test))
            _ = enumerate(ShuffleSplit(cv, random_state=split_seed).split(X, y))

        else:
            self.oof_train_proba = np.zeros([len(X), num_classes])
            self.oof_test_proba = np.zeros([len(X_test), num_classes])
            _ = enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_seed).split(X, y))

        for n_fold, (train_index, valid_index) in _:
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]

            ##############################################################
            valid_predict, test_predict = self.fit_predict(X_train, y_train, X_valid, y_valid, X_test)
            ##############################################################

            self.oof_train_proba[valid_index] = valid_predict
            self.oof_test_proba += test_predict / cv

        if self.oof_test_proba.ndim == 2:
            self.oof_train_proba = self.oof_train_proba[:, 1]
            self.oof_test_proba = self.oof_test_proba[:, 1]

        self.oof_train_test = np.r_[self.oof_train_proba, self.oof_test_proba]  # 方便后续stacking

        if feval is not None:
            self.oof_score = feval(y, self.oof_train_proba)

            print(f"\033[94mCV Sorce: {self.oof_score} ended at {time.ctime()}\033[0m\n")

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

    def plot_feature_importances(self):
        pass
