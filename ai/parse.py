from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_chunk}\n"
    "Please follow these instructions carefully: \n\n"
    "1. **Extract information:** Only extract the information that directly matches the provided description: {parse_description}\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If the content does not contain any relevant information, respond with an empty string ('').\n"
    "4. **Direct Data Only:** Provide only the extracted data without any formatting or embellishments and no other text.\n"
)

model = OllamaLLM(model="gemma3:4b", temperature=0)

def parse_with_ollama(dom_chunk: str, parse_description: str) -> str:
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunk, start=1):
        response = chain.invoke(
            {"dom_chunk": chunk, "parse_description": parse_description}
        )
        print(f"Parsed chunk {i} of {len(dom_chunk)}")
        parsed_results.append(response)
    
    return "\n".join(parsed_results)