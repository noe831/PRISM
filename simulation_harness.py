import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kinematic_verification_n import sovereign_observer, planar_2dof_fk

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'mathtext.fontset': 'stix' # Makes math look like LaTeX
})

def generate_telemetry_load(n_joints, duration_sec=10, frequency_hz=100):
    """Simulates real-time joint telemetry with Gaussian noise."""
    timestamps = np.linspace(0, duration_sec, duration_sec * frequency_hz)
    data = []
    
    for t in timestamps:
        # Simulate a trajectory moving toward a singularity (q_i -> 0)
        q_sim = np.array([0.5 * np.cos(t)] * n_joints) 
        
        # Execute the Independent Observer Audit
        is_safe, det_J, dt = sovereign_observer(q_sim, planar_2dof_fk)
        
        data.append({
            "timestamp": t,
            "det_J": det_J,
            "latency_ms": dt,
            "status": "SAFE" if is_safe else "HALT"
        })
    return pd.DataFrame(data)

# Generate results 
df = generate_telemetry_load(n_joints=2) # Match 2-DOF prototype
# Calculate Stewardship Ratio (K)
stewardship_ratio = len(df[df['status'] == 'SAFE']) / len(df)
print(f"Stewardship Ratio (K): {stewardship_ratio:.2f}")


def plot_results(df):
    plt.figure(figsize=(10, 6))
    
    # Plot Determinism Latency (Delta t)
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['latency_ms'], color='blue', label='Latency (ms)')
    plt.axhline(y=0.85, color='red', linestyle='--', label='Target (0.85ms)')
    plt.ylabel('Latency (ms)')
    plt.title('PRISM: Real-Time Determinism Audit')
    plt.legend()

    # Plot Manipulability Index |det(J)|
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['det_J'], color='green', label='|det(J)|')
    plt.axhline(y=0.05, color='orange', linestyle='--', label='Halt Threshold (epsilon)')
    plt.ylabel(r'|\det(J)| - Dexterity Metric')
    plt.xlabel('Time (s)')
    plt.legend()

    plt.tight_layout()
    
    plt.xlabel('Time (s)', fontsize=10)
    plt.ylabel('Latency (ms)', fontsize=10)

    plt.savefig('prism_results_visual.png') # Save file 
    print("SUCCESS: Graphic saved as prism_results_visual.png")

# After generating the dataframe
plot_results(df)