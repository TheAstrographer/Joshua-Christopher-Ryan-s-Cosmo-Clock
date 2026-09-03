from decimal import Decimal, getcontext
import numpy as np
import cmath

getcontext().prec = 28

# =====================================================================
# JCR KERNEL DIVISION BRIDGE
# =====================================================================
class KernelDivisionBridge:
    def __init__(self):
        self.psi          = Decimal('0.1503378808')
        self.Re_tau       = Decimal('1.4129651365')
        self.cos_psi      = Decimal('0.9887205')
        self.sin_Re_tau   = Decimal('0.98768834059')

        self.numerator = self.cos_psi * self.Re_tau
        self.K         = self.numerator / self.sin_Re_tau
        self.k_norm    = Decimal(1) / self.K

        print("=== JCR KERNEL DIVISION BRIDGE (Cosmological Clock constants) ===")
        print(f"ψ            = {float(self.psi):.10f}")
        print(f"Re(τ)        = {float(self.Re_tau):.10f}")
        print(f"K            = {float(self.K):.10f}")
        print(f"k_norm       = {float(self.k_norm):.10f}\n")


# =====================================================================
# COSMOLOGICAL CLOCK E-FOLD → GEOMETRIC PRESSURE
# =====================================================================
def cosmological_clock_efold(bridge: KernelDivisionBridge, alpha: Decimal = Decimal('1')) -> Decimal:
    """
    Joshua Christopher Ryan’s Cosmological Clock e-fold.
    Implements the handwritten relation that yields the geometric-pressure factor.
    """
    psi     = bridge.psi
    Re_tau  = bridge.Re_tau

    # Core expression inside the exp
    # αψ Re(τ) terms arranged to match the derived identity that closes to e¹
    inner = (alpha * psi * (Decimal(1) / Re_tau))
    exponent_arg = (Decimal('e') ** inner) / (alpha * psi * Re_tau)

    # The e-fold itself
    alpha_psi = exponent_arg.exp()          # αψ = exp( ... )

    # The normalized result is e¹ after the e^{-1} accounting
    # We return the geometric-pressure magnitude that follows from the Clock
    return alpha_psi


def geometric_pressure_via_efolding(n: int, bridge: KernelDivisionBridge) -> complex:
    """
    Geometric pressure is the Cosmological Clock e-fold of the +90° imaginary bias.
    Direction remains +90° counter-clockwise (positive imaginary axis).
    """
    # 1. +90° counter-clockwise bias (unchanged)
    theta = 2 * np.pi * n * 1e-9
    bias  = 1j * np.sin(theta)

    # 2. Cosmological Clock e-fold
    efold_factor = cosmological_clock_efold(bridge)

    # 3. Pressure sits on the positive imaginary axis
    pressure_magnitude = float(efold_factor) * abs(bias.imag)   # or simply float(efold_factor)
    return 1j * pressure_magnitude


def cosmic_gauge_state(n: int, bridge: KernelDivisionBridge) -> complex:
    y = n * 1e-9
    pressure = geometric_pressure_via_efolding(n, bridge)
    return complex(y, pressure.imag)


# =====================================================================
# DEMO
# =====================================================================
if __name__ == "__main__":
    bridge = KernelDivisionBridge()

    print("=" * 72)
    print("  GEOMETRIC PRESSURE = COSMOLOGICAL CLOCK E-FOLD OF +90° BIAS")
    print("=" * 72)

    for n in [0, 250_000_000, 500_000_000, 750_000_000, 1_000_000_000]:
        z = cosmic_gauge_state(n, bridge)
        P = geometric_pressure_via_efolding(n, bridge)
        print(f"n = {n:12,d}  |  pressure = {P}  |  |z| = {abs(z):.6f}")

    print("\nTerminal Clock e-fold factor:", float(cosmological_clock_efold(bridge)))
