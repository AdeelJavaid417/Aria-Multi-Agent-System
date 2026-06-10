"""
Creative Agent - Generates creative content
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts import CREATIVE_SYSTEM_PROMPT, CREATIVE_WRITING_PROMPT
from utils.logger import logger

class CreativeAgent(BaseAgent):
    """Specialized agent for creative tasks"""
    
    def __init__(self):
        """Initialize Creative Agent"""
        super().__init__(
            name="Creative Agent",
            description="Specialized in generating creative content and ideas",
            system_prompt=CREATIVE_SYSTEM_PROMPT
        )
    
    def execute(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Execute creative task
        
        Args:
            task: Creative task description
            context: Additional context (e.g., research findings)
        
        Returns:
            Creative output
        """
        logger.info(f"✍️ {self.name} executing: {task}")
        
        try:
            # Step 1: Retrieve any relevant research from memory
            relevant_context = ""
            if context:
                memories = self.retrieve_from_memory(context, top_k=3)
                if memories:
                    relevant_context = "\n".join([
                        m["content"] for m in memories
                    ])
            
            # Step 2: Think creatively
            reasoning = self.think(task, relevant_context)
            
            # Step 3: Generate creative content
            creative_output = self._generate_content(task, relevant_context)
            
            # Step 4: Enhance the output
            enhanced_output = self._enhance_content(creative_output)
            
            # Step 5: Save to memory
            self.save_to_memory(
                key=f"creative_{task[:30]}",
                content=enhanced_output,
                metadata={
                    "type": "creative",
                    "task": task
                }
            )
            
            # Record execution
            self.record_execution(
                task=task,
                result=enhanced_output,
                success=True,
                tool_calls=self.tool_calls_count
            )
            
            return {
                "status": "success",
                "task": task,
                "reasoning": reasoning,
                "creative_output": creative_output,
                "enhanced_output": enhanced_output,
                "execution_time": self.last_execution_time
            }
        
        except Exception as e:
            logger.error(f"❌ Creative agent error: {e}")
            self.record_execution(task=task, result=str(e), success=False)
            
            return {
                "status": "error",
                "error": str(e),
                "task": task
            }
    
    def _generate_content(self, task: str, context: str = "") -> str:
        """Generate initial creative content"""
        logger.info("✍️ Generating creative content...")
        
        prompt = f"""Create engaging, original content for this task:

Task: {task}

{f'Reference/Context: {context}' if context else ''}

Guidelines:
- Be creative and original
- Make it engaging and interesting
- Use clear language
- Structure it well
- Add personality"""
        
        content = self.invoke_llm(prompt)
        return content
    
    def _enhance_content(self, content: str) -> str:
        """Enhance generated content"""
        logger.info("🎨 Enhancing content...")
        
        prompt = f"""Enhance and refine this content to make it more compelling:

Original Content:
{content}

Please:
1. Improve clarity
2. Add engaging elements
3. Fix any grammar issues
4. Enhance readability
5. Keep the core message intact"""
        
        enhanced = self.invoke_llm(prompt)
        return enhanced
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return [
            {
                "name": "brainstorm",
                "description": "Generate ideas through brainstorming",
                "function": self.brainstorm
            }
        ]
    
    def brainstorm(self, topic: str, num_ideas: int = 5) -> List[str]:
        """
        Brainstorm ideas on a topic
        
        Args:
            topic: Topic to brainstorm about
            num_ideas: Number of ideas to generate
        
        Returns:
            List of creative ideas
        """
        logger.info(f"💡 Brainstorming {num_ideas} ideas for: {topic}")
        
        prompt = f"""Generate {num_ideas} creative, original ideas about: {topic}

For each idea:
- Brief title
- One sentence description
- Why it's unique

Format as a numbered list."""
        
        response = self.invoke_llm(prompt)
        
        # Parse ideas from response
        ideas = [line.strip() for line in response.split('\n') if line.strip()]
        return ideas[:num_ideas]
    
    def write_blog_post(self, topic: str, research_data: str = "", 
                       word_count: int = 500) -> str:
        """
        Write a blog post
        
        Args:
            topic: Blog topic
            research_data: Research findings to use
            word_count: Approximate word count
        
        Returns:
            Blog post content
        """
        logger.info(f"📝 Writing blog post: {topic}")
        
        prompt = f"""Write a professional blog post about: {topic}

Approximate word count: {word_count} words

{f'Use this research: {research_data}' if research_data else ''}

Include:
1. Engaging title
2. Compelling introduction
3. Well-structured body with sections
4. Practical examples
5. Conclusion with takeaways
6. Call to action

Make it informative and engaging for a general audience."""
        
        return self.invoke_llm(prompt)
    
    def create_tutorial(self, topic: str, skill_level: str = "beginner") -> str:
        """
        Create a tutorial
        
        Args:
            topic: Tutorial topic
            skill_level: Target skill level (beginner, intermediate, advanced)
        
        Returns:
            Tutorial content
        """
        logger.info(f"📚 Creating {skill_level} tutorial: {topic}")
        
        prompt = f"""Create a comprehensive {skill_level} tutorial for: {topic}

Structure:
1. Introduction & Overview
2. Prerequisites
3. Step-by-step instructions
4. Code examples/demonstrations
5. Common mistakes to avoid
6. Tips and tricks
7. Next steps

Make it clear, detailed, and practical."""
        
        return self.invoke_llm(prompt)