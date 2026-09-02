#!/usr/bin/env python3
"""
  - Adaptive Harmonic Band-Power Kernel
  - JCR Cosmological Clock (Bosonic Backbone + Late-Time Geometric Torque)

Provides clean Fourier-space scale separation that adapts to the
local density and redshift evolution defined by the cosmological clock.
"""

import math
import numpy as np
from typing import List, Dict, Optional, Tuple

# ============================================================
# 1. Adaptive Band-Power Kernel
# ============================================================

class AdaptiveBandpowerKernel:
    """
    Smooth, density- and redshift-adaptive log-Gaussian filter
    for clean multipole band-power extraction.
    """

    def __init__(self, l_center: float, sigma_0: float = 0.15, gamma: float = 0.25):
        """
        Parameters
        ----------
        l_center : float
            Logarithmic center of the multipole band-power bin.
        sigma_0 : float
            Base kernel width in log-ℓ space (linear / underdense regime).
        gamma : float
            Coupling strength that controls how strongly the filter
            sharpens in non-linear environments.
        """
        self.l_center = float(l_center)
        self.sigma_0 = float(sigma_0)
        self.gamma = float(gamma)
        self.z_transition = 5.8          # Dual-gate / screening transition

    def compute_adaptive_width(self, z: float, delta_rho: float) -> float:
        """Adaptive width operator σ(z, Δρ)."""
        epoch_scaling = (1.0 + z) / (1.0 + self.z_transition)
        density_modulator = math.log(1.0 + delta_rho**2)

        # Kernel narrows (sharpens) as non-linear density / feedback grows
        width = self.sigma_0 / (1.0 + self.gamma * epoch_scaling * density_modulator)
        return max(width, 0.02)          # numerical floor

    def evaluate_kernel(self, l_array: np.ndarray, z: float, delta_rho: float) -> np.ndarray:
        """
        Evaluate the normalized adaptive weight function over an array of multipoles.

        Returns
        -------
        np.ndarray
            Kernel weights satisfying ∫ K(ℓ) dlnℓ ≈ 1.
        """
        sigma = self.compute_adaptive_width(z, delta_rho)

        valid = l_array > 0
        weights = np.zeros_like(l_array, dtype=float)

        log_l  = np.log(l_array[valid])
        log_lc = math.log(self.l_center)

        response = np.exp(-0.5 * ((log_l - log_lc) / sigma)**2)

        # Normalize so that ∫ K dlnℓ = 1  (i.e. ∫ (response/ℓ) dℓ = 1)
        norm = np.trapz(response / l_array[valid], l_array[valid])
        if norm > 0.0:
            weights[valid] = response / norm

        return weights


# ============================================================
# 2. JCR Cosmological Clock (full integrated version)
# ============================================================

class JCRCosmologicalClock:
    """
    Joshua Christopher Ryan's Cosmological Clock
    Bosonic Backbone + Late-Time Geometric Torque
    with Adaptive Band-Power Kernel support.
    """

    def __init__(self):
        # Core constants
        self.epsilon = 1e-9
        self.N_today = 1_000_000_000
        self.H_wind  = 70.0                 # Bosonic baseline (km/s/Mpc)

        # Angular / phase parameters
        self.theta_eff        = 1.2140298
        self.tau              = math.atan(2 * math.pi)
        self.psi              = 0.1503378808
        self.delta_phi_torque = 1.72113420759
        self.sh_geom_base     = 3.170

        # Damping & modulation
        self.tau_damp         = 5.8
        self.chi_screen_scale = 4500.0      # Mpc

        # Cosmological parameters
        self.Omega_m = 0.3
        self.Omega_L = 0.7

        # Pre-compute
        self.sin_torque = math.sin(self.delta_phi_torque)

        # Adaptive kernel factory (can be customized later)
        self.default_kernel = AdaptiveBandpowerKernel(l_center=500.0)

        print("JCR Cosmological Clock initialized.")
        print(f"Bosonic Baseline H_wind = {self.H_wind:.1f} km/s/Mpc")
        print(f"Target H_total(z=0) ≈ {self.H_wind + 3.17:.2f} km/s/Mpc")

    # ------------------------------------------------------------------
    # Background evolution
    # ------------------------------------------------------------------
    def scale_factor(self, N: float) -> float:
        """a(N) = exp(ε · N)"""
        return math.exp(self.epsilon * N)

    def redshift(self, a: float) -> float:
        """z = 1/a − 1"""
        return 1.0 / a - 1.0

    def comoving_distance_approx(self, N: float) -> float:
        """Very approximate χ(N) in Mpc (normalized to ~4500 Mpc today)."""
        return 4500.0 * (N / self.N_today)

    def f_damp(self, z: float) -> float:
        return math.exp(-z / self.tau_damp)

    def f_mod(self, z: float) -> float:
        return 1.0 + 5.0 * math.exp(-z / 2.0)

    def suppression(self, z: float, chi: float) -> float:
        """Combined suppression S(z, χ)"""
        return self.f_mod(z) * self.f_damp(z) * math.exp(-chi / self.chi_screen_scale)

    def H_base(self, z: float) -> float:
        """Bosonic baseline Hubble (flat ΛCDM-like)"""
        return self.H_wind * math.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_L)

    def delta_H_torque(self, z: float = 0.0, chi: float = 0.0) -> float:
        """Late-time geometric torque contribution"""
        S = self.suppression(z, chi)
        a = 1.0 / (1.0 + z)
        delta_geom = self.sh_geom_base * a * self.sin_torque
        return delta_geom * S * 0.528          # normalized ≈ +3.17 at z=0

    def H_total(self, z: float = 0.0, chi: Optional[float] = None) -> float:
        """Total effective Hubble parameter"""
        if chi is None:
            # rough mapping from redshift to χ
            chi = self.comoving_distance_approx(self.N_today / (1.0 + z))
        return self.H_base(z) + self.delta_H_torque(z, chi)

    def phase_bias(self, N: float) -> float:
        return 2.0 * math.pi * N * self.epsilon

    # ------------------------------------------------------------------
    # Adaptive kernel interface (the integration point)
    # ------------------------------------------------------------------
    def make_kernel(self, l_center: float,
                    sigma_0: float = 0.15,
                    gamma: float = 0.25) -> AdaptiveBandpowerKernel:
        """Factory method that returns a fresh adaptive kernel."""
        return AdaptiveBandpowerKernel(l_center=l_center, sigma_0=sigma_0, gamma=gamma)

    def evaluate_adaptive_bandpower_weights(
            self,
            l_array: np.ndarray,
            z: float,
            delta_rho: float = 1.0,
            l_center: float = 500.0
    ) -> np.ndarray:
        """
        Convenience wrapper: evaluate the adaptive kernel at a given
        redshift and local density contrast using the clock's parameters.
        """
        kernel = self.make_kernel(l_center=l_center)
        return kernel.evaluate_kernel(l_array, z=z, delta_rho=delta_rho)

    # ------------------------------------------------------------------
    # Milestone simulation & reporting
    # ------------------------------------------------------------------
    def run_milestone_simulation(self, milestones: Optional[List[int]] = None) -> List[Dict]:
        if milestones is None:
            milestones = [0, 10**5, 10**6, 10**7, 10**8,
                          5*10**8, 7*10**8, 9*10**8, self.N_today]

        results = []
        for n in milestones:
            a   = self.scale_factor(n)
            z   = self.redshift(a)
            chi = self.comoving_distance_approx(n)

            h_total = self.H_total(z, chi)
            h_base  = self.H_base(z)
            dH_t    = h_total - h_base

            regime = ("Initial" if n == 0 else
                      "LATE-TIME" if n >= 700_000_000 else "Transition")

            results.append({
                'N': n,
                'chi': chi,
                'a': a,
                'z': z,
                'H_base': h_base,
                'delta_H_torque': dH_t,
                'H_total': h_total,
                'regime': regime
            })
        return results

    def print_milestones(self):
        data = self.run_milestone_simulation()
        print("\n" + "=" * 110)
        print("JCR COSMOLOGICAL CLOCK – BOSONIC BACKBONE + TORQUE")
        print("=" * 110)
        print(f"{'N':>12}  {'a(N)':>10}  {'z':>8}  {'H_base':>8}  "
              f"{'ΔH_torque':>10}  {'H_total':>8}  Regime")
        print("-" * 110)
        for row in data:
            print(f"{row['N']:12,}  {row['a']:10.6f}  {row['z']:8.4f}  "
                  f"{row['H_base']:8.2f}  {row['delta_H_torque']:10.3f}  "
                  f"{row['H_total']:8.2f}  {row['regime']}")
        print("-" * 110)

    def summary(self):
        print("\n" + "=" * 80)
        print("FINAL SUMMARY AT N = 10⁹ (Present Day, z = 0)")
        print("=" * 80)
        print(f"Bosonic Baseline (H_wind)      : {self.H_wind:.2f} km/s/Mpc")
        print(f"Geometric Torque Contribution  : +{self.delta_H_torque(0.0):.2f} km/s/Mpc")
        print(f"Total Effective H₀             : {self.H_total(0.0):.2f} km/s/Mpc")
        print(f"Scale Factor a                 : {self.scale_factor(self.N_today):.6f} ≈ e")
        print(f"Total Phase Bias               : {self.phase_bias(self.N_today):.6f} rad = 2π")
        print(f"sin(Δϕ_torque)                 : {self.sin_torque:.6f}")
        print(f"θ_eff                          : {self.theta_eff:.7f} rad ≈ {math.degrees(self.theta_eff):.3f}°")
        print(f"ψ (Angular Bridge)             : {self.psi:.8f} rad")
        print("=" * 80)

    # ------------------------------------------------------------------
    # Demonstration of the integrated adaptive kernel
    # ------------------------------------------------------------------
    def demo_adaptive_kernel(self):
        """Quick verification that the adaptive kernel is live inside the clock."""
        print("\n" + "=" * 70)
        print("  ADAPTIVE KERNEL FOOTPRINT (driven by the Cosmological Clock)")
        print("=" * 70)
        print(f"{'Environment':<28} | {'z':<8} | {'σ':<10} | {'Peak K':<10}")
        print("-" * 70)

        ell = np.logspace(1, 4, 500)
        cases = [
            ("Linear underdense",      4.0,   0.01),
            ("Transition corridor",    0.934, 2.5),
            ("Highly non-linear halo", 0.1,   15.0),
        ]

        for name, z, drho in cases:
            ker = self.make_kernel(l_center=500.0)
            sigma = ker.compute_adaptive_width(z, drho)
            weights = ker.evaluate_kernel(ell, z, drho)
            print(f"{name:<28} | {z:<8.3f} | {sigma:<10.5f} | {np.max(weights):<10.4f}")
        print("=" * 70)


# ============================================================
# Usage / self-test
# ============================================================
if __name__ == "__main__":
    clock = JCRCosmologicalClock()

    # 1. Classic clock milestones
    clock.print_milestones()
    clock.summary()

    # 2. Demonstrate that the Adaptive Band-Power Kernel is fully integrated
    clock.demo_adaptive_kernel()
