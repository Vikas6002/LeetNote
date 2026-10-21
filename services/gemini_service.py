# services/gemini_service.py
from openai import OpenAI
import json, re
from django.conf import settings

client = OpenAI(
    api_key  = settings.GROQ_API_KEY,
    base_url = "https://api.groq.com/openai/v1",
)
MODEL="llama-3.3-70b-versatile"


def _clean_json(raw):
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*",     "", raw)
    raw = re.sub(r"\s*```$",     "", raw)
    return raw.strip()


def _fallback():
    return {
        "key_points"      : ["Could not generate — add manually"],
        "time_complexity" : "",
        "space_complexity": "",
        "core_pattern"    : "",
        "similar_problems": [],
        "topic_core_idea" : "",
    }


def generate_note(problem_title, tags, code, explanation):
    first_tag = tags[0] if tags else "this topic"
    prompt = f"""
You are a DSA mentor reviewing a student's LeetCode solution.

Problem : {problem_title}
Tags    : {', '.join(tags) if tags else 'Not specified'}

Student's explanation:
{explanation if explanation else 'Not provided'}

Their code:
```
{code}
```

Return ONLY valid JSON, no markdown, no backticks:

{{
    "key_points"      : ["point 1", "point 2", "point 3"],
    "time_complexity" : "O(...) — one line reason",
    "space_complexity": "O(...) — one line reason",
    "core_pattern"    : "single most important insight to remember",
    "similar_problems": ["Problem 1", "Problem 2", "Problem 3"],
    "topic_core_idea" : "fundamental idea of {first_tag}"
}}
"""
    try:
        response = client.chat.completions.create(
            model    = MODEL,
            messages = [{"role": "user", "content": prompt}],
        )
        raw = _clean_json(response.choices[0].message.content)
        return json.loads(raw)

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response: {response.choices[0].message.content}")
        return _fallback()

    except Exception as e:
        print(f"API error: {e}")
        return _fallback()


def update_topic_note(tag_name, existing_tricks, new_note_data):
    prompt = f"""
You are maintaining a DSA topic summary for revision.

Topic: {tag_name}

Existing tricks:
{json.dumps(existing_tricks, indent=2)}

New insights from a just-solved problem:
- Core pattern : {new_note_data.get('core_pattern', '')}
- Topic idea   : {new_note_data.get('topic_core_idea', '')}
- Key points   : {json.dumps(new_note_data.get('key_points', []))}

Merge old and new. Remove duplicates. Keep concise.

Return ONLY valid JSON, no markdown, no backticks:

{{
    "core_statement": "1-2 sentences on the essence of {tag_name}",
    "key_tricks"    : ["trick 1", "trick 2", "trick 3", "trick 4"],
    "when_to_use"   : "when to apply {tag_name} techniques"
}}
"""
    try:
        response = client.chat.completions.create(
            model    = MODEL,
            messages = [{"role": "user", "content": prompt}],
        )
        raw = _clean_json(response.choices[0].message.content)
        return json.loads(raw)

    except Exception as e:
        print(f"Topic update error: {e}")
        return None