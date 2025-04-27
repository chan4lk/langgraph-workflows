GOAL_PROMPT = """
consider current date as {date}.

Generate a SMART Goals for 6 months with the following structure:

1. **Performance Goals**:  
- List 4–6 specific, measurable, achievable, relevant, and time-bound goals related to the user's role and/or project.  
- Focus areas should include technical improvement, productivity, learning/development, collaboration, and contribution to organizational activities.  
- Use a style similar to:
- [Action or Deliverable] ([Timeline or Percentage or Target])
- [Learning Goal] ([Timeframe])
- [Participation Target] ([Percentage or Frequency])

2. **KPIs (Key Performance Indicators)**:  
- List 2–4 specific KPIs to measure success, such as:
- Time allocation percentages
- Quality metrics (e.g., bug count, peer reviews)
- Efficiency or performance benchmarks

3. **Performance Evaluation Criteria**:  
- Include the following fixed structure for rating performance:
- 1: Unsatisfactory
- 2: Needs Improvement
- 3: Meets Expectations
- 4: Exceeds Expectations
- 5: Exceptional

Format the output exactly like the examples shown, using simple bullet points under each section.
"""

USER_DETAILS_PROMPT = "Find user deatails based on the user's name using tools. if user is not found, say that they are not found. otherwise return the user's role."