"""
OpenAI service for AI content generation.
"""
import openai
from typing import List, Dict, Optional
import time
import logging

from app.core.config import settings
from app.utils.exceptions import OpenAIAPIException

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API operations."""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise OpenAIAPIException("OpenAI API key not configured")
        
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.last_token_count = 0
        self.last_cost_cents = 0
    
    async def generate_caption(
        self,
        product_description: str,
        tone: str = "professional",
        style: str = "engaging",
        include_hashtags: bool = True,
        max_length: int = 1500,
        target_audience: Optional[str] = None,
        call_to_action: Optional[str] = None
    ) -> str:
        """Generate Instagram caption for home decor products."""
        
        start_time = time.time()
        
        system_prompt = f"""
        You are an expert Instagram content creator specializing in home decor for the brand "Defeah". 
        Create engaging captions that drive sales and engagement.
        
        Brand voice: {tone}
        Writing style: {style}
        Max length: {max_length} characters
        Include hashtags: {include_hashtags}
        Target audience: {target_audience or "home decor enthusiasts"}
        
        Guidelines:
        - Start with a hook that stops scrolling
        - Include emotional connection to home/comfort
        - Mention specific product benefits
        - End with a call-to-action
        - Use emojis strategically (but not excessively)
        - If hashtags included, use 5-15 relevant home decor hashtags
        - Focus on lifestyle transformation, not just product features
        - Always include #DefeahStyle as the branded hashtag
        """
        
        user_prompt = f"""
        Product: {product_description}
        
        Create an Instagram caption that will drive engagement and sales for this home decor product.
        """
        
        if call_to_action:
            user_prompt += f"\nInclude this call-to-action: {call_to_action}"
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Calculate costs (GPT-4 pricing: $0.03/1K input, $0.06/1K output)
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (input_tokens * 0.03 / 1000 + output_tokens * 0.06 / 1000) * 100
            )
            
            generation_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Generated caption: {len(caption)} chars, {self.last_token_count} tokens, ${self.last_cost_cents/100:.4f}")
            
            return caption
            
        except Exception as e:
            logger.error(f"Caption generation failed: {str(e)}")
            raise OpenAIAPIException(f"Caption generation failed: {str(e)}")
    
    async def generate_image(
        self,
        prompt: str,
        style: str = "photorealistic",
        quality: str = "hd",
        size: str = "1024x1024"
    ) -> str:
        """Generate product image using DALL-E 3."""
        
        start_time = time.time()
        
        enhanced_prompt = f"""
        {prompt}
        
        Style: {style}, high-quality home decor photography
        Lighting: Natural, soft lighting with good contrast
        Composition: Professional product photography, clean background
        Quality: {quality}, Instagram-ready, commercial use
        
        Make it look like a premium home decor catalog photo that would appeal to modern homeowners.
        Ensure the image is aesthetically pleasing and would work well for social media marketing.
        """
        
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            image_url = response.data[0].url
            
            # DALL-E 3 pricing: $0.04 for standard, $0.08 for HD quality
            self.last_cost_cents = 8 if quality == "hd" else 4
            
            generation_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Generated image: {size}, {quality}, ${self.last_cost_cents/100:.2f}")
            
            return image_url
            
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise OpenAIAPIException(f"Image generation failed: {str(e)}")
    
    async def suggest_hashtags(
        self,
        content_description: str,
        niche: str = "home_decor",
        count: int = 15,
        competition_level: str = "medium"
    ) -> List[str]:
        """Suggest relevant hashtags for content."""
        
        system_prompt = f"""
        You are a hashtag research expert for Instagram marketing in the {niche} niche.
        Suggest {count} high-performing hashtags with {competition_level} competition level.
        
        Guidelines:
        - Mix of popular and niche-specific hashtags
        - Always include the branded hashtag: #DefeahStyle
        - Balance reach and engagement potential
        - Avoid banned or shadowbanned hashtags
        - Include hashtags for home decor, interior design, and lifestyle
        - Return only hashtags, one per line, with # symbol
        - Focus on hashtags that the target audience actually searches for
        """
        
        user_prompt = f"""
        Content description: {content_description}
        
        Suggest {count} strategic hashtags for maximum reach and engagement in the home decor space.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [tag.strip() for tag in hashtags_text.split('\n') if tag.strip().startswith('#')]
            
            # Calculate costs
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (response.usage.prompt_tokens * 0.03 / 1000 + 
                 response.usage.completion_tokens * 0.06 / 1000) * 100
            )
            
            logger.info(f"Generated {len(hashtags)} hashtags, {self.last_token_count} tokens, ${self.last_cost_cents/100:.4f}")
            
            return hashtags[:count]
            
        except Exception as e:
            logger.error(f"Hashtag suggestion failed: {str(e)}")
            raise OpenAIAPIException(f"Hashtag suggestion failed: {str(e)}")
    
    async def analyze_content_performance(
        self,
        posts_data: List[Dict],
        time_period: str = "last_30_days"
    ) -> Dict:
        """Analyze content performance and provide recommendations."""
        
        system_prompt = f"""
        You are a social media analytics expert. Analyze the provided Instagram post data 
        and provide actionable insights for improving performance.
        
        Focus on:
        - Best performing content types
        - Optimal posting times
        - Caption length analysis
        - Hashtag performance
        - Engagement patterns
        - Content recommendations
        
        Return analysis as JSON with specific recommendations.
        """
        
        user_prompt = f"""
        Instagram posts data for {time_period}:
        {str(posts_data)[:4000]}  # Limit to avoid token limits
        
        Provide detailed performance analysis and 5 specific recommendations for improvement.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to text if parsing fails
            try:
                import json
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                analysis = {"raw_analysis": analysis_text}
            
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (response.usage.prompt_tokens * 0.03 / 1000 + 
                 response.usage.completion_tokens * 0.06 / 1000) * 100
            )
            
            logger.info(f"Analyzed content, {self.last_token_count} tokens, ${self.last_cost_cents/100:.4f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Content analysis failed: {str(e)}")
            raise OpenAIAPIException(f"Content analysis failed: {str(e)}")