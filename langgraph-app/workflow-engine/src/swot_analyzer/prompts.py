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

GREETING_PROMPT = """Generate a short, inspiring motivational quote that would motivate someone to do a thorough SWOT analysis. The quote should be concise, impactful, and encourage strategic thinking.

Motivational Quote:
"""

SUMMARY_PROMPT = """Based on the following description, summarize the SWOT analysis and provide a future action plan:

strengths: {strengths}
weaknesses: {weaknesses}
opportunities: {opportunities}
threats: {threats}

Summary:
"""