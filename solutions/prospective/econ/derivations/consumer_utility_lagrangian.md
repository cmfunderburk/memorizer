"""
Cobb-Douglas Utility Maximization via Lagrangian

Optimization: Constrained Maximization
Method: Lagrangian Multiplier

Derives Marshallian demand functions for a Cobb-Douglas utility function subject to a budget constraint.
"""
=== MEMO START ===
$$
\mathcal{L} = x^a y^b - \lambda(p_x x + p_y y - I)
$$

First Order Conditions (FOCs):

1. $\frac{\partial \mathcal{L}}{\partial x} = a x^{a-1} y^b - \lambda p_x = 0$
2. $\frac{\partial \mathcal{L}}{\partial y} = b x^a y^{b-1} - \lambda p_y = 0$
3. $\frac{\partial \mathcal{L}}{\partial \lambda} = p_x x + p_y y - I = 0$

Divide (1) by (2):
$$
\frac{a x^{a-1} y^b}{b x^a y^{b-1}} = \frac{p_x}{p_y} \implies \frac{a}{b} \cdot \frac{y}{x} = \frac{p_x}{p_y}
$$

Rearrange for $y$:
$$
y = \frac{b}{a} \frac{p_x}{p_y} x
$$

Substitute into (3):
$$
p_x x + p_y \left( \frac{b}{a} \frac{p_x}{p_y} x \right) = I
$$
$$
p_x x + \frac{b}{a} p_x x = I
$$
$$
p_x x \left( 1 + \frac{b}{a} \right) = I \implies p_x x \left( \frac{a+b}{a} \right) = I
$$

Demand functions:
$$
x^* = \left( \frac{a}{a+b} \right) \frac{I}{p_x}
$$
$$
y^* = \left( \frac{b}{a+b} \right) \frac{I}{p_y}
$$
