from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import PyPDF2
import os
import json
from pathlib import Path

class CVData(TypedDict):
    file_name: str
    content: str
    extracted_info: Optional[Dict[str, Any]]
    score: Optional[float]

class JobRequirements(TypedDict):
    required_skills: List[str]
    desired_experience: List[str]
    qualifications: List[str]
    key_responsibilities: List[str]

class CVReaderAgent:
    def __init__(self):
        pass

    def process(self, cv_folder_path: str) -> List[CVData]:
        cv_data_list = []
        folder_path = Path(cv_folder_path)
        
        if not folder_path.exists():
            print(f"Error: Folder {folder_path} does not exist")
            return cv_data_list
            
        if not folder_path.is_dir():
            print(f"Error: {folder_path} is not a directory")
            return cv_data_list

        # Get all PDF files in the folder
        pdf_files = list(folder_path.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in {folder_path}")

        for file_path in pdf_files:
            try:
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    
                    cv_data_list.append(CVData(
                        file_name=file_path.name,
                        content=text,
                        extracted_info=None,
                        score=None
                    ))
                    print(f"Successfully processed {file_path.name}")
            except Exception as e:
                print(f"Error processing {file_path.name}: {str(e)}")

        return cv_data_list

class JobDescriptionAnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert job description analyzer. Your task is to extract key information from job descriptions and provide meaningful insights even when the description is sparse or unclear.

Key Instructions:
1. Always provide a complete analysis with all required fields
2. If specific information is missing, infer reasonable defaults based on the job context
3. Use industry standard skills and qualifications when details are unclear
4. Maintain professional relevance in all fields

Format your response as a JSON object with these exact keys:
{
    "required_skills": ["skill1", "skill2", ...],
    "desired_experience": ["exp1", "exp2", ...],
    "qualifications": ["qual1", "qual2", ...],
    "key_responsibilities": ["resp1", "resp2", ...]
}

Guidelines for sparse descriptions:
- For technical roles: Include common programming languages, frameworks, and tools
- For business roles: Include communication, analysis, and management skills
- For qualifications: Include standard education and certification requirements
- For responsibilities: Include typical duties for the role type

Never return empty arrays. If information is unclear, provide reasonable industry-standard defaults."""),
            ("human", "Please analyze this job description and extract or infer key information:\n\n{job_description}")
        ])

    def process(self, job_description: str) -> JobRequirements:
        try:
            chain = self.prompt | self.llm
            result = chain.invoke({"job_description": job_description})
            
            # Parse the JSON string into a Python dictionary
            try:
                structured_requirements = json.loads(result.content)
                
                # Validate and ensure non-empty arrays
                for key in ["required_skills", "desired_experience", "qualifications", "key_responsibilities"]:
                    if not structured_requirements.get(key) or len(structured_requirements[key]) == 0:
                        structured_requirements[key] = self._get_default_values(key, job_description)
                
                return JobRequirements(**structured_requirements)
                
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM response: {e}")
                return self._get_default_requirements(job_description)
                
        except Exception as e:
            print(f"Error in job description analysis: {e}")
            return self._get_default_requirements(job_description)

    def _get_default_values(self, key: str, context: str) -> List[str]:
        """Provide meaningful default values based on the field type and any available context."""
        defaults = {
            "required_skills": [
                "Communication skills",
                "Problem-solving ability",
                "Team collaboration",
                "Time management",
                "Analytical thinking"
            ],
            "desired_experience": [
                "Previous relevant work experience",
                "Project management",
                "Team leadership",
                "Industry knowledge",
                "Stakeholder management"
            ],
            "qualifications": [
                "Bachelor's degree in relevant field",
                "Professional certification (if applicable)",
                "Industry-specific training",
                "Relevant technical skills",
                "Professional experience equivalent"
            ],
            "key_responsibilities": [
                "Contribute to team objectives",
                "Manage assigned projects and tasks",
                "Collaborate with team members",
                "Report on progress and metrics",
                "Maintain professional standards"
            ]
        }
        return defaults.get(key, ["Not specified"])

    def _get_default_requirements(self, context: str) -> JobRequirements:
        """Return a complete set of default requirements when analysis fails."""
        return JobRequirements(
            required_skills=self._get_default_values("required_skills", context),
            desired_experience=self._get_default_values("desired_experience", context),
            qualifications=self._get_default_values("qualifications", context),
            key_responsibilities=self._get_default_values("key_responsibilities", context)
        )

class CVInformationExtractorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert CV analyzer. Your task is to carefully extract key information from the CV text.
You must return a valid JSON object with exactly these keys and formats:
{{
    "skills": ["skill1", "skill2"],
    "experience": ["exp1", "exp2"],
    "education": ["edu1", "edu2"],
    "profile_summary": "brief summary"
}}

Important rules:
1. Always return a valid JSON object
2. Include all required keys even if empty
3. Skills, experience, and education must be arrays
4. Profile summary must be a string
5. Never include additional keys
6. Never return null values"""),
            ("human", "Please analyze this CV and extract the key information:\n\n{cv_text}")
        ])

    def validate_extracted_info(self, data: Dict[str, Any]) -> bool:
        required_keys = {"skills", "experience", "education", "profile_summary"}
        array_keys = {"skills", "experience", "education"}
        
        # Check if all required keys exist
        if not all(key in data for key in required_keys):
            print(f"Missing required keys. Found keys: {list(data.keys())}")
            return False
            
        # Validate array fields
        for key in array_keys:
            if not isinstance(data[key], list):
                print(f"Field '{key}' must be an array, got {type(data[key])}")
                return False
                
        # Validate profile summary
        if not isinstance(data["profile_summary"], str):
            print(f"Field 'profile_summary' must be a string, got {type(data['profile_summary'])}")
            return False
            
        return True

    def process(self, cv_data: CVData) -> CVData:
        try:
            print(f"\nProcessing CV: {cv_data['file_name']}")
            
            # Check if content is empty
            if not cv_data["content"].strip():
                print("Warning: CV content is empty")
                raise ValueError("Empty CV content")

            # Invoke LLM
            chain = self.prompt | self.llm
            result = chain.invoke({"cv_text": cv_data["content"]})
            
            # Parse JSON response
            try:
                extracted_info = json.loads(result.content)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw LLM response: {result.content}")
                raise

            # Validate structure
            if not self.validate_extracted_info(extracted_info):
                raise ValueError("Invalid extracted info structure")

            # Set the extracted info
            cv_data["extracted_info"] = extracted_info
            
            # Log success with some stats
            print(f"Successfully extracted info from {cv_data['file_name']}:")
            print(f"- Found {len(extracted_info['skills'])} skills")
            print(f"- Found {len(extracted_info['experience'])} experience items")
            print(f"- Found {len(extracted_info['education'])} education items")
            
        except Exception as e:
            print(f"Error processing {cv_data['file_name']}: {str(e)}")
            # Provide a valid default structure
            cv_data["extracted_info"] = {
                "skills": [],
                "experience": [],
                "education": [],
                "profile_summary": f"Error extracting information: {str(e)}"
            }
            
        return cv_data

class CandidateRankerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert candidate evaluator. Compare the candidate's profile against the job 
requirements and provide a score from 0-100 along with a brief explanation of the match.
Format your response as a JSON object:
{{
    "score": 85,
    "explanation": "Detailed explanation here"
}}"""),
            ("human", "Job Requirements: {job_requirements}\nCandidate Profile: {candidate_profile}")
        ])

    def process(self, cv_data: CVData, job_requirements: JobRequirements) -> CVData:
        chain = self.prompt | self.llm
        result = chain.invoke({
            "job_requirements": json.dumps(job_requirements),
            "candidate_profile": json.dumps(cv_data["extracted_info"])
        })
        try:
            ranking_result = json.loads(result.content)
            cv_data["score"] = float(ranking_result["score"])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing ranking result: {e}")
            cv_data["score"] = 0.0
        return cv_data

class UserQueryAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at refining candidate searches based on user queries. 
Analyze the query and adjust candidate rankings accordingly. Return a JSON object with the explanation:
{{
    "explanation": "Explanation of ranking adjustment"
}}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{query}")
        ])
        self.chat_history = []

    def process(self, query: str, candidates: List[CVData]) -> List[CVData]:
        self.chat_history.append(HumanMessage(content=query))
        chain = self.prompt | self.llm
        result = chain.invoke({
            "chat_history": self.chat_history,
            "query": query
        })
        try:
            response = json.loads(result.content)
            self.chat_history.append(AIMessage(content=response["explanation"]))
        except json.JSONDecodeError as e:
            print(f"Error parsing query response: {e}")
            self.chat_history.append(AIMessage(content=result.content))
        
        return sorted(candidates, key=lambda x: x["score"] or 0, reverse=True)

class OutputFormatterAgent:
    def __init__(self, output_format: str = "text"):
        self.output_format = output_format

    def process(self, candidates: List[CVData]) -> str:
        if self.output_format == "text":
            output = "Ranked Candidates:\n\n"
            for i, candidate in enumerate(candidates, 1):
                output += f"{i}. {candidate['file_name']} (Score: {candidate['score']})\n"
                if candidate['extracted_info']:
                    output += f"   Skills: {', '.join(candidate['extracted_info'].get('skills', []))}\n"
                    output += f"   Experience: {', '.join(candidate['extracted_info'].get('experience', []))}\n"
                output += "-" * 50 + "\n"
            return output
        # Add more format options as needed
        return "Unsupported format" 