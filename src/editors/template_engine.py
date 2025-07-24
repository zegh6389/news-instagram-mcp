"""Template engine for creating visual Instagram posts."""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

from ..config import config

logger = logging.getLogger(__name__)

class TemplateEngine:
    """Engine for creating Instagram posts from templates."""
    
    def __init__(self):
        self.template_config = config.template_config
        self.templates_dir = Path("templates")
        self.output_dir = Path("generated")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_post_from_template(self, template_name: str, content_data: Dict[str, Any]) -> Optional[str]:
        """Create an Instagram post from a template."""
        try:
            template_config = self.template_config.get('templates', {}).get(template_name)
            if not template_config:
                logger.error(f"Template not found: {template_name}")
                return None
            
            # Load base template
            base_image = self._load_base_template(template_name, template_config)
            if not base_image:
                return None
            
            # Apply content to template
            final_image = self._apply_content_to_template(base_image, template_config, content_data)
            
            # Save final image
            output_path = self._save_final_image(final_image, template_name, content_data)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating post from template {template_name}: {e}")
            return None
    
    def _load_base_template(self, template_name: str, template_config: Dict[str, Any]) -> Optional[Image.Image]:
        """Load the base template image."""
        try:
            template_file = template_config.get('file')
            if template_file:
                template_path = self.templates_dir / template_file
                if template_path.exists():
                    return Image.open(template_path)
            
            # Create blank template with configured dimensions
            dimensions = template_config.get('dimensions', [1080, 1350])
            background_color = self._get_background_color(template_name)
            
            return Image.new('RGB', dimensions, background_color)
            
        except Exception as e:
            logger.error(f"Error loading base template: {e}")
            return None
    
    def _get_background_color(self, template_name: str) -> tuple:
        """Get background color for template."""
        colors = self.template_config.get('colors', {})
        
        color_map = {
            'breaking_news': colors.get('breaking', '#FF0000'),
            'analysis_post': colors.get('analysis', '#0066CC'),
            'feature_story': colors.get('feature', '#00AA44')
        }
        
        hex_color = color_map.get(template_name, colors.get('background', '#FFFFFF'))
        
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _apply_content_to_template(self, image: Image.Image, template_config: Dict[str, Any], content_data: Dict[str, Any]) -> Image.Image:
        """Apply content data to template image."""
        try:
            draw = ImageDraw.Draw(image)
            text_areas = template_config.get('text_areas', {})
            
            for area_name, area_config in text_areas.items():
                content_key = area_name
                if content_key in content_data:
                    self._draw_text_area(draw, area_config, content_data[content_key], image.size)
            
            return image
            
        except Exception as e:
            logger.error(f"Error applying content to template: {e}")
            return image
    
    def _draw_text_area(self, draw: ImageDraw.Draw, area_config: Dict[str, Any], text: str, image_size: tuple):
        """Draw text in a specific area of the image."""
        try:
            if not text:
                return
            
            # Get area configuration
            position = area_config.get('position', [50, 50])
            max_width = area_config.get('max_width', image_size[0] - 100)
            font_size = area_config.get('font_size', 32)
            color = area_config.get('color', '#000000')
            font_weight = area_config.get('font_weight', 'normal')
            line_height = area_config.get('line_height', 1.2)
            
            # Load font
            font = self._load_font(font_size, font_weight)
            
            # Wrap text
            wrapped_lines = self._wrap_text(text, font, max_width, draw)
            
            # Draw text lines
            y_position = position[1]
            line_spacing = int(font_size * line_height)
            
            for line in wrapped_lines:
                draw.text((position[0], y_position), line, font=font, fill=color)
                y_position += line_spacing
            
        except Exception as e:
            logger.error(f"Error drawing text area: {e}")
    
    def _load_font(self, font_size: int, font_weight: str = 'normal') -> ImageFont.FreeTypeFont:
        """Load font with specified size and weight."""
        try:
            # Try to load system fonts
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if font_weight == 'bold' else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/System/Library/Fonts/Arial.ttf',
                '/Windows/Fonts/arial.ttf'
            ]
            
            for font_path in font_paths:
                try:
                    if Path(font_path).exists():
                        return ImageFont.truetype(font_path, font_size)
                except:
                    continue
            
            # Fallback to default font
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
                    # Single word too long, add anyway
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _save_final_image(self, image: Image.Image, template_name: str, content_data: Dict[str, Any]) -> str:
        """Save the final processed image."""
        try:
            # Generate filename
            article_id = content_data.get('article_id', 'unknown')
            timestamp = content_data.get('timestamp', 'now')
            filename = f"{template_name}_{article_id}_{timestamp}.jpg"
            
            output_path = self.output_dir / filename
            
            # Save image
            image.save(output_path, 'JPEG', quality=90, optimize=True)
            
            logger.info(f"Saved template image: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving final image: {e}")
            return None
    
    def get_available_templates(self) -> List[str]:
        """Get list of available templates."""
        return list(self.template_config.get('templates', {}).keys())
    
    def validate_template_data(self, template_name: str, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content data for template."""
        validation = {
            'is_valid': True,
            'missing_fields': [],
            'warnings': []
        }
        
        try:
            template_config = self.template_config.get('templates', {}).get(template_name)
            if not template_config:
                validation['is_valid'] = False
                validation['missing_fields'].append('template_config')
                return validation
            
            text_areas = template_config.get('text_areas', {})
            
            for area_name in text_areas.keys():
                if area_name not in content_data:
                    validation['missing_fields'].append(area_name)
                elif not content_data[area_name]:
                    validation['warnings'].append(f'{area_name} is empty')
            
            if validation['missing_fields']:
                validation['is_valid'] = False
            
        except Exception as e:
            logger.error(f"Error validating template data: {e}")
            validation['is_valid'] = False
            validation['missing_fields'].append('validation_error')
        
        return validation
