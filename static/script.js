// Global state
let selectedFiles = [];

// DOM elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const filesSection = document.getElementById('filesSection');
const filesList = document.getElementById('filesList');
const mergeBtn = document.getElementById('mergeBtn');
const clearBtn = document.getElementById('clearBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusMessage = document.getElementById('statusMessage');
const outputName = document.getElementById('outputName');

// Event listeners
uploadBox.addEventListener('click', () => fileInput.click());
uploadBox.addEventListener('dragover', handleDragOver);
uploadBox.addEventListener('dragleave', handleDragLeave);
uploadBox.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
mergeBtn.addEventListener('click', mergePDFs);
clearBtn.addEventListener('click', clearSelection);

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    const newFiles = Array.from(files).filter(file => {
        if (file.type !== 'application/pdf') {
            showStatus(`Invalid file type: ${file.name}. Only PDF files are allowed.`, 'error');
            return false;
        }
        
        if (file.size > 50 * 1024 * 1024) {
            showStatus(`File too large: ${file.name}. Maximum size is 50MB.`, 'error');
            return false;
        }
        
        return true;
    });
    
    if (selectedFiles.length + newFiles.length > 100) {
        showStatus('Maximum 100 files allowed.', 'error');
        return;
    }
    
    selectedFiles = [...selectedFiles, ...newFiles];
    updateFilesList();
    showStatus(`${newFiles.length} file(s) added successfully.`, 'success');
}

function updateFilesList() {
    if (selectedFiles.length === 0) {
        filesSection.style.display = 'none';
        return;
    }
    
    filesSection.style.display = 'block';
    filesList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-item-info">
                <div class="file-item-name">${escapeHtml(file.name)}</div>
                <div class="file-item-size">${formatFileSize(file.size)}</div>
            </div>
            <button class="file-item-remove" data-index="${index}">Remove</button>
        `;
        
        fileItem.querySelector('.file-item-remove').addEventListener('click', () => {
            selectedFiles.splice(index, 1);
            updateFilesList();
        });
        
        filesList.appendChild(fileItem);
    });
    
    mergeBtn.disabled = selectedFiles.length < 2;
}

async function mergePDFs() {
    if (selectedFiles.length < 2) {
        showStatus('Please select at least 2 PDF files.', 'error');
        return;
    }
    
    try {
        mergeBtn.disabled = true;
        progressSection.style.display = 'block';
        
        // Step 1: Upload files
        progressText.textContent = 'Uploading files...';
        const uploadedFiles = await uploadFiles(selectedFiles);
        
        // Step 2: Merge PDFs
        progressText.textContent = 'Merging PDFs...';
        progressFill.style.width = '60%';
        
        const mergeResponse = await fetch('/api/merge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                files: uploadedFiles.map(f => f.stored_name),
                output_name: outputName.value || 'merged.pdf'
            })
        });
        
        if (!mergeResponse.ok) {
            const error = await mergeResponse.json();
            throw new Error(error.error || 'Merge failed');
        }
        
        // Step 3: Download merged PDF
        progressText.textContent = 'Downloading...';
        progressFill.style.width = '90%';
        
        const blob = await mergeResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = outputName.value || 'merged.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Cleanup uploaded files
        for (const file of uploadedFiles) {
            await cleanupFile(file.stored_name);
        }
        
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';
        
        showStatus('PDFs merged successfully! Download started.', 'success');
        clearSelection();
        
        setTimeout(() => {
            progressSection.style.display = 'none';
            progressFill.style.width = '0%';
        }, 2000);
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        progressSection.style.display = 'none';
        progressFill.style.width = '0%';
    } finally {
        mergeBtn.disabled = false;
    }
}

async function uploadFiles(files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Upload failed');
    }
    
    const data = await response.json();
    
    if (!data.success) {
        throw new Error('Upload failed');
    }
    
    // Update progress for uploads
    progressFill.style.width = '50%';
    
    return data.files;
}

async function cleanupFile(fileName) {
    try {
        await fetch('/api/cleanup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_name: fileName })
        });
    } catch (error) {
        console.error('Cleanup error:', error);
    }
}

function clearSelection() {
    selectedFiles = [];
    fileInput.value = '';
    updateFilesList();
    filesSection.style.display = 'none';
    statusMessage.style.display = 'none';
}

function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message status-${type}`;
    statusMessage.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Check API health on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            showStatus('Warning: Server connection may be unstable.', 'warning');
        }
    } catch (error) {
        showStatus('Error: Cannot connect to server.', 'error');
    }
});
