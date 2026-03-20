#!/usr/bin/env python3
"""
Cosmic Yoyo Animation - The Universe Breathing
===============================================
Creates an animated visualization of the oscillating brane cosmology
showing the membrane vibration, dark energy evolution, and structure
growth suppression over 13.8 billion years of cosmic history.

Author: Romain Provencal (with Claude & Gemini DeepThink)
Version: 6.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.integrate import quad

# ==========================================
# COSMOLOGICAL PARAMETERS
# ==========================================
T_osc = 2.0           # Oscillation period (Gyr)
A_w = 0.003           # w(z) oscillation amplitude
A_brane = 0.1         # Brane displacement amplitude (normalized)
t_universe = 13.8     # Age of universe (Gyr)
H0 = 67.4             # Hubble constant
Omega_m = 0.315       # Matter density
Omega_L = 0.685       # Dark energy density

# Time array for animation (0 to 13.8 Gyr)
n_frames = 120
time_array = np.linspace(0, t_universe, n_frames)

# Extended arrays for smooth plotting
time_plot = np.linspace(0, t_universe, 1000)

# ==========================================
# PHYSICS CALCULATIONS
# ==========================================

def brane_displacement(t):
    """Membrane displacement in extra dimension"""
    # Start oscillating after reheating (~1 Gyr)
    oscillation = np.where(t > 1.0,
                          A_brane * np.sin(2 * np.pi * (t - 1.0) / T_osc),
                          0)
    return oscillation

def w_dark_energy(t):
    """Dark energy equation of state evolution"""
    # Oscillates around -1
    w_lcdm = -1.0
    oscillation = np.where(t > 1.0,
                          A_w * np.sin(2 * np.pi * (t - 1.0) / T_osc),
                          0)
    return w_lcdm + oscillation

def s8_evolution(t):
    """S8 parameter evolution with growth suppression"""
    # Start at high value, suppress over time due to oscillations
    s8_initial = 0.83  # Planck value

    # Calculate cumulative suppression
    suppression = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti > 1.0:
            # Number of oscillations completed
            n_osc = (ti - 1.0) / T_osc
            # Each oscillation suppresses growth slightly
            cumulative_suppression = 1.0 - 0.052 * (1.0 - np.exp(-n_osc/3))
            suppression[i] = cumulative_suppression
        else:
            suppression[i] = 1.0

    return s8_initial * suppression

# ==========================================
# ANIMATION SETUP
# ==========================================

# Create figure with dark background
plt.style.use('dark_background')
fig = plt.figure(figsize=(10, 12))

# Create three subplots
ax1 = plt.subplot(3, 1, 1)  # Brane displacement
ax2 = plt.subplot(3, 1, 2)  # Dark energy w(z)
ax3 = plt.subplot(3, 1, 3)  # S8 evolution

# Set up the axes
for ax in [ax1, ax2, ax3]:
    ax.set_xlim(0, t_universe)
    ax.grid(True, alpha=0.2, linestyle=':')
    ax.set_xlabel('Cosmic Time (Gyr)', fontsize=11)

# Specific y-axis settings
ax1.set_ylim(-A_brane * 1.2, A_brane * 1.2)
ax1.set_ylabel('Brane Displacement z(t)', fontsize=11)
ax1.set_title('The Cosmic Yoyo: 13.8 Billion Years of Oscillation',
              fontsize=14, color='white', pad=15)

ax2.set_ylim(-1.005, -0.995)
ax2.set_ylabel('Dark Energy w(t)', fontsize=11)
ax2.axhline(y=-1.0, color='gray', linestyle='--', alpha=0.5, label='ΛCDM')

ax3.set_ylim(0.76, 0.84)
ax3.set_ylabel('S₈ Parameter', fontsize=11)
ax3.axhline(y=0.787, color='#00ffcc', linestyle='--', alpha=0.5,
            label='Target (Weak Lensing)')

# Initialize plot elements
line1, = ax1.plot([], [], color='#00ffcc', linewidth=2.5, label='Membrane')
line2, = ax2.plot([], [], color='#00ffcc', linewidth=2.5, label='Oscillating Brane')
line2_lcdm, = ax2.plot([], [], color='gray', linestyle='--', linewidth=2,
                       alpha=0.7, label='ΛCDM')
line3, = ax3.plot([], [], color='#00ffcc', linewidth=2.5, label='Structure Growth')
line3_lcdm, = ax3.plot([], [], color='gray', linestyle='--', linewidth=2,
                       alpha=0.7, label='ΛCDM')

# Vertical time cursor
cursor1 = ax1.axvline(x=0, color='yellow', alpha=0.5, linewidth=1)
cursor2 = ax2.axvline(x=0, color='yellow', alpha=0.5, linewidth=1)
cursor3 = ax3.axvline(x=0, color='yellow', alpha=0.5, linewidth=1)

# Add phase markers
for t_mark in np.arange(1.0, t_universe, T_osc):
    ax1.axvline(x=t_mark, color='cyan', alpha=0.1, linewidth=0.5)
    ax2.axvline(x=t_mark, color='cyan', alpha=0.1, linewidth=0.5)
    ax3.axvline(x=t_mark, color='cyan', alpha=0.1, linewidth=0.5)

# Add legends
ax1.legend(loc='upper right', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)
ax3.legend(loc='upper right', fontsize=10)

# Add epoch labels
ax1.text(0.5, 0.08, 'Inflation', fontsize=9, alpha=0.7)
ax1.text(3, 0.08, 'First Oscillation', fontsize=9, alpha=0.7)
ax1.text(10, 0.08, 'Present', fontsize=9, alpha=0.7)

# ==========================================
# ANIMATION FUNCTIONS
# ==========================================

def init():
    """Initialize animation"""
    line1.set_data([], [])
    line2.set_data([], [])
    line2_lcdm.set_data([], [])
    line3.set_data([], [])
    line3_lcdm.set_data([], [])
    return line1, line2, line2_lcdm, line3, line3_lcdm

def animate(frame):
    """Animation update function"""
    # Current time
    t_current = time_array[frame]

    # Time arrays up to current
    t_past = time_plot[time_plot <= t_current]

    if len(t_past) > 0:
        # Calculate physics
        z_brane = brane_displacement(t_past)
        w_osc = w_dark_energy(t_past)
        s8_osc = s8_evolution(t_past)

        # ΛCDM values (constant)
        w_lcdm_array = np.full_like(t_past, -1.0)
        s8_lcdm_array = np.full_like(t_past, 0.83)

        # Update lines
        line1.set_data(t_past, z_brane)
        line2.set_data(t_past, w_osc)
        line2_lcdm.set_data(t_past, w_lcdm_array)
        line3.set_data(t_past, s8_osc)
        line3_lcdm.set_data(t_past, s8_lcdm_array)

        # Update cursors
        cursor1.set_xdata([t_current, t_current])
        cursor2.set_xdata([t_current, t_current])
        cursor3.set_xdata([t_current, t_current])

        # Update title with current time
        ax1.set_title(f'The Cosmic Yoyo: t = {t_current:.1f} Gyr (z = {np.interp(t_current, [0, 13.8], [1100, 0]):.0f})',
                      fontsize=14, color='white', pad=15)

    return line1, line2, line2_lcdm, line3, line3_lcdm, cursor1, cursor2, cursor3

# ==========================================
# CREATE AND SAVE ANIMATION
# ==========================================

print("🎬 Creating cosmic animation...")
print(f"   - Frames: {n_frames}")
print(f"   - Duration: ~{n_frames/10:.1f} seconds at 10 fps")

# Create animation
ani = animation.FuncAnimation(fig, animate, init_func=init,
                            frames=n_frames, interval=100,
                            blit=True, repeat=True)

# Save as GIF
writer = PillowWriter(fps=10, metadata=dict(artist='Cosmic Yoyo Theory'),
                     bitrate=1800)

output_path = '/root/bulk/oscillating-brane-DM/plots/cosmic_yoyo_animation.gif'
ani.save(output_path, writer=writer, dpi=80)

print(f"✅ Animation saved to {output_path}")

# Also save first and last frame as static images
fig.savefig('/root/bulk/oscillating-brane-DM/plots/cosmic_yoyo_frame_first.png',
            dpi=100, bbox_inches='tight', facecolor='black')

# Animate to last frame for final image
animate(n_frames - 1)
fig.savefig('/root/bulk/oscillating-brane-DM/plots/cosmic_yoyo_frame_last.png',
            dpi=100, bbox_inches='tight', facecolor='black')

print("✅ Static frames saved")
print("\n🌌 The Universe is now breathing on your screen!")

plt.close()  # Close to free memory

# Create a simplified version for faster loading
print("\n🎬 Creating lightweight version for web...")
fig_simple = plt.figure(figsize=(8, 6))
ax = plt.subplot(1, 1, 1)
ax.set_xlim(0, t_universe)
ax.set_ylim(-A_brane * 1.2, A_brane * 1.2)
ax.set_xlabel('Cosmic Time (Gyr)', fontsize=12)
ax.set_ylabel('Membrane Displacement', fontsize=12)
ax.set_title('The Cosmic Yoyo: Watch the Universe Breathe', fontsize=14)
ax.grid(True, alpha=0.2, linestyle=':')

line_simple, = ax.plot([], [], color='#00ffcc', linewidth=3)
cursor_simple = ax.axvline(x=0, color='yellow', alpha=0.5, linewidth=1)

def animate_simple(frame):
    t_current = time_array[frame]
    t_past = time_plot[time_plot <= t_current]
    if len(t_past) > 0:
        z_brane = brane_displacement(t_past)
        line_simple.set_data(t_past, z_brane)
        cursor_simple.set_xdata([t_current, t_current])
    return line_simple, cursor_simple

ani_simple = animation.FuncAnimation(fig_simple, animate_simple,
                                    frames=60, interval=100,
                                    blit=True, repeat=True)

ani_simple.save('/root/bulk/oscillating-brane-DM/plots/cosmic_yoyo_simple.gif',
                writer=PillowWriter(fps=10), dpi=60)

print("✅ Lightweight version saved")
print("\nAnimation creation complete! 🚀")