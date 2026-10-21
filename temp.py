# from openai import OpenAI

# # 🔑 Replace with your Groq API key
# client = OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )

# try:
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "user", "content": "Say hello in one word"}
#         ]
#     )

#     print("✅ Response:")
#     print(response.choices[0].message.content)

# except Exception as e:
#     print("❌ Error:", e)


# from google import genai

# client = genai.Client(api_key="AIzaSyDQhLJ02WwRsaTGzts_WnDYLiGiFFWHgJo")

# try:
#     response = client.models.generate_content(
#         model="gemini-1.5-flash-latest",
#         contents="Say hello in one word"
#     )

#     print("✅ Response:")
#     print(response.text)

# except Exception as e:
#     print("❌ Error:", e)


from google import genai

client = genai.Client(api_key="AIzaSyDQhLJ02WwRsaTGzts_WnDYLiGiFFWHgJo")

try:
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents="Say hello in one word"
    )

    print("✅ Response:")
    print(response.text)

except Exception as e:
    print("❌ Error:", e)