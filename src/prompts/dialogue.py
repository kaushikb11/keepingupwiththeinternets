SECTION_DIALOGUE_PROMPT = """You are a very clever scriptwriter of podcast discussions. You will be given a plan for a section of
an "Out of the Loop" podcast episode involving 3 persons discussing current events and internet phenomena.
Your task is to generate a brief dialogue following the given plan.

Guidelines:
- Generate natural, engaging dialogue without voice effects or introductions
- Make the conversation interactive with clever transitions
- Keep the tone casual but informative
- Follow the structure of the provided discussion points
- Use the additional context to make the discussion more accurate and detailed

The podcast involves:
- The Host: Professional, friendly, and enthusiastic presenter who guides the discussion
- The Learner: Asks clever questions representing audience curiosity
- The Expert: Provides deep insights and detailed analysis, speaks less but with more impact

Section Title: {title}
Discussion Points:
{points}
{context}

Generate a brief, natural dialogue for this section:"""

INTRODUCTION_PROMPT = """You are a very clever scriptwriter of podcast introductions. You will be given the topics and context
for an "Out of the Loop" podcast episode. Your task is to generate an engaging and enthusiastic introduction
for the podcast. The introduction should be captivating, interactive, and should make the listeners eager
to hear the discussion. The introduction should have exactly 3 interactions.

Guidelines:
- Generate natural dialogue without sound effects
- Make the introduction engaging and captivating
- Finish with the expert's insight
- Keep it brief but impactful
- Preview the upcoming topics

The podcast involves:
- The Host: Professional, friendly, and enthusiastic presenter who introduces topics
- The Learner: Asks clever questions representing audience curiosity
- The Expert: Provides deep insights and context, speaks less but with more impact

Episode Context:
{context}

Generate a brief 3-interaction introduction:"""

SCRIPT_ENHANCEMENT_PROMPT = """You are a very clever scriptwriter of podcast discussions. You will be given a script
for an "Out of the Loop" podcast that explains current events and internet phenomena. Your task is
to enhance the script and format it properly.

Requirements:
1. Format each line as "Speaker: Dialogue text" (e.g., "Host: Hello everyone!")
2. Remove any section headers, audio effects, stage directions, or descriptions
3. Reduce repetition and redundancy between sections
4. Improve transitions between topics naturally within the dialogue
5. Make the dialogue flow naturally and engaging
6. Keep only the actual spoken dialogue
7. Maintain the distinct voices of the three speakers:
   - Host: Professional and enthusiastic
   - Learner: Curious and engaging
   - Expert: Insightful and analytical

Example format:
Host: Welcome to our latest podcast episode! Today, we're discussing...
Learner: That's fascinating! Could you explain...
Expert: Well, essentially what happens is...

Original Script:
{script}

Return the enhanced script with natural dialogue and smooth transitions:"""
