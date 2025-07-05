import pandas as pd
import numpy as np
import json
import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import uuid
import os

OUTPUT_DIR = "data"
TRAIN_FILENAME = "train.jsonl"
VALID_FILENAME = "valid.jsonl"
TEST_FILENAME = "test.jsonl"

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
        if not text.strip():
            return text
            
        # First normalize to words
        words = []
        current_word = []
        
        # Split by common delimiters and handle case changes
        for char in text.replace('_', ' ').replace('-', ' ').replace('.', ' '):
            if char.isupper() and current_word and not current_word[-1].isupper():
                words.append(''.join(current_word))
                current_word = [char]
            elif char == ' ' and current_word:
                words.append(''.join(current_word))
                current_word = []
            else:
                current_word.append(char)
        
        if current_word:
            words.append(''.join(current_word))
        
        # Filter out empty strings and normalize case
        words = [w.strip().lower() for w in words if w.strip()]
        
        if not words:
            return text
            
        # Apply convention
        if convention == 'snake_case':
            return '_'.join(words)
        elif convention == 'camelCase':
            return words[0] + ''.join(w.capitalize() for w in words[1:])
        elif convention == 'PascalCase':
            return ''.join(w.capitalize() for w in words)
        elif convention == 'kebab-case':
            return '-'.join(words)
        elif convention == 'UPPER_CASE':
            return '_'.join(w.upper() for w in words)
        elif convention == 'Title Case':
            return ' '.join(w.capitalize() for w in words)
        elif convention == 'lowercase':
            return ' '.join(words).lower()
        elif convention == 'Sentence case':
            return ' '.join(words).capitalize()
        else:
            # Default to original text if convention not recognized
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
    
    def _get_schema_section_description(self, section_name: str) -> str:
        """Get a human-readable description of a schema section"""
        descriptions = {
            'facility_basic': 'Basic facility information (names, IDs, numbers)',
            'location': 'Location and contact information',
            'contact': 'Primary contact details',
            'request_info': 'Request metadata',
            'hospital_affiliation': 'Hospital affiliation details',
            'office_hours': 'Operating hours (e.g., Monday_From, Monday_To)',
            'directory_info': 'Directory listing information',
            'remittance': 'Billing and payment details',
            'behavioral_health': 'Behavioral health service levels (Level_of_Care_1 to Level_of_Care_25)',
            'termination': 'Termination information'
        }
        return descriptions.get(section_name, section_name)

    def _get_abbreviated_schema(self, columns: List[str]) -> Dict[str, List[str]]:
        """Get an abbreviated schema containing only the relevant sections"""
        abbreviated = {}
        
        # Determine which sections are relevant
        relevant_sections = set()
        for col in columns:
            for section, fields in self.target_schema.items():
                if any(field.lower() in col.lower() for field in fields):
                    relevant_sections.add(section)
        
        # Include the most common sections if no matches found
        if not relevant_sections:
            relevant_sections = {'facility_basic', 'location', 'contact'}
        
        # Build the abbreviated schema
        for section in relevant_sections:
            if section in self.target_schema:
                abbreviated[section] = self.target_schema[section]
        
        return abbreviated

    def _generate_column_variation(self, col: str, transformations: Dict) -> str:
        """Generate a single column variation with transformations"""
        transformed_col = col
        
        # Apply transformations with decreasing probability
        if col in transformations['abbreviations'] and random.random() < 0.3:
            transformed_col = random.choice(transformations['abbreviations'][col])
        
        if col in transformations['medical_specific'] and random.random() < 0.4:
            transformed_col = random.choice(transformations['medical_specific'][col])
        
        if random.random() < 0.2:
            prefix = random.choice(transformations['prefixes_suffixes']['prefixes'])
            transformed_col = prefix + transformed_col.replace(' ', '_')
        elif random.random() < 0.2:
            suffix = random.choice(transformations['prefixes_suffixes']['suffixes'])
            transformed_col = transformed_col.replace(' ', '_') + suffix
        
        return transformed_col

    def generate_complex_scenarios(self, num_examples: int = 200):
        """Generate complex scenarios with partial matches, abbreviations, etc."""
        complex_data = []
        
        # Define transformations
        transformations = {
            'abbreviations': {
                'Facility Name': ['Fac Name', 'Facility Nm', 'FAC_NAME', 'fac_nm'],
                'Street Address': ['St Addr', 'Street Addr', 'STRT_ADDR', 'st_addr'],
                'Primary Contact Name': ['PC Name', 'Prim Contact', 'PRI_CONTACT', 'pc_name'],
                'Primary Contact Email': ['PC Email', 'Primary Email', 'PRI_EMAIL', 'pc_email'],
                'Phone': ['Ph', 'Tel', 'PHONE', 'ph'],
                'NPI': ['NPI_Num', 'NPI_Number', 'NPI_NUM', 'npi'],
                'TIN': ['TIN_Num', 'TIN_Number', 'TIN_NUM', 'tin'],
                'Effective Date': ['Eff Date', 'Effective Dt', 'EFF_DT', 'eff_dt']
            },
            'medical_specific': {
                'NPI': ['National Provider ID', 'NPI Number', 'NPI #'],
                'TIN': ['Tax ID', 'Tax Identification Number', 'EIN'],
                'Facility Type': ['Facility Category', 'Provider Type', 'Entity Type'],
                'Medicare Number': ['Medicare ID', 'Medicare #', 'MCR_NUM'],
                'Medicaid Number': ['Medicaid ID', 'Medicaid #', 'MDCD_NUM']
            },
            'prefixes_suffixes': {
                'prefixes': ['hf_', 'hcf_', 'prov_', 'fac_', 'mstr_', 'data_', 'src_'],
                'suffixes': ['_cd', '_id', '_num', '_nm', '_txt', '_dt', '_flag']
            }
        }
        
        # Common unrelated columns to add noise
        unrelated_columns = [
            'Internal_Notes', 'Legacy_System_ID', 'Migration_Status', 
            'Data_Quality_Score', 'Last_Updated_By', 'Approval_Status',
            'Record_Source', 'ETL_Timestamp', 'Source_System', 'Last_Modified_Date',
            'Data_Owner', 'Validation_Status', 'Processing_Date', 'Batch_ID'
        ]

        for _ in range(num_examples):
            # Select a random set of base columns from different schema sections
            section_weights = {
                'facility_basic': 0.7,  # 70% chance to include columns from this section
                'location': 0.8,        # 80% chance
                'contact': 0.6,         # 60% chance
                'request_info': 0.3,    # 30% chance
                'directory_info': 0.4   # 40% chance
            }
            
            base_columns = []
            for section, weight in section_weights.items():
                if random.random() < weight:
                    # Take 1-3 columns from this section
                    cols = random.sample(
                        self.target_schema[section],
                        min(random.randint(1, 3), len(self.target_schema[section]))
                    )
                    base_columns.extend(cols)
            
            # Ensure we have between 8-15 columns total
            if len(base_columns) > 15:
                base_columns = random.sample(base_columns, 15)
            elif len(base_columns) < 8:
                # If we don't have enough columns, add some common ones
                common_columns = [
                    'Facility Name', 'NPI', 'Street Address', 'City', 'State',
                    'Zip Code', 'Phone', 'Primary Contact Name', 'Primary Contact Email'
                ]
                needed = 8 - len(base_columns)
                additional = [c for c in common_columns if c not in base_columns]
                base_columns.extend(random.sample(additional, min(needed, len(additional))))
            
            # Generate variant columns with transformations
            variant_columns = {}
            for col in base_columns:
                # Generate 1-3 variations of each column
                num_variations = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
                variations = set()
                
                # Always include the original column (with naming convention applied)
                convention = random.choice(self.naming_conventions)
                original_variation = self.apply_naming_convention(col, convention)
                variations.add(original_variation)
                
                # Generate additional variations
                for _ in range(num_variations - 1):
                    variation = self._generate_column_variation(col, transformations)
                    convention = random.choice(self.naming_conventions)
                    final_variation = self.apply_naming_convention(variation, convention)
                    variations.add(final_variation)
                
                # Add all variations to our mapping
                for variation in variations:
                    variant_columns[variation] = col
            
            # Add some unrelated columns (noise)
            num_unrelated = random.choices([0, 1, 2, 3], weights=[0.2, 0.5, 0.2, 0.1])[0]
            for _ in range(num_unrelated):
                unrelated_col = random.choice(unrelated_columns)
                if unrelated_col not in variant_columns:
                    variant_columns[unrelated_col] = None
            
            # Prepare input and output
            input_columns = list(variant_columns.keys())
            column_mapping = {k: v for k, v in variant_columns.items() if v is not None}
            
            # Get abbreviated schema for context
            abbreviated_schema = self._get_abbreviated_schema(column_mapping.values())
            
            # Create user message with optimized content
            user_content = (
                "Map these healthcare data columns to the standard schema. "
                "Handle variations, abbreviations, and medical terminology.\n\n"
                f"Input columns: {input_columns}\n\n"
                "Schema sections (with example fields):\n"
            )
            
            # Add schema section descriptions
            for section, fields in abbreviated_schema.items():
                user_content += f"- {self._get_schema_section_description(section)}: {', '.join(fields[:3])}"
                if len(fields) > 3:
                    user_content += f"... ({len(fields)-3} more)"
                user_content += "\n"
            
            user_content += "\nReturn a JSON object mapping input columns to standard schema columns."
            
            # Create assistant response with compact JSON
            assistant_content = json.dumps(column_mapping, separators=(',', ':'))
            
            # Create messages with optimized structure
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
            
            # Add to dataset if within token limits
            total_tokens = sum(len(msg["content"]) for msg in messages) // 4  # Rough estimate
            if total_tokens <= 1000:  # Leave some headroom
                complex_data.append({"messages": messages})
        
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

