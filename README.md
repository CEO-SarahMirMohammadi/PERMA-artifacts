# PERMA-Artifacts

### AZARS — 36-Week Engineering Roadmap Portfolio

A structured engineering portfolio documenting the weekly implementation, experimentation, and technical documentation of the AZARS project across AI and quantitative systems, blockchain development, and full-stack engineering.

This repository follows a milestone-based learning roadmap. Each weekly folder contains focused deliverables, implementation artifacts, documentation, and execution instructions aligned with that week's objectives.

## Project Overview

AZARS is an enterprise-oriented decision intelligence project exploring data-driven financial analysis, quantitative workflows, blockchain-based auditability, and application development.

The purpose of this repository is to demonstrate incremental engineering progress through reproducible implementations rather than isolated code snippets.

### Engineering Tracks

| Track                        | Focus Areas                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| AI & Quantitative Systems    | Data preparation, feature engineering, time-series analysis, ARIMA, walk-forward validation, and future forecasting experiments |
| Blockchain & Smart Contracts | Solidity, EVM fundamentals, access control, trade logging, contract verification, and progressive security practices            |
| Full-Stack Engineering       | React, Next.js App Router, server-side data fetching, trade interfaces, and future backend integration                          |
| Engineering Practices        | Git workflows, Conventional Commits, testing, technical documentation, reproducibility, and secure development                  |

## Repository Structure

Each week is organized into its own folder. The precise naming convention follows the existing repository structure.

```text
PERMA-Artifacts/
├── README.md
├── .gitignore
├── Week-01/
│   └── README.md
├── Week-02/
│   └── README.md
├── Week-03/
│   └── README.md
├── Week-04/
│   └── README.md
└── Week-05/
    └── README.md
```

Each weekly folder may contain domain-specific directories such as:

```text
src/
├── features/
└── timeseries/

contracts/
app/
docs/
data/
reports/
tests/
screenshots/
```

These are examples of possible subdirectories; each week's README defines its actual structure, dependencies, and execution instructions.

## Weekly Progress

| Week   | Main Focus                                                  | Representative Deliverables                                                            |
| ------ | ----------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Week 1 | Project foundations                                         | Initial engineering exercises and documentation                                        |
| Week 2 | Quantitative and blockchain foundations                     | Return calculations, trade-related TypeScript types, Merkle tree concepts              |
| Week 3 | Trading features and Ethereum concepts                      | Feature engineering, Ethereum/EVM documentation, TradeCard component                   |
| Week 4 | Time-series foundations and Solidity                        | OHLCV resampling, stationarity testing, SimpleStorage, dynamic trade route             |
| Week 5 | Walk-forward validation and access-controlled trade logging | ARIMA walk-forward evaluation, MAE report and chart, TradeLoggerV2, Next.js trade list |

For the exact contents, implementation details, and completion status of each milestone, consult the corresponding weekly README.

> A deliverable is considered complete only when its implementation, relevant validation, and documentation are available. Deployment and verification are reported as completed only when supported by actual evidence.

## Technology Stack

Technologies used or introduced throughout the roadmap include:

* **Languages:** Python, Solidity, JavaScript, TypeScript
* **AI & Data:** pandas, statsmodels, time-series analysis, feature engineering
* **Blockchain:** Ethereum, EVM, Solidity, OpenZeppelin, Sepolia testnet
* **Frontend:** React, Next.js App Router
* **Engineering Tools:** Git, GitHub, Python virtual environments, automated testing and CI workflows as introduced by the roadmap

The stack evolves incrementally. Not every technology is used in every weekly milestone.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CEO-SarahMirMohammadi/PERMA-Artifacts.git
cd PERMA-Artifacts
```

### 2. Select a weekly milestone

Open the desired weekly folder and read its `README.md` before installing dependencies or running code.

### 3. Set up the required environment

Requirements are milestone-specific. For Python-based exercises, use a virtual environment and install the dependencies specified in that week's `requirements.txt`.

Example for Week 5, if the folder is named `Week_05`:

```powershell
cd Week_05

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

Then run the commands documented in that week's README.

**Note:** Use the actual folder name in your local repository. Some environments may use hyphens (`Week-05`) rather than underscores (`Week_05`).

## Engineering Standards

### Code Quality

* Prefer small, focused, testable functions.
* Validate input data and handle expected failures explicitly.
* Avoid unnecessary abstractions and premature complexity.
* Document assumptions, limitations, and important design decisions.

### Git Workflow

* Keep each weekly milestone in its corresponding folder.
* Use meaningful commit messages following Conventional Commits.
* Avoid unrelated changes in a milestone commit.
* Review `git status` before committing and pushing.

Example:

```bash
git add Week_05/
git commit -m "feat: add week 5 walk-forward and trade logger artifacts"
git push origin main
```

Adjust the folder name to match the repository's actual naming convention.

### Security

* Never commit private keys, seed phrases, API tokens, passwords, or other secrets.
* Use testnets for learning-oriented blockchain deployments.
* Distinguish local execution, automated test results, deployment, and source verification.
* Do not treat synthetic data or successful model execution as evidence of real-world financial performance.

### Documentation

Each weekly README should describe:

* Learning objectives
* Deliverables and folder structure
* Dependencies and setup
* Execution and testing commands
* Results and limitations
* Relevant technical references

## Current Scope and Limitations

This repository documents an evolving engineering portfolio. Implementations are educational and developmental unless explicitly documented and validated otherwise.

In particular:

* Synthetic datasets are used where real datasets are unavailable or unsuitable.
* Forecasting metrics do not guarantee profitable trading strategies.
* Smart-contract examples require appropriate testing and security review before production use.
* Demo endpoints and interfaces are not equivalent to a production backend.
* A testnet deployment does not establish production readiness.

## Roadmap Direction

The repository is designed to progress from foundational exercises toward integrated engineering components, including:

1. Quantitative data preparation and evaluation.
2. More advanced forecasting and model assessment.
3. Auditable smart-contract event logging and security testing.
4. Backend and frontend integration.
5. Automated testing, CI/CD, and progressively stronger engineering controls.

Future milestones may extend these components as defined by the 36-week AZARS roadmap.

## Author

**Sarah MirMohammadi**

GitHub: [@CEO-SarahMirMohammadi](https://github.com/CEO-SarahMirMohammadi)

## License

Refer to the repository's license file for the applicable license terms.
