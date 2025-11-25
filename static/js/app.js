/**
    /* Commit 45 */
    /* Commit 42 */
    /* Commit 9 */
    /* Commit 28 */
 * Barcode Decoder - Main Application JavaScript
 */

class BarcodeDecoderApp {
    constructor() {
        this.selectedFiles = [];
        this.results = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
    }

    setupEventListeners() {
        const fileInput = document.getElementById('fileInput');
        const decodeBtn = document.getElementById('decodeBtn');
        const batchBtn = document.getElementById('batchBtn');
        const clearBtn = document.getElementById('clearBtn');
        const removeImageBtn = document.getElementById('removeImage');
        const uploadArea = document.getElementById('uploadArea');

        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        decodeBtn.addEventListener('click', () => this.decodeBarcode());
        batchBtn.addEventListener('click', () => this.batchProcess());
        clearBtn.addEventListener('click', () => this.clearAll());
        removeImageBtn.addEventListener('click', () => this.removeImage());
        uploadArea.addEventListener('click', () => fileInput.click());
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            this.handleFiles(files);
        });
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.handleFiles(files);
    }

    handleFiles(files) {
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        
        if (imageFiles.length === 0) {
            this.showError('Please select valid image files');
            return;
        }

        this.selectedFiles = imageFiles;
        this.updateUI();
        this.displayPreview(imageFiles[0]);
    }

    displayPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewContainer = document.getElementById('previewContainer');
            const previewImage = document.getElementById('previewImage');
            const uploadArea = document.getElementById('uploadArea');

            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
            uploadArea.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    removeImage() {
        this.selectedFiles = [];
        document.getElementById('previewContainer').style.display = 'none';
        document.getElementById('uploadArea').style.display = 'block';
        document.getElementById('fileInput').value = '';
        this.updateUI();
        this.hideResults();
    }

    updateUI() {
        const decodeBtn = document.getElementById('decodeBtn');
        const batchBtn = document.getElementById('batchBtn');
        
        decodeBtn.disabled = this.selectedFiles.length === 0;
        batchBtn.disabled = this.selectedFiles.length === 0;
    }

    async decodeBarcode() {
        if (this.selectedFiles.length === 0) return;

        const file = this.selectedFiles[0];
        await this.processFile(file, false);
    }

    async batchProcess() {
        if (this.selectedFiles.length === 0) return;

        this.showLoading();
        
        try {
            const formData = new FormData();
            this.selectedFiles.forEach(file => {
                formData.append('images', file);
            });
            
            const enhance = document.getElementById('enhanceImage').checked;
            formData.append('enhance', enhance);

            const response = await fetch('/api/batch', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                this.displayBatchResults(data.results);
            } else {
                this.showError(data.error || 'Batch processing failed');
            }
        } catch (error) {
            this.showError('Error processing files: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async processFile(file, isBatch = false) {
        this.showLoading();

        try {
            const formData = new FormData();
            formData.append('image', file);
            
            const enhance = document.getElementById('enhanceImage').checked;
            formData.append('enhance', enhance);

            const formatFilter = Array.from(document.getElementById('formatFilter').selectedOptions)
                .map(option => option.value)
                .filter(value => value);
            
            if (formatFilter.length > 0) {
                formData.append('formats', formatFilter.join(','));
            }

            const response = await fetch('/api/decode', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                if (isBatch) {
                    return data.results;
                } else {
                    this.displayResults(data.results);
                }
            } else {
                this.showError(data.error || 'Decoding failed');
            }
        } catch (error) {
            this.showError('Error processing image: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    displayResults(results) {
        this.results = results;
        const resultsSection = document.getElementById('resultsSection');
        const resultsContainer = document.getElementById('resultsContainer');
        const resultsCount = document.getElementById('resultsCount');

        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="result-card">
                    <p style="text-align: center; color: var(--text-secondary);">
                        No barcodes found in the image. Try enabling image enhancement or using a different image.
                    </p>
                </div>
            `;
        } else {
            resultsContainer.innerHTML = results.map((result, index) => 
                this.createResultCard(result, index)
            ).join('');
        }

        resultsCount.textContent = `${results.length} barcode${results.length !== 1 ? 's' : ''} found`;
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    displayBatchResults(batchResults) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsContainer = document.getElementById('resultsContainer');
        const resultsCount = document.getElementById('resultsCount');

        let allResults = [];
        let html = '';

        batchResults.forEach((fileResult, fileIndex) => {
            if (fileResult.success && fileResult.results.length > 0) {
                html += `
                    <div class="result-card" style="border-left-color: var(--secondary-color);">
                        <div class="result-header">
                            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">
                                <i class="fas fa-file-image"></i> ${fileResult.filename}
                            </h3>
                        </div>
                `;
                
                fileResult.results.forEach((result, index) => {
                    html += this.createResultCard(result, `${fileIndex}-${index}`, false);
                    allResults.push(result);
                });
                
                html += '</div>';
            } else if (!fileResult.success) {
                html += `
                    <div class="result-card" style="border-left-color: var(--error-color);">
                        <div class="result-header">
                            <h3 style="color: var(--text-primary);">
                                <i class="fas fa-file-image"></i> ${fileResult.filename}
                            </h3>
                        </div>
                        <p style="color: var(--error-color);">Error: ${fileResult.error || 'Unknown error'}</p>
                    </div>
                `;
            }
        });

        if (html === '') {
            html = `
                <div class="result-card">
                    <p style="text-align: center; color: var(--text-secondary);">
                        No barcodes found in any of the images.
                    </p>
                </div>
            `;
        }

        resultsContainer.innerHTML = html;
        resultsCount.textContent = `${allResults.length} barcode${allResults.length !== 1 ? 's' : ''} found across ${batchResults.length} file${batchResults.length !== 1 ? 's' : ''}`;
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    createResultCard(result, index, showHeader = true) {
        const rect = result.rect || {};
        const points = result.points || [];
        
        return `
            <div class="result-card" data-index="${index}">
                ${showHeader ? `
                    <div class="result-header">
                        <span class="result-type">
                            <i class="fas fa-qrcode"></i>
                            ${result.type || 'UNKNOWN'}
                        </span>
                        ${result.method ? `<span style="color: var(--text-secondary); font-size: 0.85rem;">${result.method}</span>` : ''}
                    </div>
                ` : ''}
                <div class="result-data">${this.escapeHtml(result.data || 'No data')}</div>
                <div class="result-meta">
                    ${rect.width ? `
                        <div class="meta-item">
                            <span class="meta-label">Position</span>
                            <span class="meta-value">(${rect.x}, ${rect.y})</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Size</span>
                            <span class="meta-value">${rect.width} × ${rect.height}px</span>
                        </div>
                    ` : ''}
                    ${points.length > 0 ? `
                        <div class="meta-item">
                            <span class="meta-label">Points</span>
                            <span class="meta-value">${points.length}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    clearAll() {
        this.selectedFiles = [];
        this.results = [];
        document.getElementById('fileInput').value = '';
        document.getElementById('previewContainer').style.display = 'none';
        document.getElementById('uploadArea').style.display = 'block';
        document.getElementById('enhanceImage').checked = true;
        document.getElementById('formatFilter').selectedIndex = 0;
        this.hideResults();
        this.updateUI();
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showError(message) {
        // Simple error display - can be enhanced with a toast notification
        alert('Error: ' + message);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new BarcodeDecoderApp();
});

