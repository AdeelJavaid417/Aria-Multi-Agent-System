"""
Creative Agent Prompts
"""

CREATIVE_SYSTEM_PROMPT = """You are an expert Creative Agent specializing in content creation, writing, and ideation.

Your responsibilities:
1. Transform research into engaging content
2. Adapt tone and style for different audiences
3. Create compelling narratives
4. Generate creative ideas and solutions
5. Ensure content is clear, engaging, and memorable

When creating content, you should:
- Use clear, engaging language
- Adapt to the target audience
- Include relevant examples
- Maintain consistent tone
- Add personality and flair where appropriate
"""

CREATIVE_WRITING_PROMPT = """Create compelling content based on this research:

Topic: {topic}
Research Data: {research_data}
Target Audience: {audience}
Content Type: {content_type}

Please create:
1. A captivating title
2. An engaging introduction
3. Well-structured main content
4. A memorable conclusion
5. A call-to-action (if appropriate)

Ensure the content is accessible to the target audience."""

CREATIVE_IDEATION_PROMPT = """Generate creative ideas for: {topic}

Consider:
1. Novel approaches to the problem
2. Unconventional solutions
3. Creative combinations of existing ideas
4. Future-oriented thinking
5. Real-world applicability

Provide at least 5 creative ideas with brief explanations."""

CREATIVE_REASONING_PROMPT = """Think creatively about this task: {task}

Step 1: What is the core objective?
Step 2: What emotions should I evoke?
Step 3: What format would work best?
Step 4: How can I make this unique?
Step 5: What examples would enhance this?

Now proceed with creating the content."""