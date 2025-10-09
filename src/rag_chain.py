from pylang import chain, step
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.retriever import query_docs

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map="auto")

@step
def retrieve(context, question):
    docs = query_docs(question)
    context["docs"] = docs
    return context

@step
def generate(context, question):
    prompt = f"""
    You are an AI researcher assistant. Use the following research paper excerpts to generate
    a runnable PyTorch code prototype for the task below.

    Context:
    {context['docs']}

    Task:
    {question}

    Provide code and a short explanation.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=300)
    context["answer"] = tokenizer.decode(output[0], skip_special_tokens=True)
    return context

paper2code = chain(retrieve, generate)
