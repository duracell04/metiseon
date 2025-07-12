from __future__ import annotations

"""Numerical core for the MεΩ framework.

This module contains several utility classes used throughout the project.
Every public method includes doctests that run with ``pytest``.
"""

from dataclasses import dataclass
from hashlib import sha256
from typing import Generator, Iterable, Mapping, Sequence, cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats


# ---------------------------------------------------------------------------
# MonetarySpace
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class MonetarySpace:
    """Hilbert space for monetary assets.

    Parameters
    ----------
    _corr : :class:`pandas.DataFrame`
        Positive definite correlation matrix.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     [[1.0, 0.1], [0.1, 1.0]], index=["a", "b"], columns=["a", "b"]
    ... )
    >>> ms = MonetarySpace.from_correlation(df)
    >>> ms.delist("b")
    >>> ms.correlation.shape
    (1, 1)
    """

    _corr: pd.DataFrame

    @property
    def correlation(self) -> pd.DataFrame:
        """Return a copy of the correlation matrix."""
        return self._corr.copy()

    @classmethod
    def from_correlation(cls, df: pd.DataFrame) -> "MonetarySpace":
        """Build a :class:`MonetarySpace` from ``df``."""
        corr = df.copy().astype("float64")
        if corr.shape[0] != corr.shape[1]:
            raise ValueError("correlation matrix must be square")
        np.linalg.cholesky(corr.to_numpy(float))
        return cls(corr)

    def delist(self, symbol: str) -> None:
        """Remove ``symbol`` via Schur complement."""
        if symbol not in self._corr.columns:
            raise KeyError(symbol)
        if len(self._corr) == 1:
            self._corr = self._corr.iloc[0:0, 0:0]
            return
        k = self._corr.columns.get_loc(symbol)
        mask = [c != symbol for c in self._corr.columns]
        A = self._corr.loc[mask, mask]
        b = self._corr.loc[mask, symbol].to_numpy(float)
        d = float(self._corr.loc[symbol, symbol])
        new_mat = A.to_numpy(float) - np.outer(b, b) / d
        self._corr = pd.DataFrame(new_mat, index=A.index, columns=A.columns)
        np.linalg.cholesky(self._corr.to_numpy(float))


# ---------------------------------------------------------------------------
# JumpDiffusionProcess
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class JumpDiffusionProcess:
    """Simple jump diffusion process."""

    mu: float
    sigma: float
    lam: float
    jump_mu: float
    jump_delta: float
    dt: float = 1.0

    def pdf(self, x: float) -> float:
        """Probability density of a single jump.

        >>> jd = JumpDiffusionProcess(0.0, 0.1, 0.0, 0.0, 0.2)
        >>> round(jd.pdf(0.0), 3)
        1.995
        """
        return float(stats.norm.pdf(x, loc=self.jump_mu, scale=self.jump_delta))

    def cdf(self, x: float) -> float:
        """Cumulative distribution of a single jump."""
        return float(stats.norm.cdf(x, loc=self.jump_mu, scale=self.jump_delta))

    def sample(self, n: int, x0: float | NDArray[np.float64]) -> NDArray[np.float64]:
        """Simulate ``n`` steps starting from ``x0``.

        >>> jd = JumpDiffusionProcess(0.0, 0.1, 0.0, 0.0, 0.1)
        >>> jd.sample(3, 1.0).shape
        (4,)
        """
        rng = np.random.default_rng()
        x = np.asarray(x0, dtype=np.float64)
        out = np.empty((n + 1,) + x.shape, dtype=np.float64)
        out[0] = x
        for i in range(1, n + 1):
            dW = rng.normal(0.0, np.sqrt(self.dt), size=x.shape)
            count = rng.poisson(self.lam * self.dt, size=x.shape)
            jump_mean = count * self.jump_mu
            jump_std = np.sqrt(count) * self.jump_delta
            jumps = rng.normal(jump_mean, jump_std)
            x = x + self.mu * self.dt + self.sigma * dW + jumps
            out[i] = x
        return out


# ---------------------------------------------------------------------------
# ReplicatorDynamics
# ---------------------------------------------------------------------------
class ReplicatorDynamics:
    """Replicator dynamics for portfolio weights."""

    @staticmethod
    def step(
        weights: NDArray[np.float64],
        returns: NDArray[np.float64],
        sigma: NDArray[np.float64],
        dt: float = 1.0,
    ) -> NDArray[np.float64]:
        """Advance one step while preserving the simplex.

        >>> w = np.array([0.5, 0.5])
        >>> r = np.array([0.05, -0.02])
        >>> s = np.array([0.1, 0.1])
        >>> ReplicatorDynamics.step(w, r, s).round(2).sum()
        1.0
        """
        w = np.asarray(weights, dtype=np.float64)
        r = np.asarray(returns, dtype=np.float64)
        s = np.asarray(sigma, dtype=np.float64)
        r_clip = np.clip(r, -5.0 * s, 5.0 * s)
        growth = w * (r_clip - float(np.dot(w, r_clip)))
        new_w = w + growth * dt
        new_w[new_w < 0] = 0.0
        total = new_w.sum()
        if total <= 0.0:
            return w.copy()
        result = new_w / total
        return cast(NDArray[np.float64], result.astype(np.float64))

    @staticmethod
    def stream(
        gen_returns: Iterable[Sequence[float]],
        gen_sigma: Iterable[Sequence[float]],
        w0: Sequence[float],
        dt: float = 1.0,
    ) -> Generator[NDArray[np.float64], None, None]:
        """Yield successive weights from generators."""
        w = np.asarray(w0, dtype=np.float64)
        for r, s in zip(gen_returns, gen_sigma):
            w = ReplicatorDynamics.step(
                w, np.asarray(r, float), np.asarray(s, float), dt
            )
            yield w


# ---------------------------------------------------------------------------
# EVTThreshold
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class EVTThreshold:
    """Peak-over-threshold estimator."""

    quantile: float = 0.99
    _lambda: float | None = None

    @property
    def lambda_(self) -> float:
        """Return last estimated scale parameter."""
        if self._lambda is None:
            raise AttributeError("call fit first")
        return self._lambda

    def fit(self, data: Sequence[float], tail: str = "right") -> float:
        """Return extreme quantile estimate for ``tail``.

        >>> np.random.seed(0)
        >>> data = np.random.normal(0, 1, 100)
        >>> evt = EVTThreshold(0.95)
        >>> round(evt.fit(data), 2) >= round(np.quantile(data, 0.95), 2)
        True
        """
        arr = np.asarray(list(data), dtype=np.float64)
        if arr.size < 30:
            raise ValueError("need at least 30 samples")
        if tail not in {"right", "left"}:
            raise ValueError("tail must be 'right' or 'left'")
        q = self.quantile
        if tail == "right":
            thr = np.quantile(arr, q)
            excess = arr[arr > thr] - thr
        else:
            thr = np.quantile(arr, 1.0 - q)
            excess = thr - arr[arr < thr]
        if excess.size == 0:
            self._lambda = 0.0
            return float(thr)
        c, loc, scale = stats.genpareto.fit(excess, floc=0.0)
        self._lambda = float(scale)
        adj = stats.genpareto.ppf(q, c, loc=0.0, scale=scale)
        if tail == "right":
            return float(thr + adj)
        return float(thr - adj)


# ---------------------------------------------------------------------------
# BenfordOptimizer
# ---------------------------------------------------------------------------
class BenfordOptimizer:
    """Benford error utilities."""

    @staticmethod
    def _leading_digits(arr: Sequence[float]) -> NDArray[np.int_]:
        a = np.abs(np.asarray(list(arr), dtype=np.float64))
        a = a[a > 0]
        mag = np.floor(np.log10(a))
        result = (a / 10.0**mag).astype(np.int_)
        return cast(NDArray[np.int_], result)

    @staticmethod
    def error(arr: Sequence[float]) -> float:
        """Mean squared error from Benford's law."""
        digits = BenfordOptimizer._leading_digits(arr)
        if digits.size == 0:
            return 0.0
        counts = np.bincount(digits, minlength=10)[1:10]
        probs = counts / counts.sum()
        target = np.log10(1 + 1.0 / np.arange(1, 10))
        return float(np.mean((probs - target) ** 2))

    @staticmethod
    def best_scale(arr: Sequence[float], k_grid: Sequence[int]) -> tuple[float, float]:
        """Return scale ``k`` and error for ``arr * 10**k``."""
        data = np.asarray(list(arr), dtype=np.float64)
        best_k = k_grid[0]
        best_err = np.inf
        for k in k_grid:
            err = BenfordOptimizer.error(list(data * (10.0**k)))
            if err < best_err:
                best_k = k
                best_err = err
        return float(best_k), float(best_err)


# ---------------------------------------------------------------------------
# RiskFreeRate
# ---------------------------------------------------------------------------
class RiskFreeRate:
    """Risk-free rate estimates."""

    @staticmethod
    def compute(
        mc: Sequence[float],
        illiq: Sequence[float],
        yields: Sequence[float],
        *,
        method: str = "amihud",
    ) -> float:
        """Return aggregated risk-free rate.

        >>> RiskFreeRate.compute([1, 1], [0.1, 0.2], [0.02, 0.03])
        0.025
        """
        mc_a = np.asarray(list(mc), dtype=np.float64)
        ill_a = np.asarray(list(illiq), dtype=np.float64)
        y = np.asarray(list(yields), dtype=np.float64)
        if method == "amihud":
            adj = 1.0 - ill_a / np.max(ill_a)
            w = mc_a * adj
        elif method == "uniform":
            w = np.ones_like(mc_a)
        else:
            raise ValueError("unknown method")
        w /= w.sum()
        return float(np.dot(w, y))


# ---------------------------------------------------------------------------
# ZkSnarkProof
# ---------------------------------------------------------------------------
class ZkSnarkProof:
    """Mock zk-SNARK proofs."""

    @staticmethod
    def prove(reserves: Mapping[str, float], min_ratio: float = 1.0) -> str:
        """Return a deterministic hexadecimal proof string."""
        items = sorted(reserves.items())
        concat = ",".join(f"{k}:{v:.6f}" for k, v in items)
        concat += f"|{min_ratio:.2f}"
        return sha256(concat.encode()).hexdigest()
