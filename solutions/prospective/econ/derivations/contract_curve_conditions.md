# Contract Curve Derivation (Edgeworth Box)

**Context:** General Equilibrium  |  **Condition:** Pareto Efficiency

## How It Works

Derives the condition for Pareto efficiency in a pure exchange economy with two agents and two goods.

1. Define MRS for each agent
2. Set MRS equal (tangency of indifference curves)
3. Apply resource constraints to express in terms of one agent's allocation

Key insight: Competitive equilibria lie on the contract curve (First Welfare Theorem).

## Derivation

```lean
variable (xA yA xB yB X_bar Y_bar : ℝ)

-- Utility functions (abstract)
variable (UA : ℝ → ℝ → ℝ)
variable (UB : ℝ → ℝ → ℝ)

-- Partial derivatives
variable (∂UA_∂x ∂UA_∂y : ℝ → ℝ → ℝ)
variable (∂UB_∂x ∂UB_∂y : ℝ → ℝ → ℝ)

-- Resource constraints (Edgeworth box)
def resource_x : Prop := xA + xB = X_bar
def resource_y : Prop := yA + yB = Y_bar

-- Marginal Rate of Substitution
def MRS_A (xA yA : ℝ) : ℝ := ∂UA_∂x xA yA / ∂UA_∂y xA yA
def MRS_B (xB yB : ℝ) : ℝ := ∂UB_∂x xB yB / ∂UB_∂y xB yB

-- Pareto efficiency: tangency of indifference curves
def pareto_efficient : Prop := MRS_A ∂UA_∂x ∂UA_∂y xA yA = MRS_B ∂UB_∂x ∂UB_∂y xB yB

-- Contract curve condition (substituting resource constraints)
-- Express B's allocation in terms of A's
def xB_from_A : ℝ := X_bar - xA
def yB_from_A : ℝ := Y_bar - yA

-- Contract curve: locus of (xA, yA) satisfying
def contract_curve : Prop :=
  MRS_A ∂UA_∂x ∂UA_∂y xA yA = MRS_B ∂UB_∂x ∂UB_∂y (X_bar - xA) (Y_bar - yA)

theorem competitive_equilibrium_on_contract_curve
    (h_eq : contract_curve ∂UA_∂x ∂UA_∂y ∂UB_∂x ∂UB_∂y xA yA X_bar Y_bar) :
    pareto_efficient ∂UA_∂x ∂UA_∂y ∂UB_∂x ∂UB_∂y xA yA (X_bar - xA) (Y_bar - yA) := by
  sorry
```

## When to Use

- General equilibrium analysis
- Welfare economics: identifying efficient allocations
- Analyzing gains from trade in exchange economies
