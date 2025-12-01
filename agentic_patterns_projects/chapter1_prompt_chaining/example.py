"""
Example usage of the Document Analysis Pipeline

This script demonstrates how to use the prompt chaining-based
document analyzer in various real-world scenarios.
"""

import json
from document_analyzer import DocumentAnalyzer


def example_basic_analysis():
    """Basic document analysis example."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Document Analysis")
    print("=" * 70)
    
    document = """
    Apple Inc. announced its latest iPhone 15 Pro Max at the September 2023 
    event in Cupertino, California. The new device features a titanium design, 
    A17 Pro chip, and advanced camera system. CEO Tim Cook highlighted the 
    device's sustainability features, noting that 100% of the aluminum used 
    is recycled. The phone starts at $1,199 and will be available on 
    September 22, 2023.
    """
    
    analyzer = DocumentAnalyzer()
    result = analyzer.analyze(document)
    
    print("\n📄 Input Document:")
    print(document.strip())
    print("\n📊 Analysis Results:")
    print(json.dumps(result, indent=2))


def example_research_paper():
    """Analyze a research paper abstract."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Research Paper Abstract Analysis")
    print("=" * 70)
    
    document = """
    Title: "Machine Learning Applications in Healthcare: A Comprehensive Review"
    
    Abstract: This paper reviews recent advances in machine learning applications 
    in healthcare. We analyzed 150 peer-reviewed articles published between 2020 
    and 2023. Key findings include improved diagnostic accuracy using deep learning 
    models, with an average improvement of 15% over traditional methods. The study 
    was conducted by researchers at Stanford University and MIT, led by Dr. Jane 
    Smith and Dr. Robert Lee. Applications span radiology, pathology, and drug 
    discovery. The research was funded by the National Institutes of Health (NIH) 
    and published in Nature Medicine in March 2023.
    """
    
    analyzer = DocumentAnalyzer()
    result = analyzer.analyze(document)
    
    print("\n📄 Input Document:")
    print(document.strip())
    print("\n📊 Analysis Results:")
    print(json.dumps(result, indent=2))


def example_step_by_step():
    """Show intermediate results from each step."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Step-by-Step Analysis (Debugging View)")
    print("=" * 70)
    
    document = """
    Microsoft Corporation announced a partnership with OpenAI to integrate 
    ChatGPT into Microsoft Office 365. The announcement was made by CEO Satya 
    Nadella at the company's headquarters in Redmond, Washington on March 16, 2023. 
    This integration will enhance productivity tools like Word, Excel, and PowerPoint 
    with AI-powered features. The partnership represents a $10 billion investment 
    over the next five years.
    """
    
    analyzer = DocumentAnalyzer()
    results = analyzer.analyze_step_by_step(document)
    
    print("\n📄 Input Document:")
    print(document.strip())
    
    print("\n" + "-" * 70)
    print("STEP 1: Information Extraction")
    print("-" * 70)
    print(results["step1_extraction"])
    
    print("\n" + "-" * 70)
    print("STEP 2: Entity Identification")
    print("-" * 70)
    print(results["step2_entities"])
    
    print("\n" + "-" * 70)
    print("STEP 3: Summary Generation")
    print("-" * 70)
    print(results["step3_summary"])
    
    print("\n" + "-" * 70)
    print("STEP 4: Structured Output")
    print("-" * 70)
    print(json.dumps(results["final_json"], indent=2))


def example_batch_processing():
    """Process multiple documents."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Batch Processing Multiple Documents")
    print("=" * 70)
    
    documents = [
        """
        Tesla Inc. reported record vehicle deliveries of 484,507 units in Q3 2023, 
        representing a 38% year-over-year increase. The company, led by CEO Elon Musk, 
        achieved this milestone despite supply chain challenges. Production facilities 
        in Fremont, California and Shanghai, China contributed significantly to these 
        numbers. The Model Y was the best-selling electric vehicle globally.
        """,
        """
        Amazon Web Services (AWS) announced new AI services at its re:Invent 2023 
        conference in Las Vegas. CEO Andy Jassy unveiled Bedrock, a service for 
        building generative AI applications. The company also announced partnerships 
        with Anthropic and Stability AI. AWS remains the market leader in cloud 
        computing with 32% market share.
        """,
        """
        The United Nations Climate Change Conference (COP28) concluded in Dubai, 
        UAE on December 13, 2023. Nearly 200 countries agreed to transition away 
        from fossil fuels. UN Secretary-General António Guterres called it a 
        "historic achievement." The agreement includes commitments to triple 
        renewable energy capacity by 2030.
        """
    ]
    
    analyzer = DocumentAnalyzer()
    
    for i, doc in enumerate(documents, 1):
        print(f"\n📄 Document {i}:")
        print("-" * 70)
        result = analyzer.analyze(doc)
        print(f"Summary: {result.get('summary', 'N/A')}")
        print(f"Main Topics: {', '.join(result.get('main_topics', []))}")
        print(f"Organizations: {', '.join(result.get('entities', {}).get('organizations', []))}")


if __name__ == "__main__":
    print("\n" + "🚀 " * 20)
    print("DOCUMENT ANALYSIS PIPELINE - PROMPT CHAINING DEMO")
    print("🚀 " * 20)
    
    try:
        # Run examples
        example_basic_analysis()
        example_research_paper()
        example_step_by_step()
        example_batch_processing()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Set your OPENAI_API_KEY in .env file")
        print("3. Have sufficient API credits")

