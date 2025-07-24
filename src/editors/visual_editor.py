"""Visual editor for advanced image editing and manipulation."""

import logging
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import cv2
import numpy as np

from ..config import config

logger = logging.getLogger(__name__)

class VisualEditor:
    """Advanced visual editor for Instagram post creation."""
    
    def __init__(self):
        self.output_dir = Path("edited")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_news_post(self, article_data: Dict[str, Any], style: str = "modern") -> Optional[str]:
        """Create a visually appealing news post."""
        try:
            # Create base canvas
            canvas = self._create_base_canvas(style)
            
            # Add background elements
            canvas = self._add_background_elements(canvas, article_data.get('category', 'general'), style)
            
            # Add headline
            canvas = self._add_headline(canvas, article_data.get('headline', ''), style)
            
            # Add summary/content
            canvas = self._add_content_text(canvas, article_data.get('summary', ''), style)
            
            # Add source and timestamp
            canvas = self._add_metadata(canvas, article_data, style)
            
            # Add category badge
            canvas = self._add_category_badge(canvas, article_data.get('category', 'general'), style)
            
            # Apply final effects
            canvas = self._apply_final_effects(canvas, style)
            
            # Save image
            output_path = self._save_image(canvas, article_data.get('article_id', 'unknown'), style)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating news post: {e}")
            return None
    
    def _create_base_canvas(self, style: str) -> Image.Image:
        """Create base canvas with appropriate dimensions."""
        width, height = 1080, 1350  # Instagram portrait ratio
        
        if style == "modern":
            # Gradient background
            canvas = Image.new('RGB', (width, height), '#FFFFFF')
            canvas = self._add_gradient_background(canvas, '#F8F9FA', '#E9ECEF')
        elif style == "bold":
            canvas = Image.new('RGB', (width, height), '#1A1A1A')
        elif style == "clean":
            canvas = Image.new('RGB', (width, height), '#FFFFFF')
        else:
            canvas = Image.new('RGB', (width, height), '#FFFFFF')
        
        return canvas
    
    def _add_gradient_background(self, canvas: Image.Image, color1: str, color2: str) -> Image.Image:
        """Add gradient background to canvas."""
        try:
            width, height = canvas.size
            
            # Create gradient
            gradient = Image.new('RGB', (width, height), color1)
            draw = ImageDraw.Draw(gradient)
            
            # Convert hex colors to RGB
            c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
            c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
            
            # Create vertical gradient
            for y in range(height):
                ratio = y / height
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            return gradient
            
        except Exception as e:
            logger.error(f"Error adding gradient background: {e}")
            return canvas
    
    def _add_background_elements(self, canvas: Image.Image, category: str, style: str) -> Image.Image:
        """Add background design elements."""
        try:
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            if style == "modern":
                # Add subtle geometric shapes
                self._add_geometric_shapes(draw, width, height, category)
            elif style == "bold":
                # Add bold accent lines
                self._add_accent_lines(draw, width, height, category)
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding background elements: {e}")
            return canvas
    
    def _add_geometric_shapes(self, draw: ImageDraw.Draw, width: int, height: int, category: str):
        """Add subtle geometric shapes to background."""
        try:
            # Category-specific colors
            colors = {
                'breaking': '#FF4444',
                'politics': '#4A90E2',
                'economy': '#50C878',
                'health': '#FF6B6B',
                'weather': '#87CEEB'
            }
            
            accent_color = colors.get(category, '#CCCCCC')
            
            # Add circles
            for i in range(3):
                x = width - 100 - (i * 30)
                y = 100 + (i * 40)
                radius = 20 - (i * 5)
                
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=accent_color + '20')  # Semi-transparent
            
        except Exception as e:
            logger.error(f"Error adding geometric shapes: {e}")
    
    def _add_accent_lines(self, draw: ImageDraw.Draw, width: int, height: int, category: str):
        """Add bold accent lines for bold style."""
        try:
            colors = {
                'breaking': '#FF0000',
                'politics': '#0066CC',
                'economy': '#00AA44',
                'health': '#FF6B6B',
                'weather': '#87CEEB'
            }
            
            accent_color = colors.get(category, '#FFFFFF')
            
            # Add vertical accent line
            draw.rectangle([50, 0, 60, height], fill=accent_color)
            
            # Add horizontal accent line
            draw.rectangle([0, 150, width, 160], fill=accent_color)
            
        except Exception as e:
            logger.error(f"Error adding accent lines: {e}")
    
    def _add_headline(self, canvas: Image.Image, headline: str, style: str) -> Image.Image:
        """Add headline text to canvas."""
        try:
            if not headline:
                return canvas
            
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            # Style-specific settings
            if style == "modern":
                font_size = 48
                color = '#2C3E50'
                y_position = 200
            elif style == "bold":
                font_size = 52
                color = '#FFFFFF'
                y_position = 180
            else:  # clean
                font_size = 44
                color = '#1A1A1A'
                y_position = 220
            
            # Load font
            font = self._load_font(font_size, 'bold')
            
            # Wrap text
            max_width = width - 100
            wrapped_lines = self._wrap_text(headline, font, max_width, draw)
            
            # Draw headline
            current_y = y_position
            line_height = int(font_size * 1.2)
            
            for line in wrapped_lines[:3]:  # Max 3 lines for headline
                # Center align
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (width - text_width) // 2
                
                draw.text((x_position, current_y), line, font=font, fill=color)
                current_y += line_height
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding headline: {e}")
            return canvas
    
    def _add_content_text(self, canvas: Image.Image, content: str, style: str) -> Image.Image:
        """Add content/summary text to canvas."""
        try:
            if not content:
                return canvas
            
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            # Style-specific settings
            if style == "modern":
                font_size = 28
                color = '#5A6C7D'
                y_position = 450
            elif style == "bold":
                font_size = 30
                color = '#E0E0E0'
                y_position = 420
            else:  # clean
                font_size = 26
                color = '#4A4A4A'
                y_position = 470
            
            # Load font
            font = self._load_font(font_size, 'normal')
            
            # Wrap text
            max_width = width - 120
            wrapped_lines = self._wrap_text(content, font, max_width, draw)
            
            # Draw content
            current_y = y_position
            line_height = int(font_size * 1.4)
            
            for line in wrapped_lines[:6]:  # Max 6 lines for content
                draw.text((60, current_y), line, font=font, fill=color)
                current_y += line_height
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding content text: {e}")
            return canvas
    
    def _add_metadata(self, canvas: Image.Image, article_data: Dict[str, Any], style: str) -> Image.Image:
        """Add source and timestamp metadata."""
        try:
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            # Style-specific settings
            if style == "modern":
                font_size = 20
                color = '#8A9BA8'
            elif style == "bold":
                font_size = 22
                color = '#B0B0B0'
            else:  # clean
                font_size = 18
                color = '#666666'
            
            # Load font
            font = self._load_font(font_size, 'normal')
            
            # Source
            source = article_data.get('source', 'Unknown Source').upper()
            draw.text((60, height - 120), f"📰 {source}", font=font, fill=color)
            
            # Timestamp
            timestamp = self._format_timestamp(article_data.get('published_date'))
            draw.text((60, height - 90), f"🕐 {timestamp}", font=font, fill=color)
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding metadata: {e}")
            return canvas
    
    def _add_category_badge(self, canvas: Image.Image, category: str, style: str) -> Image.Image:
        """Add category badge to canvas."""
        try:
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            # Category colors and emojis
            category_info = {
                'breaking': {'color': '#FF4444', 'emoji': '🚨', 'text': 'BREAKING'},
                'politics': {'color': '#4A90E2', 'emoji': '🏛️', 'text': 'POLITICS'},
                'economy': {'color': '#50C878', 'emoji': '💰', 'text': 'ECONOMY'},
                'health': {'color': '#FF6B6B', 'emoji': '��', 'text': 'HEALTH'},
                'weather': {'color': '#87CEEB', 'emoji': '🌤️', 'text': 'WEATHER'}
            }
            
            info = category_info.get(category, {'color': '#CCCCCC', 'emoji': '📰', 'text': 'NEWS'})
            
            # Badge dimensions
            badge_width = 200
            badge_height = 40
            badge_x = width - badge_width - 30
            badge_y = 30
            
            # Draw badge background
            draw.rounded_rectangle(
                [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
                radius=20,
                fill=info['color']
            )
            
            # Draw badge text
            font = self._load_font(16, 'bold')
            badge_text = f"{info['emoji']} {info['text']}"
            
            # Center text in badge
            bbox = draw.textbbox((0, 0), badge_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = badge_x + (badge_width - text_width) // 2
            text_y = badge_y + (badge_height - 16) // 2
            
            draw.text((text_x, text_y), badge_text, font=font, fill='#FFFFFF')
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding category badge: {e}")
            return canvas
    
    def _apply_final_effects(self, canvas: Image.Image, style: str) -> Image.Image:
        """Apply final visual effects."""
        try:
            if style == "modern":
                # Subtle shadow/depth effect
                enhancer = ImageEnhance.Contrast(canvas)
                canvas = enhancer.enhance(1.05)
                
            elif style == "bold":
                # Increase saturation
                enhancer = ImageEnhance.Color(canvas)
                canvas = enhancer.enhance(1.1)
                
            return canvas
            
        except Exception as e:
            logger.error(f"Error applying final effects: {e}")
            return canvas
    
    def _load_font(self, size: int, weight: str = 'normal') -> ImageFont.FreeTypeFont:
        """Load font with specified size and weight."""
        try:
            font_paths = [
                f'/usr/share/fonts/truetype/dejavu/DejaVuSans-{"Bold" if weight == "bold" else "Regular"}.ttf',
                '/System/Library/Fonts/Arial.ttf',
                '/Windows/Fonts/arial.ttf'
            ]
            
            for font_path in font_paths:
                try:
                    if Path(font_path).exists():
                        return ImageFont.truetype(font_path, size)
                except:
                    continue
            
            return ImageFont.load_default()
            
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            return ImageFont.load_default()
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """Wrap text to fit within specified width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _format_timestamp(self, published_date) -> str:
        """Format timestamp for display."""
        if not published_date:
            return "Now"
        
        from datetime import datetime
        
        if isinstance(published_date, str):
            try:
                published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            except:
                return "Now"
        
        now = datetime.utcnow()
        diff = now - published_date
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    def _save_image(self, canvas: Image.Image, article_id: str, style: str) -> str:
        """Save the final image."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_post_{article_id}_{style}_{timestamp}.jpg"
            output_path = self.output_dir / filename
            
            canvas.save(output_path, 'JPEG', quality=90, optimize=True)
            
            logger.info(f"Saved visual post: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return None
    
    def create_story_post(self, article_data: Dict[str, Any]) -> Optional[str]:
        """Create Instagram story format post."""
        try:
            # Story dimensions (9:16 ratio)
            width, height = 1080, 1920
            
            # Create canvas
            canvas = Image.new('RGB', (width, height), '#000000')
            
            # Add gradient overlay
            canvas = self._add_gradient_background(canvas, '#1A1A1A', '#2C2C2C')
            
            # Add content for story format
            canvas = self._add_story_content(canvas, article_data)
            
            # Save story image
            output_path = self._save_story_image(canvas, article_data.get('article_id', 'unknown'))
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating story post: {e}")
            return None
    
    def _add_story_content(self, canvas: Image.Image, article_data: Dict[str, Any]) -> Image.Image:
        """Add content optimized for Instagram story format."""
        try:
            draw = ImageDraw.Draw(canvas)
            width, height = canvas.size
            
            # Large headline
            headline = article_data.get('headline', '')
            if headline:
                font = self._load_font(56, 'bold')
                wrapped_lines = self._wrap_text(headline, font, width - 80, draw)
                
                current_y = 300
                for line in wrapped_lines[:4]:  # Max 4 lines
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x_position = (width - text_width) // 2
                    
                    draw.text((x_position, current_y), line, font=font, fill='#FFFFFF')
                    current_y += 70
            
            # Source at bottom
            source = article_data.get('source', '').upper()
            font = self._load_font(24, 'normal')
            draw.text((40, height - 100), f"📰 {source}", font=font, fill='#CCCCCC')
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error adding story content: {e}")
            return canvas
    
    def _save_story_image(self, canvas: Image.Image, article_id: str) -> str:
        """Save story format image."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"story_{article_id}_{timestamp}.jpg"
            output_path = self.output_dir / filename
            
            canvas.save(output_path, 'JPEG', quality=90, optimize=True)
            
            logger.info(f"Saved story post: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving story image: {e}")
            return None
