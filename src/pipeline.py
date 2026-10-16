def to_roman(question: str) -> str:
    prompt = f"""Transliterate this Hindi question into Roman script (English letters), the way people type Hinglish in a FAQ.
Do NOT use Devanagari characters in the output. Output only the question, nothing else.

Examples:
Input: प्रॉपनेक्स के फाउंडर कौन हैं?
Output: Propnex AI Technology ke founder kaun hain?

Input: बिजनेस प्रोसेस ऑटोमेशन क्या होता है?
Output: Business process automation kya hota hai?

Input: आप किन लोगों के साथ काम करते हैं?
Output: Propnex AI Technology kin logon ke saath kaam karti hai?

Input: {question}
Output:"""
    try:
        out = generate(prompt).strip()
        # agar ab bhi Devanagari aaya to original wapas
        if any("\u0900" <= ch <= "\u097F" for ch in out):
            return question
        return out
    except Exception as e:
        print("to_roman error:", e)
        return question