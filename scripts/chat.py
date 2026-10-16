from src.pipeline import answer

while True:
    q = input("\nAsk (or 'exit'): ")
    if q.lower() == "exit":
        break
    result = answer(q)
    print("\n" + result["answer"])
    print("\nSources:", [f"p{c['page']} (d={c['distance']:.2f})" for c in result["sources"]])