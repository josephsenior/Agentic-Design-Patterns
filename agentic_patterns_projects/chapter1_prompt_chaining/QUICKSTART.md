# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
cd chapter1_prompt_chaining
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run the Example

```bash
python example.py
```

Or use it in your own code:

```python
from document_analyzer import DocumentAnalyzer

# Initialize the analyzer
analyzer = DocumentAnalyzer()

# Analyze a document
document = "Your document text here..."
result = analyzer.analyze(document)

print(result)
```

## Understanding the Pipeline

The Document Analysis Pipeline uses **Prompt Chaining** to process documents through 4 sequential steps:

```
┌─────────────────┐
│  Input Document │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Step 1: Extract Info    │ ← Focused on information extraction
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Step 2: Identify        │ ← Uses Step 1 output
│        Entities         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Step 3: Generate        │ ← Uses Steps 1 & 2 outputs
│        Summary          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Step 4: Structure JSON  │ ← Uses all previous outputs
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Structured Output      │
└─────────────────────────┘
```

## Key Benefits of Prompt Chaining

1. **Modularity**: Each step has a single, focused responsibility
2. **Debuggability**: You can inspect intermediate results
3. **Reliability**: Smaller, focused prompts are more reliable than one large prompt
4. **Flexibility**: Easy to modify or replace individual steps

## Example Output

```json
{
  "summary": "Apple Inc. announced the iPhone 15 Pro Max in September 2023...",
  "entities": {
    "people": ["Tim Cook"],
    "organizations": ["Apple Inc."],
    "locations": ["Cupertino, California"],
    "dates": ["September 2023", "September 22, 2023"],
    "concepts": ["iPhone", "A17 Pro chip", "sustainability"]
  },
  "key_facts": [
    "iPhone 15 Pro Max starts at $1,199",
    "100% recycled aluminum used"
  ],
  "main_topics": [
    "Product Launch",
    "Sustainability",
    "Technology"
  ]
}
```

## Advanced Usage

### Step-by-Step Analysis

See intermediate results from each step:

```python
results = analyzer.analyze_step_by_step(document)
print(results["step1_extraction"])  # Raw extraction
print(results["step2_entities"])    # Entity identification
print(results["step3_summary"])     # Generated summary
print(results["final_json"])        # Structured output
```

### Custom Configuration

```python
analyzer = DocumentAnalyzer(
    model_name="gpt-4",      # Use GPT-4 instead of GPT-3.5
    temperature=0.3,          # Slightly more creative
    api_key="your-key"        # Custom API key
)
```

## Troubleshooting

**Error: "OpenAI API key is required"**
- Make sure you've created a `.env` file
- Verify `OPENAI_API_KEY` is set correctly
- Check that `python-dotenv` is installed

**Error: "Failed to parse JSON"**
- The LLM might have returned extra text
- Check the `raw_output` field in the error response
- Try using `analyze_step_by_step()` to debug

**Rate Limit Errors**
- You may be hitting OpenAI API rate limits
- Add delays between requests
- Consider using a different model or upgrading your plan

## Next Steps

- Modify the prompts in `document_analyzer.py` to suit your needs
- Add new steps to the pipeline
- Integrate with your own document sources
- Experiment with different models and temperatures

