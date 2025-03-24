import google.generativeai as genai

"""First test"""
# from google import genai

# client = genai.Client(api_key="AIzaSyBgVtywzT0oM5Bq933yOn-S7Th-QU6tJiM")

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain the heat death of the universe. Answer in 2-3 sentences."
# )

# print(response.text)


"""Second test"""
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyBgVtywzT0oM5Bq933yOn-S7Th-QU6tJiM")


# # First Agent
# model = genai.GenerativeModel("gemini-2.0-flash")

# response = model.generate_content("Explain time dialation. Answer briefly.", stream=True)

# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)

"""Third test"""

genai.configure(api_key="AIzaSyBgVtywzT0oM5Bq933yOn-S7Th-QU6tJiM")

model = genai.GenerativeModel("gemini-2.0-flash")

# Get user inputs
topic = input("Enter the topic: ")
loops = int(input("Enter the number of reasoning loops: "))

# First agent sets up the topic
topic_promt = f"""Here is the topic provided #### {topic} ####, 

Evaluate a set of arguments for and against it. 

Make sure to clearly and concisely present the arguments and counterarguments. Keeping the instructions generic and non-specific.

Approach the topic from multiple angles and provide a comprehensive analysis."""

first_response = model.generate_content(
    topic_promt, 
    stream=True,
    generation_config=genai.types.GenerationConfig(
        # Lower temperature results in more conservative and consistent responses
        temperature=0.3
    )
)

print("\n Formualting questions: ")
question = ""
for chunk in first_response:
    question += chunk.text
    print(chunk.text)
print("\n" + "_" * 80)    

# Second agent performs iterative reasoning
current_response = question
all_responses = []
for i in range(loops):
    print(f"\n Iteration {i+1}/{loops}: ")
    
    reasoning_prompt = f"""Here is what you need to do #### {current_response} ####, """
    
    response = model.generate_content(
        reasoning_prompt,
        stream=True,
        generation_config=genai.types.GenerationConfig(
            # Higher temperature results in more creative responses
            temperature=1.0
        )
    )
    current_response = ""
    for chunk in response:
        current_response += chunk.text
        print(chunk.text)
    all_responses.append(current_response)
    print("\n" + "_" * 80)
    

# Third agent summarizes the reasoning
print("\n Summarizing the reasoning: ")
summary_prompt = f"""Topic: {topic} 
Initial reasoning: {question} 
Reasoning chain: {' | '.join(current_response)} 

Based on the above reasoning, summarize the key points and insights. 

Provide a clear and concise summary of the arguments and counterarguments. 

Provide a cohenrent and logical conclusion in two concise paragraphs.

Use simple and clear language to communicate the key points and insights and write in short sentences.
"""

final_response = model.generate_content(
    summary_prompt,
    stream=True,
    
    generation_config=genai.types.GenerationConfig(
        # Lower temperature results in more conservative and consistent responses
        temperature=0.1
    )
)

for chunk in final_response:
    print(chunk.text)
print("_" * 80)