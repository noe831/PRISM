import numpy as np
import pandas as pd
from kinematic_verification_n import sovereign_observer, planar_2dof_fk

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

# Generate results and calculate stewardship ratio
df = generate_telemetry_load(n_joints=2) # Match 2-DOF prototype
stewardship_ratio = len(df[df['status'] == 'SAFE']) / len(df)
print(f"Stewardship Ratio (K): {stewardship_ratio:.2f}")