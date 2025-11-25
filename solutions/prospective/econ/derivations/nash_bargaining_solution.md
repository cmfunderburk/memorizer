"""
Nash Bargaining Solution

Context: Cooperative Game Theory
Objective: Maximize Nash Product

Derives the First Order Condition for the Nash Bargaining Solution on the Pareto frontier.
"""
=== MEMO START ===
Problem:
$$
\max (u - d_u)(v - d_v)
$$
subject to $(u, v) \in S$ (Feasible Set).

FOC for efficient bargaining on the frontier $v = f(u)$:
Maximize $P = (u - d_u)(f(u) - d_v)$

Log-linearize:
$$
\ln(P) = \ln(u - d_u) + \ln(f(u) - d_v)
$$

Differentiate with respect to $u$:
$$
\frac{\partial \ln(P)}{\partial u} = \frac{1}{u - d_u} + \frac{f'(u)}{f(u) - d_v} = 0
$$

Rearranging:
$$
-f'(u) = \frac{f(u) - d_v}{u - d_u}
$$

Interpretation:
Slope of frontier = Slope of rectangular hyperbola (level curve of Nash Product).
Alternatively:
$$
-\frac{dv}{du} = \frac{v - d_v}{u - d_u}
$$
Marginal Rate of Transformation = Ratio of Surplus Shares.
