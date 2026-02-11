PROMPT_GROUPS: dict[str, list[str]] = {
    "ML Engineer prompts": [
        "Summarize your end-to-end machine learning projects.",
        "How have you evaluated and compared ML models in practice?",
        "What tradeoffs have you made between model complexity and reliability?",
        "Describe an ML system you helped move toward production.",
        "What failure modes have you seen in applied ML systems?",
    ],
    "Data Scientist prompts": [
        "How do you approach exploratory data analysis on a new dataset?",
        "What data quality issues have you handled in real projects?",
        "Describe an analysis that influenced a real decision.",
        "How do you validate assumptions before modeling?",
        "What metrics do you trust most when evaluating results?",
    ],
    "Backend / Production prompts": [
        "What production systems have you contributed to?",
        "How do you ensure correctness when modifying existing services?",
        "What testing strategies have you used for APIs or data pipelines?",
        "How do you handle edge cases and contract validation?",
        "What does 'production-ready' mean to you in practice?",
    ],
}
