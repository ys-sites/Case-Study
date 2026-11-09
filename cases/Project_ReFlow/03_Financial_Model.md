# Project ReFlow: Complete Proforma Financial Model
## Portfolio Combinations, Cash Flow Schedules, and 3-Year Valuation

---

### 1. Mandatory Portfolio Synergy & Deduction Rules
Per competition specifications:
- **A + B**: Smaller gross is B ($4.8M). Deduct 15% of $4.8M = **CAD $0.72M**.
  - Combined Gross Savings = $6.2M + $4.8M - $0.72M = **CAD $10.28M**.
  - Combined Added OpEx = $1.3M + $0.9M = **CAD $2.20M**.
  - Net Annual Savings = $10.28M - $2.20M = **CAD $8.08M / year**.
- **A + C**: Smaller gross is A ($6.2M). Deduct 30% of $6.2M = **CAD $1.86M**.
  - Combined Gross Savings = $6.2M + $7.0M - $1.86M = **CAD $11.34M**.
  - Combined Added OpEx = $1.3M + $2.2M = **CAD $3.50M**.
  - Net Annual Savings = $11.34M - $3.50M = **CAD $7.84M / year**.
- **B + C**: Smaller gross is B ($4.8M). Deduct 10% of $4.8M = **CAD $0.48M**.
  - Combined Gross Savings = $4.8M + $7.0M - $0.48M = **CAD $11.32M**.
  - Combined Added OpEx = $0.9M + $2.2M = **CAD $3.10M**.
  - Net Annual Savings = $11.32M - $3.10M = **CAD $8.22M / year**.

---

### 2. Master Portfolio Comparison Table

| Portfolio | Upfront Capex | Budget Feasible? | Net Annual Savings | Simple Payback | PV of Net Savings (10%) | 3-Year NPV (CAD) | Late Rate (Base: 8.5%) | Emissions Cut (Target >=20%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Option A Only** | $8.0M | Yes | $4.90M | 1.63 Yrs | $12.186M | +$4.186M | 6.5% (Fail) | 8.0% (Fail) |
| **Option B Only** | $5.0M | Yes | $3.90M | 1.28 Yrs | $9.699M | +$4.699M | 5.3% (Fail) | 18.0% (Fail) |
| **Option C Only** | $12.0M | Yes | $4.80M | 2.50 Yrs | $11.937M | -$0.063M | 6.0% (Fail) | 12.0% (Fail) |
| **Portfolio A + B** | **$13.0M** | **Yes** | **$8.08M** | **1.61 Yrs** | **$20.094M** | **+$7.094M** | **3.5% (PASS)** | **25.0% (PASS)** |
| **Portfolio A + C** | $20.0M | Yes | $7.84M | 2.55 Yrs | $19.497M | -$0.503M | 4.0% (PASS) | 20.0% (PASS) |
| **Portfolio B + C** | $17.0M | Yes | $8.22M | 2.07 Yrs | $20.442M | +$3.442M | 3.5% (PASS) | 25.0% (PASS) |
| **Portfolio A + B + C**| $25.0M | **No (> $20M)**| N/A | N/A | N/A | N/A | Capped 3.5% | Capped 25.0% |

---

### 3. Step-by-Step Mathematical Derivations
- **Discount Factor Calculation (r = 10%)**:
  $$	ext{PV Factor}_{3	ext{yr}} = rac{1}{(1.10)^1} + rac{1}{(1.10)^2} + rac{1}{(1.10)^3} = 0.90909 + 0.82645 + 0.75131 = 2.48685$$
- **Portfolio A+B Valuation**:
  $$	ext{PV}(	ext{Savings}) = \$8,080,000 	imes 2.48685 = \$20,093,765$$
  $$	ext{NPV} = \$20,093,765 - \$13,000,000 = +\$7,093,765 	ext{ (CAD \$7.094M)}$$
- **3-Scenario Sensitivity Analysis**:
  - **Bear Case (-30% savings, +25% capex)**: Net savings = $5.66M/yr, Capex = $16.25M. 3-Year NPV = -$2.18M (Payback: 2.87 yrs).
  - **Base Case (Plan)**: Net savings = $8.08M/yr, Capex = $13.00M. 3-Year NPV = **+$7.094M** (Payback: 1.61 yrs).
  - **Bull Case (+20% volume scaling)**: Net savings = $9.70M/yr, Capex = $13.00M. 3-Year NPV = **+$11.12M** (Payback: 1.34 yrs).
