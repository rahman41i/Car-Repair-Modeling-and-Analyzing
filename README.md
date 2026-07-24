# Business Process Analysis & Modeling — Car Repair

Business Process Modeling course project, University of Pisa (Data Science and Business Informatics, A.A. 2024/2025).
Also published as a [Kaggle notebook](https://www.kaggle.com/rahman4li/business-process-analysis-and-modeling-car-repair).

## Overview

This project models and formally analyzes the interaction process between a customer and a car repair shop, using **BPMN** for the business-level model and **Petri nets (WF-nets)** for formal verification of soundness (deadlock-freedom, reachability, boundedness).

The process covers: initial contact, choice between car pick-up or in-person appointment, iterative appointment negotiation, optional courtesy-car negotiation, and three possible outcomes (delivery, partial ending, cancellation).

## Key findings

- **Original model**: Modeled as two BPMN pools (Customer, Repair Shop) connected via message flows, using only exclusive gateways so the model translates cleanly to a Petri net. Two negotiation loops (appointment scheduling, courtesy car) were captured with XOR-split/XOR-join patterns.
- **Verification**: Each module was first checked independently (no unreachable transitions, no deadlocks), then the integrated workflow net (~83 transitions, ~93 places) was verified with the **Woflan** plugin in **ProM**, confirming it is a **sound workflow net** — no deadlocks across all execution paths.
- **Redesign**: Per the extended project requirement, the model was modified so that after a cancellation, the customer can search for another repair shop and restart the process, rather than the interaction simply ending.
- **Trade-off uncovered**: This redesign introduces a **backward arc** from the final place back to the initial place, turning the net cyclic. Formally, this breaks the classical single-termination-point definition of a workflow net, so the redesigned net is no longer *strictly* sound — but it remains bounded, safe, and **relaxed sound** (every subprocess/cycle still behaves correctly), which is an accurate and useful reflection of real customer behavior (retrying with a different provider).

## Repository structure

```
business-process-car-repair/
├── report_raliyev.pdf         Full project report (modeling rationale, formal analysis, figures)
├── analyze_process.py         Python script: structural reader for the BPMN/PNML files
├── models/
│   ├── bpmn/                  BPMN source files (original + redesigned)
│   └── pnml/                  Petri net (PNML) files: customer, shop, complete, redesigned
├── diagrams/                  BPMN/Petri net diagrams referenced in the report
└── woped_analysis/            Soundness verification screenshots (WoPed, ProM Woflan)
```

## Tools used

- **BPMN modeling**: Camunda Modeler / bpmn.io
- **Petri net verification**: [WoPed](http://woped.dhbw-karlsruhe.de/) (structural analysis), [ProM](https://www.promtools.org/) with the Woflan plugin (soundness checking)
- **Structural reader**: Python (`xml.etree.ElementTree`, `pandas`)

## Running the analysis script

```bash
pip install pandas
python analyze_process.py
```

This parses every file under `models/bpmn` and `models/pnml` and prints participants/activities (BPMN) or places/transitions (Petri nets) for each.

## Author

Rahman Aliyev — Master's student, Data Science and Business Informatics, University of Pisa

Supervisor: Prof. Roberto Bruni
