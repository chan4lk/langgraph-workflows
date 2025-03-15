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
            ("system", """You are an expert job description analyzer. Extract key information from the job description 
and categorize it into required skills, desired experience, qualifications, and key responsibilities.
Format your response as a JSON object with these exact keys:
{{
    "required_skills": ["skill1", "skill2"],
    "desired_experience": ["exp1", "exp2"],
    "qualifications": ["qual1", "qual2"],
    "key_responsibilities": ["resp1", "resp2"]
}}"""),
            ("human", "{job_description}")
        ])

    def process(self, job_description: str) -> JobRequirements:
        chain = self.prompt | self.llm
        result = chain.invoke({"job_description": job_description})
        try:
            # Parse the JSON string into a Python dictionary
            structured_requirements = json.loads(result.content)
            return JobRequirements(**structured_requirements)
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            # Return empty requirements if parsing fails
            return JobRequirements(
                required_skills=[],
                desired_experience=[],
                qualifications=[],
                key_responsibilities=[]
            )

class CVInformationExtractorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert CV analyzer. Extract key information from the CV text and structure it into 
categories: skills, experience, education, and profile summary. Format your response as a JSON object with these exact keys:
{{
    "skills": ["skill1", "skill2"],
    "experience": ["exp1", "exp2"],
    "education": ["edu1", "edu2"],
    "profile_summary": "brief summary"
}}"""),
            ("human", "{cv_text}")
        ])

    def process(self, cv_data: CVData) -> CVData:
        chain = self.prompt | self.llm
        result = chain.invoke({"cv_text": cv_data["content"]})
        try:
            cv_data["extracted_info"] = json.loads(result.content)
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            cv_data["extracted_info"] = {
                "skills": [],
                "experience": [],
                "education": [],
                "profile_summary": ""
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