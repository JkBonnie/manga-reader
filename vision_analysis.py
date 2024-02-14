import json 

def analyze_images_with_gpt4_vision(character_profiles, pages, client, prompt, instructions, detail="low"):
    # Construct the messages including the prompt and images
    messages = [
        {
            "role": "system",
            "content": instructions
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here are some character profile pages, for your reference:"}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": detail}} for img_base64 in character_profiles]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": detail}} for img_base64 in pages]
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=4096
    )
    
    return response


def detect_important_pages(profile_reference, chapter_reference, pages, client, prompt, instructions, detail="low"):
    # Construct the messages including the prompt and images
    messages = [
        {
            "role": "system",
            "content": instructions
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here are some character profile pages, for your reference:"}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": detail}} for img_base64 in profile_reference]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here are some chapter start pages, for your reference:"}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": detail}} for img_base64 in chapter_reference]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": detail}} for img_base64 in pages]
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=4096
    )
    response_text = response.choices[0].message.content
    tokens = response.usage.total_tokens

    # parse response text json from response.choices[0].message.content into object
    try:
        # Extract the text content from the first choice's message (if structured as expected)
        parsed_response = json.loads(response_text)
    except (AttributeError, IndexError, json.JSONDecodeError) as e:
        # Handle cases where parsing fails or the structure is not as expected
        print(f"Using GPT as a backup to format JSON object...")
        response = completions(client, response_text)
        tokens += response.usage.total_tokens
        try:
            parsed_response = json.loads(response.choices[0].message.content)
        except (AttributeError, IndexError, json.JSONDecodeError) as e:
            parsed_response = None
            print("Even after using GPT to parse the json, we failed. Fatal error.")
            raise e
    
    return {"total_tokens": tokens, "parsed_response": parsed_response["important_pages"]}


JSON_PARSE_PROMPT ="""
You are a JSON parser. Return a properly formatted json object based on the input from the user.
Your response must be in the following format:
{"important_pages": Array<{"page_index": int 0-9, "page_type": "profile" | "chapter"}>}

Examples of valid responses:
```
{
    "important_pages": [
        {"page_index": 0, "page_type": "profile"},
        {"page_index": 3, "page_type": "chapter"}
    ]
}
```

```
{
    "important_pages": []
}
```

"""

def completions(client, text):
    messages = [
        {
            "role": "system",
            "content": JSON_PARSE_PROMPT
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text}
            ]
        },
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    return response
