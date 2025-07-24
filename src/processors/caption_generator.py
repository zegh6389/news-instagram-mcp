"""Caption generator for Instagram posts."""

import logging
from typing import Dict, Any, Optional, List
from ..config import config

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class CaptionGenerator:
    """Generates captions for Instagram posts based on news articles."""
    
    def __init__(self):
        """Initialize the caption generator."""
        self.max_caption_length = 2200  # Instagram caption limit
        self.hashtag_limit = 30  # Instagram hashtag limit
        self.gemini_client = None

        if GEMINI_AVAILABLE and config.gemini_api_key:
            genai.configure(api_key=config.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(config.gemini_model)
        
    def generate_caption(self, article: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Generate an Instagram caption from a news article and its analysis.
        
        Args:
            article: NewsArticle object containing article data
            analysis: Dictionary containing article analysis results
            
        Returns:
            Generated caption string
        """
        try:
            # Extract key information
            headline = article.headline or ''
            summary = analysis.get('summary', article.summary or '')
            keywords = analysis.get('keywords', [])
            
            # Start building the caption
            caption_parts = []
            
            # Add engaging headline
            if headline:
                caption_parts.append(f"📰 {headline}")
                caption_parts.append("")  # Empty line for spacing
            
            # Add summary
            if summary:
                caption_parts.append(summary)
                caption_parts.append("")  # Empty line for spacing
            
            # Add relevant hashtags
            hashtags = self._generate_hashtags(keywords, analysis)
            if hashtags:
                caption_parts.append(hashtags)
            
            # Join all parts
            caption = "\n".join(caption_parts)

            if self.gemini_client:
                caption = self._refine_caption_with_ai(caption)
            
            # Ensure caption doesn't exceed Instagram's limit
            if len(caption) > self.max_caption_length:
                caption = caption[:self.max_caption_length - 3] + "..."
            
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return f"📰 {article.headline or 'News Update'}"

    def _refine_caption_with_ai(self, caption: str) -> str:
        """Refine the caption using an AI model for better engagement."""
        try:
            prompt = f"""
            Refine this Instagram caption to be more engaging and impactful. Keep the core information and hashtags, but improve the tone and style for a social media audience. The caption should be easy to read and encourage interaction.

            Original caption:
            {caption}

            Refined caption:
            """

            response = self.gemini_client.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error refining caption with AI: {e}")
            return caption # Fallback to original caption
    
    def _generate_hashtags(self, keywords: List[str], analysis: Dict[str, Any]) -> str:
        """
        Generate relevant hashtags from keywords and analysis.
        
        Args:
            keywords: List of extracted keywords
            analysis: Analysis results
            
        Returns:
            String of hashtags
        """
        try:
            hashtags = set()
            
            # Add basic news hashtags
            hashtags.update(['#news', '#breaking', '#update'])
            
            # Add category-based hashtags
            category = analysis.get('category', '').lower()
            if category:
                category_hashtags = {
                    'politics': ['#politics', '#government', '#policy'],
                    'business': ['#business', '#economy', '#finance'],
                    'technology': ['#tech', '#technology', '#innovation'],
                    'health': ['#health', '#healthcare', '#medical'],
                    'sports': ['#sports', '#athletics'],
                    'entertainment': ['#entertainment', '#celebrity'],
                    'science': ['#science', '#research'],
                    'environment': ['#environment', '#climate', '#green']
                }
                hashtags.update(category_hashtags.get(category, []))
            
            # Add keyword-based hashtags (clean and format)
            for keyword in keywords[:10]:  # Limit to top 10 keywords
                if len(keyword) > 2 and keyword.isalpha():
                    clean_tag = f"#{keyword.lower().replace(' ', '')}"
                    if len(clean_tag) <= 30:  # Instagram hashtag length limit
                        hashtags.add(clean_tag)
            
            # Limit total hashtags
            hashtag_list = list(hashtags)[:self.hashtag_limit]
            
            return " ".join(hashtag_list)
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return "#news #update"
    
    def generate_story_caption(self, article: Dict[str, Any]) -> str:
        """
        Generate a shorter caption for Instagram stories.
        
        Args:
            article: NewsArticle object containing article data
            
        Returns:
            Generated story caption string
        """
        try:
            headline = article.headline or ''
            source = article.source or ''
            
            # Stories have much less text space
            if len(headline) > 80:
                headline = headline[:77] + "..."
            
            caption = f"📰 {headline}"
            if source:
                caption += f"\n\nSource: {source}"
            
            return caption
            
        except Exception as e:
            logger.error(f"Error generating story caption: {e}")
            return "📰 News Update"
    
    def generate_caption_data(self, article, template_type: str = 'feature') -> Dict[str, Any]:
        """
        Generate caption data with hashtags for Instagram post.
        
        Args:
            article: NewsArticle object containing article data
            template_type: Type of template to use for caption generation
            
        Returns:
            Dictionary containing caption and hashtags
        """
        try:
            # Create analysis dictionary for the caption generator
            analysis = {
                'summary': getattr(article, 'summary', '') or '',
                'keywords': [],  # Could be enhanced to extract keywords from content
                'sentiment': 'neutral'
            }
            
            # Generate the caption
            caption = self.generate_caption(article, analysis)
            
            # Generate hashtags based on template type and article content
            hashtags = self._generate_hashtags(analysis.get('keywords', []), analysis)
            
            return {
                'caption': caption,
                'hashtags': hashtags,
                'template_type': template_type
            }
            
        except Exception as e:
            logger.error(f"Error generating caption data: {e}")
            return {
                'caption': f"📰 {getattr(article, 'headline', 'News Update')}",
                'hashtags': '#News #Update',
                'template_type': template_type,
                'error': str(e)
            }