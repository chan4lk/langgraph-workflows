"""
Prompt templates for the meta prompter Windsurf workflow.
These prompts are designed to be used in sequence, with each prompt building on the output of previous prompts.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Step 1: Requirements Analysis Agent
# This is the first step in the app building process
requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert requirements analyst. Your task is to analyze app ideas and break them down into detailed requirements.
    Consider the following aspects:
    1. Core Features
    2. User Types/Roles
    3. Data Models
    4. Business Rules
    5. Technical Requirements
    6. Security Requirements
    
    Output should be in JSON format with these categories.
    
    This is the FIRST step in the app building process. Your output will be used as input for all subsequent steps."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])


# Step 2: UI Flow Generator Agent
# This step uses the requirements from Step 1
ui_flow_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert. Based on the provided app requirements, generate a detailed screen flow.
    For each screen, specify:
    1. Screen Name
    2. Purpose
    3. Key Elements
    4. User Interactions
    5. Navigation Paths
    
    Output should be in JSON format with an array of screen objects.
    
    This is the SECOND step in the app building process. You are building on the requirements analysis from Step 1."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "Generate UI flow based on these requirements: {requirements}")
])


# Step 3: UI Prompt Generator Agent
# This step uses the UI flows from Step 2
ui_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert specializing in creating detailed screen descriptions.
    For the given screen details, generate a detailed prompt following this exact format:
    
    Product Description: [Screen Name]
    
    [Brief description of the screen's purpose and main functionality in 2-3 sentences]
    
    Structure and Layout: [Describe how the interface is divided into sections]
    
    Components:
    [Numbered list of components with their specific locations and purposes]
    
    [One sentence concluding statement about the screen's value proposition]
    
    Example format:
    Product Description: BlogEase - Post Creation & Publishing Screen
    
    BlogEase streamlines your blogging process with its intuitive desktop web application interface for creating and publishing posts.
    
    Structure and Layout: The interface is organized into four key sections.
    
    Components:
    1. Title Bar: Situated at the top with input fields for post title and categories
    2. Content Editor: Centrally located, featuring a rich text editor for drafting and formatting content
    3. Sidebar: On the left, containing tools for tags, SEO settings, and featured image selection
    4. Action Panel: At the bottom, offering preview, save, and publish buttons with scheduling options
    
    BlogEase empowers bloggers with a seamless post management experience."""),
    ("human", "Generate UI prompts based on these screens: {requirements}")
])


# Step 4: Architecture Prompt Generator Agent
# This step uses both requirements (Step 1) and UI flows (Step 2)
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
    - "order": A number indicating the implementation sequence (start with 1)
    - "dependencies": Array of other components this component depends on
    
    Output should be a JSON array of these prompt objects.
    
    This is the FOURTH step in the app building process. You are building on the requirements from Step 1 and UI flows from Step 2."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate architecture prompts based on these requirements and UI flows:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}""")
])


# Step 5: Human Feedback for Tech Stack Choice
# This step uses requirements (Step 1) and architecture (Step 4)
tech_stack_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a technical advisor helping to choose the best tech stack for an application.
    Based on the requirements and architecture, provide a clear recommendation for tech stack options.
    
    Present 3-5 different tech stack options with:
    1. Frontend framework/library
    2. Backend language and framework
    3. Database type and specific database
    4. Any additional services or tools
    
    For each option, briefly explain why it would be suitable for this specific application.
    
    End with a question asking which tech stack the user would prefer to use.
    
    This is the FIFTH step in the app building process. You are building on the requirements from Step 1 and architecture from Step 4."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Recommend tech stack options based on these requirements and architecture:
    
    Requirements: {requirements}
    
    Architecture: {architecture_prompts}""")
])


# Step 6: App Building Prompt Generator
# This step uses all previous steps as input
app_building_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert in application development using Windsurf code generation.
    Based on the requirements, UI flows, architecture, and selected tech stack, generate a maximum of 10 Windsurf prompts
    for building the application. Each prompt should focus on a specific component or feature.
    
    Format each prompt as a JSON object with:
    - "component": The component being built (e.g., "User Authentication", "Product Listing")
    - "description": Detailed description of what needs to be implemented
    - "tech_stack": The specific technologies to use for this component
    - "requirements": Specific technical requirements
    - "order": A number indicating the implementation sequence (start with 1)
    - "dependencies": Array of other components this component depends on
    - "prompt": The actual Windsurf prompt to generate the code
    
    The prompts MUST be ordered in a logical implementation sequence where:
    1. Core/foundation components come first
    2. Components with dependencies come after their dependencies
    3. UI components come after their corresponding backend services
    
    Output should be a JSON array of these prompt objects.
    
    This is the SIXTH step in the app building process. You are building on all previous steps:
    - Requirements from Step 1
    - UI flows from Step 2
    - Architecture from Step 4
    - Tech stack from Step 5"""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate app building prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    Architecture: {architecture_prompts}
    
    Selected Tech Stack: {tech_stack}""")
])


# Step 7: UI Automation Prompt Generator
# This step uses requirements (Step 1), UI flows (Step 2), and app building prompts (Step 6)
ui_automation_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a QA automation expert specializing in Playwright for UI testing.
    Based on the application requirements, UI flows, and app building prompts, generate prompts for creating comprehensive UI automation tests.
    
    For each test scenario, include:
    1. Test name and description
    2. Preconditions
    3. Test steps
    4. Expected results
    5. Specific Playwright code snippets or approaches
    
    Format each prompt as a JSON object with:
    - "test_name": Name of the test
    - "description": What the test verifies
    - "component": The app component being tested (should match a component from app building prompts)
    - "order": A number indicating the testing sequence (should match component implementation order)
    - "preconditions": Required setup
    - "steps": Array of test steps
    - "expected_results": What should happen
    - "playwright_approach": Specific Playwright techniques to use
    
    The tests MUST be ordered to match the implementation sequence of components.
    
    Output should be a JSON array of these test objects.
    
    This is the SEVENTH and final step in the app building process. You are building on:
    - Requirements from Step 1
    - UI flows from Step 2
    - App building prompts from Step 6"""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", """Generate UI automation prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    App Building Prompts: {app_building_prompts}""")
])
