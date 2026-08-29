import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D

# Values from Kernel Division Bridge
psi = 0.1503378808
Re_tau = 1.4129651365
cos_psi = 0.9887205          # given
sin_Re = 0.98768834059       # given
K = 1.4144417210
k_norm = 0.7069927203

fig, ax = plt.subplots(figsize=(12, 12))

# Unit circle
theta = np.linspace(0, 2*np.pi, 600)
ax.plot(np.cos(theta), np.sin(theta), 'b-', linewidth=2.5, label='Unit Circle (r=1, Diameter=2)')

# Axes
ax.axhline(0, color='black', linewidth=1.0, zorder=1)
ax.axvline(0, color='black', linewidth=1.0, zorder=1)

# ========== Diameter (full width / full height) ==========
ax.plot([-1, 1], [0, 0], 'r-', linewidth=3.5, alpha=0.8, zorder=2)
ax.annotate('', xy=(1.02, 0), xytext=(-1.02, 0),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2.5))
ax.text(0, -0.18, 'Diameter = 2\n(= full WIDTH / full LENGTH)', ha='center', va='top',
        color='red', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red', alpha=0.9))

# Vertical diameter as HEIGHT
ax.plot([0, 0], [-1, 1], color='darkorange', linewidth=2.5, alpha=0.7, linestyle='--')
ax.annotate('', xy=(0, 1.02), xytext=(0, -1.02),
            arrowprops=dict(arrowstyle='<->', color='darkorange', lw=2))
ax.text(0.12, 0.7, 'HEIGHT\n= Diameter = 2', color='darkorange', fontsize=10, fontweight='bold')

# ========== Standard radian labels ==========
standard_angles = {
    0: '0',
    np.pi/6: r'$\pi/6$',
    np.pi/4: r'$\pi/4$',
    np.pi/3: r'$\pi/3$',
    np.pi/2: r'$\pi/2$',
    2*np.pi/3: r'$2\pi/3$',
    3*np.pi/4: r'$3\pi/4$',
    np.pi: r'$\pi$',
    5*np.pi/4: r'$5\pi/4$',
    3*np.pi/2: r'$3\pi/2$',
    7*np.pi/4: r'$7\pi/4$',
    11*np.pi/6: r'$11\pi/6$',
}

for ang, lab in standard_angles.items():
    ax.plot([0, 1.05*np.cos(ang)], [0, 1.05*np.sin(ang)], 'g--', alpha=0.35, lw=0.9)
    ax.text(1.18*np.cos(ang), 1.18*np.sin(ang), lab,
            ha='center', va='center', fontsize=9, color='darkgreen')

# ========== ψ (red) ==========
ax.plot([0, np.cos(psi)], [0, np.sin(psi)], 'r-', linewidth=3, zorder=5)
ax.plot(np.cos(psi), np.sin(psi), 'ro', markersize=10, zorder=6)
ax.text(1.32*np.cos(psi), 1.32*np.sin(psi), f'ψ ≈ {psi:.4f} rad',
        ha='left', va='center', fontsize=11, color='red', fontweight='bold')

# Arc for ψ
arc_psi = Arc((0,0), 0.35, 0.35, theta1=0, theta2=np.degrees(psi), color='red', lw=2.5)
ax.add_patch(arc_psi)

# Projections for ψ → WIDTH (cos) and HEIGHT (sin)
ax.plot([np.cos(psi), np.cos(psi)], [0, np.sin(psi)], 'r:', lw=1.8, alpha=0.8)
ax.plot([0, np.cos(psi)], [np.sin(psi), np.sin(psi)], 'r:', lw=1.8, alpha=0.8)
ax.text(np.cos(psi)/2, -0.08, f'WIDTH\ncos(ψ)≈{cos_psi:.5f}', ha='center', va='top',
        color='red', fontsize=9, fontweight='bold')
ax.text(np.cos(psi)+0.05, np.sin(psi)/2, f'HEIGHT\nsin(ψ)≈{np.sin(psi):.4f}', 
        ha='left', va='center', color='red', fontsize=9)

# ========== Re_τ (magenta) ==========
ax.plot([0, np.cos(Re_tau)], [0, np.sin(Re_tau)], color='magenta', linewidth=3, zorder=5)
ax.plot(np.cos(Re_tau), np.sin(Re_tau), 'o', color='magenta', markersize=10, zorder=6)
ax.text(1.28*np.cos(Re_tau), 1.28*np.sin(Re_tau), f'Re_τ ≈ {Re_tau:.4f} rad',
        ha='left', va='center', fontsize=11, color='magenta', fontweight='bold')

# Arc for Re_τ
arc_re = Arc((0,0), 0.55, 0.55, theta1=0, theta2=np.degrees(Re_tau), color='magenta', lw=2.5)
ax.add_patch(arc_re)

# Projections for Re_τ
ax.plot([np.cos(Re_tau), np.cos(Re_tau)], [0, np.sin(Re_tau)], color='magenta', linestyle=':', lw=1.8, alpha=0.8)
ax.plot([0, np.cos(Re_tau)], [np.sin(Re_tau), np.sin(Re_tau)], color='magenta', linestyle=':', lw=1.8, alpha=0.8)
ax.text(np.cos(Re_tau)-0.05, -0.12, f'WIDTH\ncos(Re_τ)≈{np.cos(Re_tau):.4f}', 
        ha='right', va='top', color='magenta', fontsize=9)
ax.text(np.cos(Re_tau)+0.08, np.sin(Re_tau)/2, f'HEIGHT\nsin(Re_τ)≈{sin_Re:.5f}\n(given)', 
        ha='left', va='center', color='magenta', fontsize=9, fontweight='bold')

# ========== Kernel info box ==========
info = (
    f"Kernel Division Bridge\n"
    f"─────────────────────\n"
    f"ψ          = {psi:.10f} rad\n"
    f"Re_τ       = {Re_tau:.10f} rad\n"
    f"cos(ψ)     ≈ {cos_psi:.7f}  (given)\n"
    f"sin(Re_τ)  ≈ {sin_Re:.8f}  (given)\n"
    f"K          = cos(ψ)·Re_τ / sin(Re_τ)\n"
    f"           ≈ {K:.10f}  (≈√2)\n"
    f"k_norm     = 1/K ≈ {k_norm:.10f}\n"
    f"\n"
    f"On unit circle:\n"
    f"• Diameter = full WIDTH = full HEIGHT = 2\n"
    f"• cos(θ) = horizontal WIDTH projection\n"
    f"• sin(θ) = vertical HEIGHT projection"
)
props = dict(boxstyle='round,pad=0.6', facecolor='lightyellow', edgecolor='black', alpha=0.95)
ax.text(-1.55, -1.55, info, fontsize=9, family='monospace', verticalalignment='bottom',
        bbox=props, linespacing=1.3)

# Title and limits
ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-1.7, 1.7)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_xlabel('cos θ  →  WIDTH / LENGTH projection', fontsize=12)
ax.set_ylabel('sin θ  →  HEIGHT projection', fontsize=12)
ax.set_title('Unit Circle Radians Graph\nLength • Height | Width • Diameter\nfrom Kernel Division Bridge (ψ & Re_τ)',
             fontsize=14, fontweight='bold', pad=15)

# Custom legend
legend_elements = [
    Line2D([0], [0], color='b', lw=2.5, label='Unit Circle (Diameter = 2)'),
    Line2D([0], [0], color='r', lw=3, label=f'ψ ≈ {psi:.4f} rad'),
    Line2D([0], [0], color='magenta', lw=3, label=f'Re_τ ≈ {Re_tau:.4f} rad'),
    Line2D([0], [0], color='red', lw=3.5, label='Diameter (= full Width/Length)'),
    Line2D([0], [0], color='darkorange', lw=2.5, linestyle='--', label='Height (= Diameter)'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.95)

plt.tight_layout()
plt.savefig('/tmp/kernel_circle_radians_dimensions.png', dpi=160, bbox_inches='tight')
print("Plot saved successfully")
plt.close()
