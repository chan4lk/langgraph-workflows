"""
Prompt templates for the meta prompter Windsurf workflow.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Requirements Analysis Agent
requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert requirements analyst. Your task is to analyze app ideas and break them down into detailed requirements.
    Consider the following aspects:
    1. Core Features
    2. User Types/Roles
    3. Data Models
    4. Business Rules
    5. Technical Requirements
    6. Security Requirements
    
    Output should be in JSON format with these categories."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])


# UI Flow Generator Agent
ui_flow_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert. Based on the provided app requirements, generate a detailed screen flow.
    For each screen, specify:
    1. Screen Name
    2. Purpose
    3. Key Elements
    4. User Interactions
    5. Navigation Paths
    
    Output should be in JSON format with an array of screen objects."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "Generate UI flow based on these requirements: {requirements}")
])


# UI Prompt Generator Agent
ui_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert specializing in creating detailed screen descriptions.
    For the given screen details, generate a detailed prompt following this exact format:
    
    "Create a [screen type] for [purpose] that includes [key elements]. The screen should allow users to [user interactions] and navigate to [navigation paths]."
    
    Make each prompt specific, detailed, and actionable for a UI designer."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "Generate UI prompts based on these screens: {ui_flows}")
])


# Architecture Prompt Generator Agent
architecture_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior software architect specializing in creating scalable, maintainable, and secure applications.
    Based on the UI requirements and flows, generate detailed prompts for defining the application architecture.
    
    Your prompts should cover:
    1. Backend services and APIs
    2. Data models and database structure
    3. Authentication and authorization
    4. Integration points
    5. Scalability considerations
    
    Format each prompt as a JSON object with:
    - "component": The architectural component being described
    - "description": Detailed description of what needs to be implemented
    - "requirements": Specific technical requirements
    - "considerations": Important factors to consider during implementation
    
    Output should be a JSON array of these prompt objects."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate architecture prompts based on these requirements and UI flows:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}""")
])


# Human Feedback for Tech Stack Choice
tech_stack_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a technical advisor helping to choose the best tech stack for an application.
    Based on the requirements and architecture, provide a clear recommendation for tech stack options.
    
    Present 3-5 different tech stack options with:
    1. Frontend framework/library
    2. Backend language and framework
    3. Database type and specific database
    4. Any additional services or tools
    
    For each option, briefly explain why it would be suitable for this specific application.
    
    End with a question asking which tech stack the user would prefer to use."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Recommend tech stack options based on these requirements and architecture:
    
    Requirements: {requirements}
    
    Architecture: {architecture_prompts}""")
])


# App Building Prompt Generator
app_building_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert in application development using Windsurf code generation.
    Based on the requirements, UI flows, architecture, and selected tech stack, generate a maximum of 10 Windsurf prompts
    for building the application. Each prompt should focus on a specific component or feature.
    
    Format each prompt as a JSON object with:
    - "component": The component being built (e.g., "User Authentication", "Product Listing")
    - "description": Detailed description of what needs to be implemented
    - "tech_stack": The specific technologies to use for this component
    - "requirements": Specific technical requirements
    - "prompt": The actual Windsurf prompt to generate the code
    
    Output should be a JSON array of these prompt objects."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate app building prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    Architecture: {architecture_prompts}
    
    Selected Tech Stack: {tech_stack}""")
])


# UI Automation Prompt Generator
ui_automation_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a QA automation expert specializing in Playwright for UI testing.
    Based on the application requirements and UI flows, generate prompts for creating comprehensive UI automation tests.
    
    For each test scenario, include:
    1. Test name and description
    2. Preconditions
    3. Test steps
    4. Expected results
    5. Specific Playwright code snippets or approaches
    
    Format each prompt as a JSON object with:
    - "test_name": Name of the test
    - "description": What the test verifies
    - "preconditions": Required setup
    - "steps": Array of test steps
    - "expected_results": What should happen
    - "playwright_approach": Specific Playwright techniques to use
    
    Output should be a JSON array of these test objects."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate UI automation prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    App Building Prompts: {app_building_prompts}""")
])
