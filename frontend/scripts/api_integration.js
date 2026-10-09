/**
 * API Integration for File Comparison System
 * Connects frontend to FastAPI backend
 */

// Configuration
const API_CONFIG = {
    baseUrl: 'http://localhost:8000', // FastAPI server URL
    endpoints: {
        health: '/api/health',
        upload: '/api/files/upload',
        process: '/api/files/{file_id}/process',
        compare: '/api/comparison/compare',
        getComparison: '/api/comparison/{comparison_id}',
        getComparisonSummary: '/api/comparison/{comparison_id}/summary'
    }
};

// Global state - use shared state from main.js
// uploadedFiles is already declared in main.js, just reference it here
if (typeof window.uploadedFiles === 'undefined') {
    // Create new state if main.js hasn't loaded yet (fallback)
    window.uploadedFiles = { file1: null, file2: null };
}
uploadedFiles = window.uploadedFiles;
let processedFiles = { file1: null, file2: null };
// Use shared comparisonResults from main.js
// comparisonResults is already declared in main.js, just reference it here
if (typeof window.comparisonResults === 'undefined') {
    window.comparisonResults = null;
}
comparisonResults = window.comparisonResults;

/**
 * API Helper Functions
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(`${API_CONFIG.baseUrl}${url}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`API Request failed: ${url}`, error);
        throw error;
    }
}

async function uploadFile(fileKey, file) {
    const formData = new FormData();
    // Preserve the correct MIME type for Excel files
    const mimeType = file.type || 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    formData.append('file', file, file.name);

    try {
        if (typeof window.setFilePreviewStatus === 'function') {
            window.setFilePreviewStatus(fileKey, 'uploading');
        }
        const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.upload}`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('File upload failed:', error);
        throw error;
    }
}

async function processFile(fileKey, fileId, fileName) {
    try {
        if (typeof window.setFilePreviewStatus === 'function') {
            window.setFilePreviewStatus(fileKey, 'processing');
        }
        const result = await apiRequest(API_CONFIG.endpoints.process.replace('{file_id}', fileId), {
            method: 'POST'
        });
        
        // Store raw extracted data for display
        console.log('Processing result:', result);
        if (result && result.structured_data) {
            rawExtractedData[fileKey] = result.structured_data;
            console.log(`Stored raw data for ${fileKey}:`, result.structured_data);
        } else if (result && result.data) {
            // Fallback for different response format
            rawExtractedData[fileKey] = result.data;
            console.log(`Stored raw data (fallback) for ${fileKey}:`, result.data);
        } else {
            console.warn('No structured data found in processing result:', result);
        }

        const markdown = result?.data?.processed_content || result?.processed_content || '';
        if (typeof window.setFilePreviewMarkdown === 'function') {
            const placeholder = markdown ? '' : 'Không có nội dung Markdown trích xuất';
            window.setFilePreviewMarkdown(fileKey, markdown, placeholder);
        }
        if (typeof window.setFilePreviewStatus === 'function') {
            const message = markdown ? 'Đã chuyển sang Markdown' : 'Đã xử lý, không có nội dung Markdown';
            const status = markdown ? 'ready' : 'ready';
            window.setFilePreviewStatus(fileKey, status, message);
        }
        
        return result;
    } catch (error) {
        console.error('File processing failed:', error);
        if (typeof window.setFilePreviewError === 'function') {
            window.setFilePreviewError(fileKey, `Lỗi xử lý: ${error.message}`);
        }
        throw error;
    }
}

async function compareFilesApi(file1Id, file2Id, options = {}) {
    try {
        return await apiRequest(API_CONFIG.endpoints.compare, {
            method: 'POST',
            body: JSON.stringify({
                file1_id: file1Id,
                file2_id: file2Id,
                comparison_options: {
                    exact_match: false,
                    ignore_formatting: true,
                    tolerance_settings: {
                        quantity: 0.01,
                        unit_price: 0.001,
                        amount: 0.01
                    },
                    ...options
                }
            })
        });
    } catch (error) {
        console.error('File comparison failed:', error);
        throw error;
    }
}

/**
 * Backend connection functions
 */
async function checkBackendHealth() {
    try {
        const health = await apiRequest(API_CONFIG.endpoints.health);
        console.log('Backend is healthy:', health);
        return true;
    } catch (error) {
        console.error('Backend health check failed:', error);
        return false;
    }
}

async function processUploadedFiles() {
    const loading = document.getElementById('loading');
    const statusText = document.getElementById('processingStatus') || createStatusElement();

    try {
        // Update status
        statusText.textContent = 'Đang tải file lên server...';
        loading.classList.add('show');

        // Upload files
        const [upload1, upload2] = await Promise.all([
            uploadFile('file1', uploadedFiles.file1),
            uploadFile('file2', uploadedFiles.file2)
        ]);

        processedFiles.file1 = upload1.data.file_id;
        processedFiles.file2 = upload2.data.file_id;

        // Update status
        statusText.textContent = 'Đang xử lý file...';

        // Process files with file names for raw data storage
        const [process1, process2] = await Promise.all([
            processFile('file1', processedFiles.file1, uploadedFiles.file1.name),
            processFile('file2', processedFiles.file2, uploadedFiles.file2.name)
        ]);

        // Update status
        statusText.textContent = 'Đang so sánh dữ liệu...';

        // Compare files
        const comparisonResult = await compareFilesApi(processedFiles.file1, processedFiles.file2);

        comparisonResults = comparisonResult.data;
        displayBackendResults(comparisonResults);

    } catch (error) {
        console.error('Error processing files:', error);
        alert(`Lỗi khi xử lý file: ${error.message}`);
        if (typeof window.setFilePreviewError === 'function') {
            window.setFilePreviewError('file1', `Lỗi xử lý: ${error.message}`);
            window.setFilePreviewError('file2', `Lỗi xử lý: ${error.message}`);
        }
    } finally {
        loading.classList.remove('show');
        if (statusText) {
            statusText.textContent = '';
        }
    }
}

function createStatusElement() {
    const statusEl = document.createElement('div');
    statusEl.id = 'processingStatus';
    statusEl.style.cssText = 'text-align: center; margin: 20px 0; font-weight: bold; color: var(--color-primary);';

    const loading = document.getElementById('loading');
    if (loading) {
        loading.parentNode.insertBefore(statusEl, loading.nextSibling);
    }

    return statusEl;
}

/**
 * Display backend results
 */
function displayBackendResults(results) {
    const resultsContainer = document.getElementById('results');
    if (!resultsContainer) return;

    // Update summary statistics
    const summary = results.summary;
    document.getElementById('totalRows').textContent = summary.total_rows_compared || 0;
    document.getElementById('matchingRows').textContent = summary.matching_rows || 0;
    document.getElementById('differentRows').textContent = summary.different_rows || 0;
    document.getElementById('accuracyRate').textContent = (summary.accuracy_rate || 0).toFixed(1) + '%';

    // Update percentage displays
    const total = summary.total_rows_compared || 1;
    const matchingPercent = Math.round(((summary.matching_rows || 0) / total) * 100);
    const differentPercent = Math.round(((summary.different_rows || 0) / total) * 100);

    document.getElementById('matchingPercent').textContent = matchingPercent + '%';
    document.getElementById('differentPercent').textContent = differentPercent + '%';

    // Update file names
    if (results.file1_info) {
        document.getElementById('file1Name').textContent = results.file1_info.original_name;
    }
    if (results.file2_info) {
        document.getElementById('file2Name').textContent = results.file2_info.original_name;
    }

    // Display detailed differences
    displayBackendDifferences(results.detailed_differences || []);

    // Generate comparison table
    populateBackendComparisonTable(results);

    // Show results
    resultsContainer.classList.add('show');

    // Show diff view container
    const diffContainer = document.getElementById('diffViewContainer');
    if (diffContainer) {
        diffContainer.style.display = 'block';
    }
}

function displayBackendDifferences(differences) {
    const differencesList = document.getElementById('differencesList');
    if (!differencesList) return;

    differencesList.innerHTML = '';

    if (differences.length === 0) {
        differencesList.innerHTML = '<p style="color: var(--color-success); text-align: center;">✓ Không có sai lệch nào được phát hiện!</p>';
    } else {
        // Group differences by row number for better organization
        const groupedDifferences = {};
        differences.forEach(diff => {
            if (!groupedDifferences[diff.row_number]) {
                groupedDifferences[diff.row_number] = [];
            }
            groupedDifferences[diff.row_number].push(diff);
        });

        // Display differences grouped by row
        Object.keys(groupedDifferences).sort((a, b) => a - b).forEach(rowNumber => {
            const rowDifferences = groupedDifferences[rowNumber];
            const diffItem = document.createElement('div');
            diffItem.className = 'difference-group';

            // Find the most severe level for this row
            const severityOrder = { critical: 4, error: 3, warning: 2, info: 1 };
            const maxSeverity = Math.max(...rowDifferences.map(d => severityOrder[d.severity] || 0));
            const severityClass = Object.keys(severityOrder).find(key => severityOrder[key] === maxSeverity) || 'info';
            
            diffItem.className += ` ${severityClass}`;

            let diffHTML = `
                <div class="difference-header">
                    <span class="difference-row-number">📍 Dòng ${rowNumber}</span>
                    <span class="difference-severity-badge ${severityClass}">
                        ${getSeverityIcon(severityClass)} ${getSeverityText(severityClass)}
                    </span>
                </div>
                <div class="difference-content">
            `;

            // Add each field difference for this row
            rowDifferences.forEach(diff => {
                const fieldNames = {
                    description: 'Mô tả sản phẩm',
                    quantity: 'Số lượng',
                    unit_price: 'Đơn giá',
                    amount: 'Thành tiền'
                };

                const fieldName = fieldNames[diff.field] || diff.field;
                const value1 = diff.value1 !== null ? formatFieldValue(diff.field, diff.value1) : 'N/A';
                const value2 = diff.value2 !== null ? formatFieldValue(diff.field, diff.value2) : 'N/A';

                diffHTML += `
                    <div class="field-difference">
                        <div class="field-name">📝 ${fieldName}</div>
                        <div class="field-values">
                            <div class="value-pair">
                                <span class="file-label">File 1:</span>
                                <span class="file-value value-1">${value1}</span>
                            </div>
                            <div class="value-pair">
                                <span class="file-label">File 2:</span>
                                <span class="file-value value-2">${value2}</span>
                            </div>
                            ${diff.difference !== null ? `
                                <div class="diff-calculations">
                                    <span class="diff-absolute">Chênh lệch: ${formatFieldValue(diff.field, diff.difference)}</span>
                                    ${diff.percentage_diff !== null ? 
                                        `<span class="diff-percentage">(${diff.percentage_diff.toFixed(2)}%)</span>` : ''}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            });

            diffHTML += '</div>';
            diffItem.innerHTML = diffHTML;
            differencesList.appendChild(diffItem);
        });
    }
}

// Helper functions for difference display
function getSeverityIcon(severity) {
    const icons = {
        critical: '🚨',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[severity] || 'ℹ️';
}

function getSeverityText(severity) {
    const texts = {
        critical: 'Nghiêm trọng',
        error: 'Lỗi',
        warning: 'Cảnh báo',
        info: 'Thông tin'
    };
    return texts[severity] || 'Thông tin';
}

function formatFieldValue(field, value) {
    if (value === null || value === undefined) return 'N/A';
    
    // Format based on field type
    switch(field) {
        case 'quantity':
            return typeof value === 'number' ? value.toLocaleString('vi-VN') : value;
        case 'unit_price':
        case 'amount':
            return typeof value === 'number' ? 
                value.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' }) : 
                value;
        default:
            return value;
    }
}

function populateBackendComparisonTable(results) {
    const tableBody = document.getElementById('comparisonTable');
    if (!tableBody) return;

    tableBody.innerHTML = '';

    // Create a simple table view from backend data
    const differences = results.detailed_differences || [];

    differences.forEach(diff => {
        const row = document.createElement('tr');
        row.className = diff.severity;

        const severityIcon = diff.severity === 'info' ? '✓' :
                           diff.severity === 'warning' ? '⚠️' :
                           diff.severity === 'error' ? '✗' : '🚨';

        row.innerHTML = `
            <td>${diff.row_number}</td>
            <td>${diff.field}</td>
            <td>${diff.value1 !== null ? diff.value1 : 'N/A'}</td>
            <td>${diff.value2 !== null ? diff.value2 : 'N/A'}</td>
            <td>${diff.difference !== null ? diff.difference.toFixed(2) : 'N/A'}</td>
            <td>${diff.percentage_diff !== null ? diff.percentage_diff.toFixed(2) + '%' : 'N/A'}</td>
            <td><span class="status-icon ${diff.severity}">${severityIcon}</span></td>
        `;

        tableBody.appendChild(row);
    });

    // If no differences, show a message
    if (differences.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="7" style="text-align: center; color: var(--color-success);">
                ✓ Không có sai lệch nào được phát hiện giữa các file
            </td>
        `;
        tableBody.appendChild(row);
    }
}

/**
 * Enhanced comparison function with backend integration
 */
async function compareFilesWithBackend() {
    // Validate files are uploaded
    if (!uploadedFiles.file1 || !uploadedFiles.file2) {
        alert('Vui lòng chọn cả 2 file để so sánh!');
        return;
    }

    // Check backend health first
    const isBackendHealthy = await checkBackendHealth();
    if (!isBackendHealthy) {
        alert('Không thể kết nối đến server. Vui lòng kiểm tra lại kết nối và thử lại.');
        return;
    }

    // Process files through backend
    await processUploadedFiles();
}

/**
 * Fallback to frontend comparison if backend is unavailable
 */
function compareFilesFrontend() {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    loading.classList.add('show');
    results.classList.remove('show');

    // Simulate file processing delay
    setTimeout(() => {
        // For demonstration, use sample data
        const data1 = sampleData.file1;
        const data2 = sampleData.file2;

        comparisonResults = performComparison(data1, data2);
        displayResults(comparisonResults);

        loading.classList.remove('show');
        results.classList.add('show');
    }, 2000);
}

/**
 * Main comparison function with backend fallback
 */
async function compareFiles() {
    console.log('Backend API compareFiles called');
    
    // First check if backend is available
    const isBackendHealthy = await checkBackendHealth();
    
    if (isBackendHealthy) {
        console.log('Backend is healthy, trying backend comparison');
        try {
            await compareFilesWithBackend();
            return;
        } catch (error) {
            console.warn('Backend comparison failed, falling back to frontend:', error);
        }
    } else {
        console.log('Backend not healthy, using frontend comparison');
    }
    
    // Fallback to frontend comparison
    console.log('Falling back to frontend comparison');
    
    // Check if frontend comparison function exists
    if (typeof window.originalCompareFiles === 'function') {
        console.log('Using original frontend compareFiles');
        await window.originalCompareFiles();
    } else {
        console.log('Using fallback frontend comparison');
        compareFilesFrontend();
    }
}

/**
 * Export enhanced functionality
 */
function exportBackendReport(format) {
    if (!comparisonResults) {
        alert('Vui lòng thực hiện so sánh trước khi xuất báo cáo!');
        return;
    }

    if (format === 'excel') {
        // Generate CSV from backend results
        const csvContent = generateBackendCSVContent();
        downloadFile(csvContent, 'backend-comparison-report.csv', 'text/csv');
    } else if (format === 'pdf') {
        // Generate PDF from backend results
        generateBackendPDFReport();
    }
}

function generateBackendCSVContent() {
    if (!comparisonResults) return '';

    let csv = 'STT,Trường,Giá trị File 1,Giá trị File 2,Chênh lệch,Phần trăm,Mức độ\n';

    const differences = comparisonResults.detailed_differences || [];
    differences.forEach(diff => {
        const severity = diff.severity || 'info';
        csv += `${diff.row_number},"${diff.field}","${diff.value1}","${diff.value2}","${diff.difference || 0}","${diff.percentage_diff || 0}%","${severity}"\n`;
    });

    return csv;
}

/**
 * Generate PDF report from backend results
 */
async function generateBackendPDFReport() {
    try {
        // Use the same PDF generation function as main.js
        if (typeof generatePDFReport === 'function') {
            await generatePDFReport();
        } else {
            // Fallback to HTML report
            generateBackendHTMLReport();
        }
    } catch (error) {
        console.error('Backend PDF generation error:', error);
        generateBackendHTMLReport();
    }
}

/**
 * Generate HTML report from backend results
 */
function generateBackendHTMLReport() {
    const summary = comparisonResults.summary || {};
    const differences = comparisonResults.detailed_differences || [];
    const timestamp = new Date().toLocaleString('vi-VN');
    
    let html = `
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo So Sánh File Dữ Liệu (Backend)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .difference { margin-bottom: 15px; padding: 10px; border-left: 4px solid #dc3545; background: #fff5f5; }
        .info { margin-bottom: 15px; padding: 10px; border-left: 4px solid #17a2b8; background: #f0f8ff; }
        .warning { margin-bottom: 15px; padding: 10px; border-left: 4px solid #ffc107; background: #fff8e1; }
        .error { margin-bottom: 15px; padding: 10px; border-left: 4px solid #dc3545; background: #fff5f5; }
        .critical { margin-bottom: 15px; padding: 10px; border-left: 4px solid #721c24; background: #f8d7da; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .severity { padding: 2px 6px; border-radius: 3px; color: white; font-size: 10px; }
        .severity.info { background: #17a2b8; }
        .severity.warning { background: #ffc107; color: #000; }
        .severity.error { background: #dc3545; }
        .severity.critical { background: #721c24; }
        .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BÁO CÁO SO SÁNH FILE DỮ LIỆU (Backend)</h1>
        <p>Ngày tạo: ${timestamp}</p>
        <p>File 1: ${comparisonResults.file1_info?.original_name || 'N/A'}</p>
        <p>File 2: ${comparisonResults.file2_info?.original_name || 'N/A'}</p>
    </div>

    <div class="summary">
        <h2>TÓM TẮT KẾT QUẢ</h2>
        <p><strong>Tổng số dòng đã so sánh:</strong> ${summary.total_rows_compared || 0}</p>
        <p><strong>Dòng khớp:</strong> ${summary.matching_rows || 0}</p>
        <p><strong>Dòng sai lệch:</strong> ${summary.different_rows || 0}</p>
        <p><strong>Tỷ lệ chính xác:</strong> ${(summary.accuracy_rate || 0).toFixed(1)}%</p>
    </div>

    <h2>CHI TIẾT SAI LỆCH</h2>`;

    if (differences.length === 0) {
        html += '<p style="color: #28a745; text-align: center;">✓ Không có sai lệch nào được phát hiện!</p>';
    } else {
        differences.forEach(diff => {
            const severityClass = diff.severity || 'info';
            const fieldNames = {
                description: 'Mô tả sản phẩm',
                quantity: 'Số lượng',
                unit_price: 'Đơn giá',
                amount: 'Thành tiền'
            };

            html += `
            <div class="${severityClass}">
                <strong>Dòng ${diff.row_number}: ${fieldNames[diff.field] || diff.field}</strong>
                <span class="severity ${severityClass}">${diff.severity || 'info'}</span><br>
                <strong>File 1:</strong> ${diff.value1 !== null ? diff.value1 : 'N/A'}<br>
                <strong>File 2:</strong> ${diff.value2 !== null ? diff.value2 : 'N/A'}`;
            
            if (diff.difference !== null) {
                html += `<br><strong>Chênh lệch:</strong> ${diff.difference.toFixed(2)}`;
            }
            if (diff.percentage_diff !== null) {
                html += `<br><strong>Phần trăm:</strong> ${diff.percentage_diff.toFixed(2)}%`;
            }
            html += '</div>';
        });
    }

    html += `
    <div class="footer">
        <p>Generated by File Comparison System (Backend Processing)</p>
    </div>
</body>
</html>`;

    // Create and open HTML report
    const blob = new Blob([html], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    
    const printWindow = window.open(url, '_blank');
    printWindow.onload = function() {
        setTimeout(() => {
            printWindow.print();
        }, 500);
    };
    
    // Show success message
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
    `;
    notification.textContent = 'Backend PDF report opened. You can print or save as PDF from your browser.';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        document.body.removeChild(notification);
    }, 3000);
}

/**
 * Initialize backend integration
 */
function initializeBackendIntegration() {
    // Check if backend is available on page load
    checkBackendHealth().then(isHealthy => {
        if (isHealthy) {
            console.log('✅ Backend is available');
        } else {
            console.warn('⚠️ Backend is not available, using frontend-only mode');
        }
    });
}

// Export functions for use in main.js
window.backendAPI = {
    compareFiles,
    exportBackendReport,
    checkBackendHealth,
    initializeBackendIntegration
};