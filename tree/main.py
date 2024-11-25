import os
from groq import Groq  # type: ignore

# Initialize Groq Client with API key from environment variables
client = Groq(
    #api_key=os.environ.get("GROQ_API_KEY"),
    api_key="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"
)

# Global character setting (modifiable)
CHARACTER = "Donald Trump"

# Helper Function: Build User Message
def build_user_message(stateOutcome, stateStorySummary, stateAdditionalContext):
    """
    Constructs the user message for the API call based on inputs.
    """
    return f"""
    Think about the following situation and generate a positive and negative outcome with state story summary, focusing not only on the immediate effects but also on second-order events—the ripple effects or consequences that emerge from the initial situation. Ensure the outcomes are unique, avoid repeating what has already been stated, and add meaningful depth to each.
    Here is the information:
    - State Story Summary: "{stateStorySummary}"  
    - State Outcome: "{stateOutcome}"  
    - Additional Context: "{stateAdditionalContext}"
    """
def build_system_prompt():
    """
    Constructs the detailed system message for the API call.
    """
    return f"""
    You are a highly creative and concise assistant, inspired by {CHARACTER}. Your personality blends the wit of a comedian, the depth of a philosopher, and the efficiency of someone who values every word. Your task is to analyze a situation, identify second-order events, and generate meaningful JSON responses. 

    Second-order events are indirect outcomes that add depth and nuance to a situation. Examples:
    1. Winning a local contest leads to a national-level opportunity.
    2. Saving money enables an investment that grows wealth.
    3. Learning a skill secures a new job with global exposure.
    4. Helping a friend strengthens a bond, leading to unexpected benefits.

    JSON structure:
    
    {{
        "positive_outcome": "A single sentence; string (<= 150 characters, conversational tone addressing the user)",
        "negative_outcome": "A single sentence; string (<= 150 characters, conversational tone addressing the user)",
        "stateStorySummary": "A single sentence; string (<= 190 characters, conversational tone summarizing how the current state relates to the parent state)"
    }}


    Input Definitions:
    1. State Outcome: The main action or event being evaluated.
    2. State Story Summary: Context linking the current and previous states.
    3. State Additional Context: Optional nuances for clarity.

    Guidelines for Output:
    1. Focus on second-order events to add depth.
    2. Each repeated outcome will incur a penalty to you, so avoid repeating or rephrasing the input; outcomes must explore new angles.
    3. Positive outcomes:
        - Describe the best result of the stateOutcome in a creative and optimistic way.
        - Ensure the outcome adds new meaning and avoids repetition.
        - IMPORTANT: When the situation is very positive then Construct a humourous response in an exaggerated positivity
        - IMPORTANT: if positivity becomes repetitive, be very funny. 
    4. Negative outcomes:
        - Explain realistic downsides thoughtfully and clearly.
        - IMPORTANT: If no clear downside or negative aspect exists, exaggerate humorously and create a negative aspect.
        - For example, "I will start eating healthy everyday", for this there's no negative aspect but you can think like "your friends might become jealous of fitness and avoid you"
    5. State Story Summaries should clearly bridge the context without redundancy.

    Expectations:
    - Avoid jargon; use concise and engaging English.
    - DEEPLY RESPECT word count limits & stay within them; you will be ceased to if NOT followed: Positive/Negative outcomes (150), Story Summary (190).
    - Penalize repetition—introduce new dimensions to each response.
    - Think like {CHARACTER}: What unique perspective would they offer in this situation? Don't use {CHARACTER} name

    Your responses should be original, engaging, and rooted in second-order thinking. If context is unclear, add humor to keep the narrative engaging.
    """
def outcomeGenerator(stateOutcome, stateStorySummary="none", stateAdditionalContext="none"):
    """
    Generates positive and negative outcomes for a given state using the Groq Cloud API in JSON mode.
    
    Args:
        stateOutcome (str): Description of the action or event (<= 160 characters).
        stateStorySummary (str): Summary of how we arrived at this state (<= 200 characters, default: "none").
        stateAdditionalContext (str): Optional additional details about the stateOutcome (<= 160 characters, default: "none").
    
    Returns:
        dict: A dictionary containing the positive and negative outcomes, along with the stateStorySummary.
    """
    # Validate input lengths
    if len(stateOutcome) > 160:
        raise ValueError("stateOutcome exceeds 160 characters.")
    if len(stateStorySummary) > 200:
        raise ValueError("stateStorySummary exceeds 200 characters.")
    if len(stateAdditionalContext) > 160:
        raise ValueError("stateAdditionalContext exceeds 160 characters.")
    
    # Build system and user messages
    system_message = build_system_prompt()
    user_message = build_user_message(stateOutcome, stateStorySummary, stateAdditionalContext)

    print(" "*15+user_message+" "*15)

    # Generate the response using Groq Cloud with JSON mode
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"},  # Request JSON mode
        )
    except Exception as e:
        raise Exception(f"Groq API request failed: {e}")
    
    # Parse the ChatCompletion object
    choices = chat_completion.choices
    if not choices or not hasattr(choices[0], "message"):
        raise Exception("No valid choices returned from the model.")
    
    # Extract JSON content from the message
    content = choices[0].message.content
    print(content)
    try:
        outcome_data = eval(content)  # Convert JSON-like string to dictionary

        positive_outcome = outcome_data.get("positive_outcome")
        negative_outcome = outcome_data.get("negative_outcome")
        generated_stateStorySummary = outcome_data.get("stateStorySummary")  # Extract from LLM
        print(len(positive_outcome),len(negative_outcome),len(generated_stateStorySummary))

        #print(outcome_data.get("stateStorySummary"))
    except Exception as e:
        raise Exception(f"Failed to parse JSON content: {content}, Error: {e}")
    
    if not positive_outcome or not negative_outcome or not generated_stateStorySummary:
        raise Exception("Incomplete outcomes or story summary returned from the model.")
    
    # Return outcomes
    return {
        "positive_outcome": positive_outcome,
        "negative_outcome": negative_outcome,
        "stateStorySummary": generated_stateStorySummary  # Generated by LLM
    }

"""
# Example Usage
if __name__ == "__main__":
    # Set a new character dynamically if needed
    #CHARACTER = "Donald Trump"
    CHARACTER = "Donald Trump"

    try:
        #result = outcomeGenerator(
        #    outcomeID=1,
        #    stateOutcome="I want to quit my job and start a company",
        #    stateStorySummary="none",
        #    stateAdditionalContext="I feel financially stable to take this risk."
        #)

        #result = outcomeGenerator(
        #    outcomeID=1,
        #    stateOutcome="You achieve great success with your new company, becoming a leader in your industry.",
        #    stateStorySummary="This is your first step: deciding to quit your job to start a company.",
        #    stateAdditionalContext="None"
        #)

        #result = outcomeGenerator(
        #    outcomeID=1,
        #    stateOutcome="You might face challenges maintaining your work-life balance.",
        #    stateStorySummary="You started a company and found success after quitting your job.",
        #    stateAdditionalContext="I have no life"
        #)

        #result = outcomeGenerator(
        #    outcomeID=1,
        #    stateOutcome="You find a way to balance work and life, achieving a healthy lifestyle.",
        #    stateStorySummary="You started a company and found success after quitting your job, but now face challenges maintaining your work-life balance.",
        #    stateAdditionalContext="None"
        #)

        #result = outcomeGenerator(
        #    outcomeID=1,
        #    stateOutcome="You master the art of work-life balance, achieving a healthy lifestyle and continued success in your company.",
        #    stateStorySummary="You started a company and found success after quitting your job, but now face challenges maintaining your work-life balance.",
        #    stateAdditionalContext="None"
        #)

        result = outcomeGenerator(
            outcomeID=1,
            stateOutcome="Your friends might become jealous of your success and start plotting against you.",
            stateStorySummary="You mastered the art of work-life balance, achieving a healthy lifestyle and continued success in your company.",
            stateAdditionalContext="None"
        )

        print("Generated Outcomes:")
        print(f"Positive Outcome: {result['positive_outcome']}")
        print(f"Negative Outcome: {result['negative_outcome']}")
        print(f"State Story Summary: {result['stateStorySummary']}")
    except Exception as e:
        print(f"Error: {e}")
"""