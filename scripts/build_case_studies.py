"""Render the technical case study pages in case-studies/ from the data below.

Each study answers the same questions so a reader can compare projects quickly:
problem, architecture, technologies, engineering decisions, tests, results, limitations, next steps.
Run: python3 scripts/build_case_studies.py
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "case-studies"
SITE = "https://brandoncandela.github.io"
EMAIL = "Brandon.d.candela@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/brandon-candela/"

STUDIES = [
    {
        "slug": "aml-backlog-command-center",
        "title": "AML Backlog Command Center",
        "pillar": "Investigation tooling",
        "oneliner": "Turns 5,343 alerts from three monitoring systems into 1,240 ranked customer cases and a staffing plan that meets a regulatory deadline.",
        "demo": "/aml-backlog-command-center/",
        "repo": "https://github.com/brandoncandela/aml-backlog-command-center",
        "image": "aml-backlog-command-center.jpg",
        "glance": [("5,343 → 1,240", "alerts grouped into customer cases"), ("100%", "of 4,923 automatic matches correct"), ("6 vs 9", "analysts needed to meet the deadline"), ("19", "automated tests")],
        "who": "AML operations leaders, BSA Officers and implementation teams onboarding a bank onto new tooling.",
        "built": "A config-driven ingestion pipeline, a tiered entity resolver, an explainable case scorer, a capacity forecaster and a six-view operator app.",
        "result": "Same workload, 41% fewer analyst hours, because each customer is researched once instead of once per alert.",
        "problem": [
            "A bank under a consent order has open alerts in three systems: an Actimize-style export, a legacy SQL rules engine and fraud team referrals. Each uses its own customer ID, date format and money format. Analysts work alert by alert, research the same customer several times, and leadership reports a raw alert count that hides where the risk is.",
            "The real question from the BSA Officer is simple: how many analysts do we need to clear this by March 31, and which customers do we look at first?",
        ],
        "flow": [
            ("Generate exports", "Deterministic generator writes three realistic, messy source files plus a hidden answer key."),
            ("Onboard by config", "One JSON mapping per source: columns, ID type, date and money formats, open statuses."),
            ("Reconcile every row", "Loaded + duplicates + closed + rejected must equal rows read, or the load fails."),
            ("Resolve identities", "Crosswalk, CIF with zeros restored, account, masked account plus name, name plus DOB. Below 0.9 confidence goes to a person."),
            ("Build cases", "One case per customer, ranked by named point rules."),
            ("Forecast capacity", "Handle-time assumptions and a working-day calendar give clear dates for 4 to 30 analysts."),
            ("Operator app", "Static app: onboarding, matching, queue, staffing slider, QA sample."),
        ],
        "tech": ["Python 3 (standard library)", "JSON source mappings", "unittest", "Vanilla JavaScript", "CSS", "GitHub Pages"],
        "decisions": [
            ("Config, not code, per source", "Adding a fourth system is a new JSON file. A test onboards a semicolon-delimited source with European dates using config only."),
            ("A wrong match is worse than no match", "Matches under 0.9 confidence are never auto-accepted. Two customers sharing a name stay ambiguous and go to review with both candidates listed."),
            ("Additive points instead of a model", "Every case shows its score as named parts (risk rating, typology, multiple systems, volume, amount, days past SLA). Examiners can read it; a model can be benchmarked against it later."),
            ("Assumptions as named constants", "Handle times and SAR rates live in one file so operations and finance can challenge them, then replace them with measured times after the pilot."),
            ("Reproducible QA sample", "10% of cases drawn with a stored random seed, so an examiner can rerun the selection and get the same list."),
        ],
        "tests": ("19 unittest cases", ["Money and date parsing across all three formats, including bad dates", "Onboarding a brand new source with config only", "Every resolver tier, including the ambiguous and masked-account cases that must not be guessed", "Case grouping, score parts summing to the total, tier boundaries", "Working-day calendar with holidays and the minimum-analyst calculation", "Automatic match precision at least 99.5% against the answer key", "Byte-identical output on every build"]),
        "results": ["5,343 alerts loaded; 57 duplicates and 25 unreadable dates rejected with reasons", "4,923 automatic matches, all correct; 420 sent to identity review, where 25 name-only guesses would have been wrong", "695 customers flagged by more than one system, which no one could see before", "Alert by alert needs 9 analysts; working by customer needs 6 and clears on March 12, 2027"],
        "limits": ["The bank, customers and alerts are synthetic; accuracy can be measured only because an answer key exists", "Handle times are planning assumptions until a pilot measures them", "Read-only: it does not write back to a case management system", "Score weights are starting values, not calibrated to outcomes"],
        "next": ["Measured handle times from a pilot feeding the forecast", "Write-back of case IDs to the bank's case management system", "Reviewer roles and an audit log for identity decisions"],
        "docs": [("Discovery notes", "docs/discovery.md"), ("Product requirements", "docs/prd.md"), ("Deployment playbook", "docs/deployment-playbook.md"), ("Pilot plan", "docs/pilot-plan.md")],
    },
    {
        "slug": "crypto-exchange-monitoring-lab",
        "title": "Crypto Exchange Monitoring Lab",
        "pillar": "Blockchain intelligence",
        "oneliner": "Six SQL monitoring rules that screen a fictional exchange's deposits and withdrawals against every crypto wallet on the OFAC list and their real Tron USDT counterparties.",
        "demo": "/crypto-exchange-monitoring-lab/",
        "repo": "https://github.com/brandoncandela/crypto-exchange-monitoring-lab",
        "image": "crypto-exchange-monitoring-lab.jpg",
        "glance": [("521", "OFAC-listed crypto addresses screened"), ("5,170", "real USDT transfers of 126 sanctioned wallets"), ("100%", "recall on every rule"), ("25", "automated tests")],
        "who": "Crypto exchange compliance teams and blockchain analytics vendors deciding which transfers to stop and review.",
        "built": "A public-data snapshot pipeline, a seeded exchange ledger, six parameterized SQL rules, per-rule scoring and an analyst queue with an answer key.",
        "result": "Every rule catches every customer it was built to catch; the misses on precision are realistic businesses that look risky.",
        "problem": [
            "An exchange has to decide, for every deposit and withdrawal, whether the counterparty is sanctioned, one step removed from a sanctioned wallet, or showing a laundering pattern such as pass-through, structuring under the Travel Rule threshold or fan-out to new wallets.",
            "Rules that only work on clean test data are easy to write. The hard part is measuring how a rule behaves against customers whose normal business looks suspicious.",
        ],
        "flow": [
            ("Snapshot public data", "OFAC SDN crypto addresses, TronGrid USDT transfers of sanctioned Tron wallets and CoinGecko prices, saved on Nov 5, 2026."),
            ("Seed an exchange", "30 fictional customers, each doing at most one risky thing so rules can be scored."),
            ("Load SQLite", "Customers, transfers, sanctioned addresses and on-chain transfers."),
            ("Run six rules", "One commented SQL file per rule with a params block for windows and thresholds."),
            ("Score rules", "Precision, recall and named false positives per rule."),
            ("Analyst queue", "Static page with evidence, next steps and an answer key."),
        ],
        "tech": ["Python 3 (standard library)", "SQLite", "SQL: joins, CTEs, ROW_NUMBER, JSON output", "TronGrid and CoinGecko public APIs", "unittest", "Vanilla JavaScript"],
        "decisions": [
            ("Freeze public data in a snapshot", "The lab rebuilds identically offline and in tests. Refreshing is one command, so results never drift silently."),
            ("Stop at one hop", "Every alert stays explainable to an analyst. Deeper tracing is where commercial tools add value, and where false links multiply."),
            ("Design the false positives", "An OTC desk, a payroll company and a busy service-like wallet are built in, because tuning judgment matters more than a perfect score."),
            ("Test at the edges", "Each rule is tested exactly at its boundaries: 79% vs 80% withdrawn, 60 vs 61 minutes, $2,999.99 vs $3,000."),
            ("No keys, no server", "Keyless public APIs for collection and a static page for review, so there is nothing to leak or pay for."),
        ],
        "tests": ("25 unittest cases", ["Boundary tests for all six rules", "Ordinary customers never alert", "The build is identical on every run"]),
        "results": ["26 alerts on 15 of 30 customers; 2 critical alerts for direct sanctions exposure", "Recall is 100% on all six rules; precision is 100% for direct exposure and Travel Rule gaps and 67% for the rest", "10 of the 12 pass-through alerts come from one legitimate OTC desk, which a real team would tune for once"],
        "limits": ["Follows one hop only", "Pulls transaction history for Tron USDT only; Ethereum addresses are screened directly", "Does not attribute wallets to exchanges, mixers or scams", "Uses a single price snapshot, not the price at each transfer"],
        "next": ["Customer-type tuning for OTC desks and payroll businesses", "Ethereum history through a keyed provider behind a server-side proxy", "Attribution labels from a vendor feed, clearly separated from raw links"],
        "docs": [],
    },
    {
        "slug": "fraud-intelligence-control-lab",
        "title": "Fraud Intelligence & Control Lab",
        "pillar": "Fintech risk infrastructure",
        "oneliner": "A fraud spike on a payments platform, turned into SQL features, a tunable control and a written decision on where to set the threshold.",
        "demo": "/fraud-intelligence-control-lab/",
        "repo": "https://github.com/brandoncandela/fraud-intelligence-control-lab",
        "image": "fraud-intelligence-control-lab.jpg",
        "glance": [("3,771", "synthetic transactions across 60 accounts"), ("87.5%", "precision at the chosen threshold"), ("100%", "recall of seeded review-worthy accounts"), ("7", "automated tests")],
        "who": "Fraud strategy and risk operations teams deciding how to change a control without flooding the review queue.",
        "built": "A deterministic data generator, SQL feature engineering, an auditable point score, a threshold console tied to analyst capacity, a shared-device graph and a decision brief export.",
        "result": "At a score of 40 the control queues 8 accounts, catches all 7 review-worthy ones and stays within 8 daily reviews.",
        "problem": [
            "A payments platform sees a possible fraud spike. The team has to decide which accounts enter the review queue, which signals form one incident, and how to change the control without overwhelming 8 reviews of daily capacity or treating a single shared device as proof.",
        ],
        "flow": [
            ("Generate data", "Deterministic accounts, devices and transactions with seeded fraud scenarios and benign lookalikes."),
            ("Model in SQLite", "Schema with foreign keys and indexes."),
            ("Engineer features", "SQL CTEs: shared-device peers, distinct inbound senders in 24 hours, rapid outbound amount, new foreign device amount."),
            ("Score", "Transparent point score per account."),
            ("Export", "Dashboard JSON with the threshold corridor and monitoring trend."),
            ("Decide", "Threshold console, link graph, four-week monitoring and a downloadable brief."),
        ],
        "tech": ["Python 3", "SQLite", "SQL: CTEs, time windows, aggregation", "unittest", "Vanilla JavaScript", "Graph rendering in SVG"],
        "decisions": [
            ("Point score over a black box", "Each point maps to a signal an investigator can verify, which is what a control owner needs before a model is justified."),
            ("Capacity is a hard constraint", "Every threshold shows its alert volume against the 8 daily reviews, so a better recall that the team cannot work is visible as a cost."),
            ("Labels for evaluation only", "Synthetic ground truth is shown to score the control, and the page says a live team would not have it at decision time."),
            ("A shared device is a lead", "The graph shows the cluster, and the brief treats it as something to check, not as proof of fraud."),
        ],
        "tests": ("7 unittest cases", ["Foreign keys are clean and the population is as expected", "The mule cluster is linked through its shared device", "The account takeover feature fires, and a benign marketplace lookalike is kept", "The threshold tradeoff is present", "The dashboard export is valid JSON"]),
        "results": ["Score 40: 8 alerts, 87.5% precision, 100% recall, within capacity", "Score 50: 5 alerts but recall drops to 71.4%", "A 5-account mule cluster linked by one shared device, reconstructed as one incident"],
        "limits": ["All people, devices and transactions are synthetic", "Weights are illustrative, not calibrated probabilities", "Production would need real outcomes, ongoing monitoring and model governance"],
        "next": ["Backtesting against labeled historical outcomes", "Champion and challenger comparison with a simple model", "Drift alerts on feature distributions"],
        "docs": [],
    },
    {
        "slug": "modelguard",
        "title": "ModelGuard",
        "pillar": "Model risk and AI governance",
        "oneliner": "A working model risk management and AI governance platform for a fictional bank: it inventories ten financial crime models, measures them every month from the records they scored, runs independent validations and writes every change to a tamper-evident audit trail.",
        "demo": None,
        "repo": "https://github.com/brandoncandela/modelguard",
        "image": "modelguard.jpg",
        "tour": ("modelguard-tour", "modelguard-tour-poster.jpg",
                 "A tour of ModelGuard: executive overview, model inventory, monitoring, a simulated month of severe drift creating new breaches, validation, EU AI Act readiness, LLM evaluation, committee reporting and the audit trail",
                 "Recorded from the running app with its seeded data. ModelGuard needs a backend and database, so it runs locally or with Docker Compose rather than as a hosted demo."),
        "extra_links": [("Sample committee report (PDF)", "https://github.com/brandoncandela/modelguard/blob/main/docs/sample-reports/executive-committee-report.pdf")],
        "glance": [("10", "financial crime models monitored monthly"), ("180,974", "scored records behind the metrics"), ("15", "automated control tests over live data"), ("75", "automated tests on SQLite and PostgreSQL")],
        "who": "Heads of model risk management, model validators, financial crime compliance leaders and the technology teams that support them.",
        "built": "A FastAPI and PostgreSQL backend with role-based access, a synthetic bank scored by ten detection models, monthly monitoring with drift tests, validation and findings workflows, EU AI Act readiness assessments, LLM evaluation, committee PDFs and a hash-chained audit trail, behind a React and TypeScript front end.",
        "result": "Every figure in a committee pack traces back to records in one database. A simulated month of severe drift shows up as graded breaches within seconds.",
        "problem": [
            "A bank running transaction monitoring, sanctions screening, customer risk rating and newer machine learning and LLM tools has to show its supervisors that each model is inventoried, independently validated, monitored against agreed limits and fixed when it fails. In practice that evidence lives in spreadsheets, email and slide decks, and the numbers in committee packs are typed in by hand.",
            "The questions a Head of Model Risk Management gets asked are simple to state and hard to answer quickly: which models are breaching their limits right now, did recall fall because the model got worse or because the data broke, which findings are past target, and can we prove nobody edited the approval history?",
        ],
        "flow": [
            ("Generate a bank", "A deterministic generator creates 1,200 customers, 64,997 transactions, 8,139 alerts and 6,240 news articles over twelve months, with data quality defects and drift scenarios."),
            ("Score with ten models", "A weighted rules engine, gradient boosting, logistic regression, TF-IDF classifiers and fuzzy name screening score every record. The two LLM systems use seeded or recorded outputs."),
            ("Monitor monthly", "Precision, recall, F1, PSI, Kolmogorov-Smirnov and chi-square drift tests and data quality rates are compared with each model's limits to raise graded breaches."),
            ("Validate and remediate", "Validations and findings move through enforced workflows with independence rules and SHA-256 hashed evidence."),
            ("Govern AI", "An AI system inventory, an EU AI Act readiness self-assessment, an LLM evaluation suite and outcome disparity tests."),
            ("Map to regulation", "40 requirements and 21 controls mapped to models, with 15 automated control tests that run over live data."),
            ("Report and audit", "An executive dashboard, packs for three committees as PDFs and an append-only, hash-chained audit trail."),
        ],
        "tech": ["Python, FastAPI, Pydantic", "SQLAlchemy 2.0 and Alembic", "PostgreSQL 16 or SQLite", "pandas, NumPy, SciPy, scikit-learn", "ReportLab", "React 18, TypeScript, Tailwind CSS, Plotly", "pytest", "Docker Compose and GitHub Actions"],
        "decisions": [
            ("Analytics are pure functions", "Metrics, PSI and drift tests have no database or framework imports, so each one is tested against values worked out by hand."),
            ("The server enforces every rule", "The interface hides buttons a user cannot use, but the API checks again: a validator who owns a model cannot validate it, and a finding cannot close without remediation evidence and an independent validator."),
            ("Real detection models, not canned numbers", "Monitoring reads what the models actually scored. Only the two LLM systems use seeded or recorded outputs, and the app labels them that way."),
            ("A tamper-evident audit trail", "Each event stores a SHA-256 hash chained to the previous event, database triggers block updates and deletes, and a verify endpoint recomputes the whole chain."),
            ("Current guidance, no compliance claims", "Controls map to the April 2026 interagency model risk guidance (SR 26-2 / OCC 2026-13), with SR 11-7 and OCC 2011-12 recorded as superseded. The EU AI Act module is an internal readiness self-assessment, not a certification."),
        ],
        "tests": ("75 pytest cases", ["Metric, PSI and drift calculations against hand-computed values", "Threshold breaches and severity grading", "Validation and finding workflows, including independence rules", "AI assessment, an LLM evaluator that catches every planted defect, and disparity testing", "Regulatory mapping, control tests and PDF content", "Audit chain tamper detection", "One end-to-end workflow from drift to committee report", "Run in CI on Python 3.9, Python 3.12 and PostgreSQL 16, plus a Docker Compose start-up check"]),
        "results": ["Gradient boosting beats the rules engine on precision by roughly three times, and both lose recall when launderers change behaviour", "Suspicious activity model recall falls from 99.6% to 81.7% under drift, past its warning limit, with a channel input PSI of 0.156", "9 of 15 control tests pass; the six exceptions point at real issues such as overdue revalidations and an AI pilot running without an approved assessment", "The LLM evaluator catches all 17 planted defects, passes all 38 clean answers and fails the production research assistant at an 11.8% hallucination rate"],
        "limits": ["Candela Bank and all of its data are synthetic; recall can be measured only because the generator knows the ground truth", "The two LLM systems are simulated or replayed from recorded responses, not live model calls", "Assessments and control tests are internal governance tools, not certifications or legal opinions", "No hosted demo: it needs a backend and database, so it runs locally or with Docker Compose", "Demo sign-in with synthetic users; no single sign-on"],
        "next": ["An import format so a bank can load its own scored records", "Single sign-on and access rules per legal entity", "A hosted read-only demo"],
        "docs": [("Architecture", "docs/ARCHITECTURE.md"), ("Validation methodology", "docs/VALIDATION_METHODOLOGY.md"), ("Model governance", "docs/MODEL_GOVERNANCE.md"), ("AI governance", "docs/AI_GOVERNANCE.md"), ("Regulatory mapping", "docs/REGULATORY_MAPPING.md")],
    },
    {
        "slug": "ai-sar-narrative-lab",
        "title": "AI SAR Narrative Lab",
        "pillar": "AI-assisted investigations",
        "oneliner": "Claude drafts Suspicious Activity Report narratives where every sentence cites its evidence, plain rules check every amount, date and citation, and a person has the final say.",
        "demo": "/ai-sar-narrative-lab/",
        "repo": "https://github.com/brandoncandela/ai-sar-narrative-lab",
        "image": "ai-sar-narrative-lab.jpg",
        "glance": [("24", "evidence packets across 9 typologies"), ("7 + 4", "hard checks and warnings on every draft"), ("8", "planted error types that test the checker"), ("49", "automated tests")],
        "who": "Financial crime investigators, SAR quality control teams and compliance leaders deciding how to use language models safely.",
        "built": "Evidence packets with citable IDs, a structured-output drafting call, a rule-based evaluator, a fault injector that tests the evaluator, and a human review log.",
        "result": "Drafts have not been generated yet, so no pass rates are published. Every figure will come from the committed results files once they are.",
        "problem": [
            "Writing the narrative is the slowest part of a Suspicious Activity Report. A language model can write a first draft in seconds, but an investigator cannot file a sentence they cannot check, and a fluent draft can hide an invented amount or date.",
            "The question is not whether a model can write, but how a bank would know which sentences to trust.",
        ],
        "flow": [
            ("Build evidence packets", "24 cases picked with a fixed seed from the AML Backlog Command Center. Every fact gets an ID a draft can cite."),
            ("Draft with Claude", "Structured output forces five sections (who, what, when, where, why) and a citations list on every sentence."),
            ("Check with rules", "Every amount, date, count, branch and account ending must appear in the records the sentence cites."),
            ("Test the tester", "Plant one known error per copy of a draft and confirm the right rule fires."),
            ("Human review", "Accept, edit or reject with a reason; edits are rescored and disagreements with the rules are logged."),
            ("Static demo", "Drafts and scores committed as JSON; the page never calls a model."),
        ],
        "tech": ["Python 3", "Claude API (structured output)", "JSON Schema", "unittest", "Vanilla JavaScript", "Content Security Policy"],
        "decisions": [
            ("Citations are required, not optional", "The output schema makes every sentence carry its evidence IDs, so a reviewer can check any claim in one click."),
            ("Rules check the model, not another model", "The evaluator is plain code, so the same draft always gets the same result and anyone can read why a sentence failed."),
            ("Test the checker with planted errors", "Eight kinds of known mistakes are injected on purpose to prove each rule actually catches what it claims to."),
            ("No API key outside one machine", "Only the local generator calls the API. The public demo is static, its Content Security Policy blocks outside connections, and a test scans the repo for keys."),
            ("A person signs off", "The model drafts and the rules flag; the reviewer decides, and every disagreement with the rules is recorded."),
        ],
        "tests": ("49 unittest cases", ["The packet builder rebuilds byte for byte and never exposes a full account number", "Every evaluator rule with passing and failing sentences", "The fault injector plants each error and the right rule catches it", "Refusals, cut-off replies and bad JSON from the API are recorded, not hidden", "Review validation, disagreement scoring and the secret checks"]),
        "results": ["Pending: the 24 drafts are generated offline and have not been run yet", "Pass rates and planted-error catch rates will be published from results/evaluation.json and results/faults.json"],
        "limits": ["Synthetic data, and each alert carries one amount, so drafts cite alerts rather than individual transactions", "Rules can confirm a number is in the evidence, not whether the reasoning is convincing; that is the reviewer's job", "Amounts written in words are not checked", "A drafting aid only: people at a bank own the filing decision"],
        "next": ["Generate the drafts and publish pass rates and catch rates", "Transaction-level citations once alerts carry their underlying transactions", "Agreement tracking across several reviewers"],
        "docs": [],
    },
    {
        "slug": "trace-desk",
        "title": "Trace Desk: USDT Investigations",
        "pillar": "Blockchain intelligence",
        "oneliner": "A crypto investigation workspace that pulls real Ethereum USDT transfers, decodes them from raw logs, maps a bounded wallet network and hands a checksummed case file to QC.",
        "demo": "/trace-desk-aml-workspace/",
        "repo": "https://github.com/brandoncandela/trace-desk-aml-workspace",
        "extra_links": [("Version 1 demo", "/usdt-investigator/"), ("Version 1 source", "https://github.com/brandoncandela/usdt-investigator")],
        "image": "usdt-workspace.jpg",
        "glance": [("7,640", "USDT transfers decoded from 80 blocks"), ("15", "wallets in the saved two-hop case"), ("49", "tests across both versions"), ("0", "API keys needed")],
        "who": "Crypto investigators and blockchain intelligence teams who need evidence a reviewer can verify.",
        "built": "A node collector, a log decoder with exact integer amounts, an evidence verifier, a bounded graph, live browser queries, portable case files and QC rounds.",
        "result": "The saved case rebuilds identically offline from raw node responses, and every number traces back to a transaction.",
        "problem": [
            "Investigating a crypto address usually means copying transactions out of block explorers into spreadsheets. Evidence gets lost, amounts get rounded, and the reviewer cannot tell what was checked.",
            "I built this twice. Version 1 (USDT Investigator) proved the evidence pipeline on one saved case. Version 2 (Trace Desk) added live queries, case files and a QC workflow.",
        ],
        "flow": [
            ("Collect", "JSON-RPC calls for USDT Transfer logs and block headers from a public node, in batches."),
            ("Verify", "Raw responses saved with SHA-256 checksums and block hashes in a manifest."),
            ("Decode", "Sender, recipient and amount from raw log data, kept as whole-number base units."),
            ("Bound the graph", "Start from a wallet with 6 to 12 counterparties and expand at most two hops."),
            ("Investigate", "Warning signs that link to the transfers behind them; pin evidence."),
            ("Hand off", "JSON case file with a checksum; frozen QC snapshots for review."),
        ],
        "tech": ["Python 3 (standard library)", "Ethereum JSON-RPC", "JavaScript ES modules", "SHA-256 checksums", "unittest and node:test"],
        "decisions": [
            ("Hard limits on scope", "700 blocks, 1,000 transfers, five wallets and a two-hour window per live query. An over-budget query never replaces the case on screen."),
            ("Never use floating point for money", "Amounts stay as integer base units from decoding to export."),
            ("Warning signs, not risk scores", "Matching amounts in sequence are shown as a lead with the transfers behind it, not as proof of the same funds."),
            ("Empty means empty", "A window with no transfers is reported as no data, never as a clean wallet."),
            ("Frozen QC rounds", "If the analyst edits evidence after submission, the earlier review no longer applies."),
        ],
        "tests": ("49 tests (41 in Trace Desk, 8 in version 1)", ["JavaScript decoding agrees with the Python saved evidence", "Large uint256 amounts stay exact; removed logs and malformed hashes fail closed", "No activity is not a clean bill of health, and a provider failure is not an empty case", "Checksums detect changed payloads; fabricated QC outcomes are rejected on import", "Resubmission keeps the previous outcome and creates a fresh snapshot"]),
        "results": ["80 blocks (25,929,879 to 25,929,958) and 7,640 USDT transfers decoded", "A 15-wallet, 15-transfer case with a written report", "Live queries run from the browser against a public node with no server and no keys"],
        "limits": ["A wallet address is not a person; nothing is attributed", "A window is a slice of activity, not full history or balance", "Data comes from one public node; checksums catch local changes, not node errors", "Notes stay in the browser until a case file is saved"],
        "next": ["Cross-checking a second node for the saved case", "Tron support using the same evidence model", "Signed case files so a reviewer can verify who produced them"],
        "docs": [("Case report", "CASE_REPORT.md")],
    },
    {
        "slug": "sanctions-review-desk",
        "title": "Sanctions Review Desk",
        "pillar": "Investigation tooling",
        "oneliner": "Takes a possible OFAC name match to a documented decision a QC reviewer can check, with live search over the official list refreshed every hour.",
        "demo": "/sanctions-review-desk/",
        "repo": "https://github.com/brandoncandela/sanctions-review-desk",
        "image": "sanctions-review-desk.jpg",
        "glance": [("~19,500", "OFAC SDN entries searchable"), ("Hourly", "automated list refresh"), ("24 h", "staleness limit before search refuses"), ("21", "automated tests")],
        "who": "Sanctions screening analysts, trade compliance teams and QC reviewers.",
        "built": "A scheduled OFAC data pipeline, in-browser name search, identifier comparison, evidence pinning, information requests and multi-round QC.",
        "result": "A screening hit becomes a reviewable case file, and the search never answers from data older than a day.",
        "problem": [
            "A screening tool says a customer or shipment party might match the sanctions list. The analyst still has to compare identifiers, request what is missing, decide and explain it well enough that QC can challenge it.",
        ],
        "flow": [
            ("Refresh", "A GitHub Action downloads the official SDN and alias files every hour."),
            ("Publish", "The normalized list is committed as JSON with a retrieval timestamp."),
            ("Search", "The browser loads it and matches every query word against names and aliases, ignoring accents and punctuation."),
            ("Compare", "Each identifier marked as supporting, against or unknown."),
            ("Document", "Pinned sources, information requests and a written assessment."),
            ("QC", "Frozen submissions, findings, returns and resubmissions in one case file."),
        ],
        "tech": ["TypeScript", "React", "Vite", "Tailwind CSS", "GitHub Actions", "node:test"],
        "decisions": [
            ("Refuse stale data", "If the list copy is more than 24 hours old the search will not run, because a confident answer on old data is worse than no answer."),
            ("Unknown is its own state", "Missing information is never counted as a mismatch."),
            ("Keep sanctions and export controls apart", "A shipment can raise both, and the case records them separately."),
            ("Validate case files on import", "Broken references are rejected so a reopened case is the case that was saved."),
        ],
        "tests": ("21 node:test cases", ["Official OFAC CSV parsing keeps quoted commas and the end-of-file marker", "A fresh feed is accepted; a stale or failed feed is rejected", "Editing a draft cannot change a submitted case", "A QC return needs an analyst response before resubmission", "Malformed, dangling or colliding case files are rejected on import"]),
        "results": ["Three training cases covering rerouted shipments, a similar name and a third-party payer", "Live search over the current SDN list with the retrieval time on every result"],
        "limits": ["Searches SDN names and aliases only; no 50 Percent Rule ownership, other lists or export classifications", "Reviewer names are typed in, not authenticated", "Case files can be edited by anyone who holds them"],
        "next": ["Ownership checks for entities owned 50% or more by listed persons", "Consolidated Screening List coverage", "Authenticated reviewers and a locked audit trail"],
        "docs": [],
    },
    {
        "slug": "adverse-media-review-desk",
        "title": "Adverse Media Review Desk",
        "pillar": "Investigation tooling",
        "oneliner": "Decides whether a news story is really about your customer, with the same triage rules written in TypeScript for analysts and SQL for auditors.",
        "demo": "/adverse-media-review-desk/",
        "repo": "https://github.com/brandoncandela/adverse-media-review-desk",
        "image": "adverse-media-review-desk.jpg",
        "glance": [("9", "SQL training cases"), ("27", "identifier comparisons"), ("4", "comparison states, not two"), ("20", "automated tests")],
        "who": "KYC and screening analysts reviewing negative news hits, and the QC teams who check them.",
        "built": "A side-by-side identifier comparison, news search, triage rules in TypeScript and a SQL view, and an export pipeline that runs the SQL migrations.",
        "result": "The interface and the SQL view reach the same outcome, and a query proves it by returning nothing when they agree.",
        "problem": [
            "Name screening finds articles that mention someone with your customer's name. Most are about someone else. The common mistake is treating missing information as a mismatch, which closes alerts that were never actually cleared.",
        ],
        "flow": [
            ("Compare", "Bank record and article subject side by side: match, variant, conflict or unknown."),
            ("Search news", "GDELT news search, a Google search link, or a manual article."),
            ("Triage in code", "Rules in lib/matching.ts drive the interface."),
            ("Triage in SQL", "Migrations build 9 cases and a view using a CTE, CASE, conditional aggregation and JSON extraction."),
            ("Export", "A script runs the migrations in SQLite and exports the SQL-derived outcomes."),
            ("Decide", "Escalate, rule out or request information, with the reasoning saved."),
        ],
        "tech": ["TypeScript", "React", "Vite", "SQLite migrations", "GDELT API", "node:test"],
        "decisions": [
            ("Four states instead of match or no match", "Only a verified conflict counts against a hit; unknown stays an evidence gap."),
            ("Two implementations, one answer", "The SQL view and the TypeScript rules are checked against the expected outcome so they cannot drift apart unnoticed."),
            ("Location alone never rules a hit out", "People move. A name and full date of birth match escalates even if the city differs."),
        ],
        "tests": ("20 node:test cases", ["A missing middle name or unknown identifier is never a mismatch", "An unverified DOB conflict is not a false positive; a verified one needs evidence and a source", "Name and full DOB escalate despite a country conflict", "Day-month reversals are ambiguous, and age is judged on the article date", "Unsafe links are rejected and stale QC is flagged after a customer change"]),
        "results": ["Nine training cases that each test a tricky situation", "A disagreement query between SQL and expected outcomes that returns zero rows"],
        "limits": ["Training cases are fictional", "News search depends on GDELT coverage", "The full case store in data-model.sql is a design proposal, not used by the demo"],
        "next": ["Storing reviews in the proposed case store", "Source reliability scoring per outlet", "Batch review of many hits for one customer"],
        "docs": [],
    },
    {
        "slug": "sql-fincrime-lab",
        "title": "SQL Financial Crime Lab",
        "pillar": "Fintech risk infrastructure",
        "oneliner": "Real SQLite queries running in the browser to show which monitoring threshold changes cut review work and which ones miss cases that matter.",
        "demo": "/sql-fincrime-lab/",
        "repo": "https://github.com/brandoncandela/sql-fincrime-lab",
        "image": "sql-fincrime-lab.jpg",
        "glance": [("3", "tunable monitoring scenarios"), ("36", "customers, 177 transactions"), ("44% / 67%", "baseline precision and recall"), ("8", "SQL tests")],
        "who": "Transaction monitoring and model risk teams tuning scenarios.",
        "built": "A deterministic fixture generator, an indexed schema, parameterized scenario queries, an in-browser SQL engine, an alert review flow and an implementation and UAT guide.",
        "result": "Tightening thresholds visibly trades fewer alerts for missed cases, which is the failure mode tuning has to watch for.",
        "problem": [
            "A fintech has too many alerts. Some threshold changes reduce work; others quietly remove cases that still deserve investigation. Teams need to see both effects before they change a rule.",
        ],
        "flow": [
            ("Generate fixtures", "Deterministic customers, accounts and transactions with authored labels."),
            ("Model", "Schema with constraints and a query-driven index."),
            ("Query", "Rapid movement, customer profile and many-to-one scenarios as parameterized SQL."),
            ("Run in browser", "SQL.js executes the same queries as the tests."),
            ("Review", "Open an alert, see the exact SQL, write an assessment, role-play QC."),
            ("Export", "Case with evidence, thresholds, SQL and review history."),
        ],
        "tech": ["SQLite", "SQL.js (WebAssembly)", "SQL: joins, CTEs, ROW_NUMBER", "Python fixture generator", "unittest"],
        "decisions": [
            ("The browser runs the real queries", "No precomputed results, so what a reviewer sees is what the SQL returns."),
            ("Show the misses", "Recall and missed cases sit next to alert volume on every change."),
            ("Index for the query, then prove it", "A test checks the query plan uses the account, direction and time index."),
        ],
        "tests": ("8 unittest cases", ["Known baseline cases and confusion counts", "Threshold boundary inclusion", "A repeated sender is not counted twice", "Transactions on the wrong day are excluded", "Duplicate IDs and orphans are rejected", "A tighter queue can miss more, and the query uses its index"]),
        "results": ["Baseline: 18 alerts, 8 true positives, 4 review-worthy cases missed", "Each scenario tunable live with the effect on precision and recall"],
        "limits": ["Small fictional test set", "Rapid movement uses timing and similar amounts; it does not prove the same funds", "QC is a browser role-play without real accounts or a locked audit trail"],
        "next": ["Rolling windows instead of a fixed calendar day", "Above- and below-the-line testing samples", "Scenario documentation in a model risk template"],
        "docs": [("Implementation and UAT guide", "dist/implementation.md")],
    },
    {
        "slug": "payments-strategy-lab",
        "title": "Payments Strategy Lab",
        "pillar": "Fintech risk infrastructure",
        "oneliner": "A tested unit-economics model that compares three approval strategies on revenue, fraud loss and review capacity, ending in a 90-day pilot memo.",
        "demo": "/payments-strategy-lab/",
        "repo": "https://github.com/brandoncandela/payments-strategy-lab",
        "image": "payments-strategy-lab.jpg",
        "glance": [("3", "strategies compared"), ("5", "adjustable assumptions"), ("$479K", "best monthly contribution in the base case"), ("7", "model tests")],
        "who": "Payments, risk and finance leaders deciding whether more approvals are worth the fraud and staffing cost.",
        "built": "A pure JavaScript financial model, sensitivity tables, a staffing payback analysis and a downloadable decision memo.",
        "result": "Targeted review wins the base case, and the model shows that hiring to cover every review would cost $67K a month more than it saves.",
        "problem": [
            "A payments business wants to approve more legitimate purchases. Approving more also lets more fraud through and sends more payments to a review team with fixed capacity. The decision needs numbers a CFO and a risk lead both accept.",
        ],
        "flow": [
            ("Assumptions", "Volume, ticket size, fraud rate, margin and review headcount."),
            ("Model", "Pure functions compute approvals, fraud loss, review cost and contribution per strategy."),
            ("Stress", "Sensitivity across fraud rates and a staffing payback scenario."),
            ("Decide", "Pick a strategy, write the reasoning, export the memo."),
        ],
        "tech": ["JavaScript (pure model module)", "node:test", "HTML and CSS"],
        "decisions": [
            ("Keep the model pure", "No DOM in the model, so it can be tested on its own and reused."),
            ("Check against an independent calculation", "A reference case computed separately guards the formulas."),
            ("Capacity overflow is declined", "Payments the team has no time to review are declined, which makes the staffing tradeoff explicit."),
        ],
        "tests": ("7 node:test cases", ["An independently calculated reference case", "The cash bridge reconciles", "Capacity limits reviews, and spare staff cost money without adding approvals", "Zero fraud gives zero fraud loss; invalid inputs are rejected"]),
        "results": ["Base case: targeted review $479,342, conservative $464,660, growth first $388,364 monthly contribution", "Full review coverage needs 25 FTE; adding 13 costs $67,073 a month net"],
        "limits": ["All inputs are fictional, not benchmarks", "Contribution excludes overhead, tax, capital and lifetime value", "A scenario model, not a forecast"],
        "next": ["Chargeback timing and dispute costs", "Segment-level strategies instead of one policy", "Confidence ranges on fraud rate"],
        "docs": [("Methodology and formulas", "dist/methodology.md")],
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def head(title: str, desc: str, path: str, image: str) -> str:
    url = f"{SITE}{path}"
    ld = {"@context": "https://schema.org", "@type": "TechArticle", "headline": title, "description": desc,
          "author": {"@type": "Person", "name": "Brandon Candela", "url": SITE + "/"}, "url": url, "image": image}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fbfcff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<title>{esc(title)} | Brandon Candela</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld)}</script>
<link rel="stylesheet" href="/assets/page.css">
</head>
<body>
<nav><div><a href="/">Brandon Candela</a><span class="navlinks"><a href="/case-studies/">Case studies</a><a href="/#writing">Writing</a><a href="/#contact">Contact</a></span></div></nav>
"""


def contact_band() -> str:
    return f"""<div class="card contact-band"><p>Building financial crime tooling and want to talk about this project?</p>
<div class="actions"><a class="btn primary" href="mailto:{EMAIL}">Email Brandon</a><a class="btn ghost" href="{LINKEDIN}">LinkedIn</a></div></div>"""


def render(s: dict) -> str:
    title = f"{s['title']}: technical case study"
    out = [head(title, s["oneliner"], f"/case-studies/{s['slug']}.html", f"{SITE}/assets/projects/{s['image']}")]
    out.append("<main>")
    out.append(f'<p class="eyebrow">Technical case study · {esc(s["pillar"])}</p>')
    out.append(f"<h1>{esc(s['title'])}</h1>")
    out.append(f'<p class="lede">{esc(s["oneliner"])}</p>')
    links = [f'<a class="btn primary" href="{s["demo"]}">Live demo</a>'] if s.get("demo") else []
    links.append(f'<a class="btn {"ghost" if s.get("demo") else "primary"}" href="{s["repo"]}">Source code</a>')
    links += [f'<a class="btn ghost" href="{u}">{esc(t)}</a>' for t, u in s.get("extra_links", [])]
    links.append(f'<a class="btn ghost" href="mailto:{EMAIL}">Contact</a>')
    out.append(f'<div class="actions">{"".join(links)}</div>')
    if s.get("tour"):
        src, still, alt, caption = s["tour"]
        # Video plays only when motion is allowed (assets/motion-video.js); the description stays available to screen readers.
        out.append('<figure class="card" id="tour" style="margin:22px 0;padding:0;overflow:hidden">'
                   f'<video data-autoplay muted loop playsinline preload="none" poster="/assets/projects/{still}" width="960" height="640" aria-hidden="true" style="display:block;width:100%;height:auto">'
                   f'<source src="/assets/projects/{src}.webm" type="video/webm"><source src="/assets/projects/{src}.mp4" type="video/mp4"></video>'
                   f'<p class="sr-only">{esc(alt)}</p>'
                   f'<figcaption style="padding:12px 18px;font-size:.9rem;color:var(--muted)">{esc(caption)}</figcaption></figure>')
    out.append('<div class="glance">' + "".join(f'<div class="card"><b>{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in s["glance"]) + "</div>")
    out.append('<section class="cs card"><div class="summary-grid">'
               f'<div><h3>Who it is for</h3><p>{esc(s["who"])}</p></div>'
               f'<div><h3>What I built</h3><p>{esc(s["built"])}</p></div>'
               f'<div><h3>Result</h3><p>{esc(s["result"])}</p></div></div></section>')
    out.append('<section class="cs card"><h2>The problem</h2>' + "".join(f"<p>{esc(p)}</p>" for p in s["problem"]) + "</section>")
    out.append('<section class="cs card"><h2>Architecture</h2><p>How data moves from source to decision.</p><ol class="flow">'
               + "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in s["flow"]) + "</ol>"
               + '<h3 style="margin-top:18px">Technologies</h3><ul class="chips">' + "".join(f"<li>{esc(t)}</li>" for t in s["tech"]) + "</ul></section>")
    out.append('<section class="cs card"><h2>Engineering decisions</h2><div class="decisions">'
               + "".join(f"<div><b>{esc(a)}</b><p>{esc(b)}</p></div>" for a, b in s["decisions"]) + "</div></section>")
    count, items = s["tests"]
    out.append('<section class="cs two">'
               f'<div class="card"><h2>Tests</h2><p><b style="color:var(--ink)">{esc(count)}</b>, run with one command and no network.</p><ul class="tight">'
               + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul></div>"
               '<div class="card"><h2>Results</h2><ul class="tight">' + "".join(f"<li>{esc(i)}</li>" for i in s["results"]) + "</ul></div></section>")
    out.append('<section class="cs two">'
               '<div class="card"><h2>Limitations</h2><ul class="tight">' + "".join(f"<li>{esc(i)}</li>" for i in s["limits"]) + "</ul></div>"
               '<div class="card"><h2>What I would build next</h2><ul class="tight">' + "".join(f"<li>{esc(i)}</li>" for i in s["next"]) + "</ul></div></section>")
    if s["docs"]:
        out.append('<section class="cs card"><h2>Product and delivery documents</h2><ul class="tight">'
                   + "".join(f'<li><a href="{s["repo"]}/blob/main/{p}">{esc(t)}</a></li>' for t, p in s["docs"]) + "</ul></section>")
    out.append(contact_band())
    out.append("</main>")
    out.append('<footer>All data in this project is synthetic or public. Built and tested by Brandon Candela. <a href="/case-studies/">All case studies</a> · <a href="/">Portfolio</a></footer>')
    if s.get("tour"):
        out.append('<script src="/assets/motion-video.js" defer></script>')
    out.append("</body>\n</html>\n")
    return "\n".join(out)


def render_index() -> str:
    desc = "Technical case studies of financial crime systems built by Brandon Candela: the problem, architecture, engineering decisions, tests, results and limitations."
    out = [head("Technical case studies", desc, "/case-studies/", f"{SITE}/assets/og-image.jpg"), "<main>"]
    out.append('<p class="eyebrow">Brandon Candela · Financial crime technology</p><h1>Technical case studies</h1>')
    out.append('<p class="lede">Every project answers the same questions: what problem it solves, how it is built, which decisions I made and why, how it is tested, what it achieved and where it stops.</p>')
    out.append('<div class="cs-list">')
    for s in STUDIES:
        out.append(f'<div class="card"><p class="eyebrow">{esc(s["pillar"])}</p><h2>{esc(s["title"])}</h2><p>{esc(s["oneliner"])}</p>'
                   f'<div class="actions"><a class="btn primary" href="/case-studies/{s["slug"]}.html">Read case study</a>'
                   + (f'<a class="btn ghost" href="{s["demo"]}">Live demo</a>' if s.get("demo") else "")
                   + f'<a class="btn ghost" href="{s["repo"]}">Source</a></div></div>')
    out.append("</div>")
    out.append(contact_band())
    out.append('</main><footer><a href="/">Back to portfolio</a></footer></body>\n</html>\n')
    return "\n".join(out)


def main():
    OUT.mkdir(exist_ok=True)
    for s in STUDIES:
        (OUT / f"{s['slug']}.html").write_text(render(s))
    (OUT / "index.html").write_text(render_index())
    print(f"Wrote {len(STUDIES)} case studies and an index to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
