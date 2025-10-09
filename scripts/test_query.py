import os
import sys

# Ensure project root is on sys.path so `from src...` imports work when running this script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.retriever import query_docs, collection, embedder

q = 'implement diffusion model in PyTorch'
print('Query:', q)
res = collection.query(query_embeddings=embedder.encode([q]), n_results=3)
print('Raw result keys:', list(res.keys()))
print('Counts:')
for k, v in res.items():
    try:
        print(' ', k, '->', len(v) if hasattr(v, '__len__') else type(v))
    except Exception:
        print(' ', k, '->', type(v))
print('\nFormatted:')
# Debug: inspect raw document and metadata content
print('\nres["documents"] repr:')
print(repr(res.get('documents')))
print('\nres["metadatas"] repr:')
print(repr(res.get('metadatas')))

print('\nFormatted from helper:')
print(query_docs(q, n=3))

# Inspect collection contents
try:
    print('\nCollection count:', collection.count())
except Exception as e:
    print('Collection.count() failed:', e)

try:
    sample = collection.get(limit=5)
    print('\nSample collection.get(limit=5) keys:', list(sample.keys()))
    print('Sample documents repr:', repr(sample.get('documents')))
    print('Sample metadatas repr:', repr(sample.get('metadatas')))
except Exception as e:
    print('collection.get() failed:', e)
