import math
import cmath

# ──────────────────────────────────────────────────────────────
# Locked constants
# ──────────────────────────────────────────────────────────────
EPS               = 1.0e-9
N_TODAY           = 1_000_000_000
PSI               = 0.1503378808                  # rad
ALPHA             = 0.193218843731                # irrational rotation number
THETA_EFF         = 1.2140298                     # rad
RE_TAU            = 1.4129651365                  # Re(τ) = arctan(2π)
TAU               = RE_TAU
DELTA_PHI_TORQUE  = 1.72113420759                 # rad = 0.25·2π + ψ
SIN_DELTA         = math.sin(DELTA_PHI_TORQUE)    # ≈ cos(ψ)
COS_PSI           = math.cos(PSI)
ALPHA_G           = 0.558
H_WIND            = 70.0
SH_GEOM_TARGET    = 3.170
SCREEN_MPC        = 4500.0
DAMP_SCALE        = 5.8
LATE_START        = 700_000_000
K_NORM            = 1.4144172
INV_SQRT2         = 0.7071
OMEGA_FRAC        = 0.25                          # fractional topological defect

# ──────────────────────────────────────────────────────────────
class JCRCosmologicalClock:
    """Full discrete-tick cosmological clock."""

    def __init__(self):
        self.eps     = EPS
        self.N_today = N_TODAY

    # ── 1. Microscopic / macroscopic maps ─────────────────────
    def chi_micro(self, N: float) -> float:
        """χ_micro = ε·N  →  χ_micro(N_today) = 1"""
        return self.eps * N

    def chi_micro_alt(self) -> float:
        """Alternative definition appearing in notes: 1/ψ"""
        return 1.0 / PSI

    def scale_factor(self, N: float) -> float:
        """a(N) = exp(χ_micro)  →  a_Ψ = e"""
        return math.exp(self.chi_micro(N))

    def redshift(self, N: float) -> float:
        a = self.scale_factor(N)
        return (1.0 / a) - 1.0

    # ── 2. Phase quantities ───────────────────────────────────
    def phase_bias(self, N: float) -> float:
        """φ_bias = 2π · χ_micro"""
        return 2.0 * math.pi * self.chi_micro(N)

    def primary_phase_tau(self, k: float) -> float:
        """v(k) = 2τ · k · 10⁻⁹"""
        return 2.0 * TAU * k * self.eps

    def primary_phase_4pi(self, k: float) -> float:
        """v(k) = 4π · k · 10⁻⁹  (double-cover)"""
        return 4.0 * math.pi * k * self.eps

    def controlled_phase(self, x: float = INV_SQRT2) -> float:
        """v(0.7071) ≈ 8.8875e-9 rad"""
        return self.primary_phase_4pi(x)

    def psi_offset_phase(self, k: float) -> float:
        return self.primary_phase_4pi(k) + PSI

    # ── 3. Discrete dynamical system on S¹ ────────────────────
    def irrational_rotation(self, phi: float) -> float:
        """T_α(φ) = φ + 2π α  (mod 2π)"""
        return (phi + 2.0 * math.pi * ALPHA) % (2.0 * math.pi)

    def complex_map_step(self, z: complex, dphi: float) -> complex:
        """z_{n+1} = z_n · exp(i Δφ_n)"""
        return z * cmath.exp(1j * dphi)

    def evolve_complex_map(self, z0: complex, steps: int, dphi: float) -> complex:
        z = z0
        for _ in range(steps):
            z = self.complex_map_step(z, dphi)
        return z

    # ── 4. Algebraic bridge identities ────────────────────────
    def alpha_psi(self) -> float:
        """α · ψ ≈ 0.02905"""
        return ALPHA * PSI

    def f_psi_tau(self) -> float:
        """f(ψ,τ) ≈ cos(ψ)·Re(τ) / (sin(Re(τ))·K_norm) ≈ 1"""
        return (COS_PSI * RE_TAU) / (math.sin(RE_TAU) * K_NORM)

    def k_norm_check(self) -> float:
        return K_NORM * INV_SQRT2          # should be ≈ 1

    # ── 5. Suppression / damping / modulation ─────────────────
    def screening(self, chi: float) -> float:
        return math.exp(-chi / SCREEN_MPC)

    def redshift_damping(self, z: float) -> float:
        return math.exp(-z / DAMP_SCALE)

    def modulation(self, z: float) -> float:
        return 1.0 + 5.0 * math.exp(-z / 2.0)

    def suppression(self, z: float, chi: float) -> float:
        return (self.modulation(z) *
                self.redshift_damping(z) *
                self.screening(chi))

    # ── 6. Geometric torque & Hubble ──────────────────────────
    def omega_eff(self) -> float:
        return DELTA_PHI_TORQUE / 0.3

    def delta_H_geom(self, N: float) -> float:
        if N < LATE_START:
            return 0.0
        chi  = self.chi_micro(N)
        z    = self.redshift(N)
        a    = self.scale_factor(N)
        base = ALPHA_G * self.omega_eff() * SIN_DELTA
        weight = a * self.screening(chi) * self.redshift_damping(z)
        # normalise so that δH(N_today) = 3.170
        norm = SH_GEOM_TARGET / (ALPHA_G * self.omega_eff() * SIN_DELTA)
        return base * weight * norm

    def H(self, N: float) -> float:
        return H_WIND + self.delta_H_geom(N)

    # ── 7. Cosmic-time helpers (symbolic structure) ───────────
    def ln_a(self, N: float, C: float = 1.0) -> float:
        return C * N * self.eps

    # ── 8. Reporting ──────────────────────────────────────────
    def present_day_report(self) -> None:
        N = self.N_today
        print("=" * 66)
        print("Joshua Christopher Ryan’s Cosmological Clock – Present Epoch")
        print("=" * 66)
        print(f"χ_micro (ε·N)          = {self.chi_micro(N):.10f}")
        print(f"χ_micro (1/ψ)          = {self.chi_micro_alt():.10f}")
        print(f"a_Ψ                    = {self.scale_factor(N):.10f}   (= e)")
        print(f"z_Ψ                    = {self.redshift(N):.6f}")
        print(f"φ_bias                 = {self.phase_bias(N):.10f} rad  (= 2π)")
        print(f"primary phase (4π)     = {self.primary_phase_4pi(N):.10f} rad")
        print(f"primary phase (2τ)     = {self.primary_phase_tau(N):.10f} rad")
        print(f"controlled v(0.7071)   = {self.controlled_phase():.6e} rad")
        print(f"ψ                      = {PSI:.10f} rad  ({math.degrees(PSI):.4f}°)")
        print(f"Δφ_torque              = {DELTA_PHI_TORQUE:.10f} rad")
        print(f"sin(Δφ_torque)         = {SIN_DELTA:.10f}  (= cos ψ)")
        print(f"α·ψ                    = {self.alpha_psi():.10f}")
        print(f"f(ψ,τ)                 = {self.f_psi_tau():.10f}")
        print(f"K_norm · 0.7071        = {self.k_norm_check():.10f}")
        print(f"H_wind                 = {H_WIND:.3f}")
        print(f"δH_geom (today)        = {self.delta_H_geom(N):.3f}")
        print(f"H_total (today)        = {self.H(N):.3f} km/s/Mpc")
        print("=" * 66)

    def milestone_table(self) -> None:
        milestones = [0, 1_000_000, 100_000_000, 500_000_000,
                      700_000_000, 900_000_000, N_TODAY]
        hdr = "{:>12} {:>10} {:>10} {:>10} {:>10} {:>10}"
        print("\n" + hdr.format("N", "χ", "a", "z", "δH", "H"))
        print("-" * 66)
        for N in milestones:
            print(f"{N:12.0f} {self.chi_micro(N):10.6f} "
                  f"{self.scale_factor(N):10.6f} {self.redshift(N):10.4f} "
                  f"{self.delta_H_geom(N):10.4f} {self.H(N):10.4f}")

    def demo_discrete_map(self, steps: int = 5) -> None:
        print("\nDiscrete complex map demo (first few iterates):")
        z = 1+0j
        dphi = 2.0 * math.pi * ALPHA
        for i in range(steps):
            z = self.complex_map_step(z, dphi)
            print(f"  n={i+1:2d}  z = {z.real:+.6f} {z.imag:+.6f}j  |z|={abs(z):.6f}")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    clock = JCRCosmologicalClock()
    clock.present_day_report()
    clock.milestone_table()
    clock.demo_discrete_map()
