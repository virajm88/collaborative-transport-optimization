# Collaborative Transport Optimisation

**Mixed-integer optimisation · Cooperative game theory · Benders decomposition**

A reproducible computational study of when independent logistics companies benefit
from shared consolidation hubs, how the joint cost can be allocated, and whether
participants have incentives to remain in the collaboration.

The implementation combines a capacitated hub-activation MILP, exact coalition
costs, Shapley cost allocation, core checks, and an explicit Benders decomposition
algorithm using LP dual cuts. Python and the open-source HiGHS solver are used;
no commercial solver licence, API key or external dataset is required.

> **Data and scope:** All company names, demand, coordinates, capacity and prices
> are fictional. This is an educational research prototype, not a calibrated
> Antwerp transport study. Standard methods are implemented; no algorithmic novelty
> or real-world savings are claimed. The initial implementation and documentation
> were prepared with AI assistance.

![Synthetic shared transport network](examples/reference_run/demo/figures/network.png)

## Research questions

1. How much can joint hub activation and shipment allocation change transport cost?
2. Does a marginal-contribution allocation give every company a reason to participate?
3. Can any coalition reduce its cost by leaving the grand coalition?
4. How does an explicit Benders outer loop compare with the compact MILP?
5. How do capacity, fixed costs and demand affect savings and stability?

## Reference findings

The included reference instance has **3 companies, 18 orders and 4 candidate hubs**.
All amounts below are EUR per synthetic planning period.

| Measure | Computed result |
| --- | ---: |
| Sum of separate-operation costs | 5,236.98 |
| Grand-coalition cost | 4,665.82 |
| Modelled saving | 571.16 / **10.91%** |
| Shapley allocation in the core | Yes, for this instance |
| Benders iterations | 4 |
| Compact / Benders objective difference | Less than 0.0001 EUR |

Capacity matters. At 50% of baseline hub capacity, the same counterfactual
comparison gives **−17.54% savings** and an **empty core**. At 125% of baseline
demand, the core is also empty even though total savings remain positive.
See [the interpretation of this comparison](docs/MODEL.md#coalition-cost-interpretation):
standalone hub leases are evaluated separately and their capacities are not added
to the pooled network. These outcomes should not be read as observed market effects.

![Company cost allocation](examples/reference_run/demo/figures/allocation.png)

Full evidence:

- [Computed study report](examples/reference_run/demo/report.md)
- [Coalition costs](examples/reference_run/demo/coalition_costs.csv)
- [Sensitivity results](examples/reference_run/sensitivity/sensitivity.csv)
- [Algorithm comparison](examples/reference_run/benchmark/report.md)
- [Reference-run environment and validation](examples/reference_run/VALIDATION.md)

## Run in a few commands

Use **Python 3.11 or later**. The reference run was verified on Python 3.12.14.
Run commands from the extracted repository folder.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m collab_transport demo
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m collab_transport demo
```

Then open **`outputs/demo/report.md`** in VS Code, another Markdown viewer or a text
editor. Plots are PNG files inside `outputs/demo/figures/`. Expected objective:
approximately `4665.824955`; floating-point rounding and tied optimal flows can vary.
No notebook server or web application is needed.

### Verify and reproduce everything

```bash
python -m unittest discover -s tests -v
python reproduce.py
```

The second command runs the main study, nine sensitivity scenarios, and nine
algorithm comparisons. It writes into `outputs/`; the committed reference
results in `examples/reference_run/` are preserved. Solves are generally small,
but total runtime depends on your machine. A failed or time-limited solve is
reported as an error rather than being silently included as an exact coalition cost.

## Experiments and custom data

```bash
# Generate JSON data and solve it with both approaches.
python -m collab_transport generate --seed 17 --output outputs/custom.json
python -m collab_transport solve --instance outputs/custom.json --method compact
python -m collab_transport solve --instance outputs/custom.json --method benders --output outputs/benders.json

# Full analysis of a custom JSON instance.
python -m collab_transport demo --instance outputs/custom.json --output outputs/custom_study

# Change one parameter family at a time; re-solve coalition costs.
python -m collab_transport sensitivity --output outputs/sensitivity

# Paired sizes: 6 orders/company with 4 hubs, 12 with 6, and 24 with 8.
python -m collab_transport benchmark --orders 6 12 24 --hubs 4 6 8 --seeds 7 42 101

# Show all command options.
python -m collab_transport --help
python -m collab_transport demo --help
```

An existing `--instance` overrides generator parameters. Exact cooperative analysis
is limited to 8 companies because the number of non-empty coalitions is `2^n - 1`.
`--time-limit` is a limit per compact solve, or a total wall-clock budget for one
Benders run; it is not a budget for the entire multi-scenario experiment.

For editable installation and the optional console command:

```bash
python -m pip install --no-deps -e .
collab-transport demo
```

## What the model does

- Binary decisions activate candidate hubs with fixed leasing costs.
- Continuous flows assign divisible order quantities through active hubs or direct delivery.
- Demand conservation and shared hub capacities constrain the plan.
- A cooperative cost game assigns each coalition its minimum operating cost.
- The Shapley formula allocates cost by exact marginal contributions.
- Every proper coalition is checked for a profitable departure.
- A linear program tests core existence using a minimum non-negative relaxation.
- Benders separates the binary activation decisions from the continuous allocation LP.

![Benders bounds](examples/reference_run/demo/figures/benders_convergence.png)

The full [mathematical formulation and dual-cut derivation](docs/MODEL.md) explain
the assumptions, inequality signs, convergence checks and cost-game definitions.

## Repository map

| Location | Purpose |
| --- | --- |
| `collab_transport/data.py` | Data classes, validation, JSON I/O and seeded generator |
| `collab_transport/model.py` | Sparse compact MILP, allocation LP and solution validation |
| `collab_transport/benders.py` | Explicit master/subproblem loop and dual optimality cuts |
| `collab_transport/game.py` | Coalition costs, Shapley allocation, core checks and relaxation |
| `collab_transport/experiments.py` | End-to-end study, sensitivity and benchmark |
| `collab_transport/reporting.py` | CSV/JSON outputs, plots and reporting helpers |
| `collab_transport/cli.py` | Command-line interface |
| `data/` | Small demonstration and hand-computable JSON instances |
| `tests/` | Analytical, exhaustive, dual-validity, game-theory and workflow checks |
| `examples/reference_run/` | Actual computed outputs, plots and validation record |
| `docs/MODEL.md` | Mathematical details and interpretation |
| `docs/LEARNING_GUIDE.md` | Code walkthrough, explanations and exercises |
| `docs/REFERENCES.md` | Original methods and official software documentation |
| `UPLOAD_TO_GITHUB.md` | Browser upload and Git instructions |
| `.github/workflows/ci.yml` | Tests and small experiments on push / pull request |

## Verification

The test suite includes a hand-solvable two-player instance; exhaustive enumeration
of all binary hub decisions on several small instances; independent checks of
Benders cut validity at other binary and fractional points; primal feasibility;
cost reconstruction; monotone bound checks; Shapley efficiency, symmetry and dummy
player checks; empty-core and blocking-coalition examples; and end-to-end output tests.

The included benchmark verifies objective agreement on all nine instances.
It measures each instance once after warm-up and alternates method order. It does
not demonstrate general superiority or industrial scalability. The GitHub workflow
is configured for Python 3.11 and 3.12; its remote status will be available after upload.

## Limitations and extensions

The model assumes one origin, known demand and tariffs, divisible flows,
unlimited direct delivery and enforceable monetary transfers. It does not model
vehicle tours, time windows, private information, a non-cooperative equilibrium,
bilevel optimisation, column generation or branch-and-price. Cost-allocation
stability is tested under the specified coalition-cost convention, not every
possible institutional interpretation of hub ownership or access.

Useful extensions include pooled capacity that scales with members' contributed
resources, repeated runtime measurements, stronger Benders cuts, realistic road
distances, uncertainty, and genuinely strategic pricing or participation models.
Each would require changes to assumptions and fresh validation.

**Licence:** MIT. See [LICENSE](LICENSE). Mathematical and software references are
credited in [docs/REFERENCES.md](docs/REFERENCES.md).

