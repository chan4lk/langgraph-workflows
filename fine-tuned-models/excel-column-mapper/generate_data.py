import pandas as pd
import numpy as np
import json
import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import uuid
import os

OUTPUT_DIR = "data/jsonl"
TRAIN_FILENAME = "train_messages.jsonl"
VALID_FILENAME = "valid_messages.jsonl"
TEST_FILENAME = "test_messages.jsonl"

# Define split ratios (adjust if needed)
TRAIN_RATIO = 0.70
VALID_RATIO = 0.15


class SyntheticColumnMappingDataGenerator:
    def __init__(self):
        # Define the target schema based on your PLM_FR_DSE_Facility_Roster structure
        self.target_schema = {
            'request_info': [
                'DSE Facility Request Type',
                'Effective Date',
                'Healthfirst Provider ID'
            ],
            'facility_basic': [
                'Facility Type',
                'Facility Name',
                'Medicare Number',
                'Medicaid Number',
                'NPI',
                'TIN',
                'Taxonomy'
            ],
            'location': [
                'Practice Name',
                'Street Address',
                'City',
                'State',
                'Zip Code',
                'County',
                'Phone',
                'Fax'
            ],
            'contact': [
                'Primary Contact Name',
                'Primary Contact Email'
            ],
            'hospital_affiliation': [
                'In-Network Hospital Name'
            ],
            'office_hours': [
                'Monday From', 'Monday To',
                'Tuesday From', 'Tuesday To',
                'Wednesday From', 'Wednesday To',
                'Thursday From', 'Thursday To',
                'Friday From', 'Friday To',
                'Saturday From', 'Saturday To',
                'Sunday From', 'Sunday To'
            ],
            'directory_info': [
                'List in the HF Directory',
                'Language 1', 'Language 2', 'Language 3', 'Language 4', 'Language 5',
                'Age Range',
                'Handicap Access',
                'Primary Specialty',
                'Secondary Specialty'
            ],
            'remittance': [
                'Corporation / Group Pay To Name',
                'Remittance Street Address',
                'Remittance City',
                'Remittance State',
                'Remittance Zip Code'
            ],
            'behavioral_health': [
                f'Level of Care {i}' for i in range(1, 26)
            ],
            'termination': [
                'Termination Reason'
            ]
        }
        
        # Common variations and synonyms for column names
        self.column_variations = {
            'DSE Facility Request Type': [
                'Request Type', 'Facility Request', 'Action Type', 'Operation Type',
                'Request Category', 'Change Type', 'Modification Type'
            ],
            'Effective Date': [
                'Date', 'Start Date', 'Begin Date', 'Activation Date',
                'Implementation Date', 'Go Live Date', 'Valid From'
            ],
            'Healthfirst Provider ID': [
                'Provider ID', 'HF Provider ID', 'Provider Number',
                'HF ID', 'Provider Code', 'Internal ID', 'System ID'
            ],
            'Facility Name': [
                'Name', 'Practice Name', 'Clinic Name', 'Hospital Name',
                'Organization Name', 'Entity Name', 'Business Name'
            ],
            'NPI': [
                'National Provider Identifier', 'Provider NPI', 'NPI Number',
                'National Provider ID', 'Provider Identifier'
            ],
            'TIN': [
                'Tax ID', 'Tax Identification Number', 'Federal Tax ID',
                'EIN', 'Employer ID', 'Tax Number'
            ],
            'Street Address': [
                'Address', 'Address Line 1', 'Street', 'Physical Address',
                'Location Address', 'Primary Address', 'Mailing Address'
            ],
            'Phone': [
                'Phone Number', 'Telephone', 'Contact Number', 'Primary Phone',
                'Business Phone', 'Office Phone', 'Main Phone'
            ],
            'Primary Contact Name': [
                'Contact Name', 'Contact Person', 'Primary Contact',
                'Main Contact', 'Representative', 'Point of Contact'
            ],
            'Primary Contact Email': [
                'Email', 'Contact Email', 'Email Address',
                'Primary Email', 'Business Email', 'Contact Email Address'
            ]
        }
        
        # Different naming conventions
        self.naming_conventions = [
            'snake_case',
            'camelCase', 
            'PascalCase',
            'kebab-case',
            'UPPER_CASE',
            'Title Case',
            'lowercase',
            'Sentence case'
        ]
        
        # System message for column mapping
        self.system_message = "You are an expert healthcare data integration specialist. Your task is to analyze column names from provider facility spreadsheets and map them to the standard Healthfirst schema. You understand medical terminology, various naming conventions, and can handle abbreviations and variations in column names."
        
    def apply_naming_convention(self, text: str, convention: str) -> str:
        """Apply different naming conventions to column names"""
        if convention == 'snake_case':
            return text.lower().replace(' ', '_').replace('-', '_')
        elif convention == 'camelCase':
            words = text.split()
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif convention == 'PascalCase':
            return ''.join(word.capitalize() for word in text.split())
        elif convention == 'kebab-case':
            return text.lower().replace(' ', '-').replace('_', '-')
        elif convention == 'UPPER_CASE':
            return text.upper().replace(' ', '_').replace('-', '_')
        elif convention == 'Title Case':
            return text.title()
        elif convention == 'lowercase':
            return text.lower()
        elif convention == 'Sentence case':
            return text.capitalize()
        return text
    
    def generate_column_variations(self, base_columns: List[str], num_variations: int = 5) -> List[Dict]:
        """Generate different variations of column names"""
        variations = []
        
        for _ in range(num_variations):
            variant_columns = {}
            convention = random.choice(self.naming_conventions)
            
            for col in base_columns:
                # Sometimes use exact match, sometimes use variations
                if col in self.column_variations and random.random() < 0.7:
                    variant_name = random.choice(self.column_variations[col])
                else:
                    variant_name = col
                
                # Apply naming convention
                final_name = self.apply_naming_convention(variant_name, convention)
                variant_columns[final_name] = col
            
            # Add some noise columns
            noise_columns = [
                'ID', 'Record_ID', 'Row_Number', 'Created_Date', 'Modified_Date',
                'Status', 'Notes', 'Comments', 'Internal_Use', 'Reserved',
                'Temp_Field', 'Legacy_ID', 'Migration_Flag', 'Validation_Status'
            ]
            
            for _ in range(random.randint(2, 5)):
                noise_col = random.choice(noise_columns)
                noise_col = self.apply_naming_convention(noise_col, convention)
                if noise_col not in variant_columns:
                    variant_columns[noise_col] = None  # No mapping for noise columns
            
            variations.append({
                'columns': variant_columns,
                'convention': convention,
                'schema_id': str(uuid.uuid4())
            })
        
        return variations
    
    def generate_training_examples(self, num_examples: int = 1000) -> List[Dict]:
        """Generate training examples for column mapping in messages format"""
        training_data = []
        
        # Get all target columns
        all_target_columns = []
        for category, columns in self.target_schema.items():
            all_target_columns.extend(columns)
        
        for i in range(num_examples):
            # Randomly select a subset of target columns
            num_cols = random.randint(10, min(30, len(all_target_columns)))
            selected_columns = random.sample(all_target_columns, num_cols)
            
            # Generate variations for these columns
            variations = self.generate_column_variations(selected_columns, 1)[0]
            
            # Create the training example
            input_columns = list(variations['columns'].keys())
            
            # Create mapping
            column_mapping = {}
            for input_col, target_col in variations['columns'].items():
                if target_col:  # Skip noise columns
                    column_mapping[input_col] = target_col
            
            # Create user message
            user_content = f"""Map the following column names from a provider facility spreadsheet to the standard Healthfirst schema:

Input columns: {input_columns}

Standard schema categories and columns:
{json.dumps(self.target_schema, indent=2)}

Provide a JSON mapping where keys are input column names and values are the corresponding standard schema column names. Only include mappings for columns that have clear matches."""

            # Create assistant response
            assistant_content = json.dumps(column_mapping, indent=2)
            
            # Create messages format
            messages = [
                {
                    "role": "system",
                    "content": self.system_message
                },
                {
                    "role": "user", 
                    "content": user_content
                },
                {
                    "role": "assistant",
                    "content": assistant_content
                }
            ]
            
            training_data.append({
                "messages": messages
            })
        
        return training_data
    
    def generate_complex_scenarios(self, num_examples: int = 200) -> List[Dict]:
        """Generate complex scenarios with partial matches, abbreviations, etc."""
        complex_data = []
        
        # Define complex transformations
        transformations = {
            'abbreviations': {
                'Street Address': ['St Addr', 'Str Add', 'Address St'],
                'Phone Number': ['Ph', 'Tel', 'Phone #'],
                'Email Address': ['Email Addr', 'E-mail', 'Email Add'],
                'Zip Code': ['Zip', 'Postal Code', 'ZIP'],
                'Tax Identification Number': ['Tax ID', 'TIN', 'Fed Tax ID']
            },
            'prefixes_suffixes': {
                'prefixes': ['Primary_', 'Main_', 'Default_', 'Current_', 'Active_'],
                'suffixes': ['_Primary', '_Main', '_Current', '_1', '_Info']
            },
            'medical_specific': {
                'NPI': ['National_Provider_Identifier', 'Provider_NPI', 'NPI_Number'],
                'Taxonomy': ['Provider_Taxonomy', 'Specialty_Code', 'Tax_Code'],
                'Medicare Number': ['Medicare_ID', 'Medicare_Num', 'CMS_Number'],
                'Medicaid Number': ['Medicaid_ID', 'Medicaid_Num', 'State_ID']
            }
        }
        
        for i in range(num_examples):
            # Start with a base set of columns
            base_columns = random.sample(list(self.target_schema['facility_basic']) + 
                                       list(self.target_schema['location']) +
                                       list(self.target_schema['contact']), 
                                       random.randint(8, 15))
            
            variant_columns = {}
            
            for col in base_columns:
                # Apply various transformations
                transformed_col = col
                
                # Abbreviations
                if col in transformations['abbreviations']:
                    if random.random() < 0.3:
                        transformed_col = random.choice(transformations['abbreviations'][col])
                
                # Medical specific
                if col in transformations['medical_specific']:
                    if random.random() < 0.4:
                        transformed_col = random.choice(transformations['medical_specific'][col])
                
                # Add prefixes/suffixes
                if random.random() < 0.2:
                    prefix = random.choice(transformations['prefixes_suffixes']['prefixes'])
                    transformed_col = prefix + transformed_col.replace(' ', '_')
                elif random.random() < 0.2:
                    suffix = random.choice(transformations['prefixes_suffixes']['suffixes'])
                    transformed_col = transformed_col.replace(' ', '_') + suffix
                
                # Apply naming convention
                convention = random.choice(self.naming_conventions)
                final_col = self.apply_naming_convention(transformed_col, convention)
                
                variant_columns[final_col] = col
            
            # Add some completely unrelated columns
            unrelated = ['Internal_Notes', 'Legacy_System_ID', 'Migration_Status', 
                        'Data_Quality_Score', 'Last_Updated_By', 'Approval_Status']
            for _ in range(random.randint(1, 3)):
                unrelated_col = random.choice(unrelated)
                if unrelated_col not in variant_columns:
                    variant_columns[unrelated_col] = None
            
            input_columns = list(variant_columns.keys())
            column_mapping = {k: v for k, v in variant_columns.items() if v is not None}
            
            # Create user message for complex scenario
            user_content = f"""Analyze these column names from a healthcare provider data file and map them to the standard schema. Handle medical abbreviations, naming variations, and prefixes/suffixes appropriately:

Input columns: {input_columns}

Standard schema:
{json.dumps(self.target_schema, indent=2)}

Return a JSON mapping of input columns to standard schema columns. Only include clear matches and handle medical terminology correctly."""

            assistant_content = json.dumps(column_mapping, indent=2)
            
            # Create messages format
            messages = [
                {
                    "role": "system",
                    "content": self.system_message
                },
                {
                    "role": "user",
                    "content": user_content
                },
                {
                    "role": "assistant", 
                    "content": assistant_content
                }
            ]
            
            complex_data.append({
                "messages": messages
            })
        
        return complex_data
    
    def save_training_data(self, filename: str = 'data/data.jsonl'):
        """Generate and save all training data in messages format"""
        print("Generating basic training examples...")
        basic_examples = self.generate_training_examples(800)
        
        print("Generating complex scenarios...")
        complex_examples = self.generate_complex_scenarios(200)
        
        all_examples = basic_examples + complex_examples
        random.shuffle(all_examples)
        
        num_train = int(len(all_examples) * TRAIN_RATIO)
        num_valid = int(len(all_examples) * VALID_RATIO)
        train_records = all_examples[:num_train]
        valid_records = all_examples[num_train : num_train + num_valid]
        test_records = all_examples[num_train + num_valid :]
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        self.write_jsonl(filepath=os.path.join(OUTPUT_DIR, TRAIN_FILENAME), records=train_records)
        self.write_jsonl(filepath=os.path.join(OUTPUT_DIR, VALID_FILENAME), records=valid_records)
        self.write_jsonl(filepath=os.path.join(OUTPUT_DIR, TEST_FILENAME), records=test_records)


        print(f"Generated {len(all_examples)} training examples")
        print(f"Saved to {filename}")
        
        # Also save a sample for inspection
        sample_file = filename.replace('.jsonl', '_sample.json')
        with open(sample_file, 'w') as f:
            json.dump(all_examples[:10], f, indent=2)
        
        print(f"Sample data saved to {sample_file}")
        
        return all_examples

    def write_jsonl(self, filepath: str, records: List[Dict]):
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in records:
                json.dump(record, f, ensure_ascii=False)
                f.write('\n')

