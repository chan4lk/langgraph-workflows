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
```

## MLX Evaluate

```bash
uv run mlx_lm.generate --model microsoft/Phi-3-mini-4k-instruct --adapter-path ./adapters --max-token 2048 --prompt "<|user|>\nClassify the sentiment (Positive, Negative, or Neutral) for this ServiceNow ticket text:\nRequesting access to Outlook for new user Marc Crawford.<|end|>"
```


## without adaptors
```bash
uv run mlx_lm.generate --model microsoft/Phi-3-mini-4k-instruct --max-token 2048 --prompt "<|user|>\nClassify the sentiment (Positive, Negative, or Neutral) for this ServiceNow ticket text:\nRequesting access to Outlook for new user Marc Crawford.<|end|>"
```

## merge model
```bash
uv run mlx_lm.fuse --model microsoft/Phi-3-mini-4k-instruct
```


## Convert to gguf

```bash
source venv/bin/activate
python convert_hf_to_gguf.py \
  /Users/chandima/repos/sentiment-analysis-model/fused_model/ \
  --outfile /Users/chandima/repos/sentiment-analysis-model/gguf/sentiment-finetuned-mps.gguf \
  --outtype f16 # Or f32, q8_0, q4_k_m etc.
```

## Create ollama model
```bash
ollama create phi3ft -f Modelfile
```

## Run ollama model
```bash
ollama run phi3ft "<|user|>\nClassify the sentiment (Positive, Negative, or Neutral) for this ServiceNow ticket text:\nRequesting access to Outlook for new user Marc Crawford.<|end|>" 
```