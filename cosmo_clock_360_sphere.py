import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

# Cosmo Clock precise values
psi = 0.1503378808
theta_eff = 1.21403
delta_phi = 1.72113420759

cos_psi = np.cos(psi)
sin_psi = np.sin(psi)
cos_te = np.cos(theta_eff)
sin_te = np.sin(theta_eff)
cos_dp = np.cos(delta_phi)
sin_dp = np.sin(delta_phi)

fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')
# ========== Unit Sphere ==========
u = np.linspace(0, 2 * np.pi, 70)
v = np.linspace(0, np.pi, 35)
x_s = np.outer(np.cos(u), np.sin(v))
y_s = np.outer(np.sin(u), np.sin(v))
z_s = np.outer(np.ones_like(u), np.cos(v))
ax.plot_surface(x_s, y_s, z_s, color='royalblue', alpha=0.13, edgecolor='none')
ax.plot_wireframe(x_s, y_s, z_s, color='blue', alpha=0.22, linewidth=0.35)

# Equator (great circle, full 2π)
eq = np.linspace(0, 2*np.pi, 120)
ax.plot(np.cos(eq), np.sin(eq), 0, 'b-', lw=2.2, alpha=0.75, label='Equator (arc length 2π)')

# ========== Diameters ==========
# X-diameter (LENGTH / WIDTH)
ax.plot([-1.18, 1.18], [0, 0], [0, 0], 'r-', lw=3.5, alpha=0.9)
ax.text(1.35, 0, -0.05, 'Diameter = 2\n(LENGTH / WIDTH)', color='red', fontsize=9, fontweight='bold')

# Y-diameter (WIDTH)
ax.plot([0, 0], [-1.18, 1.18], [0, 0], color='darkorange', lw=2.5, alpha=0.85)
ax.text(0, 1.35, 0, 'WIDTH', color='darkorange', fontsize=9, fontweight='bold')

# Z-diameter (HEIGHT)
ax.plot([0, 0], [0, 0], [-1.18, 1.18], color='purple', lw=2.5, alpha=0.85)
ax.text(0.05, 0, 1.35, 'HEIGHT = 2', color='purple', fontsize=9, fontweight='bold')
# ========== Helper to draw angle on equatorial plane (great-circle arc) ==========
def draw_sphere_angle(ax, ang, color, label, short, cos_v, sin_v, arc_r=0.4):
    # Radius (great-circle direction in XY plane)
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], [0, 0], color=color, lw=3.0, zorder=5)
    ax.scatter([np.cos(ang)], [np.sin(ang)], [0], color=color, s=70, zorder=6)
    
    # Arc on the sphere equator
    phi_arc = np.linspace(0, ang, 50)
    ax.plot(arc_r * np.cos(phi_arc), arc_r * np.sin(phi_arc), 0, color=color, lw=2.8)
    
    # Label
    off = 1.32
    ax.text(off*np.cos(ang), off*np.sin(ang), 0.08,
            f'{short}\n{ang:.5f} rad\nArc={ang:.5f}',
            color=color, fontsize=8.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=color, alpha=0.9))
# Projection drop lines (width / height style)
    ax.plot([np.cos(ang), np.cos(ang)], [0, np.sin(ang)], [0, 0], color=color, ls=':', lw=1.4, alpha=0.75)
    ax.plot([0, np.cos(ang)], [np.sin(ang), np.sin(ang)], [0, 0], color=color, ls=':', lw=1.4, alpha=0.75)

# Draw the three Cosmo Clock angles
draw_sphere_angle(ax, psi, 'red', 'ψ angular bridge', 'ψ', cos_psi, sin_psi, arc_r=0.32)
draw_sphere_angle(ax, theta_eff, 'green', 'θ_eff rotation', 'θ_eff', cos_te, sin_te, arc_r=0.48)
draw_sphere_angle(ax, delta_phi, 'magenta', 'Δφ_torque phase slip', 'Δφ_torque', cos_dp, sin_dp, arc_r=0.65)
# ========== Identity annotation ==========
ax.text(-0.9, -0.9, 0.9, r'$\sin(\Delta\phi_{\rm torque})=\cos\psi$' + f'\n≈ {sin_dp:.8f}',
        color='purple', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lavender', edgecolor='purple', alpha=0.95))

# ========== Radian markers ==========
for ang, lab in [(0, '0'), (np.pi/2, r'π/2'), (np.pi, r'π'), (3*np.pi/2, r'3π/2')]:
    ax.text(1.28*np.cos(ang), 1.28*np.sin(ang), 0, lab, color='darkgreen', fontsize=9)
# ========== Info box ==========
info = (
    "Joshua Christopher Ryan’s Cosmological Clock\n"
    "360° Sphere Radians Representation\n"
    "Arc Length • Height | Width • Diameter\n"
    "────────────────────────────────────────\n"
    f"ψ (angular bridge)     = {psi:.10f} rad\n"
    f"  Arc length (great circle) = {psi:.10f}\n"
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
    "Unit sphere geometry:\n"
    "• Diameter = 2 = full LENGTH = full WIDTH = full HEIGHT\n"
    "• Great-circle arc length = central angle (radians)\n"
    "• Full equator circumference = 2π\n"
    "• Full solid angle = 4π steradians\n"
    "• Width = cos θ (horizontal projection)\n"
    "• Height = sin θ (vertical projection)\n"
    "Identity: sin(Δφ_torque) = cos ψ  (machine precision)"
)
fig.text(0.02, 0.02, info, fontsize=8.2, family='monospace',
         verticalalignment='bottom', linespacing=1.2,
         bbox=dict(boxstyle='round,pad=0.45', facecolor='lightyellow', edgecolor='black', alpha=0.95))
# View and labels
ax.set_xlim(-1.55, 1.55)
ax.set_ylim(-1.55, 1.55)
ax.set_zlim(-1.55, 1.55)
ax.set_xlabel('X  (LENGTH / WIDTH)', fontsize=10)
ax.set_ylabel('Y  (WIDTH)', fontsize=10)
ax.set_zlabel('Z  (HEIGHT)', fontsize=10)
ax.set_title("Joshua Christopher Ryan’s Cosmological Clock\n"
             "360° Sphere Radians Representation\n"
             "Arc Length • Height | Width • Diameter\n"
             "(from Unit Circle Radians Graph)",
             fontsize=13, fontweight='bold', pad=12)

ax.view_init(elev=22, azim=38)

legend_elems = [
    Line2D([0], [0], color='blue', lw=2.2, label='Unit Sphere + Equator (2π)'),
    Line2D([0], [0], color='red', lw=3.5, label='Diameter = 2 (Length/Width)'),
    Line2D([0], [0], color='purple', lw=2.5, label='Height = Diameter = 2'),
    Line2D([0], [0], color='red', lw=3, label=f'ψ ≈ {psi:.5f} rad (angular bridge)'),
    Line2D([0], [0], color='green', lw=3, label=f'θ_eff ≈ {theta_eff:.5f} rad (rotation)'),
    Line2D([0], [0], color='magenta', lw=3, label=f'Δφ_torque ≈ {delta_phi:.5f} rad (phase slip)'),
]
ax.legend(handles=legend_elems, loc='upper left', fontsize=8, framealpha=0.95)

plt.tight_layout(rect=[0, 0.26, 1, 0.97])
plt.savefig('/tmp/jcr_cosmo_clock_360_sphere.png', dpi=160, bbox_inches='tight', facecolor='white')
print("360° Sphere Cosmo Clock plot saved")
print(f"Identity check: sin(Δφ) - cos(ψ) = {sin_dp - cos_psi:.2e}")
plt.close()
