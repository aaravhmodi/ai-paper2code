from fastapi import FastAPI, Body
from src.rag_chain import paper2code
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/generate")
def generate_code(payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(status_code=400, content={"error": "Missing 'query' in payload"})

    try:
        result = paper2code.run(query)
        return {"result": result.get("answer")}
    except Exception as e:
        # Return a JSON error instead of an HTML 500 page so clients can handle it
        return JSONResponse(status_code=500, content={"error": "Server error during generation", "details": str(e)})
