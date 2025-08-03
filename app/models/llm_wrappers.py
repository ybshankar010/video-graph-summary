import json
import re
import time
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import OllamaLLM
from app.utils.constants import MODEL_NAME

llm = OllamaLLM(model=MODEL_NAME, temperature=0.1)

prompt = PromptTemplate.from_template(
    "You are an expert information extractor. Given a video frame caption, extract all possible (subject, predicate, object) triples that describe the visual scene.\n\n"
    "Input: A single image caption.\n"
    "Output: A valid JSON list of (subject, predicate, object) triples. Do NOT include any explanation, markdown, or code blocks.\n"
    "Format: [[\"subject\", \"predicate\", \"object\"], ...]\n\n"
    "Caption: {caption}\n"
    "Triples:"
)

chain = prompt | llm

MAX_RETRIES = 3

def is_junk_caption(caption: str) -> bool:
    tokens = caption.lower().split()
    return len(tokens) > 5 and len(set(tokens)) <= 2  # e.g., repeated 'chip chip...'

def is_valid_json_triple_list(response: str) -> bool:
    try:
        parsed = json.loads(response)
        return isinstance(parsed, list) and all(
            isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) for x in t)
            for t in parsed
        )
    except:
        return False

def clean_json_response(response):
    response = re.sub(r"```json|```", "", response).strip()
    return response

def extract_triples_with_llm(caption: str, trace: int = 0) -> list:
    if is_junk_caption(caption):
        print(f"⏭️ Skipping repetitive/junk caption: {caption}")
        return []

    print("=" * 20)
    print(f"Extracting triples for caption: {caption}")

    for attempt in range(MAX_RETRIES):
        try:
            response = chain.invoke({"caption": caption})
            print(f"LLM response: {response}")

            cleaned = clean_json_response(response)
            if is_valid_json_triple_list(cleaned):
                triples = json.loads(cleaned)
                print(f"✅ Extracted: {triples}")
                return triples
            else:
                print(f"⚠️ Invalid structure, retrying ({attempt+1}/{MAX_RETRIES})...")
        except Exception as e:
            print(f"❌ Exception during triple extraction: {e}")
            time.sleep(1)

    print(f"❌ Giving up on caption: {caption}")
    return []

def run_query_with_llm(prompt: str, trace: int = 0) -> str:
    print("=" * 20)
    print(f"Answering query based on prompt: {prompt}")
    
    template = PromptTemplate.from_template("{prompt}")
    answer_chain = template | llm

    for attempt in range(MAX_RETRIES):
        try:
            response = answer_chain.invoke({"prompt": prompt})
            print(f"LLM response: {response}")
            return response.strip()
        except Exception as e:
            print(f"❌ Exception during query execution: {e}")
            time.sleep(1)

    return ""
