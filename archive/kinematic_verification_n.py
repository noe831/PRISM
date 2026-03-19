import numpy as np
import time

def planar_2dof_fk(q):
    """
    Equation (1) from the PRISM paper.
    Forward Kinematics for a 2-DOF planar manipulator.
    """
    l1, l2 = 100, 100  # Link lengths in mm  
    theta1, theta2 = q[0], q[1]
    
    x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
    print("""DEBUG: FK Output - x: {:.2f}, y: {:.2f} for q: [{:.2f}, {:.2f}]""".format(x, y, theta1, theta2))
    return np.array([x, y])

def get_jacobian(q, forward_kinematics_func, epsilon=1e-6):
    """
    Numerically computes the Jacobian J(theta).
    Supports n-dimensions state matrices.
    """
    n = len(q)
    x0 = forward_kinematics_func(q)
    J = np.zeros((len(x0), n))
    eps = 1e-6

    for i in range(n):
        q_eps = np.copy(q)
        q_eps[i] += eps
        # Finite difference method for gradient calculation
        J[:, i] = (forward_kinematics_func(q_eps) - x0) / eps
    return J

def sovereign_observer(q, fk_func):
    """
    The Independent Observer Pattern (PRISM Framework).
    Performs real-time kinematic auditing.
    Returns safety status, manipulability index, and latency.
    """
    start_time = time.perf_counter()
    
    # Compute Jacobian and determinant
    J = get_jacobian(q, fk_func)
    det_J = np.linalg.det(J) if J.shape[0] == J.shape[1] else np.linalg.norm(J)
    
    # Singularity stress test (threshold epsilon)
    # deterministic halt if |det(J)| < epsilon, indicating proximity to singularity
    epsilon = 0.05
    is_safe = np.abs(det_J) > epsilon
    
    # Calculate determinism latency (delta t)
    latency = (time.perf_counter() - start_time) * 1000  # in ms
    
    return is_safe, det_J, latency

# Simulation Loop for Demo
for t in range(100):
    simulated_q = np.array([0.5, np.sin(t * 0.1)]) # Simulate movement toward 0
    # planar_2dof_fk is the Forward Kinematic (FK) model, the mapping from joint angles q to end-effector coordinates (x, y)
    safe, metric, dt = sovereign_observer(simulated_q, planar_2dof_fk)
    
    if not safe:
        print(f"DETERMINISTIC HALT TRIGGERED: metric={metric:.4f}, dt={dt:.4f}ms")
        break