import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# ===== Left: Rectangle / Box (Length, Width, Height) =====
ax1 = axes[0]
ax1.set_xlim(-0.5, 5)
ax1.set_ylim(-0.5, 4)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Rectangular Prism / Box\nLength • Width • Height', fontsize=14, fontweight='bold')

# Draw a 3D-looking box (isometric-ish)
# Front face
front = Rectangle((0.5, 0.5), 3, 2, linewidth=2, edgecolor='navy', facecolor='lightblue', alpha=0.7)
ax1.add_patch(front)

# Top face
top_x = [0.5, 1.5, 4.5, 3.5]
top_y = [2.5, 3.5, 3.5, 2.5]
ax1.fill(top_x, top_y, color='skyblue', alpha=0.7, edgecolor='navy', linewidth=2)

# Side face
side_x = [3.5, 4.5, 4.5, 3.5]
side_y = [0.5, 1.5, 3.5, 2.5]
ax1.fill(side_x, side_y, color='steelblue', alpha=0.7, edgecolor='navy', linewidth=2)

# Dimension arrows and labels
# Length (along x, front bottom)
ax1.annotate('', xy=(0.5, 0.3), xytext=(3.5, 0.3),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax1.text(2.0, 0.1, 'LENGTH', ha='center', va='top', fontsize=11, color='red', fontweight='bold')

# Height (vertical front)
ax1.annotate('', xy=(0.3, 0.5), xytext=(0.3, 2.5),
            arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax1.text(0.1, 1.5, 'HEIGHT', ha='right', va='center', fontsize=11, color='green', fontweight='bold', rotation=90)

# Width (depth, on top/side)
ax1.annotate('', xy=(3.7, 2.6), xytext=(4.5, 3.4),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax1.text(4.3, 3.0, 'WIDTH', ha='left', va='bottom', fontsize=11, color='purple', fontweight='bold')

# ===== Right: Circle / Cylinder (Diameter, Radius, Height) =====
ax2 = axes[1]
ax2.set_xlim(-1.5, 4)
ax2.set_ylim(-1.5, 4)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Circle / Cylinder\nDiameter • Radius • Height (or Length)', fontsize=14, fontweight='bold')

# Cylinder body (side view simplified as rectangle + ellipses)
# Main body
body = Rectangle((0.5, 0.5), 2, 2.5, linewidth=2, edgecolor='darkred', facecolor='lightcoral', alpha=0.6)
ax2.add_patch(body)

# Top ellipse
from matplotlib.patches import Ellipse
top_ell = Ellipse((1.5, 3.0), 2, 0.6, linewidth=2, edgecolor='darkred', facecolor='salmon', alpha=0.8)
ax2.add_patch(top_ell)

# Bottom ellipse (partial)
bottom_ell = Ellipse((1.5, 0.5), 2, 0.6, linewidth=2, edgecolor='darkred', facecolor='none')
ax2.add_patch(bottom_ell)
# Draw lower half dashed or something
theta = np.linspace(np.pi, 2*np.pi, 50)
ax2.plot(1.5 + 1*np.cos(theta), 0.5 + 0.3*np.sin(theta), 'darkred', lw=2)

# Circle face (front view on the side)
circle = Circle((-0.3, 2.0), 0.9, linewidth=2, edgecolor='darkorange', facecolor='moccasin', alpha=0.8)
ax2.add_patch(circle)

# Diameter on the circle
ax2.annotate('', xy=(-1.2, 2.0), xytext=(0.6, 2.0),
            arrowprops=dict(arrowstyle='<->', color='darkorange', lw=2.5))
ax2.text(-0.3, 1.7, 'DIAMETER', ha='center', va='top', fontsize=11, color='darkorange', fontweight='bold')

# Radius
ax2.plot([-0.3, 0.6], [2.0, 2.0], 'orange', lw=1.5)
ax2.plot(0.6, 2.0, 'o', color='orange')
ax2.text(0.2, 2.15, 'RADIUS', ha='center', fontsize=9, color='orange')

# Height of cylinder
ax2.annotate('', xy=(2.7, 0.5), xytext=(2.7, 3.0),
            arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax2.text(2.9, 1.75, 'HEIGHT\n(or LENGTH)', ha='left', va='center', fontsize=11, color='green', fontweight='bold')

# Width note
ax2.text(1.5, -0.8, 'WIDTH ≈ DIAMETER\n(for circular cross-section)', ha='center', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Common relations
fig.suptitle('Length / Height  |  Width / Diameter', fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('/tmp/dimensions_length_height_width_diameter.png', dpi=150, bbox_inches='tight')
print("Saved")
plt.close()
