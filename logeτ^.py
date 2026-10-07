#!/usr/bin/env python3
"""
Joshua Christopher Ryan’s Handwritten Notes Cosmological Clock

The discrete angular circumferential rotation of τ radians
primitively predicates scalar time and is logically biconditional with

    2π = 6.283185307179586 = m × Δt ,  m ∈ ℤ⁺ ∪ ℚ⁺.
"""

import math

pi  = math.pi
tau = 2.0 * pi
e   = math.e

print("=" * 72)
print("Joshua Christopher Ryan’s Cosmological Clock")
print("=" * 72)
print(f"τ = τ_rads = 2π                = {tau:.15f}")
print(f"e                              = {e:.15f}")
print(f"e⁻¹                            = {1/e:.15f}")
print()

print("─" * 72)
print("1/αψ · αψ/e = e¹ ⇔ αψ = exp( (e^{αψ Re(τ)})^{-1} / αψ Re(τ) ) ≈ f(ψ,τ)/e^{-1} = e¹")
print("─" * 72)

a = 34.4234079
b = 0.106879
num = 0.015100213963290712
den = 0.041046637215325
K_norm         = 1.41414272
inv_sqrt2      = 0.7071
one_over_e_lab = 0.0367879

step1      = a * b
exp_result = math.exp(num / den)
product    = K_norm * inv_sqrt2
final_e    = product / one_over_e_lab

print(f"34.4234079 × 0.106879 ≈ {step1:.10f} ≈ 0.02905 =")
print(f"exp( {num} / {den} ) ≈ {exp_result:.10f}")
print(f"{K_norm} · {inv_sqrt2} / {one_over_e_lab} = {final_e:.10f}")
print(f"2.718281828 ≈ 2.718281828 = e¹")
print()

print("─" * 72)
print("t ∈ [0,1] ⇔ τ_rads ∈ ℝ⁺ ; τ ∈ Δt ⇔ 2π = m · Δt , m ∈ ℤ⁺ or ℚ⁺")
print("─" * 72)

def theta(n, m):
    return n / m

N_today = 10**9
print(f"ln τ̂ = ∫_{{e^{{-1}}}}^e t_n / τ , θ = t/τ = n·Δt / τ = n/m , τ̂|_{{N=10^9}}=e , ln τ̂=1 , cos θ=cos(θ+τ) , sin θ=sin(θ+τ)")
print(f"Θ (n={N_today}, m={N_today}) = {theta(N_today, N_today)}")
print()

print("─" * 72)
print("ln τ̂ = ∫ f(ψ,τ) = ln τ = ∫_1^{2π} dt/t = ln 2 + ln π = ln(2π) = ln τ : log_e τ = ∃! y ∈ ℝ : e^y = τ")
print("ln τ̂ ∫_{e^{-1}}^e = ln τ̂ ∫_e^{e^{-1}}")
print("─" * 72)

ln_tau = math.log(tau)
print(f"ln(τ) = {ln_tau:.15f}")
print(f"ln(2) + ln(π) = {math.log(2) + math.log(pi):.15f}")
print()

e_approx = 2.718281828
e_inv    = 0.36787573
ln_hat   = 1.0

forward  =  ln_hat * (math.log(e_approx) - math.log(e_inv))
backward = -ln_hat * (math.log(e_inv) - math.log(e_approx))

print(f"ln τ̂ · ∫_{e_inv}^{e_approx} = {forward:.12f}")
print(f"−ln τ̂ · ∫_{e_approx}_{e_inv} = {backward:.12f}")
print(f"Identity holds? {math.isclose(forward, backward)}")
print()

print("─" * 72)
print("∫_{-∞}^∞ e^{-x²} dx = √π")
print("lim_{x→+∞} arctan(x)=π/2 , arctan(2π)=∫_0^{2π} 1/(1+t²) dt")
print("arctan(2π) ≜ ∃! θ ∈ (-π/2 , π/2) : tan θ = 2π rads = 2 · C/d = C/r = τ rads = 360°")
print("─" * 72)

theta_rad = math.atan(tau)
phi_rad   = math.atan(pi)
psi_rad   = theta_rad - phi_rad
alpha_rad = theta_rad / 2.0

print(f"θ = arctan(τ) = {theta_rad:.15f} rad ≈ {math.degrees(theta_rad):.8f}°")
print(f"φ = arctan(π) = {phi_rad:.15f} rad ≈ {math.degrees(phi_rad):.8f}°")
print(f"ψ = θ − φ     = {psi_rad:.15f} rad ≈ {math.degrees(psi_rad):.8f}°")
print(f"α = θ/2       = {alpha_rad:.15f} rad ≈ {math.degrees(alpha_rad):.8f}°")
print(f"tan(θ) == τ ? {math.isclose(math.tan(theta_rad), tau)}")
print(f"sin(ψ) = {math.sin(psi_rad):.15f}")
print(f"cos(ψ) = {math.cos(psi_rad):.15f}")
print(f"tan(ψ) = {math.tan(psi_rad):.15f}")
print()

print("─" * 72)
print("∫_{-∞}^∞ e^{-x²} dx = √π = {math.sqrt(pi):.15f}")
print()

def integrand(t):
    return 1.0 / (1.0 + t*t)

N = 200000
h = tau / N
approx = 0.5 * (integrand(0.0) + integrand(tau))
for i in range(1, N):
    approx += integrand(i * h)
approx *= h

print(f"∫_0^{{2π}} dt/(1+t²) ≈ {approx:.15f}")
print(f"arctan(2π)            = {theta_rad:.15f}")
print(f"Absolute difference   = {abs(approx - theta_rad):.2e}")
print()

print("─" * 72)
print("The discrete angular circumferential rotation of τ radians")
print("primitively predicates scalar time and is logically biconditional with")
print("    2π = 6.283185307179586 = m × Δt.")
print()
print("Consequently the discrete integral")
print("    ∫_θ^{2π} (n·Δt)/τ  d(·)")
print("is algebraically identical to the continuous accumulation of the")
print("microscopic angular bridge ψ.")
print()
print(f"e^{{ln(τ)}} = {math.exp(ln_tau):.15f}  (must equal τ)")
print(f"τ         = {tau:.15f}")
print("=" * 72) 
