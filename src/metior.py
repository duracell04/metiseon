from __future__ import annotations

"""Core components for the M\xea\x82\x81\u03a9 num\xe9raire framework."""

from typing import Iterable, Sequence
from datetime import date
import numpy as np
from scipy import stats


class MonetarySpace:
    """Monetary Hilbert space represented by a positive-definite matrix.

    Parameters
    ----------
    rho : np.ndarray
        Positive-definite inner-product matrix.

    Examples
    --------
    >>> rho = np.eye(3) * 2.0
    >>> ms = MonetarySpace(rho)
    >>> ms.delist(1)
    >>> ms.rho.shape
    (2, 2)
    """

    def __init__(self, rho: Sequence[Sequence[float]]) -> None:
        self.rho = np.array(rho, dtype=float)
        self._validate()

    def _validate(self) -> None:
        if self.rho.ndim != 2 or self.rho.shape[0] != self.rho.shape[1]:
            raise ValueError("rho must be square")
        # Cholesky fails if not positive definite
        np.linalg.cholesky(self.rho)

    def delist(self, k: int) -> None:
        """Remove an asset using the Schur complement.

        Parameters
        ----------
        k : int
            Index of the asset to remove.
        """

        n = self.rho.shape[0]
        if not 0 <= k < n:
            raise IndexError("invalid index")
        if n == 1:
            self.rho = np.empty((0, 0))
            return
        mask = np.arange(n) != k
        A = self.rho[np.ix_(mask, mask)]
        b = self.rho[mask, k]
        d = self.rho[k, k]
        self.rho = A - np.outer(b, b) / d
        self._validate()


class JumpDiffusionProcess:
    """Jump diffusion process with normally distributed jumps.

    Parameters
    ----------
    mu : float
        Drift coefficient.
    sigma : float
        Diffusion volatility.
    lam : float
        Jump intensity (events per unit time).
    jump_mu : float
        Mean jump size.
    jump_delta : float
        Jump size volatility.
    dt : float
        Time step.

    Examples
    --------
    >>> j = JumpDiffusionProcess(0.0, 0.1, 0.2, 0.0, 0.05, 1.0)
    >>> path = j.sample(0.0, 5)
    >>> len(path)
    6
    """

    def __init__(
        self,
        mu: float,
        sigma: float,
        lam: float,
        jump_mu: float,
        jump_delta: float,
        dt: float = 1.0,
    ) -> None:
        self.mu = mu
        self.sigma = sigma
        self.lam = lam
        self.jump_mu = jump_mu
        self.jump_delta = jump_delta
        self.dt = dt

    def sample(self, x0: float, steps: int) -> np.ndarray:
        """Simulate a sample path."""

        path = np.empty(steps + 1)
        path[0] = x0
        for i in range(1, steps + 1):
            dW = np.random.normal(0.0, np.sqrt(self.dt))
            jumps = 0.0
            n = np.random.poisson(self.lam * self.dt)
            if n > 0:
                jumps = np.random.normal(self.jump_mu, self.jump_delta, n).sum()
            path[i] = path[i - 1] + self.mu * self.dt + self.sigma * dW + jumps
        return path


class ReplicatorDynamics:
    """Replicator dynamics for portfolio weights."""

    @staticmethod
    def step(
        weights: np.ndarray, returns: np.ndarray, sigma: np.ndarray, dt: float
    ) -> np.ndarray:
        """Advance weights one step.

        Parameters
        ----------
        weights : np.ndarray
            Current weights summing to one.
        returns : np.ndarray
            Asset returns.
        sigma : np.ndarray
            Volatility estimates.
        dt : float
            Time increment.

        Examples
        --------
        >>> w = np.array([0.5, 0.5])
        >>> r = np.array([0.01, -0.02])
        >>> s = np.array([0.1, 0.1])
        >>> ReplicatorDynamics.step(w, r, s, 1.0).round(2)
        array([0.53, 0.47])
        """

        r_clip = np.clip(returns, -5.0 * sigma, 5.0 * sigma)
        growth = weights * (r_clip - float(np.dot(weights, r_clip)))
        new_weights = weights + growth * dt
        new_weights[new_weights < 0] = 0.0
        total = new_weights.sum()
        if total > 0:
            new_weights /= total
        else:
            new_weights = weights
        return new_weights


class EVTThreshold:
    """Peak-over-threshold estimator using a GPD fit."""

    def __init__(self, quantile: float = 0.999) -> None:
        self.quantile = quantile

    def fit(self, data: Sequence[float]) -> float:
        """Return the estimated extreme threshold."""

        arr = np.asarray(list(data), dtype=float)
        thr = np.quantile(arr, self.quantile)
        excess = arr[arr > thr] - thr
        if len(excess) < 5:
            return float(thr)
        c, loc, scale = stats.genpareto.fit(excess, floc=0.0)
        return float(thr + stats.genpareto.ppf(self.quantile, c, loc=0, scale=scale))


class BenfordOptimizer:
    """Compute Benford error for leading digits."""

    @staticmethod
    def _leading_digits(x: Sequence[float]) -> np.ndarray:
        arr = np.abs(np.asarray(list(x), dtype=float))
        arr = arr[arr > 0]
        digits = np.floor(arr / 10 ** np.floor(np.log10(arr))).astype(int)
        return np.asarray(digits, dtype=int)

    @staticmethod
    def error(data: Sequence[float]) -> float:
        """Return mean squared error against Benford frequencies."""

        digits = BenfordOptimizer._leading_digits(list(data))
        if digits.size == 0:
            return 0.0
        counts = np.bincount(digits, minlength=10)[1:10]
        probs = counts / counts.sum()
        target = np.log10(1 + 1 / np.arange(1, 10))
        return float(((probs - target) ** 2).sum())


class RiskFreeRate:
    """Compute MEΩ risk-free rate."""

    @staticmethod
    def rate(
        mc: Sequence[float], illiq: Sequence[float], yields: Sequence[float]
    ) -> float:
        """Return r_f^{MEΩ}.

        Examples
        --------
        >>> RiskFreeRate.rate([1, 1], [0.1, 0.2], [0.02, 0.03])
        0.025
        """

        mc_a = np.asarray(list(mc), dtype=float)
        ill = np.asarray(list(illiq), dtype=float)
        y = np.asarray(list(yields), dtype=float)
        adj = 1.0 - ill / np.max(ill)
        w = mc_a * adj
        w /= w.sum()
        return float(np.dot(w, y))


class ZkSnarkProof:
    """Placeholder for a zk-SNARK proof of reserves."""

    @staticmethod
    def batched_proof(assets: Iterable[str], reserves: Iterable[float]) -> str:
        """Return a dummy proof string."""

        _ = list(assets)
        _ = list(reserves)
        return "proof"


def main() -> None:
    """Print MEΩ price and simulated weights."""

    from . import meo

    today = date.today()
    df, m_world = meo.fetch_meo_components(today)
    price = meo.meo_price_usd(m_world)
    weights = df["weight"].values
    print(f"MEΩ price USD: {price:.4f}")
    rd = ReplicatorDynamics()
    for _ in range(3):
        ret = np.random.normal(0, 0.01, len(weights))
        sig = np.full_like(ret, 0.02)
        weights = rd.step(weights, ret, sig, 1.0)
        print(weights.round(4))


if __name__ == "__main__":
    main()
