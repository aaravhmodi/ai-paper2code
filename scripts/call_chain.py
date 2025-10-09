import os
import sys
import traceback

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from src import rag_chain
    paper2code = rag_chain.paper2code
    print('paper2code object:', paper2code)
    print('Calling paper2code.run("debug test")')
    try:
        out = paper2code.run('debug test')
        print('Output:', out)
    except Exception:
        print('Exception while running paper2code.run:')
        traceback.print_exc()
except Exception:
    print('Exception while importing rag_chain:')
    traceback.print_exc()
