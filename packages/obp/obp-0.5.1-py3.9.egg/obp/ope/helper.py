# Copyright (c) Yuta Saito, Yusuke Narita, and ZOZO Technologies, Inc. All rights reserved.
# Licensed under the Apache 2.0 License.

from typing import Optional

import numpy as np
from sklearn.utils import check_scalar


def estimate_bias_in_ope(
    reward: np.ndarray,
    iw: np.ndarray,
    iw_hat: np.ndarray,
    q_hat: Optional[np.ndarray] = None,
) -> float:
    """Helper to estimate a bias in OPE.

    Parameters
    ----------
    reward: array-like, shape (n_rounds,)
        Reward observed in each round of the logged bandit feedback, i.e., :math:`r_t`.

    iw: array-like, shape (n_rounds,)
        Importance weight in each round of the logged bandit feedback, i.e., :math:`w(x,a)=\\pi_e(a|x)/ \\pi_b(a|x)`.

    iw_hat: array-like, shape (n_rounds,)
        Importance weight (IW) modified by a hyparpareter. How IW is modified depends on the estimator as follows.
            - clipping: :math:`\\hat{w}(x,a) := \\min \\{ \\lambda, w(x,a) \\}`
            - switching: :math:`\\hat{w}(x,a) := w(x,a) \\cdot \\mathbb{I} \\{ w(x,a) < \\lambda \\}`
            - shrinkage: :math:`\\hat{w}(x,a) := (\\lambda w(x,a)) / (\\lambda + w^2(x,a))`
        where :math:`\\lambda` is a hyperparameter value.

    q_hat: array-like, shape (n_rounds,), default=None
        Estimated expected reward given context :math:`x_t` and action :math:`a_t`.

    Returns
    ----------
    estimated_bias: float
        Estimated the bias in OPE.
        This is based on the direct bias estimation stated on page 17 of Su et al.(2020).

    References
    ----------
    Yi Su, Maria Dimakopoulou, Akshay Krishnamurthy, and Miroslav Dudik.
    "Doubly Robust Off-Policy Evaluation with Shrinkage.", 2020.

    """
    n_rounds = reward.shape[0]
    if q_hat is None:
        q_hat = np.zeros(n_rounds)
    estimated_bias_arr = (iw - iw_hat) * (reward - q_hat)
    estimated_bias = np.abs(estimated_bias_arr.mean())

    return estimated_bias


def estimate_high_probability_upper_bound_bias(
    reward: np.ndarray,
    iw: np.ndarray,
    iw_hat: np.ndarray,
    q_hat: Optional[np.ndarray] = None,
    delta: float = 0.05,
) -> float:
    """Helper to estimate a high probability upper bound of bias in OPE.

    Parameters
    ----------
    reward: array-like, shape (n_rounds,)
        Reward observed in each round of the logged bandit feedback, i.e., :math:`r_t`.

    iw: array-like, shape (n_rounds,)
        Importance weight in each round of the logged bandit feedback, i.e., :math:`w(x,a)=\\pi_e(a|x)/ \\pi_b(a|x)`.

    iw_hat: array-like, shape (n_rounds,)
        Importance weight (IW) modified by a hyparpareter. How IW is modified depends on the estimator as follows.
            - clipping: :math:`\\hat{w}(x,a) := \\min \\{ \\lambda, w(x,a) \\}`
            - switching: :math:`\\hat{w}(x,a) := w(x,a) \\cdot \\mathbb{I} \\{ w(x,a) < \\lambda \\}`
            - shrinkage: :math:`\\hat{w}(x,a) := (\\lambda w(x,a)) / (\\lambda + w^2(x,a))`
        where :math:`\\lambda` and :math:`\\lambda` are hyperparameters.

    q_hat: array-like, shape (n_rounds,), default=None
        Estimated expected reward given context :math:`x_t` and action :math:`a_t`.

    delta: float, default=0.05
        A confidence delta to construct a high probability upper bound based on the Bernstein’s inequality.

    Returns
    ----------
    bias_upper_bound: float
        Estimated (high probability) upper bound of the bias.
        This upper bound is based on the direct bias estimation
        stated on page 17 of Su et al.(2020).

    References
    ----------
    Yi Su, Maria Dimakopoulou, Akshay Krishnamurthy, and Miroslav Dudik.
    "Doubly Robust Off-Policy Evaluation with Shrinkage.", 2020.

    """
    check_scalar(delta, "delta", (int, float), min_val=0.0, max_val=1.0)

    bias_upper_bound = estimate_bias_in_ope(
        reward=reward,
        iw=iw,
        iw_hat=iw_hat,
        q_hat=q_hat,
    )
    n_rounds = reward.shape[0]
    bias_upper_bound += np.sqrt((2 * (iw ** 2).mean() * np.log(2 / delta)) / n_rounds)
    bias_upper_bound += (2 * iw.max() * np.log(2 / delta)) / (3 * n_rounds)

    return bias_upper_bound
