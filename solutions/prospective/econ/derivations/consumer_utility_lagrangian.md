# Cobb-Douglas Utility Maximization via Lagrangian

**Type:** Constrained Maximization  |  **Method:** Lagrangian Multiplier

## How It Works

Derives Marshallian demand functions for a Cobb-Douglas utility function $U = x^a y^b$ subject to budget constraint $p_x x + p_y y = I$.

1. Form Lagrangian with budget constraint
2. Take FOCs, divide to eliminate λ
3. Substitute back into budget constraint
4. Solve for demand functions

Key insight: Budget shares are constant fractions $\frac{a}{a+b}$ and $\frac{b}{a+b}$.

## Derivation

```lean
variable (x y px py I a b λ : ℝ)
variable (hpos : px > 0 ∧ py > 0 ∧ I > 0 ∧ a > 0 ∧ b > 0)

-- Utility function
def U : ℝ := x^a * y^b

-- Budget constraint
def budget_constraint : Prop := px * x + py * y = I

-- Lagrangian
def L : ℝ := x^a * y^b - λ * (px * x + py * y - I)

-- First Order Conditions
def FOC_x : Prop := a * x^(a-1) * y^b - λ * px = 0
def FOC_y : Prop := b * x^a * y^(b-1) - λ * py = 0
def FOC_λ : Prop := px * x + py * y - I = 0

-- Divide FOC_x by FOC_y to eliminate λ
-- (a * x^(a-1) * y^b) / (b * x^a * y^(b-1)) = px / py
-- (a/b) * (y/x) = px / py

-- Rearrange for y
def y_from_x : ℝ := (b/a) * (px/py) * x

-- Substitute into budget constraint and solve
-- px * x + py * ((b/a) * (px/py) * x) = I
-- px * x * (1 + b/a) = I
-- px * x * ((a+b)/a) = I

-- Marshallian demand functions
def x_star : ℝ := (a / (a + b)) * (I / px)
def y_star : ℝ := (b / (a + b)) * (I / py)

theorem marshallian_demand_satisfies_budget :
    px * x_star px I a b + py * y_star py I a b = I := by
  sorry
```

## When to Use

- Consumer theory: deriving optimal consumption bundles
- Welfare analysis: computing indirect utility and expenditure functions
- Comparative statics on prices and income
