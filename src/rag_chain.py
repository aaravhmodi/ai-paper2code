try:
    from pylang import chain, step
except Exception:
    # Provide minimal fallback implementations so the app can run without pylang.
    def step(func):
        # simple decorator passthrough
        return func

    def chain(*steps):
        # Return an object with a .run(question) API that executes steps sequentially.
        class SimpleChain:
            def __init__(self, steps):
                self.steps = steps

            def run(self, question):
                context = {}
                for s in self.steps:
                    # Each step expected to accept (context, question) and return context
                    try:
                        context = s(context, question)
                    except TypeError:
                        # Fallback if step only accepts question -> returns dict or str
                        res = s(question)
                        if isinstance(res, dict):
                            context.update(res)
                        else:
                            context["answer"] = str(res)
                return context

        return SimpleChain(steps)

from src.retriever import query_docs

# Lazy model/tokenizer loader to avoid heavy downloads on import
_tokenizer = None
_model = None

def _get_model_and_tokenizer():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        import os
        from transformers import AutoTokenizer, AutoModelForCausalLM

        model_id = "mistralai/Mistral-7B-v0.1"
        # Read HF token from env var (set this in your shell or via huggingface-cli login)
        hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN")

        # Pass token to from_pretrained so gated models can be downloaded when authenticated
        _tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_token)
        _model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", use_auth_token=hf_token)
    return _tokenizer, _model


@step
def retrieve(context, question):
    context["docs"] = query_docs(question)
    return context


@step
def generate(context, question):
    try:
        tokenizer, model = _get_model_and_tokenizer()
    except Exception as e:
        # Model couldn't be loaded (gated model, auth, download error). Return a clear message
        msg = (
            "Model unavailable: could not load the generation model. "
            "This may be because the model is gated on Hugging Face or you are not authenticated. "
            f"Underlying error: {e}"
        )
        context["answer"] = msg
        return context

    prompt = f"""
    You are an AI researcher assistant.
    Based on the context below, generate runnable PyTorch code for the request.

    Context:
    {context.get('docs', '')}

    Task:
    {question}
    """

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=300)
        context["answer"] = tokenizer.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        context["answer"] = f"Generation failed: {e}"
    return context


paper2code = chain(retrieve, generate)

