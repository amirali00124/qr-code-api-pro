import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os

# Try to import advanced styling features, fallback to basic if not available
try:
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer
    ADVANCED_STYLING = True
except ImportError:
    ADVANCED_STYLING = False

class QRCodeGenerator:
    def __init__(self):
        self.default_options = {
            'size': 10,
            'border': 4,
            'error_correction': 'M',
            'format': 'PNG',
            'foreground_color': '#000000',
            'background_color': '#FFFFFF',
            'module_drawer': 'square',
            'logo_path': None,
            'logo_size_ratio': 0.3
        }
    
    def _get_error_correction_level(self, level):
        """Convert string error correction level to qrcode constant"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,  # ~7%
            'M': qrcode.constants.ERROR_CORRECT_M,  # ~15%
            'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
            'H': qrcode.constants.ERROR_CORRECT_H   # ~30%
        }
        return levels.get(level.upper(), qrcode.constants.ERROR_CORRECT_M)
    
    def _get_module_drawer(self, drawer_type):
        """Get module drawer based on type"""
        if not ADVANCED_STYLING:
            return None
        
        drawers = {
            'square': SquareModuleDrawer(),
            'rounded': RoundedModuleDrawer(), 
            'circle': CircleModuleDrawer()
        }
        return drawers.get(drawer_type.lower(), SquareModuleDrawer())
    
    def _create_qr_code(self, data, options):
        """Create base QR code with given data and options"""
        merged_options = {**self.default_options, **options}
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=self._get_error_correction_level(merged_options['error_correction']),
            box_size=merged_options['size'],
            border=merged_options['border'],
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Try advanced styling first, fallback to basic if colors don't work
        if ADVANCED_STYLING and merged_options['module_drawer'] != 'square':
            try:
                module_drawer = self._get_module_drawer(merged_options['module_drawer'])
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=module_drawer,
                    fill_color=merged_options['foreground_color'],
                    back_color=merged_options['background_color']
                )
                
                # Verify colors were applied correctly by checking a corner pixel
                test_pixel = img.getpixel((5, 5))
                # If pixel is not the expected background color, fallback to basic
                expected_bg = merged_options['background_color']
                if (expected_bg != '#FFFFFF' and expected_bg != '#ffffff' and 
                    test_pixel == (255, 255, 255)):
                    # Colors weren't applied properly, use basic generation
                    raise Exception("Colors not applied with StyledPilImage")
                    
            except Exception as e:
                logging.warning(f"Advanced styling failed, using basic: {str(e)}")
                # Fallback to basic generation
                img = qr.make_image(
                    fill_color=merged_options['foreground_color'],
                    back_color=merged_options['background_color']
                )
        else:
            # Use basic image generation for square modules or when advanced styling unavailable
            img = qr.make_image(
                fill_color=merged_options['foreground_color'],
                back_color=merged_options['background_color']
            )
        
        # Add logo if specified
        if merged_options.get('logo_path'):
            img = self._add_logo(img, merged_options['logo_path'], merged_options['logo_size_ratio'])
        
        return img
    
    def _add_logo(self, qr_img, logo_path, size_ratio=0.3):
        """Add logo to QR code image"""
        try:
            logo = Image.open(logo_path)
            
            # Calculate logo size
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * size_ratio)
            
            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Create a white background for the logo
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg.paste(logo, (10, 10))
            
            # Calculate position to center the logo
            pos = ((qr_width - logo_size - 20) // 2, (qr_height - logo_size - 20) // 2)
            
            # Paste logo onto QR code
            qr_img.paste(logo_bg, pos)
            
            return qr_img
        except Exception as e:
            logging.warning(f"Failed to add logo: {str(e)}")
            return qr_img
    
    def _image_to_base64(self, img, format='PNG'):
        """Convert PIL image to base64 string"""
        buffer = io.BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/{format.lower()};base64,{img_base64}"
    
    def _generate_svg(self, data, options):
        """Generate SVG format QR code"""
        merged_options = {**self.default_options, **options}
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=self._get_error_correction_level(merged_options['error_correction']),
            box_size=merged_options['size'],
            border=merged_options['border'],
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Get the QR code matrix
        matrix = qr.get_matrix()
        size = merged_options['size']
        border = merged_options['border']
        
        # Calculate SVG dimensions
        matrix_size = len(matrix)
        total_size = (matrix_size + 2 * border) * size
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_size}" height="{total_size}" viewBox="0 0 {total_size} {total_size}">
<rect width="{total_size}" height="{total_size}" fill="{merged_options['background_color']}"/>'''

        # Add QR code modules
        for row in range(matrix_size):
            for col in range(matrix_size):
                if matrix[row][col]:
                    x = (col + border) * size
                    y = (row + border) * size
                    
                    if merged_options['module_drawer'] == 'circle':
                        radius = size // 2
                        cx = x + radius
                        cy = y + radius
                        svg_content += f'\n<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{merged_options["foreground_color"]}"/>'
                    elif merged_options['module_drawer'] == 'rounded':
                        rx = ry = size // 4
                        svg_content += f'\n<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx}" ry="{ry}" fill="{merged_options["foreground_color"]}"/>'
                    else:  # square
                        svg_content += f'\n<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{merged_options["foreground_color"]}"/>'
        
        svg_content += '\n</svg>'
        
        return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"
    
    def _generate_pdf(self, data, options):
        """Generate PDF format QR code"""
        merged_options = {**self.default_options, **options}
        
        # Create QR code image first
        img = self._create_qr_code(data, merged_options)
        
        # Create temporary file for the image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
            img.save(temp_img.name, 'PNG')
            temp_img_path = temp_img.name
        
        # Create PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # Calculate position to center QR code
        page_width, page_height = letter
        img_width = img_height = 200  # Fixed size for PDF
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2
        
        # Draw QR code on PDF
        c.drawImage(temp_img_path, x, y, width=img_width, height=img_height)
        c.save()
        
        # Clean up temporary file
        os.unlink(temp_img_path)
        
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
        return f"data:application/pdf;base64,{pdf_base64}"
    
    def _generate_response(self, data, options):
        """Generate response with multiple formats"""
        merged_options = {**self.default_options, **options}
        format_type = merged_options['format'].upper()
        
        response = {
            'success': True,
            'data': {
                'content': data,
                'options': merged_options
            }
        }
        
        if format_type == 'SVG':
            response['data']['qr_code'] = self._generate_svg(data, options)
            response['data']['format'] = 'SVG'
        elif format_type == 'PDF':
            response['data']['qr_code'] = self._generate_pdf(data, options)
            response['data']['format'] = 'PDF'
        else:  # Default to PNG
            img = self._create_qr_code(data, options)
            response['data']['qr_code'] = self._image_to_base64(img, 'PNG')
            response['data']['format'] = 'PNG'
        
        return response
    
    def generate_url_qr(self, url, options=None):
        """Generate QR code for URL"""
        if options is None:
            options = {}
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return self._generate_response(url, options)
    
    def generate_text_qr(self, text, options=None):
        """Generate QR code for plain text"""
        if options is None:
            options = {}
        
        return self._generate_response(text, options)
    
    def generate_email_qr(self, email, subject='', message='', options=None):
        """Generate QR code for email"""
        if options is None:
            options = {}
        
        # Create mailto URL
        mailto_url = f"mailto:{email}"
        params = []
        
        if subject:
            params.append(f"subject={subject}")
        if message:
            params.append(f"body={message}")
        
        if params:
            mailto_url += "?" + "&".join(params)
        
        return self._generate_response(mailto_url, options)
    
    def generate_phone_qr(self, phone, options=None):
        """Generate QR code for phone number"""
        if options is None:
            options = {}
        
        # Create tel URL
        tel_url = f"tel:{phone}"
        
        return self._generate_response(tel_url, options)
    
    def generate_sms_qr(self, phone, message='', options=None):
        """Generate QR code for SMS"""
        if options is None:
            options = {}
        
        # Create SMS URL
        sms_url = f"sms:{phone}"
        if message:
            sms_url += f"?body={message}"
        
        return self._generate_response(sms_url, options)
    
    def generate_vcard_qr(self, vcard_data, options=None):
        """Generate QR code for vCard contact"""
        if options is None:
            options = {}
        
        # Create vCard format
        vcard = "BEGIN:VCARD\n"
        vcard += "VERSION:3.0\n"
        
        if vcard_data.get('first_name') or vcard_data.get('last_name'):
            vcard += f"FN:{vcard_data.get('first_name', '')} {vcard_data.get('last_name', '')}\n"
            vcard += f"N:{vcard_data.get('last_name', '')};{vcard_data.get('first_name', '')}\n"
        
        if vcard_data.get('organization'):
            vcard += f"ORG:{vcard_data['organization']}\n"
        
        if vcard_data.get('phone_work'):
            vcard += f"TEL;TYPE=WORK:{vcard_data['phone_work']}\n"
        
        if vcard_data.get('phone_mobile'):
            vcard += f"TEL;TYPE=CELL:{vcard_data['phone_mobile']}\n"
        
        if vcard_data.get('email'):
            vcard += f"EMAIL:{vcard_data['email']}\n"
        
        if vcard_data.get('website'):
            vcard += f"URL:{vcard_data['website']}\n"
        
        # Address
        address_parts = [
            vcard_data.get('street', ''),
            vcard_data.get('city', ''),
            vcard_data.get('state', ''),
            vcard_data.get('zipcode', ''),
            vcard_data.get('country', '')
        ]
        
        if any(address_parts):
            vcard += f"ADR:;;{';'.join(address_parts)}\n"
        
        vcard += "END:VCARD"
        
        return self._generate_response(vcard, options)
    
    def generate_wifi_qr(self, ssid, password, encryption='WPA', options=None):
        """Generate QR code for WiFi connection"""
        if options is None:
            options = {}
        
        # Create WiFi string format
        if encryption.upper() == 'NOPASS':
            wifi_string = f"WIFI:T:nopass;S:{ssid};;"
        else:
            wifi_string = f"WIFI:T:{encryption.upper()};S:{ssid};P:{password};;"
        
        return self._generate_response(wifi_string, options)
    
    def generate_location_qr(self, latitude, longitude, options=None):
        """Generate QR code for location coordinates"""
        if options is None:
            options = {}
        
        # Create geo URL
        geo_url = f"geo:{latitude},{longitude}"
        
        return self._generate_response(geo_url, options)
