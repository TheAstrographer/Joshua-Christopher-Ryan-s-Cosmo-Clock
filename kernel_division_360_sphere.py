import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch
import matplotlib.lines as mlines

# Kernel values
psi = 0.1503378808
Re_tau = 1.4129651365
cos_psi = 0.9887205
sin_Re = 0.98768834059
K = 1.4144417210
k_norm = 0.7069927203

fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# ========== Unit Sphere ==========
u = np.linspace(0, 2 * np.pi, 80)
v = np.linspace(0, np.pi, 40)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x, y, z, color='royalblue', alpha=0.15, edgecolor='none')

# Wireframe for better visibility
ax.plot_wireframe(x, y, z, color='blue', alpha=0.25, linewidth=0.4)

# ========== Equator (full 2π circumference) ==========
eq_u = np.linspace(0, 2*np.pi, 100)
ax.plot(np.cos(eq_u), np.sin(eq_u), np.zeros_like(eq_u), 'b-', linewidth=2.5, label='Equator (2π radians)')

# ========== Key meridians / great circles ==========
# XZ plane meridian (0 and π)
mer_v = np.linspace(0, np.pi, 50)
ax.plot(np.sin(mer_v), np.zeros_like(mer_v), np.cos(mer_v), 'g--', alpha=0.5, lw=1.2)
ax.plot(-np.sin(mer_v), np.zeros_like(mer_v), np.cos(mer_v), 'g--', alpha=0.5, lw=1.2)

# ========== Diameter lines ==========
# X-diameter (Length / Width)
ax.plot([-1.05, 1.05], [0, 0], [0, 0], 'r-', linewidth=3.5, alpha=0.9)
ax.text(1.2, 0, 0, 'Diameter = 2\n(LENGTH / WIDTH)', color='red', fontsize=10, fontweight='bold')

# Y-diameter
ax.plot([0, 0], [-1.05, 1.05], [0, 0], color='darkorange', linewidth=2.5, alpha=0.8)
ax.text(0, 1.25, 0, 'Diameter\n(WIDTH)', color='darkorange', fontsize=9)

# Z-diameter (Height)
ax.plot([0, 0], [0, 0], [-1.05, 1.05], color='purple', linewidth=2.5, alpha=0.8)
ax.text(0, 0, 1.25, 'HEIGHT\n= Diameter = 2', color='purple', fontsize=10, fontweight='bold')

# ========== Highlight ψ (small angle from +X axis in XY plane) ==========
# Ray for ψ
ax.plot([0, np.cos(psi)], [0, np.sin(psi)], [0, 0], 'r-', linewidth=4, zorder=10)
ax.scatter([np.cos(psi)], [np.sin(psi)], [0], color='red', s=80, zorder=11)
ax.text(1.15*np.cos(psi), 1.15*np.sin(psi), 0.1, f'ψ ≈ {psi:.4f} rad', 
        color='red', fontsize=11, fontweight='bold')

# Small arc for ψ on equator
arc_psi = np.linspace(0, psi, 30)
ax.plot(0.3*np.cos(arc_psi), 0.3*np.sin(arc_psi), np.zeros_like(arc_psi), 'r-', lw=3)

# ========== Highlight Re_τ ==========
# Place Re_τ in the XZ plane as polar-ish angle from +X toward +Z for visibility
# or keep it in XY plane for consistency with previous 2D
ax.plot([0, np.cos(Re_tau)], [0, np.sin(Re_tau)], [0, 0], color='magenta', linewidth=4, zorder=10)
ax.scatter([np.cos(Re_tau)], [np.sin(Re_tau)], [0], color='magenta', s=80, zorder=11)
ax.text(1.2*np.cos(Re_tau), 1.2*np.sin(Re_tau), 0.15, f'Re_τ ≈ {Re_tau:.4f} rad',
        color='magenta', fontsize=11, fontweight='bold')

# Arc for Re_τ
arc_re = np.linspace(0, Re_tau, 40)
ax.plot(0.45*np.cos(arc_re), 0.45*np.sin(arc_re), np.zeros_like(arc_re), color='magenta', lw=3)

# ========== Projections (height / width style) ==========
# For ψ: horizontal (cos) and "height" in plane (sin)
ax.plot([np.cos(psi), np.cos(psi)], [0, np.sin(psi)], [0, 0], 'r:', lw=1.5, alpha=0.7)
ax.plot([0, np.cos(psi)], [np.sin(psi), np.sin(psi)], [0, 0], 'r:', lw=1.5, alpha=0.7)

# For Re_τ
ax.plot([np.cos(Re_tau), np.cos(Re_tau)], [0, np.sin(Re_tau)], [0, 0], color='magenta', linestyle=':', lw=1.5, alpha=0.7)
ax.plot([0, np.cos(Re_tau)], [np.sin(Re_tau), np.sin(Re_tau)], [0, 0], color='magenta', linestyle=':', lw=1.5, alpha=0.7)

# ========== Radian markers on equator (selected) ==========
radian_labels = {
    0: '0',
    np.pi/2: r'$\pi/2$',
    np.pi: r'$\pi$',
    3*np.pi/2: r'$3\pi/2$',
    2*np.pi: r'$2\pi$'
}
for ang, lab in radian_labels.items():
    ax.text(1.35*np.cos(ang), 1.35*np.sin(ang), 0, lab, color='darkgreen', fontsize=10, ha='center')

# ========== Info text ==========
info_text = (
    "Kernel Division Bridge  →  360° Sphere (4π steradians solid angle)\n"
    "────────────────────────────────────────────────\n"
    f"ψ          = {psi:.10f} rad   ≈ {np.degrees(psi):.2f}°\n"
    f"Re_τ       = {Re_tau:.10f} rad   ≈ {np.degrees(Re_tau):.2f}°\n"
    f"cos(ψ)     ≈ {cos_psi:.7f}   (WIDTH projection)\n"
    f"sin(Re_τ)  ≈ {sin_Re:.8f}  (HEIGHT projection, given)\n"
    f"K          ≈ {K:.10f}   (≈ √2)\n"
    f"k_norm     ≈ {k_norm:.10f}\n\n"
    "Sphere geometry:\n"
    "• Diameter = 2  (= full LENGTH = full WIDTH = full HEIGHT)\n"
    "• Circumference of great circle = 2π radians\n"
    "• Full solid angle = 4π steradians\n"
    "• cos(θ) → horizontal WIDTH / LENGTH component\n"
    "• sin(θ) → transverse HEIGHT / WIDTH component"
)

# Position the text in 3D space is tricky; use fig.text instead
fig.text(0.02, 0.02, info_text, fontsize=9, family='monospace',
         verticalalignment='bottom', linespacing=1.25,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='lightyellow', edgecolor='black', alpha=0.95))

# ========== View & labels ==========
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_zlim(-1.6, 1.6)
ax.set_xlabel('X  (LENGTH / WIDTH)', fontsize=11)
ax.set_ylabel('Y  (WIDTH)', fontsize=11)
ax.set_zlabel('Z  (HEIGHT)', fontsize=11)
ax.set_title('360° Sphere Radians Representation\nLength • Height | Width • Diameter\nfrom Kernel Division Bridge (ψ & Re_τ)',
             fontsize=14, fontweight='bold', pad=20)

# Better viewing angle
ax.view_init(elev=22, azim=35)

# Legend
legend_elements = [
    mlines.Line2D([0], [0], color='blue', lw=2.5, label='Unit Sphere + Equator (2π)'),
    mlines.Line2D([0], [0], color='red', lw=4, label=f'ψ ≈ {psi:.4f} rad'),
    mlines.Line2D([0], [0], color='magenta', lw=4, label=f'Re_τ ≈ {Re_tau:.4f} rad'),
    mlines.Line2D([0], [0], color='red', lw=3.5, label='Diameter = 2 (Length/Width)'),
    mlines.Line2D([0], [0], color='purple', lw=2.5, label='Height = Diameter = 2'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.95)

plt.tight_layout(rect=[0, 0.18, 1, 1])  # leave space for the info box
plt.savefig('/tmp/kernel_360_sphere_radians.png', dpi=160, bbox_inches='tight', facecolor='white')
print("3D Sphere plot saved")
plt.close()
