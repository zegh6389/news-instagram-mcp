"""Content analyzer for processing and categorizing news articles."""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

from ..config import config
from ..database import DatabaseManager, NewsArticle, ArticleStatus

logger = logging.getLogger(__name__)

class ContentAnalyzer:
    """Analyzes and processes news article content."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.categories = config.get_categories()
        self.content_filters = config.get_content_filters()
        
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_client = None
        
        if OPENAI_AVAILABLE and config.openai_api_key:
            openai.api_key = config.openai_api_key
            self.openai_client = openai
        
        if ANTHROPIC_AVAILABLE and config.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=config.anthropic_api_key)

        if GEMINI_AVAILABLE and config.gemini_api_key:
            genai.configure(api_key=config.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(config.gemini_model)
    
    def analyze_article(self, article: NewsArticle) -> Dict[str, Any]:
        """Analyze a news article and extract insights."""
        try:
            analysis = {
                'article_id': article.id,
                'timestamp': datetime.utcnow().isoformat(),
                'category': self._categorize_article(article),
                'sentiment': self._analyze_sentiment(article),
                'keywords': self._extract_keywords(article),
                'importance_score': self._calculate_importance_score(article),
                'readability_score': self._calculate_readability_score(article),
                'summary': self._generate_summary(article),
                'key_points': self._extract_key_points(article),
                'entities': self._extract_entities(article),
                'content_quality': self._assess_content_quality(article)
            }
            
            logger.info(f"Analyzed article {article.id}: {article.headline}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing article {article.id}: {e}")
            return {'error': str(e)}
    
    def _categorize_article(self, article: NewsArticle) -> str:
        """Categorize article based on content."""
        text = (article.headline + " " + article.content).lower()
        
        # Check each category
        for category, category_config in self.categories.items():
            keywords = category_config.get('keywords', [])
            keyword_matches = sum(1 for keyword in keywords if keyword.lower() in text)
            
            # If significant number of keywords match, assign category
            if keyword_matches >= len(keywords) * 0.3:  # 30% threshold
                return category
        
        # Use AI for categorization if available
        if self.openai_client or self.anthropic_client or self.gemini_client:
            ai_category = self._ai_categorize_article(article)
            if ai_category:
                return ai_category
        
        return article.category or 'general'
    
    def _ai_categorize_article(self, article: NewsArticle) -> Optional[str]:
        """Use AI to categorize article."""
        try:
            categories_list = list(self.categories.keys())
            
            prompt = f"""
            Categorize this news article into one of these categories: {', '.join(categories_list)}
            
            Headline: {article.headline}
            Content: {article.content[:500]}...
            
            Return only the category name, nothing else.
            """
            
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model=config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                    temperature=0.1
                )
                category = response.choices[0].message.content.strip().lower()
                if category in categories_list:
                    return category
            
            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=50,
                    messages=[{"role": "user", "content": prompt}]
                )
                category = response.content[0].text.strip().lower()
                if category in categories_list:
                    return category
            
            elif self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                category = response.text.strip().lower()
                if category in categories_list:
                    return category
                    
        except Exception as e:
            logger.error(f"Error in AI categorization: {e}")
        
        return None
    
    def _analyze_sentiment(self, article: NewsArticle) -> Dict[str, Any]:
        """Analyze sentiment of the article."""
        sentiment_data = {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'classification': 'neutral'
        }
        
        try:
            if TEXTBLOB_AVAILABLE:
                # Use TextBlob for basic sentiment analysis
                blob = TextBlob(article.content)
                sentiment_data['polarity'] = blob.sentiment.polarity
                sentiment_data['subjectivity'] = blob.sentiment.subjectivity
                
                # Classify sentiment
                if sentiment_data['polarity'] > 0.1:
                    sentiment_data['classification'] = 'positive'
                elif sentiment_data['polarity'] < -0.1:
                    sentiment_data['classification'] = 'negative'
                else:
                    sentiment_data['classification'] = 'neutral'
            
            # Use AI for more detailed sentiment analysis
            if self.openai_client or self.anthropic_client or self.gemini_client:
                ai_sentiment = self._ai_analyze_sentiment(article)
                if ai_sentiment:
                    sentiment_data.update(ai_sentiment)
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
        
        return sentiment_data
    
    def _ai_analyze_sentiment(self, article: NewsArticle) -> Optional[Dict[str, Any]]:
        """Use AI for detailed sentiment analysis."""
        try:
            prompt = f"""
            Analyze the sentiment and emotional tone of this news article. Return a JSON object with:
            - overall_sentiment: positive/negative/neutral
            - emotional_tone: angry/sad/hopeful/concerned/excited/etc.
            - urgency_level: low/medium/high
            - impact_level: local/regional/national/international
            
            Headline: {article.headline}
            Content: {article.content[:1000]}...
            """
            
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model=config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.1
                )
                result = response.choices[0].message.content.strip()
                return json.loads(result)
            
            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text.strip()
                return json.loads(result)

            elif self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                result = response.text.strip()
                return json.loads(result)
                
        except Exception as e:
            logger.error(f"Error in AI sentiment analysis: {e}")
        
        return None
    
    def _extract_keywords(self, article: NewsArticle) -> List[str]:
        """Extract keywords from article content."""
        keywords = []
        
        try:
            text = (article.headline + " " + article.content).lower()
            
            # Predefined important keywords
            important_keywords = [
                'breaking', 'urgent', 'alert', 'developing', 'exclusive',
                'government', 'politics', 'election', 'parliament', 'minister',
                'trudeau', 'singh', 'poilievre', 'conservative', 'liberal', 'ndp',
                'economy', 'inflation', 'recession', 'gdp', 'unemployment',
                'healthcare', 'hospital', 'covid', 'pandemic', 'vaccine',
                'climate', 'environment', 'carbon', 'emissions', 'temperature',
                'housing', 'mortgage', 'rental', 'affordability',
                'immigration', 'refugee', 'border', 'visa',
                'education', 'university', 'school', 'student',
                'technology', 'ai', 'cyber', 'digital', 'internet'
            ]
            
            # Find matching keywords
            for keyword in important_keywords:
                if keyword in text:
                    keywords.append(keyword)
            
            # Extract proper nouns (potential entities)
            proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', article.content)
            keywords.extend(proper_nouns[:10])  # Limit to 10
            
            # Use AI for advanced keyword extraction
            if self.openai_client or self.anthropic_client or self.gemini_client:
                ai_keywords = self._ai_extract_keywords(article)
                if ai_keywords:
                    keywords.extend(ai_keywords)
            
            # Remove duplicates and return
            return list(set(keywords))
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return keywords
    
    def _ai_extract_keywords(self, article: NewsArticle) -> Optional[List[str]]:
        """Use AI to extract keywords."""
        try:
            prompt = f"""
            Extract the 10 most important keywords and phrases from this news article.
            Focus on: people, places, organizations, events, topics, and key concepts.
            Return as a JSON array of strings.
            
            Headline: {article.headline}
            Content: {article.content[:1000]}...
            """
            
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model=config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.1
                )
                result = response.choices[0].message.content.strip()
                return json.loads(result)

            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text.strip()
                return json.loads(result)

            elif self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                result = response.text.strip()
                return json.loads(result)
                
        except Exception as e:
            logger.error(f"Error in AI keyword extraction: {e}")
        
        return None
    
    def _calculate_importance_score(self, article: NewsArticle) -> float:
        """Calculate importance score for the article."""
        score = 0.0
        
        try:
            text = (article.headline + " " + article.content).lower()
            
            # Breaking news indicators
            breaking_keywords = ['breaking', 'urgent', 'alert', 'developing', 'exclusive']
            for keyword in breaking_keywords:
                if keyword in text:
                    score += 2.0
            
            # Government/political importance
            political_keywords = ['government', 'minister', 'parliament', 'election', 'trudeau']
            for keyword in political_keywords:
                if keyword in text:
                    score += 1.5
            
            # Economic importance
            economic_keywords = ['economy', 'inflation', 'recession', 'market', 'unemployment']
            for keyword in economic_keywords:
                if keyword in text:
                    score += 1.2
            
            # Health importance
            health_keywords = ['health', 'hospital', 'covid', 'pandemic', 'outbreak']
            for keyword in health_keywords:
                if keyword in text:
                    score += 1.0
            
            # Recency bonus
            if article.published_date:
                hours_old = (datetime.utcnow() - article.published_date).total_seconds() / 3600
                if hours_old < 2:
                    score += 1.0
                elif hours_old < 6:
                    score += 0.5
            
            # Content length factor
            word_count = len(article.content.split())
            if word_count > 500:
                score += 0.5
            
            # Normalize score to 0-10 range
            score = min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error calculating importance score: {e}")
        
        return score
    
    def _calculate_readability_score(self, article: NewsArticle) -> float:
        """Calculate readability score using Flesch Reading Ease."""
        try:
            text = article.content
            
            # Count sentences, words, and syllables
            sentences = len(re.findall(r'[.!?]+', text))
            words = len(text.split())
            syllables = self._count_syllables(text)
            
            if sentences == 0 or words == 0:
                return 0.0
            
            # Flesch Reading Ease formula
            score = 206.835 - (1.015 * words / sentences) - (84.6 * syllables / words)
            
            # Normalize to 0-100 scale
            return max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"Error calculating readability: {e}")
            return 0.0
    
    def _count_syllables(self, text: str) -> int:
        """Count syllables in text (approximation)."""
        try:
            # Simple syllable counting heuristic
            text = text.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in text:
                if char in vowels:
                    if not prev_was_vowel:
                        syllable_count += 1
                    prev_was_vowel = True
                else:
                    prev_was_vowel = False
            
            # Adjust for silent 'e'
            if text.endswith('e'):
                syllable_count -= 1
            
            # Ensure at least 1 syllable per word
            word_count = len(text.split())
            return max(syllable_count, word_count)
            
        except Exception as e:
            logger.error(f"Error counting syllables: {e}")
            return len(text.split())  # Fallback to word count
    
    def _generate_summary(self, article: NewsArticle) -> str:
        """Generate a concise summary of the article."""
        try:
            # Use AI for summary generation if available
            if self.openai_client or self.anthropic_client or self.gemini_client:
                ai_summary = self._ai_generate_summary(article)
                if ai_summary:
                    return ai_summary
            
            # Fallback to simple summary
            return self._simple_summary(article.content)
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return article.summary or ""
    
    def _ai_generate_summary(self, article: NewsArticle) -> Optional[str]:
        """Use AI to generate article summary."""
        try:
            prompt = f"""
            Create a concise 2-3 sentence summary of this news article suitable for social media.
            Focus on the key facts and main points.
            
            Headline: {article.headline}
            Content: {article.content}
            """
            
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model=config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()

            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()

            elif self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            logger.error(f"Error in AI summary generation: {e}")
        
        return None
    
    def _simple_summary(self, content: str, max_sentences: int = 3) -> str:
        """Generate simple summary from first few sentences."""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences)
        
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def _extract_key_points(self, article: NewsArticle) -> List[str]:
        """Extract key points from the article."""
        try:
            # Use AI for key point extraction if available
            if self.openai_client or self.anthropic_client or self.gemini_client:
                ai_points = self._ai_extract_key_points(article)
                if ai_points:
                    return ai_points
            
            # Fallback to simple extraction
            return self._simple_key_points(article.content)
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []
    
    def _ai_extract_key_points(self, article: NewsArticle) -> Optional[List[str]]:
        """Use AI to extract key points."""
        try:
            prompt = f"""
            Extract 3-5 key points from this news article as bullet points.
            Each point should be a concise, factual statement.
            Return as a JSON array of strings.
            
            Headline: {article.headline}
            Content: {article.content}
            """
            
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model=config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.2
                )
                result = response.choices[0].message.content.strip()
                return json.loads(result)

            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text.strip()
                return json.loads(result)

            elif self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                result = response.text.strip()
                return json.loads(result)
                
        except Exception as e:
            logger.error(f"Error in AI key point extraction: {e}")
        
        return None
    
    def _simple_key_points(self, content: str) -> List[str]:
        """Extract simple key points from content."""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 30]
        
        # Take every 3rd sentence as a key point
        key_points = []
        for i in range(0, min(15, len(sentences)), 3):
            if sentences[i]:
                key_points.append(sentences[i])
        
        return key_points[:5]  # Limit to 5 points
    
    def _extract_entities(self, article: NewsArticle) -> Dict[str, List[str]]:
        """Extract named entities from the article."""
        entities = {
            'people': [],
            'places': [],
            'organizations': [],
            'dates': []
        }
        
        try:
            # Simple regex-based entity extraction
            text = article.content
            
            # Extract potential person names (capitalized words)
            people = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
            entities['people'] = list(set(people))[:10]
            
            # Extract potential place names
            places = re.findall(r'\b(?:in|at|from|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', text)
            entities['places'] = list(set(places))[:10]
            
            # Extract dates
            dates = re.findall(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', text)
            entities['dates'] = list(set(dates))[:5]
            
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
        
        return entities
    
    def _assess_content_quality(self, article: NewsArticle) -> Dict[str, Any]:
        """Assess the quality of the article content."""
        quality = {
            'score': 0.0,
            'issues': [],
            'strengths': []
        }
        
        try:
            content = article.content
            headline = article.headline
            
            # Check content length
            word_count = len(content.split())
            if word_count < 100:
                quality['issues'].append('Content too short')
                quality['score'] -= 2.0
            elif word_count > 300:
                quality['strengths'].append('Comprehensive content')
                quality['score'] += 1.0
            
            # Check headline quality
            if len(headline.split()) < 5:
                quality['issues'].append('Headline too short')
                quality['score'] -= 1.0
            elif len(headline.split()) > 15:
                quality['issues'].append('Headline too long')
                quality['score'] -= 0.5
            else:
                quality['strengths'].append('Good headline length')
                quality['score'] += 0.5
            
            # Check for author
            if article.author:
                quality['strengths'].append('Has author attribution')
                quality['score'] += 0.5
            else:
                quality['issues'].append('No author attribution')
                quality['score'] -= 0.5
            
            # Check for image
            if article.image_url:
                quality['strengths'].append('Has accompanying image')
                quality['score'] += 0.5
            
            # Check for recency
            if article.published_date:
                hours_old = (datetime.utcnow() - article.published_date).total_seconds() / 3600
                if hours_old < 24:
                    quality['strengths'].append('Recent content')
                    quality['score'] += 1.0
                elif hours_old > 72:
                    quality['issues'].append('Content is old')
                    quality['score'] -= 1.0
            
            # Normalize score
            quality['score'] = max(0, min(10, quality['score'] + 5))  # Base score of 5
            
        except Exception as e:
            logger.error(f"Error assessing content quality: {e}")
        
        return quality
    
    def process_articles(self, limit: Optional[int] = None) -> Dict[str, int]:
        """Process articles that need analysis."""
        try:
            # Get articles that need processing
            articles = self.db_manager.get_articles_by_status(ArticleStatus.SCRAPED, limit)
            
            stats = {
                'processed': 0,
                'failed': 0,
                'skipped': 0
            }
            
            for article in articles:
                try:
                    # Check content filters
                    if not self._passes_content_filters(article):
                        self.db_manager.update_article_status(
                            article.id, 
                            ArticleStatus.SKIPPED, 
                            "Failed content filters"
                        )
                        stats['skipped'] += 1
                        continue
                    
                    # Analyze article
                    analysis = self.analyze_article(article)
                    
                    if 'error' in analysis:
                        self.db_manager.update_article_status(
                            article.id, 
                            ArticleStatus.FAILED, 
                            f"Analysis failed: {analysis['error']}"
                        )
                        stats['failed'] += 1
                    else:
                        # Update article with analysis results
                        article.category = analysis['category']
                        article.keywords = analysis['keywords']
                        article.summary = analysis['summary']
                        
                        self.db_manager.update_article_status(
                            article.id, 
                            ArticleStatus.PROCESSED, 
                            f"Analysis completed. Score: {analysis.get('importance_score', 0)}"
                        )
                        stats['processed'] += 1
                        
                except Exception as e:
                    logger.error(f"Error processing article {article.id}: {e}")
                    self.db_manager.update_article_status(
                        article.id, 
                        ArticleStatus.FAILED, 
                        f"Processing error: {str(e)}"
                    )
                    stats['failed'] += 1
            
            logger.info(f"Content analysis completed: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error in process_articles: {e}")
            return {'error': str(e)}
    
    def _passes_content_filters(self, article: NewsArticle) -> bool:
        """Check if article passes content filters."""
        try:
            content = article.content.lower()
            headline = article.headline.lower()
            text = content + " " + headline
            
            # Check minimum word count
            min_word_count = self.content_filters.get('min_word_count', 100)
            if len(article.content.split()) < min_word_count:
                return False
            
            # Check maximum age
            max_age_hours = self.content_filters.get('max_age_hours', 24)
            if article.published_date:
                hours_old = (datetime.utcnow() - article.published_date).total_seconds() / 3600
                if hours_old > max_age_hours:
                    return False
            
            # Check exclude keywords
            exclude_keywords = self.content_filters.get('exclude_keywords', [])
            if any(keyword.lower() in text for keyword in exclude_keywords):
                return False
            
            # Check required keywords
            required_keywords = self.content_filters.get('required_keywords', [])
            if required_keywords:
                if not any(keyword.lower() in text for keyword in required_keywords):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking content filters: {e}")
            return False