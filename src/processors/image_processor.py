"""Image processor for downloading and processing news images."""

import logging
import requests
import os
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from urllib.parse import urlparse
import hashlib

from ..config import config
from ..database import DatabaseManager

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Processes and optimizes images for Instagram posts."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.download_dir = Path("downloads/images")
        self.processed_dir = Path("processed/images")
        
        # Create directories
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Instagram image specifications
        self.target_width = config.image_max_width
        self.target_height = config.image_max_height
        self.max_file_size = 8 * 1024 * 1024  # 8MB
    
    def download_image(self, url: str, article_id: int) -> Optional[str]:
        """Download image from URL."""
        try:
            if not url:
                return None
            
            # Generate filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            parsed_url = urlparse(url)
            extension = Path(parsed_url.path).suffix or '.jpg'
            filename = f"article_{article_id}_{url_hash}{extension}"
            filepath = self.download_dir / filename
            
            # Skip if already downloaded
            if filepath.exists():
                logger.info(f"Image already downloaded: {filepath}")
                return str(filepath)
            
            # Download image
            headers = {
                'User-Agent': config.user_agent,
                'Accept': 'image/*,*/*;q=0.8',
                'Referer': url
            }
            
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                logger.warning(f"Invalid content type for image: {content_type}")
                return None
            
            # Save image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify image
            if self._verify_image(filepath):
                logger.info(f"Downloaded image: {filepath}")
                return str(filepath)
            else:
                filepath.unlink()  # Delete invalid image
                return None
                
        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            return None
    
    def _verify_image(self, filepath: Path) -> bool:
        """Verify that downloaded file is a valid image."""
        try:
            with Image.open(filepath) as img:
                img.verify()
            return True
        except Exception as e:
            logger.error(f"Invalid image file {filepath}: {e}")
            return False
    
    def process_image(self, input_path: str, article_id: int) -> Optional[str]:
        """Process image for Instagram posting."""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                logger.error(f"Input image not found: {input_path}")
                return None
            
            # Generate output filename
            output_filename = f"processed_article_{article_id}_{input_path.stem}.jpg"
            output_path = self.processed_dir / output_filename
            
            # Skip if already processed
            if output_path.exists():
                logger.info(f"Image already processed: {output_path}")
                return str(output_path)
            
            # Open and process image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize image
                processed_img = self._resize_for_instagram(img)
                
                # Enhance image
                processed_img = self._enhance_image(processed_img)
                
                # Save processed image
                processed_img.save(
                    output_path,
                    'JPEG',
                    quality=85,
                    optimize=True
                )
                
                logger.info(f"Processed image: {output_path}")
                return str(output_path)
                
        except Exception as e:
            logger.error(f"Error processing image {input_path}: {e}")
            return None
    
    def _resize_for_instagram(self, img: Image.Image) -> Image.Image:
        """Resize image for Instagram format."""
        try:
            original_width, original_height = img.size
            
            # Calculate target dimensions maintaining aspect ratio
            aspect_ratio = original_width / original_height
            target_aspect = self.target_width / self.target_height
            
            if aspect_ratio > target_aspect:
                # Image is wider, fit to width
                new_width = self.target_width
                new_height = int(self.target_width / aspect_ratio)
            else:
                # Image is taller, fit to height
                new_height = self.target_height
                new_width = int(self.target_height * aspect_ratio)
            
            # Resize image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create canvas with target dimensions
            canvas = Image.new('RGB', (self.target_width, self.target_height), (255, 255, 255))
            
            # Center the resized image on canvas
            x_offset = (self.target_width - new_width) // 2
            y_offset = (self.target_height - new_height) // 2
            canvas.paste(resized_img, (x_offset, y_offset))
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return img
    
    def _enhance_image(self, img: Image.Image) -> Image.Image:
        """Enhance image quality."""
        try:
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            # Enhance color saturation slightly
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.05)
            
            # Enhance sharpness slightly
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
            
            return img
            
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return img
    
    def create_news_graphic(self, headline: str, category: str, template_name: str = "feature_story") -> Optional[str]:
        """Create a news graphic with text overlay."""
        try:
            # Load template configuration
            template_config = config.get_template_config(template_name)
            if not template_config:
                logger.error(f"Template configuration not found: {template_name}")
                return None
            
            # Create base image
            dimensions = template_config.get('dimensions', [1080, 1350])
            img = Image.new('RGB', dimensions, (255, 255, 255))
            
            # Add background gradient or color
            img = self._add_background(img, category)
            
            # Add text elements
            img = self._add_text_overlay(img, headline, template_config)
            
            # Save graphic
            output_filename = f"graphic_{category}_{hashlib.md5(headline.encode()).hexdigest()[:8]}.jpg"
            output_path = self.processed_dir / output_filename
            
            img.save(output_path, 'JPEG', quality=90, optimize=True)
            
            logger.info(f"Created news graphic: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error creating news graphic: {e}")
            return None
    
    def _add_background(self, img: Image.Image, category: str) -> Image.Image:
        """Add background based on category."""
        try:
            # Get category colors from config
            template_config = config.template_config
            colors = template_config.get('colors', {})
            
            # Choose background color based on category
            color_map = {
                'breaking': colors.get('breaking', '#FF0000'),
                'politics': colors.get('analysis', '#0066CC'),
                'economy': colors.get('analysis', '#0066CC'),
                'health': colors.get('feature', '#00AA44'),
                'weather': colors.get('feature', '#00AA44')
            }
            
            bg_color = color_map.get(category, '#FFFFFF')
            
            # Create gradient background
            width, height = img.size
            gradient = Image.new('RGB', (width, height), bg_color)
            
            # Blend with original
            img = Image.blend(img, gradient, 0.3)
            
            return img
            
        except Exception as e:
            logger.error(f"Error adding background: {e}")
            return img
    
    def _add_text_overlay(self, img: Image.Image, headline: str, template_config: Dict) -> Image.Image:
        """Add text overlay to image."""
        try:
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(img)
            
            # Get text areas configuration
            text_areas = template_config.get('text_areas', {})
            headline_config = text_areas.get('headline', {})
            
            # Load font (fallback to default if font file not found)
            try:
                font_size = headline_config.get('font_size', 48)
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
            except:
                font = ImageFont.load_default()
            
            # Get text properties
            position = headline_config.get('position', [50, 200])
            max_width = headline_config.get('max_width', 980)
            color = headline_config.get('color', '#000000')
            
            # Wrap text to fit width
            wrapped_text = self._wrap_text(headline, font, max_width, draw)
            
            # Draw text
            y_position = position[1]
            for line in wrapped_text:
                draw.text((position[0], y_position), line, font=font, fill=color)
                y_position += font_size + 10  # Line spacing
            
            return img
            
        except Exception as e:
            logger.error(f"Error adding text overlay: {e}")
            return img
    
    def _wrap_text(self, text: str, font, max_width: int, draw) -> list:
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
                    lines.append(word)  # Single word too long
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def optimize_for_instagram(self, image_path: str) -> Optional[str]:
        """Final optimization for Instagram posting."""
        try:
            input_path = Path(image_path)
            if not input_path.exists():
                return None
            
            output_path = input_path.parent / f"optimized_{input_path.name}"
            
            with Image.open(input_path) as img:
                # Ensure RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Ensure correct dimensions
                if img.size != (self.target_width, self.target_height):
                    img = img.resize((self.target_width, self.target_height), Image.Resampling.LANCZOS)
                
                # Save with optimal settings for Instagram
                img.save(
                    output_path,
                    'JPEG',
                    quality=95,
                    optimize=True,
                    progressive=True
                )
            
            # Check file size
            if output_path.stat().st_size > self.max_file_size:
                # Reduce quality if file is too large
                with Image.open(output_path) as img:
                    img.save(output_path, 'JPEG', quality=80, optimize=True)
            
            logger.info(f"Optimized image for Instagram: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error optimizing image: {e}")
            return None
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get information about an image."""
        try:
            path = Path(image_path)
            if not path.exists():
                return {}
            
            with Image.open(path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'mode': img.mode,
                    'format': img.format,
                    'file_size': path.stat().st_size,
                    'aspect_ratio': img.width / img.height
                }
                
        except Exception as e:
            logger.error(f"Error getting image info: {e}")
            return {}
    
    def cleanup_old_images(self, days_old: int = 7) -> Dict[str, int]:
        """Clean up old downloaded and processed images."""
        try:
            from datetime import datetime, timedelta
            
            cutoff_time = datetime.now() - timedelta(days=days_old)
            stats = {'deleted_downloads': 0, 'deleted_processed': 0}
            
            # Clean download directory
            for image_file in self.download_dir.glob('*'):
                if image_file.is_file():
                    file_time = datetime.fromtimestamp(image_file.stat().st_mtime)
                    if file_time < cutoff_time:
                        image_file.unlink()
                        stats['deleted_downloads'] += 1
            
            # Clean processed directory
            for image_file in self.processed_dir.glob('*'):
                if image_file.is_file():
                    file_time = datetime.fromtimestamp(image_file.stat().st_mtime)
                    if file_time < cutoff_time:
                        image_file.unlink()
                        stats['deleted_processed'] += 1
            
            logger.info(f"Cleaned up old images: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error cleaning up images: {e}")
            return {'error': str(e)}
