import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

# Precise values from Cosmo Clock / Kernel
psi = 0.1503378808
theta_eff = 1.21403
delta_phi = 1.72113420759   # more precise from repo

# Computed projections
cos_psi = np.cos(psi)
sin_psi = np.sin(psi)
cos_te = np.cos(theta_eff)
sin_te = np.sin(theta_eff)
cos_dp = np.cos(delta_phi)
sin_dp = np.sin(delta_phi)

print("Verification: sin(delta_phi) ≈", sin_dp, "  cos(psi) ≈", cos_psi)

fig, ax = plt.subplots(figsize=(12, 12))

# Unit circle
theta = np.linspace(0, 2*np.pi, 600)
ax.plot(np.cos(theta), np.sin(theta), 'b-', linewidth=2.8, label='Unit Circle (r=1, Diameter=2)', zorder=2)

# Axes
ax.axhline(0, color='black', linewidth=1.0, zorder=1)
ax.axvline(0, color='black', linewidth=1.0, zorder=1)

# ========== Diameter (full Length / Width) ==========
ax.annotate('', xy=(1.02, 0), xytext=(-1.02, 0),
            arrowprops=dict(arrowstyle='<->', color='red', lw=3))
ax.text(0, -0.22, 'Diameter = 2\n(= full WIDTH / LENGTH)', ha='center', va='top',
        color='red', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='red', alpha=0.9))

# Vertical height reference
ax.annotate('', xy=(0, 1.02), xytext=(0, -1.02),
            arrowprops=dict(arrowstyle='<->', color='darkorange', lw=2, linestyle='--'))
ax.text(0.15, 0.85, 'HEIGHT\nmax = 2', color='darkorange', fontsize=10, fontweight='bold')

# ========== Helper function to draw one angle ==========
def draw_angle(ax, ang, color, name, short_name, cos_val, sin_val, arc_r=0.35):
    # Radius line
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=color, linewidth=2.8, zorder=4)
    ax.plot(np.cos(ang), np.sin(ang), 'o', color=color, markersize=10, zorder=5)
    
    # Arc
    arc = Arc((0, 0), 2*arc_r, 2*arc_r, theta1=0, theta2=np.degrees(ang),
              color=color, lw=2.5, zorder=3)
    ax.add_patch(arc)
    
    # Label near the point
    offset = 1.28
    ax.text(offset*np.cos(ang), offset*np.sin(ang), 
            f'{short_name}\n{ang:.5f} rad\nArc = {ang:.5f}',
            ha='center', va='center', fontsize=9, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color, alpha=0.85))
    
    # Width (cos) drop line
    ax.plot([np.cos(ang), np.cos(ang)], [0, np.sin(ang)], color=color, linestyle=':', lw=1.6, alpha=0.8)
    # Height (sin) drop line
    ax.plot([0, np.cos(ang)], [np.sin(ang), np.sin(ang)], color=color, linestyle=':', lw=1.6, alpha=0.8)
    
    # Small text for projections
    if sin_val > 0.05:
        ax.text(np.cos(ang) + 0.03, sin_val/2, f'H={sin_val:.5f}', 
                color=color, fontsize=8, rotation=90, va='center')
    ax.text(np.cos(ang)/2, -0.09 if ang < np.pi/2 else 0.05, f'W={cos_val:.5f}',
            color=color, fontsize=8, ha='center')

# Draw the three Cosmo Clock angles
draw_angle(ax, psi, 'red', 'ψ (angular bridge)', 'ψ', cos_psi, sin_psi, arc_r=0.28)
draw_angle(ax, theta_eff, 'green', 'θ_eff (rotation)', 'θ_eff', cos_te, sin_te, arc_r=0.45)
draw_angle(ax, delta_phi, 'magenta', 'Δφ_torque (phase slip)', 'Δφ_torque', cos_dp, sin_dp, arc_r=0.62)

# ========== Central identity annotation ==========
ax.annotate('', xy=(np.cos(delta_phi), np.sin(delta_phi)), 
            xytext=(np.cos(psi), np.sin(psi)),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.5, connectionstyle='arc3,rad=0.2'))
ax.text(-0.6, 0.55, r'$\sin(\Delta\phi_{\rm torque}) = \cos\psi$' + f'\n≈ {sin_dp:.8f}',
        color='purple', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='lavender', edgecolor='purple', alpha=0.95))

# ========== Info box ==========
info = (
    "Joshua Christopher Ryan’s Cosmological Clock\n"
    "Unit Circle Radians Graph\n"
    "─────────────────────────────────────\n"
    f"ψ (angular bridge)     = {psi:.10f} rad\n"
    f"  Arc length           = {psi:.10f}\n"
    f"  Width  cos ψ         ≈ {cos_psi:.8f}\n"
    f"  Height sin ψ         ≈ {sin_psi:.8f}\n\n"
    f"θ_eff (rotation)       ≈ {theta_eff:.5f} rad\n"
    f"  Arc length           ≈ {theta_eff:.5f}\n"
    f"  Width  cos θ_eff     ≈ {cos_te:.5f}\n"
    f"  Height sin θ_eff     ≈ {sin_te:.5f}\n\n"
    f"Δφ_torque (phase slip) ≈ {delta_phi:.8f} rad\n"
    f"  Arc length           ≈ {delta_phi:.8f}\n"
    f"  Width  cos Δφ        ≈ {cos_dp:.5f}\n"
    f"  Height sin Δφ        ≈ {sin_dp:.8f}\n\n"
    "On unit circle (r=1):\n"
    "• Diameter = 2 = full WIDTH / LENGTH\n"
    "• Arc length = θ (radians)\n"
    "• Width  = cos θ (horizontal)\n"
    "• Height = sin θ (vertical)\n"
    "Identity: sin(Δφ_torque) = cos ψ"
)
props = dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black', alpha=0.95)
ax.text(-1.65, -1.55, info, fontsize=8.5, family='monospace', va='bottom', bbox=props, linespacing=1.2)

# Limits, title, legend
ax.set_xlim(-1.75, 1.75)
ax.set_ylim(-1.75, 1.75)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_xlabel('Width = cos θ   (LENGTH / WIDTH projection)', fontsize=12)
ax.set_ylabel('Height = sin θ   (HEIGHT projection)', fontsize=12)
ax.set_title("Joshua Christopher Ryan’s Cosmological Clock\n"
             "Unit Circle Radians Graph\n"
             "Length / Arc Length • Height • Width • Diameter",
             fontsize=14, fontweight='bold', pad=12)

legend_elements = [
    Line2D([0], [0], color='b', lw=2.8, label='Unit Circle (r=1, Diameter=2)'),
    Line2D([0], [0], color='red', lw=2.8, label=f'ψ ≈ {psi:.5f} rad (angular bridge)'),
    Line2D([0], [0], color='green', lw=2.8, label=f'θ_eff ≈ {theta_eff:.5f} rad (rotation)'),
    Line2D([0], [0], color='magenta', lw=2.8, label=f'Δφ_torque ≈ {delta_phi:.5f} rad (phase slip)'),
    Line2D([0], [0], color='red', lw=3, label='Diameter = 2'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.95)

plt.tight_layout()
plt.savefig('/tmp/jcr_cosmo_clock_unit_circle.png', dpi=170, bbox_inches='tight', facecolor='white')
print("Cosmo Clock unit circle graph saved")
plt.close()
