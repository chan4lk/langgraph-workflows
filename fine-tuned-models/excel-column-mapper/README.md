# Generate Synthetic Data

If you don't have your own labeled sentiment data, you can generate synthetic service desk ticket data:

```bash
uv run generate.py
```


## MLX Train

```bash
uv add mlx_lm
```

```bash
uv run mlx_lm.lora --model microsoft/Phi-3-mini-4k-instruct --train --data ./data --iters 1000
uv run mlx_lm.lora --model Qwen/Qwen3-0.6B-MLX-4bit --train --data ./data --iters 1000 --batch-size 1 --max-seq-length 1024 --num-layers 2 --fine-tune-type lora
```

## MLX Evaluate

```bash
uv run mlx_lm.generate --model Qwen/Qwen3-0.6B-MLX-4bit --adapter-path ./adapters --max-token 2048 --prompt "Map the following column names from a provider facility spreadsheet to the standard Healthfirst schema:\n\nInput columns: ['ListInTheHfDirectory', 'LevelOfCare18', 'PrimarySpecialty', 'FridayFrom', 'EmailAddress', 'PointOfContact', 'NpiNumber', 'FridayTo', 'DseFacilityRequestType', 'LevelOfCare25', 'City', 'Language4', 'Telephone', 'LevelOfCare19', 'LevelOfCare7', 'Corporation/GroupPayToName', 'MigrationFlag', 'RowNumber']\n\nStandard schema categories and columns:\n{\n  \"request_info\": [\n    \"DSE Facility Request Type\",\n    \"Effective Date\",\n    \"Healthfirst Provider ID\"\n  ],\n  \"facility_basic\": [\n    \"Facility Type\",\n    \"Facility Name\",\n    \"Medicare Number\",\n    \"Medicaid Number\",\n    \"NPI\",\n    \"TIN\",\n    \"Taxonomy\"\n  ],\n  \"location\": [\n    \"Practice Name\",\n    \"Street Address\",\n    \"City\",\n    \"State\",\n    \"Zip Code\",\n    \"County\",\n    \"Phone\",\n    \"Fax\"\n  ],\n  \"contact\": [\n    \"Primary Contact Name\",\n    \"Primary Contact Email\"\n  ],\n  \"hospital_affiliation\": [\n    \"In-Network Hospital Name\"\n  ],\n  \"office_hours\": [\n    \"Monday From\",\n    \"Monday To\",\n    \"Tuesday From\",\n    \"Tuesday To\",\n    \"Wednesday From\",\n    \"Wednesday To\",\n    \"Thursday From\",\n    \"Thursday To\",\n    \"Friday From\",\n    \"Friday To\",\n    \"Saturday From\",\n    \"Saturday To\",\n    \"Sunday From\",\n    \"Sunday To\"\n  ],\n  \"directory_info\": [\n    \"List in the HF Directory\",\n    \"Language 1\",\n    \"Language 2\",\n    \"Language 3\",\n    \"Language 4\",\n    \"Language 5\",\n    \"Age Range\",\n    \"Handicap Access\",\n    \"Primary Specialty\",\n    \"Secondary Specialty\"\n  ],\n  \"remittance\": [\n    \"Corporation / Group Pay To Name\",\n    \"Remittance Street Address\",\n    \"Remittance City\",\n    \"Remittance State\",\n    \"Remittance Zip Code\"\n  ],\n  \"behavioral_health\": [\n    \"Level of Care 1\",\n    \"Level of Care 2\",\n    \"Level of Care 3\",\n    \"Level of Care 4\",\n    \"Level of Care 5\",\n    \"Level of Care 6\",\n    \"Level of Care 7\",\n    \"Level of Care 8\",\n    \"Level of Care 9\",\n    \"Level of Care 10\",\n    \"Level of Care 11\",\n    \"Level of Care 12\",\n    \"Level of Care 13\",\n    \"Level of Care 14\",\n    \"Level of Care 15\",\n    \"Level of Care 16\",\n    \"Level of Care 17\",\n    \"Level of Care 18\",\n    \"Level of Care 19\",\n    \"Level of Care 20\",\n    \"Level of Care 21\",\n    \"Level of Care 22\",\n    \"Level of Care 23\",\n    \"Level of Care 24\",\n    \"Level of Care 25\"\n  ],\n  \"termination\": [\n    \"Termination Reason\"\n  ]\n}\n\nProvide a JSON mapping where keys are input column names and values are the corresponding standard schema column names. Only include mappings for columns that have clear matches."

```

``````bash
uv run mlx_lm.generate --model Qwen/Qwen3-0.6B-MLX-4bit --max-token 2048 --prompt "Map the following column names from a provider facility spreadsheet to the standard Healthfirst schema:\n\nInput columns: ['ListInTheHfDirectory', 'LevelOfCare18', 'PrimarySpecialty', 'FridayFrom', 'EmailAddress', 'PointOfContact', 'NpiNumber', 'FridayTo', 'DseFacilityRequestType', 'LevelOfCare25', 'City', 'Language4', 'Telephone', 'LevelOfCare19', 'LevelOfCare7', 'Corporation/GroupPayToName', 'MigrationFlag', 'RowNumber']\n\nStandard schema categories and columns:\n{\n  \"request_info\": [\n    \"DSE Facility Request Type\",\n    \"Effective Date\",\n    \"Healthfirst Provider ID\"\n  ],\n  \"facility_basic\": [\n    \"Facility Type\",\n    \"Facility Name\",\n    \"Medicare Number\",\n    \"Medicaid Number\",\n    \"NPI\",\n    \"TIN\",\n    \"Taxonomy\"\n  ],\n  \"location\": [\n    \"Practice Name\",\n    \"Street Address\",\n    \"City\",\n    \"State\",\n    \"Zip Code\",\n    \"County\",\n    \"Phone\",\n    \"Fax\"\n  ],\n  \"contact\": [\n    \"Primary Contact Name\",\n    \"Primary Contact Email\"\n  ],\n  \"hospital_affiliation\": [\n    \"In-Network Hospital Name\"\n  ],\n  \"office_hours\": [\n    \"Monday From\",\n    \"Monday To\",\n    \"Tuesday From\",\n    \"Tuesday To\",\n    \"Wednesday From\",\n    \"Wednesday To\",\n    \"Thursday From\",\n    \"Thursday To\",\n    \"Friday From\",\n    \"Friday To\",\n    \"Saturday From\",\n    \"Saturday To\",\n    \"Sunday From\",\n    \"Sunday To\"\n  ],\n  \"directory_info\": [\n    \"List in the HF Directory\",\n    \"Language 1\",\n    \"Language 2\",\n    \"Language 3\",\n    \"Language 4\",\n    \"Language 5\",\n    \"Age Range\",\n    \"Handicap Access\",\n    \"Primary Specialty\",\n    \"Secondary Specialty\"\n  ],\n  \"remittance\": [\n    \"Corporation / Group Pay To Name\",\n    \"Remittance Street Address\",\n    \"Remittance City\",\n    \"Remittance State\",\n    \"Remittance Zip Code\"\n  ],\n  \"behavioral_health\": [\n    \"Level of Care 1\",\n    \"Level of Care 2\",\n    \"Level of Care 3\",\n    \"Level of Care 4\",\n    \"Level of Care 5\",\n    \"Level of Care 6\",\n    \"Level of Care 7\",\n    \"Level of Care 8\",\n    \"Level of Care 9\",\n    \"Level of Care 10\",\n    \"Level of Care 11\",\n    \"Level of Care 12\",\n    \"Level of Care 13\",\n    \"Level of Care 14\",\n    \"Level of Care 15\",\n    \"Level of Care 16\",\n    \"Level of Care 17\",\n    \"Level of Care 18\",\n    \"Level of Care 19\",\n    \"Level of Care 20\",\n    \"Level of Care 21\",\n    \"Level of Care 22\",\n    \"Level of Care 23\",\n    \"Level of Care 24\",\n    \"Level of Care 25\"\n  ],\n  \"termination\": [\n    \"Termination Reason\"\n  ]\n}\n\nProvide a JSON mapping where keys are input column names and values are the corresponding standard schema column names. Only include mappings for columns that have clear matches."

## merge model
```bash
uv run mlx_lm.fuse --model Qwen/Qwen3-0.6B-MLX-4bit
```

## Upload to Huggingface

```bash
huggingface-cli upload chan4lk/excel-column-mapper /Users/chandima/repos/langgraph-workflows/fine-tuned-models/excel-column-mapper/fused_model 
```

```bash
source venv/bin/activate
python convert_hf_to_gguf.py \
  /Users/chandima/repos/langgraph-workflows/fine-tuned-models/excel-column-mapper/fused_model/ \
  --outfile /Users/chandima/repos/langgraph-workflows/fine-tuned-models/excel-column-mapper/gguf/excel-column-mapper-mps.gguf \
  --outtype f16 # Or f32, q8_0, q4_k_m etc.
```

## Create ollama model
```bash
ollama create excel-column-mapper -f Modelfile
```

## Run ollama model
```bash
ollama run excel-column-mapper "Map the following column names from a provider facility spreadsheet to the standard Healthfirst schema:\n\nInput columns: ['ListInTheHfDirectory', 'LevelOfCare18', 'PrimarySpecialty', 'FridayFrom', 'EmailAddress', 'PointOfContact', 'NpiNumber', 'FridayTo', 'DseFacilityRequestType', 'LevelOfCare25', 'City', 'Language4', 'Telephone', 'LevelOfCare19', 'LevelOfCare7', 'Corporation/GroupPayToName', 'MigrationFlag', 'RowNumber']\n\nStandard schema categories and columns:\n{\n  \"request_info\": [\n    \"DSE Facility Request Type\",\n    \"Effective Date\",\n    \"Healthfirst Provider ID\"\n  ],\n  \"facility_basic\": [\n    \"Facility Type\",\n    \"Facility Name\",\n    \"Medicare Number\",\n    \"Medicaid Number\",\n    \"NPI\",\n    \"TIN\",\n    \"Taxonomy\"\n  ],\n  \"location\": [\n    \"Practice Name\",\n    \"Street Address\",\n    \"City\",\n    \"State\",\n    \"Zip Code\",\n    \"County\",\n    \"Phone\",\n    \"Fax\"\n  ],\n  \"contact\": [\n    \"Primary Contact Name\",\n    \"Primary Contact Email\"\n  ],\n  \"hospital_affiliation\": [\n    \"In-Network Hospital Name\"\n  ],\n  \"office_hours\": [\n    \"Monday From\",\n    \"Monday To\",\n    \"Tuesday From\",\n    \"Tuesday To\",\n    \"Wednesday From\",\n    \"Wednesday To\",\n    \"Thursday From\",\n    \"Thursday To\",\n    \"Friday From\",\n    \"Friday To\",\n    \"Saturday From\",\n    \"Saturday To\",\n    \"Sunday From\",\n    \"Sunday To\"\n  ],\n  \"directory_info\": [\n    \"List in the HF Directory\",\n    \"Language 1\",\n    \"Language 2\",\n    \"Language 3\",\n    \"Language 4\",\n    \"Language 5\",\n    \"Age Range\",\n    \"Handicap Access\",\n    \"Primary Specialty\",\n    \"Secondary Specialty\"\n  ],\n  \"remittance\": [\n    \"Corporation / Group Pay To Name\",\n    \"Remittance Street Address\",\n    \"Remittance City\",\n    \"Remittance State\",\n    \"Remittance Zip Code\"\n  ],\n  \"behavioral_health\": [\n    \"Level of Care 1\",\n    \"Level of Care 2\",\n    \"Level of Care 3\",\n    \"Level of Care 4\",\n    \"Level of Care 5\",\n    \"Level of Care 6\",\n    \"Level of Care 7\",\n    \"Level of Care 8\",\n    \"Level of Care 9\",\n    \"Level of Care 10\",\n    \"Level of Care 11\",\n    \"Level of Care 12\",\n    \"Level of Care 13\",\n    \"Level of Care 14\",\n    \"Level of Care 15\",\n    \"Level of Care 16\",\n    \"Level of Care 17\",\n    \"Level of Care 18\",\n    \"Level of Care 19\",\n    \"Level of Care 20\",\n    \"Level of Care 21\",\n    \"Level of Care 22\",\n    \"Level of Care 23\",\n    \"Level of Care 24\",\n    \"Level of Care 25\"\n  ],\n  \"termination\": [\n    \"Termination Reason\"\n  ]\n}\n\nProvide a JSON mapping where keys are input column names and values are the corresponding standard schema column names. Only include mappings for columns that have clear matches."