"""
Contract Curve Derivation (Edgeworth Box)

Context: General Equilibrium / Pure Exchange
Condition: Pareto Efficiency

Derives the condition for Pareto efficiency in an exchange economy, defining the contract curve.
"""
=== MEMO START ===
Person A: $U_A(x_A, y_A)$
Person B: $U_B(x_B, y_B)$
Endowments: $x_A + x_B = \bar{X}$, $y_A + y_B = \bar{Y}$

Marginal Rates of Substitution:
$$
MRS_A = \frac{\partial U_A / \partial x_A}{\partial U_A / \partial y_A}
$$
$$
MRS_B = \frac{\partial U_B / \partial x_B}{\partial U_B / \partial y_B}
$$

Pareto efficiency requires tangency of indifference curves:
$$
MRS_A(x_A, y_A) = MRS_B(x_B, y_B)
$$

Substitute $x_B = \bar{X} - x_A$, $y_B = \bar{Y} - y_A$ into $MRS_B$:
$$
MRS_A(x_A, y_A) = MRS_B(\bar{X} - x_A, \bar{Y} - y_A)
$$

This equation defines the Contract Curve in terms of $(x_A, y_A)$.
Any competitive equilibrium must lie on this curve.
