import os
import json
from groq import Groq
from .schemas import GeminiOutline, SlideContent

def _prompt(topic, n):
    return f"""Create a detailed PowerPoint presentation about: {topic}

Return JSON format:
{{
    "presentation_title": "compelling title",
    "subtitle": "descriptive subtitle",
    "slides": [
        {{
            "title": "slide title",
            "bullets": [
                "detailed point 1 with specific information",
                "detailed point 2 with facts or examples",
                "detailed point 3 with insights",
                "detailed point 4 with practical info",
                "detailed point 5 with more details",
                "detailed point 6 with additional context"
            ],
            "image_keyword": "relevant keyword"
        }}
    ]
}}

IMPORTANT:
- Create exactly {n} slides
- Each slide MUST have 5-7 detailed bullet points
- Each bullet should be 10-20 words with real information
- Be specific, informative, educational
- Include facts, examples, statistics where relevant
- No generic filler content
- Progress logically through the topic

Return ONLY valid JSON, no markdown, no explanation."""

def _parse(t):
    t = t.strip()
    if "```" in t:
        parts = t.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                t = part
                break
    
    try:
        return json.loads(t)
    except:
        s, e = t.find("{"), t.rfind("}")
        if s == -1 or e == -1:
            raise ValueError("No JSON found")
        return json.loads(t[s:e+1])

def _norm(raw, n, topic):
    t = raw.get("presentation_title", topic)
    sub = raw.get("subtitle", f"An in-depth look at {topic}")
    slides = raw.get("slides", [])
    
    if not isinstance(slides, list):
        slides = []
    
    out = []
    for i, s in enumerate(slides[:n]):
        title = s.get("title", f"Slide {i+1}")
        b = s.get("bullets", [])
        if not isinstance(b, list):
            b = []
        # Keep all bullets, just clean them
        b = [str(x).strip() for x in b if str(x).strip() and len(str(x).strip()) > 3]
        img = s.get("image_keyword", topic.split()[0] if topic else "")
        out.append(SlideContent(title=str(title), bullets=b, image_keyword=str(img)))
    
    return GeminiOutline(
        presentation_title=str(t),
        subtitle=str(sub),
        slides=out
    )

def generate_outline(topic, num_slides_total):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Missing GROQ_API_KEY")
    
    # Use the best available model
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    n = max(1, num_slides_total - 1)
    
    client = Groq(api_key=key)
    resp = client.chat.completions.create(
        model=model,
        temperature=0.7,
        max_tokens=4000,
        messages=[
            {
                "role": "system", 
                "content": "You are an expert presentation creator. Create detailed, informative, professional content. Return only valid JSON."
            },
            {
                "role": "user", 
                "content": _prompt(topic, n)
            }
        ]
    )
    
    content = resp.choices[0].message.content or ""
    data = _parse(content)
    return _norm(data, n, topic)