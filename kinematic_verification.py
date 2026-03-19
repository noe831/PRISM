import numpy as np
import matplotlib.pyplot as plt

# Parameters
l1, l2 = 1.0, 1.0  # Lengths of modular segments  
epsilon = 0.1      # Determinant threshold for action, safety halt  

def calculate_det_j(theta1, theta2):
    # Determinant of Jacobian matrix for a 2-DOF planar manipulator
    # det(J) = l1 * l2 * sin(theta2)
    return l1 * l2 * np.sin(theta2)

# Create a grid for the joint configuration manifold
t1 = np.linspace(-np.pi, np.pi, 100)
t2 = np.linspace(-np.pi, np.pi, 100)
T1, T2 = np.meshgrid(t1, t2)
Z = calculate_det_j(T1, T2)

# Plot the safe operating envelope (omega) based on the determinant of the Jacobian
plt.figure(figsize=(10, 8))
cp = plt.contourf(T1, T2, np.abs(Z), cmap='viridis', levels=20)
plt.colorbar(cp, label='|det(J)| - Dexterity Metric')
plt.title(r'PRISM: Safe Operating Envelope ($\Omega$)')
plt.xlabel('Joint 1 Angle (rad)')
plt.ylabel('Joint 2 Angle (rad)')

# Draw the singularity boundary (deterministic halt)
plt.contour(T1, T2, np.abs(Z), levels=[epsilon], colors='red', linestyles='dashed')
plt.text(0, 0, 'Singularity Line', color='red', fontweight='bold')

plt.show()