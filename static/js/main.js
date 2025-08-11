// QR Code Generator Demo JavaScript

class QRCodeDemo {
    constructor() {
        this.currentQRType = 'url';
        this.generateBtn = document.getElementById('generate-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.previewContainer = document.getElementById('qr-preview');
        this.apiResponse = document.getElementById('api-response');
        this.currentQRData = null;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.generateHeroQR();
    }

    bindEvents() {
        // Tab switching
        document.querySelectorAll('#qr-tabs button').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.currentQRType = e.target.id.replace('-tab', '');
                this.resetPreview();
            });
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => {
            this.generateQRCode();
        });

        // Download button
        this.downloadBtn.addEventListener('click', () => {
            this.downloadQRCode();
        });

        // Real-time updates for customization options
        const customizationInputs = [
            'foreground-color', 'background-color', 'module-drawer', 
            'error-correction', 'format', 'size'
        ];
        
        customizationInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('change', () => {
                    console.log(`Changed ${inputId} to ${input.value}`);
                    if (this.currentQRData) {
                        this.generateQRCode();
                    }
                });
            }
        });
    }

    generateHeroQR() {
        // Generate a demo QR code for the hero section
        const canvas = document.getElementById('heroQR');
        if (canvas) {
            this.createDemoQR(canvas, 'https://rapidapi.com', '#000000', '#ffffff');
        }
    }

    createDemoQR(canvas, text, foreground = '#000000', background = '#ffffff') {
        const ctx = canvas.getContext('2d');
        const size = 300;
        const moduleSize = 10;
        const modules = Math.floor(size / moduleSize);
        
        // Clear canvas and set background
        ctx.clearRect(0, 0, size, size);
        ctx.fillStyle = background;
        ctx.fillRect(0, 0, size, size);
        
        // Create a simple QR-like pattern for demo
        ctx.fillStyle = foreground;
        
        // Finder patterns (corners)
        this.drawFinderPattern(ctx, 0, 0, moduleSize, foreground);
        this.drawFinderPattern(ctx, size - 7 * moduleSize, 0, moduleSize, foreground);
        this.drawFinderPattern(ctx, 0, size - 7 * moduleSize, moduleSize, foreground);
        
        // Random data modules for visual effect
        for (let i = 8; i < modules - 8; i++) {
            for (let j = 8; j < modules - 8; j++) {
                if (Math.random() > 0.5) {
                    ctx.fillRect(i * moduleSize, j * moduleSize, moduleSize - 1, moduleSize - 1);
                }
            }
        }
        
        // Timing patterns
        for (let i = 8; i < modules - 8; i++) {
            if (i % 2 === 0) {
                ctx.fillRect(i * moduleSize, 6 * moduleSize, moduleSize - 1, moduleSize - 1);
                ctx.fillRect(6 * moduleSize, i * moduleSize, moduleSize - 1, moduleSize - 1);
            }
        }
    }

    drawFinderPattern(ctx, x, y, moduleSize, foreground = '#000000') {
        // Draw 7x7 finder pattern
        ctx.fillStyle = foreground;
        ctx.fillRect(x, y, 7 * moduleSize, 7 * moduleSize);
        ctx.clearRect(x + moduleSize, y + moduleSize, 5 * moduleSize, 5 * moduleSize);
        ctx.fillStyle = foreground;
        ctx.fillRect(x + 2 * moduleSize, y + 2 * moduleSize, 3 * moduleSize, 3 * moduleSize);
    }

    async generateQRCode() {
        const requestData = this.buildRequestData();
        
        if (!requestData) {
            this.showError('Please fill in all required fields');
            return;
        }

        console.log('Generating QR code with data:', requestData);

        // Show loading state
        this.setLoading(true);

        try {
            const endpoint = `/api/v1/qr/${this.currentQRType}`;
            console.log('Calling endpoint:', endpoint);
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();
            console.log('API Response:', result);

            if (response.ok && result.success) {
                this.displayQRCode(result.data);
                this.showApiResponse(result, response.status);
            } else {
                console.error('API Error:', result);
                this.showError(result.error || 'Failed to generate QR code');
            }
        } catch (error) {
            console.error('Network error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    buildRequestData() {
        const data = {};
        const options = this.getCustomizationOptions();

        switch (this.currentQRType) {
            case 'url':
                const url = document.getElementById('url-input').value.trim();
                if (!url) return null;
                data.url = url;
                break;

            case 'text':
                const text = document.getElementById('text-input').value.trim();
                if (!text) return null;
                data.text = text;
                break;

            case 'email':
                const email = document.getElementById('email-input').value.trim();
                if (!email) return null;
                data.email = email;
                data.subject = document.getElementById('email-subject').value.trim();
                data.message = document.getElementById('email-message').value.trim();
                break;

            case 'phone':
                const phone = document.getElementById('phone-input').value.trim();
                if (!phone) return null;
                data.phone = phone;
                break;

            case 'wifi':
                const ssid = document.getElementById('wifi-ssid').value.trim();
                if (!ssid) return null;
                data.ssid = ssid;
                data.password = document.getElementById('wifi-password').value.trim();
                data.encryption = document.getElementById('wifi-encryption').value;
                break;

            default:
                return null;
        }

        data.options = options;
        return data;
    }

    getCustomizationOptions() {
        return {
            foreground_color: document.getElementById('foreground-color').value,
            background_color: document.getElementById('background-color').value,
            module_drawer: document.getElementById('module-drawer').value,
            error_correction: document.getElementById('error-correction').value,
            format: document.getElementById('format').value,
            size: parseInt(document.getElementById('size').value),
            border: 4
        };
    }

    displayQRCode(data) {
        this.currentQRData = data;
        
        const img = document.createElement('img');
        img.src = data.qr_code;
        img.alt = 'Generated QR Code';
        img.className = 'img-fluid fade-in';
        
        this.previewContainer.innerHTML = '';
        this.previewContainer.appendChild(img);
        
        // Show download button
        this.downloadBtn.style.display = 'inline-block';
    }

    showApiResponse(result, status) {
        document.getElementById('response-status').textContent = `${status} OK`;
        document.getElementById('response-status').className = 'badge bg-success';
        document.getElementById('response-format').textContent = result.data.format;
        
        // Calculate approximate size
        const sizeKB = Math.round(result.data.qr_code.length * 0.75 / 1024);
        document.getElementById('response-size').textContent = `~${sizeKB} KB`;
        
        this.apiResponse.style.display = 'block';
        this.apiResponse.classList.add('fade-in');
    }

    showError(message) {
        this.previewContainer.innerHTML = `
            <div class="alert alert-danger fade-in">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
        
        // Hide API response and download button
        this.apiResponse.style.display = 'none';
        this.downloadBtn.style.display = 'none';
        
        // Update API response to show error
        document.getElementById('response-status').textContent = '400 Error';
        document.getElementById('response-status').className = 'badge bg-danger';
    }

    setLoading(isLoading) {
        if (isLoading) {
            this.generateBtn.disabled = true;
            this.generateBtn.innerHTML = '<span class="loading-spinner me-2"></span>Generating...';
            
            this.previewContainer.innerHTML = `
                <div class="text-center">
                    <div class="loading-spinner me-2" style="width: 40px; height: 40px;"></div>
                    <p class="mt-3 text-muted">Generating your QR code...</p>
                </div>
            `;
        } else {
            this.generateBtn.disabled = false;
            this.generateBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate QR Code';
        }
    }

    resetPreview() {
        this.previewContainer.innerHTML = `
            <div class="placeholder-message">
                <i class="fas fa-qrcode fa-4x text-muted mb-3"></i>
                <p class="text-muted">Generate a QR code to see preview</p>
            </div>
        `;
        
        this.apiResponse.style.display = 'none';
        this.downloadBtn.style.display = 'none';
        this.currentQRData = null;
    }

    downloadQRCode() {
        if (!this.currentQRData || !this.currentQRData.qr_code) {
            return;
        }

        const format = this.currentQRData.format.toLowerCase();
        const link = document.createElement('a');
        link.href = this.currentQRData.qr_code;
        
        // Generate filename based on content and timestamp
        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
        const contentType = this.currentQRType;
        link.download = `qr-${contentType}-${timestamp}.${format}`;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Utility method to show notifications
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Initialize demo when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new QRCodeDemo();
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation classes when elements come into view
const observeElements = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe feature cards and pricing cards
    document.querySelectorAll('.feature-card, .pricing-card').forEach(card => {
        observer.observe(card);
    });
};

// Initialize observers when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observeElements);
} else {
    observeElements();
}

// Add some interactive feedback for form inputs
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('focus', (e) => {
            e.target.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', (e) => {
            e.target.parentElement.classList.remove('focused');
        });
        
        input.addEventListener('input', (e) => {
            if (e.target.value.trim()) {
                e.target.parentElement.classList.add('has-value');
            } else {
                e.target.parentElement.classList.remove('has-value');
            }
        });
    });
});
