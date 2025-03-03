STRENGTHS_PROMPT = """Based on the following description, list the strengths:

{user_input}

Strengths:
"""

WEAKNESSES_PROMPT = """Based on the following description, list the weaknesses:

{user_input}

Weaknesses:
"""

OPPORTUNITIES_PROMPT = """Based on the following description, list the opportunities:

{user_input}

Opportunities:
"""

THREATS_PROMPT = """Based on the following description, list the threats:

{user_input}

Threats:
"""

SUMMARY_PROMPT = """Based on the following description, summarize the SWOT analysis:

strengths: {strengths}
weaknesses: {weaknesses}
opportunities: {opportunities}
threats: {threats}

Summary:
"""