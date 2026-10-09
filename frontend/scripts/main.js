/**
 * Main JavaScript for File Comparison System
 */

// No sample data - only real user files are processed

// Global state - make available globally for other scripts
window.uploadedFiles = {file1: null, file2: null};
let uploadedFiles = window.uploadedFiles;
window.comparisonResults = null;
let comparisonResults = window.comparisonResults;

// Store raw extracted data for display
window.rawExtractedData = {file1: null, file2: null};
let rawExtractedData = window.rawExtractedData;

function createDefaultPreviewState() {
    return {
        name: 'Chưa chọn',
        status: 'idle',
        statusMessage: 'Chưa có dữ liệu',
        markdown: '',
        error: null,
        placeholder: 'Chưa có nội dung để hiển thị'
    };
}

const previewState = {
    file1: createDefaultPreviewState(),
    file2: createDefaultPreviewState()
};

const statusClassMap = {
    uploading: 'loading',
    processing: 'loading',
    ready: 'success',
    error: 'error'
};

const defaultStatusMessages = {
    idle: 'Chưa có dữ liệu',
    selected: 'Đã chọn file, chờ tải lên',
    uploading: 'Đang tải file lên...',
    processing: 'Đang chuyển sang Markdown...',
    ready: 'Đã chuyển sang Markdown',
    error: 'Lỗi xử lý'
};

function renderPreview(fileKey) {
    const state = previewState[fileKey];
    if (!state) return;
    const capitalized = fileKey.charAt(0).toUpperCase() + fileKey.slice(1);
    const nameEl = document.getElementById(`preview${capitalized}Name`);
    const statusEl = document.getElementById(`preview${capitalized}Status`);
    const placeholderEl = document.getElementById(`previewPlaceholder${capitalized}`);
    const markdownEl = document.getElementById(`markdownPreview${capitalized}`);
    if (!nameEl || !statusEl || !placeholderEl || !markdownEl) return;

    nameEl.textContent = state.name || 'Chưa chọn';

    statusEl.classList.remove('loading', 'success', 'error');
    if (statusClassMap[state.status]) {
        statusEl.classList.add(statusClassMap[state.status]);
    }
    statusEl.textContent = state.statusMessage || defaultStatusMessages[state.status] || defaultStatusMessages.idle;

    const hasContent = Boolean(state.markdown && state.markdown.trim());
    if (hasContent) {
        placeholderEl.style.display = 'none';
        markdownEl.style.display = 'block';
        if (window.marked && typeof window.marked.parse === 'function') {
            markdownEl.innerHTML = window.marked.parse(state.markdown);
        } else {
            markdownEl.textContent = state.markdown;
        }
    } else {
        markdownEl.style.display = 'none';
        markdownEl.innerHTML = '';
        placeholderEl.style.display = 'block';
        const placeholderText = state.placeholder || state.statusMessage || defaultStatusMessages.idle;
        placeholderEl.textContent = placeholderText;
    }
}

function setPreviewState(fileKey, updates = {}) {
    if (!previewState[fileKey]) return;
    Object.assign(previewState[fileKey], updates);
    renderPreview(fileKey);
}

function resetPreviewState(fileKey) {
    previewState[fileKey] = createDefaultPreviewState();
    renderPreview(fileKey);
}

window.setFilePreviewName = function(fileKey, name) {
    setPreviewState(fileKey, { name: name || 'Chưa chọn' });
};

window.setFilePreviewStatus = function(fileKey, status, message) {
    if (!previewState[fileKey]) return;
    const statusMessage = message || defaultStatusMessages[status] || defaultStatusMessages.idle;
    const nextState = { status, statusMessage };
    if (status !== 'error') {
        nextState.error = null;
    }
    setPreviewState(fileKey, nextState);
};

window.setFilePreviewMarkdown = function(fileKey, markdown, placeholder) {
    if (!previewState[fileKey]) return;
    const hasContent = Boolean(markdown && markdown.trim());
    const nextPlaceholder = hasContent ? previewState[fileKey].placeholder : (placeholder || 'Không có nội dung Markdown');
    setPreviewState(fileKey, {
        markdown: markdown || '',
        placeholder: nextPlaceholder
    });
};

window.setFilePreviewError = function(fileKey, message) {
    if (!previewState[fileKey]) return;
    const errorMessage = message || defaultStatusMessages.error;
    setPreviewState(fileKey, {
        status: 'error',
        statusMessage: errorMessage,
        error: errorMessage,
        markdown: '',
        placeholder: errorMessage
    });
};

window.resetFilePreview = function(fileKey) {
    resetPreviewState(fileKey);
};

/**
 * File handling functions
 */
function handleFileSelect(fileNumber, input) {
    console.log(`🔍 handleFileSelect called for file${fileNumber}`);
    console.log(`🔍 Input element:`, input.id);
    console.log(`🔍 Input files count:`, input.files.length);
    console.log(`🔍 Call stack:`, new Error().stack);
    
    const file = input.files[0];
    console.log(`🔍 Selected file:`, file ? file.name : 'No file');
    
    if (file) {
        uploadedFiles[`file${fileNumber}`] = file;
        console.log(`🔍 File stored in uploadedFiles.file${fileNumber}:`, uploadedFiles[`file${fileNumber}`]);
        
        const infoDiv = document.getElementById(`file${fileNumber}-info`);
        console.log(`🔍 infoDiv for file${fileNumber}:`, !!infoDiv);
        
        // Extract just the filename from path (fix for browsers showing full path)
        const fileName = getFileName(file);
        console.log(`🔍 fileName for file${fileNumber}:`, fileName);
        
        infoDiv.textContent = `✓ ${fileName} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        infoDiv.style.display = 'block';
        console.log(`🔍 infoDiv content set to:`, infoDiv.textContent);

        // Update upload area appearance
        const uploadArea = input.parentElement;
        uploadArea.style.borderColor = 'var(--color-success)';
        uploadArea.style.background = 'var(--color-bg-3)';

        const fileKey = `file${fileNumber}`;
        window.setFilePreviewName(fileKey, fileName);
        window.setFilePreviewStatus(fileKey, 'selected');
        window.setFilePreviewMarkdown(fileKey, '', 'Chưa có nội dung để hiển thị');

        checkFilesReady();
        console.log(`🔍 handleFileSelect completed for file${fileNumber}`);
    } else {
        console.log(`🔍 No file selected for file${fileNumber}`);
        console.log(`🔍 Input.files is empty, was the file cleared?`);
    }
}

function checkFilesReady() {
    const compareBtn = document.getElementById('compareBtn');
    console.log('🔍 checkFilesReady called');
    console.log('🔍 uploadedFiles.file1:', uploadedFiles.file1 ? uploadedFiles.file1.name : 'null');
    console.log('🔍 uploadedFiles.file2:', uploadedFiles.file2 ? uploadedFiles.file2.name : 'null');
    console.log('🔍 compareBtn found:', !!compareBtn);
    
    if (uploadedFiles.file1 && uploadedFiles.file2) {
        compareBtn.disabled = false;
        compareBtn.textContent = '🔍 So Sánh Dữ Liệu';
        console.log('🔍 Both files ready - Compare button enabled');
    } else {
        console.log('🔍 Not both files ready yet');
    }
}

/**
 * Drag and drop functionality
 */
function initializeDragAndDrop() {
    document.querySelectorAll('.upload-area').forEach(area => {
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', (e) => {
            e.preventDefault();
            console.log('🔍 DROP event triggered on:', area);
            area.classList.remove('dragover');
            const files = e.dataTransfer.files;
            console.log('🔍 Dropped files:', files.length);
            if (files.length > 0) {
                const fileInput = area.querySelector('.file-input');
                console.log('🔍 File input found:', fileInput.id);
                console.log('🔍 Before overwrite - fileInput.files:', fileInput.files.length);
                fileInput.files = files;
                console.log('🔍 After overwrite - fileInput.files:', fileInput.files.length);
                const fileNumber = fileInput.id === 'file1' ? 1 : 2;
                console.log('🔍 Calling handleFileSelect from drop for file', fileNumber);
                handleFileSelect(fileNumber, fileInput);
            }
        });
        
        // Add fallback click event listener to handle file input clicks
        const fileInput = area.querySelector('.file-input');
        if (fileInput) {
            console.log('🔍 Adding change event listener to:', fileInput.id);
            fileInput.addEventListener('change', function(e) {
                console.log('🔍 File input change event triggered for:', fileInput.id);
                const fileNumber = fileInput.id === 'file1' ? 1 : 2;
                handleFileSelect(fileNumber, this);
            });
            
            // Also add click event to make sure input is clickable
            area.addEventListener('click', function(e) {
                console.log('🔍 Upload area clicked:', area);
                if (e.target.tagName !== 'INPUT') {
                    console.log('🔍 Triggering file input click for:', fileInput.id);
                    fileInput.click();
                }
            });
        }
    });
    
    console.log('✅ Drag and drop initialized');
}

/**
 * Main comparison function - now uses backend API only
 */
async function compareFiles() {
    console.log('compareFiles() called - using backend API');
    
    // Validate files are uploaded
    if (!uploadedFiles.file1 || !uploadedFiles.file2) {
        alert('Vui lòng chọn cả 2 file để so sánh!');
        return;
    }

    // Use backend API for comparison
    if (typeof window.backendAPI === 'object' && typeof window.backendAPI.compareFiles === 'function') {
        console.log('Using backend API for comparison');
        try {
            await window.backendAPI.compareFiles();
        } catch (error) {
            console.error('Backend comparison failed:', error);
            alert(`Lỗi khi so sánh file qua backend: ${error.message}`);
        }
    } else {
        console.error('Backend API not available');
        alert('Backend API không sẵn sàng. Vui lòng tải lại trang và thử lại.');
    }
}

/**
 * Perform enhanced data comparison
 */
function performComparison(data1, data2) {
    const results = {
        matches: [],
        differences: [],
        warnings: [],
        summary: {
            totalRows: Math.max(data1.length, data2.length),
            matchingRows: 0,
            differentRows: 0,
            accuracyRate: 0,
            added: 0,
            removed: 0,
            modified: 0
        }
    };

    // Enhanced tolerance levels
    const tolerance = {
        quantity: 0.01,        // More strict for quantity
        unit_price: 0.001,     // More strict for unit price
        amount: 0.01          // Amount tolerance
    };

    // Smart matching based on description
    const findMatchingRow = (item, data, currentIndex) => {
        for (let i = 0; i < data.length; i++) {
            const candidate = data[i];
            if (i === currentIndex) continue; // Skip current index

            // Check if descriptions are similar (case-insensitive, ignore extra spaces)
            const desc1 = (item.description || '').toLowerCase().trim();
            const desc2 = (candidate.description || '').toLowerCase().trim();

            if (desc1 === desc2) {
                return candidate;
            }

            // Fuzzy matching: check if one description contains the other
            if (desc1.includes(desc2) || desc2.includes(desc1)) {
                return candidate;
            }
        }
        return null;
    };

    for (let i = 0; i < Math.max(data1.length, data2.length); i++) {
        const item1 = data1[i];
        const item2 = data2[i];

        // Handle empty/null items
        if (!item1 || !item2 || !item1.description || !item2.description) {
            if (!item1 && item2 && item2.description) {
                // Item added in file 2
                results.differences.push({
                    type: 'added',
                    rowNumber: i + 1,
                    description: 'Dòng dữ liệu được thêm',
                    severity: 'info',
                    item1: null,
                    item2: item2,
                    status: 'difference'
                });
                results.summary.added++;
            } else if (item1 && !item2 && item1.description) {
                // Item removed from file 2
                results.differences.push({
                    type: 'removed',
                    rowNumber: i + 1,
                    description: 'Dòng dữ liệu bị xóa',
                    severity: 'warning',
                    item1: item1,
                    item2: null,
                    status: 'difference'
                });
                results.summary.removed++;
            }
            results.summary.differentRows++;
            continue;
        }

        const comparison = {
            rowNumber: i + 1,
            item1: item1,
            item2: item2,
            status: 'match',
            differences: [],
            type: 'modified',
            similarityScore: 0
        };

        // Calculate similarity score for description
        const desc1 = (item1.description || '').toLowerCase().trim();
        const desc2 = (item2.description || '').toLowerCase().trim();
        comparison.similarityScore = calculateStringSimilarity(desc1, desc2);

        // Compare each field
        ['quantity', 'unit_price', 'amount'].forEach(field => {
            const val1 = parseFloat(item1[field]) || 0;
            const val2 = parseFloat(item2[field]) || 0;

            // Handle numeric comparison
            if (!isNaN(val1) && !isNaN(val2)) {
                const diff = Math.abs(val1 - val2);
                const percentDiff = val1 !== 0 ? (diff / val1) * 100 : 0;

                // Check if difference exceeds tolerance
                if (diff > tolerance[field] || percentDiff > 5) { // 5% tolerance for percentages
                    const severity = percentDiff > 20 ? 'critical' :
                                  percentDiff > 10 ? 'warning' : 'info';

                    comparison.differences.push({
                        field: field,
                        value1: val1,
                        value2: val2,
                        difference: diff,
                        percentDiff: percentDiff,
                        severity: severity
                    });
                }
            } else if (val1 !== val2) {
                // Handle text comparison
                const str1 = String(item1[field]);
                const str2 = String(item2[field]);

                if (str1 !== str2 && str1 && str2) {
                    comparison.differences.push({
                        field: field,
                        value1: val1,
                        value2: val2,
                        severity: 'info'
                    });
                }
            }
        });

        // Determine status based on differences and similarity
        if (comparison.differences.length > 0 || comparison.similarityScore < 0.8) {
            comparison.status = 'difference';
            results.differences.push(comparison);
            results.summary.modified++;
            results.summary.differentRows++;
        } else {
            results.matches.push(comparison);
            results.summary.matchingRows++;
        }
    }

    // Calculate accuracy rate
    results.summary.accuracyRate = Math.round(
        (results.summary.matchingRows / results.summary.totalRows) * 100
    );

    // Generate warnings for critical differences
    results.differences.forEach(diff => {
        if (diff.differences) {
            diff.differences.forEach(d => {
                if (d.severity === 'critical') {
                    results.warnings.push({
                        rowNumber: diff.rowNumber,
                        field: d.field,
                        message: `Sai lệch quan trọng trong ${d.field}: ${d.value1} → ${d.value2}`,
                        severity: 'critical'
                    });
                }
            });
        }
    });

    return results;
}

/**
 * Calculate string similarity using Levenshtein distance
 */
function calculateStringSimilarity(str1, str2) {
    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;

    if (longer.length === 0) return 1.0;
    if (shorter.length === 0) return 0.0;

    const distance = levenshteinDistance(longer, shorter);
    return (longer.length - distance) / longer.length;
}

/**
 * Simple Levenshtein distance calculation
 */
function levenshteinDistance(str1, str2) {
    const matrix = [];

    for (let i = 0; i <= str2.length; i++) {
        matrix[i] = [i];
    }

    for (let j = 0; j <= str1.length; j++) {
        matrix[0][j] = [j];
    }

    for (let i = 1; i <= str2.length; i++) {
        for (let j = 1; j <= str1.length; j++) {
            if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1]
                ) + 1;
            }
        }
    }

    return matrix[str2.length][str1.length];
}

/**
 * Display raw extracted data for verification
 */
function displayRawData() {
    if (!rawExtractedData.file1 || !rawExtractedData.file2) {
        console.log('No raw data to display');
        return;
    }

    console.log('Raw data types:', {
        file1: typeof rawExtractedData.file1,
        file2: typeof rawExtractedData.file2,
        file1Value: rawExtractedData.file1,
        file2Value: rawExtractedData.file2
    });

    // Extract data from structured_data if available
    const file1DataArray = extractDataFromStructured(rawExtractedData.file1);
    const file2DataArray = extractDataFromStructured(rawExtractedData.file2);

    if (file1DataArray.length === 0 && file2DataArray.length === 0) {
        console.log('Raw data arrays are empty');
        return;
    }

    // Update file names
    document.getElementById('rawFile1Name').textContent = uploadedFiles.file1?.name || 'File 1';
    document.getElementById('rawFile2Name').textContent = uploadedFiles.file2?.name || 'File 2';

    // Populate raw data tables
    const file1Data = document.getElementById('rawFile1Data');
    const file2Data = document.getElementById('rawFile2Data');

    file1Data.innerHTML = '';
    file2Data.innerHTML = '';

    // Helper function to create table row
    function createDataRow(data, index) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.no || data.STT || index + 1}</td>
            <td>${data.description || data['Mô tả sản phẩm'] || ''}</td>
            <td>${formatNumber(data.quantity || data['Số lượng'] || 0)}</td>
            <td>${formatCurrency(data.unit_price || data['Đơn giá'] || 0)}</td>
            <td>${formatCurrency(data.amount || data['Thành tiền'] || 0)}</td>
        `;
        return row;
    }

    // Populate file 1 data
    file1DataArray.forEach((item, index) => {
        file1Data.appendChild(createDataRow(item, index));
    });

    // Populate file 2 data
    file2DataArray.forEach((item, index) => {
        file2Data.appendChild(createDataRow(item, index));
    });

    console.log('Raw data displayed successfully');
}

/**
 * Extract data from structured data returned by backend
 */
function extractDataFromStructured(structuredData) {
    if (!structuredData) return [];
    
    // Handle different data formats from backend
    if (Array.isArray(structuredData)) {
        return structuredData;
    }
    
    // Handle structured_data format from backend
    if (structuredData.tables && Array.isArray(structuredData.tables)) {
        const allRows = [];
        structuredData.tables.forEach(table => {
            if (table.rows && Array.isArray(table.rows)) {
                // Convert backend row format to frontend format
                const convertedRows = table.rows.map(row => {
                    if (Array.isArray(row)) {
                        // Convert array to object using headers
                        const headers = table.headers || ['STT', 'Mô tả sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền'];
                        return {
                            no: row[0],
                            description: row[1],
                            quantity: parseFloat(row[2]) || 0,
                            unit_price: parseFloat(row[3]) || 0,
                            amount: parseFloat(row[4]) || 0
                        };
                    } else if (typeof row === 'object') {
                        return row;
                    }
                    return row;
                });
                allRows.push(...convertedRows);
            }
        });
        return allRows;
    }
    
    // Handle data format
    if (structuredData.data && Array.isArray(structuredData.data)) {
        return structuredData.data;
    }
    
    // Single object case
    if (typeof structuredData === 'object') {
        return [structuredData];
    }
    
    return [];
}

/**
 * Toggle raw data section visibility
 */
function toggleRawDataSection() {
    const section = document.getElementById('rawDataSection');
    if (section.style.display === 'none') {
        displayRawData();
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }
}

/**
 * Toggle raw data view within section
 */
function toggleRawDataView() {
    const container = document.getElementById('rawDataContainer');
    container.style.display = container.style.display === 'none' ? 'flex' : 'none';
}

/**
 * Export raw data to Markdown for verification
 */
function exportToMarkdown() {
    if (!rawExtractedData.file1 || !rawExtractedData.file2) {
        alert('Không có dữ liệu để xuất. Vui lòng so sánh file trước.');
        return;
    }

    // Extract data from structured format
    const file1Array = extractDataFromStructured(rawExtractedData.file1);
    const file2Array = extractDataFromStructured(rawExtractedData.file2);

    if (file1Array.length === 0 && file2Array.length === 0) {
        alert('Dữ liệu rỗng, không có gì để xuất.');
        return;
    }

    let markdown = `# Báo Cáo Dữ Liệu Gốc Trích Xuất\n\n`;
    markdown += `**Ngày tạo:** ${new Date().toLocaleString('vi-VN')}\n\n`;
    markdown += `**Mục đích:** Kiểm tra đối chứng dữ liệu trích xuất từ 2 file\n\n`;
    markdown += `**File 1:** ${uploadedFiles.file1?.name || 'File 1'}\n`;
    markdown += `**File 2:** ${uploadedFiles.file2?.name || 'File 2'}\n\n`;

    // File 1 data
    markdown += `## 📁 File 1: ${uploadedFiles.file1?.name || 'File 1'}\n\n`;
    markdown += `| STT | Mô tả sản phẩm | Số lượng | Đơn giá | Thành tiền |\n`;
    markdown += `|-----|---------------|----------|---------|------------|\n`;
    
    file1Array.forEach(item => {
        const stt = item.no || item.STT || '';
        const description = item.description || item['Mô tả sản phẩm'] || '';
        const quantity = item.quantity || item['Số lượng'] || 0;
        const unitPrice = item.unit_price || item['Đơn giá'] || 0;
        const amount = item.amount || item['Thành tiền'] || 0;
        
        markdown += `| ${stt} | ${description} | ${formatNumber(quantity)} | ${formatCurrency(unitPrice)} | ${formatCurrency(amount)} |\n`;
    });

    // File 2 data
    markdown += `\n## 📁 File 2: ${uploadedFiles.file2?.name || 'File 2'}\n\n`;
    markdown += `| STT | Mô tả sản phẩm | Số lượng | Đơn giá | Thành tiền |\n`;
    markdown += `|-----|---------------|----------|---------|------------|\n`;
    
    file2Array.forEach(item => {
        const stt = item.no || item.STT || '';
        const description = item.description || item['Mô tả sản phẩm'] || '';
        const quantity = item.quantity || item['Số lượng'] || 0;
        const unitPrice = item.unit_price || item['Đơn giá'] || 0;
        const amount = item.amount || item['Thành tiền'] || 0;
        
        markdown += `| ${stt} | ${description} | ${formatNumber(quantity)} | ${formatCurrency(unitPrice)} | ${formatCurrency(amount)} |\n`;
    });

    // Summary
    const file1Total = file1Array.reduce((sum, item) => sum + (item.amount || item['Thành tiền'] || 0), 0);
    const file2Total = file2Array.reduce((sum, item) => sum + (item.amount || item['Thành tiền'] || 0), 0);
    
    markdown += `\n## 📊 Tóm Tắt\n\n`;
    markdown += `- **Số dòng File 1:** ${file1Array.length}\n`;
    markdown += `- **Số dòng File 2:** ${file2Array.length}\n`;
    markdown += `- **Tổng tiền File 1:** ${formatCurrency(file1Total)}\n`;
    markdown += `- **Tổng tiền File 2:** ${formatCurrency(file2Total)}\n`;
    markdown += `- **Chênh lệch:** ${formatCurrency(Math.abs(file1Total - file2Total))}\n`;
    
    if (file1Total !== file2Total) {
        const percentage = ((Math.abs(file1Total - file2Total) / Math.max(file1Total, file2Total)) * 100).toFixed(2);
        markdown += `- **Chênh lệch (%):** ${percentage}%\n`;
    }

    // Create and download file
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `raw_data_verification_${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('Markdown file exported successfully');
}

/**
 * Display comparison results
 */
function displayResults(results) {
    // Update enhanced statistics
    const totalRows = results.summary.totalRows;
    const matchingRows = results.summary.matchingRows;
    const differentRows = results.summary.differentRows;
    const accuracyRate = results.summary.accuracyRate;

    document.getElementById('totalRows').textContent = totalRows;
    document.getElementById('matchingRows').textContent = matchingRows;
    document.getElementById('differentRows').textContent = differentRows;
    document.getElementById('accuracyRate').textContent = accuracyRate + '%';

    // Update percentage displays
    const matchingPercent = totalRows > 0 ? Math.round((matchingRows / totalRows) * 100) : 0;
    const differentPercent = totalRows > 0 ? Math.round((differentRows / totalRows) * 100) : 0;

    document.getElementById('matchingPercent').textContent = matchingPercent + '%';
    document.getElementById('differentPercent').textContent = differentPercent + '%';

    // Update diff summary badges
    updateDiffSummaryBadges(results);

    // Update file names
    if (uploadedFiles.file1) {
        document.getElementById('file1Name').textContent = uploadedFiles.file1.name;
    }
    if (uploadedFiles.file2) {
        document.getElementById('file2Name').textContent = uploadedFiles.file2.name;
    }

    // Generate side-by-side diff view with actual comparison data
    if (results.matches && results.differences) {
        const data1 = [];
        const data2 = [];

        // Reconstruct data from comparison results
        const allComparisons = [...results.matches, ...results.differences];
        allComparisons.sort((a, b) => a.rowNumber - b.rowNumber);

        allComparisons.forEach(comparison => {
            data1.push(comparison.item1 || {});
            data2.push(comparison.item2 || {});
        });

        if (typeof generateSideBySideDiffEnhanced === 'function') {
            generateSideBySideDiffEnhanced(data1, data2);
        } else if (typeof generateSideBySideDiff === 'function') {
            generateSideBySideDiff(data1, data2);
        }
    }

    // Show diff view container
    const diffContainer = document.getElementById('diffViewContainer');
    if (diffContainer) {
        diffContainer.style.display = 'block';
    }

    // Initialize diff navigation if available
    if (typeof updateNavigationState === 'function') {
        updateNavigationState();
    }

    // Populate comparison table (for table view)
    populateComparisonTable(results);

    // Display differences
    displayDifferences(results);
}

/**
 * Populate comparison table
 */
function populateComparisonTable(results) {
    const tableBody = document.getElementById('comparisonTable');
    if (!tableBody) return;

    tableBody.innerHTML = '';

    const allComparisons = [...results.matches, ...results.differences];
    allComparisons.sort((a, b) => a.rowNumber - b.rowNumber);

    allComparisons.forEach(comparison => {
        const row = document.createElement('tr');
        row.className = comparison.status;

        const statusIcon = comparison.status === 'match' ?
            '<span class="status-icon success">✓</span>' :
            '<span class="status-icon error">✗</span>';

        row.innerHTML = `
            <td>${comparison.rowNumber}</td>
            <td>${comparison.item1?.description || 'N/A'}</td>
            <td>${comparison.item1?.quantity || 'N/A'}</td>
            <td>${comparison.item2?.quantity || 'N/A'}</td>
            <td>${comparison.item1?.unit_price || 'N/A'}</td>
            <td>${comparison.item2?.unit_price || 'N/A'}</td>
            <td>${comparison.item1?.amount || 'N/A'}</td>
            <td>${comparison.item2?.amount || 'N/A'}</td>
            <td>${statusIcon}</td>
        `;

        if (comparison.differences && comparison.differences.length > 0) {
            const tooltip = comparison.differences.map(diff =>
                `${diff.field}: ${String(diff.value1)} → ${String(diff.value2)}`
            ).join(', ');
            row.title = tooltip;
        }

        tableBody.appendChild(row);
    });
}

/**
 * Display detailed differences
 */
function displayDifferences(results) {
    const differencesList = document.getElementById('differencesList');
    if (!differencesList) return;

    differencesList.innerHTML = '';

    if (results.differences.length === 0) {
        differencesList.innerHTML = '<p style="color: var(--color-success); text-align: center;">✓ Không có sai lệch nào được phát hiện!</p>';
    } else {
        results.differences.forEach(diff => {
            if (diff.differences) {
                diff.differences.forEach(fieldDiff => {
                    const diffItem = document.createElement('div');
                    diffItem.className = `difference-item ${fieldDiff.severity}`;

                    const fieldNames = {
                        description: 'Mô tả sản phẩm',
                        quantity: 'Số lượng',
                        unit_price: 'Đơn giá',
                        amount: 'Thành tiền'
                    };

                    diffItem.innerHTML = `
                        <div class="difference-title">Dòng ${diff.rowNumber}: ${fieldNames[fieldDiff.field]}</div>
                        <div class="difference-details">
                            File 1: ${fieldDiff.value1}<br>
                            File 2: ${fieldDiff.value2}
                            ${fieldDiff.difference ? `<br>Chênh lệch: ${fieldDiff.difference.toFixed(2)}` : ''}
                        </div>
                    `;

                    differencesList.appendChild(diffItem);
                });
            }
        });
    }
}

/**
 * Update diff summary badges
 */
function updateDiffSummaryBadges(results) {
    const addedCount = results.summary.added || 0;
    const removedCount = results.summary.removed || 0;
    const modifiedCount = results.summary.modified || 0;

    // Update counts
    const addedCountEl = document.getElementById('addedCount');
    const removedCountEl = document.getElementById('removedCount');
    const modifiedCountEl = document.getElementById('modifiedCount');

    if (addedCountEl) addedCountEl.textContent = addedCount;
    if (removedCountEl) removedCountEl.textContent = removedCount;
    if (modifiedCountEl) modifiedCountEl.textContent = modifiedCount;

    // Show/hide badges
    const addedBadge = document.querySelector('.diff-badge.added');
    const removedBadge = document.querySelector('.diff-badge.removed');
    const modifiedBadge = document.querySelector('.diff-badge.modified');

    if (addedBadge) addedBadge.style.display = addedCount > 0 ? 'flex' : 'none';
    if (removedBadge) removedBadge.style.display = removedCount > 0 ? 'flex' : 'none';
    if (modifiedBadge) modifiedBadge.style.display = modifiedCount > 0 ? 'flex' : 'none';
}

/**
 * Export functionality - now uses backend API
 */
function exportReport(format) {
    if (!comparisonResults) {
        alert('Vui lòng thực hiện so sánh trước khi xuất báo cáo!');
        return;
    }

    // Use backend export if available
    if (typeof window.backendAPI === 'object' && typeof window.backendAPI.exportBackendReport === 'function') {
        console.log('Using backend export for', format);
        window.backendAPI.exportBackendReport(format);
    } else {
        // Fallback to frontend export
        console.warn('Backend export not available, using frontend fallback');
        if (format === 'excel') {
            const csvContent = generateCSVContent();
            downloadFile(csvContent, 'comparison-report.csv', 'text/csv');
        } else if (format === 'pdf') {
            generatePDFReport();
        }
    }
}

function generateCSVContent() {
    if (!comparisonResults) return '';

    let csv = 'STT,Mô tả sản phẩm,Số lượng (File 1),Số lượng (File 2),Đơn giá (File 1),Đơn giá (File 2),Thành tiền (File 1),Thành tiền (File 2),Trạng thái\n';

    const allComparisons = [...comparisonResults.matches, ...comparisonResults.differences];
    allComparisons.sort((a, b) => a.rowNumber - b.rowNumber);

    allComparisons.forEach(comparison => {
        const status = comparison.status === 'match' ? 'Khớp' : 'Sai lệch';
        csv += `${comparison.rowNumber},"${comparison.item1?.description || 'N/A'}",${comparison.item1?.quantity || 'N/A'},${comparison.item2?.quantity || 'N/A'},${comparison.item1?.unit_price || 'N/A'},${comparison.item2?.unit_price || 'N/A'},${comparison.item1?.amount || 'N/A'},${comparison.item2?.amount || 'N/A'},${status}\n`;
    });

    return csv;
}

function downloadFile(content, fileName, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * Generate PDF report using jsPDF library
 */
async function generatePDFReport() {
    try {
        // Load jsPDF library if not already loaded
        if (typeof jspdf === 'undefined') {
            await loadJSPDFLibrary();
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF('p', 'mm', 'a4');

        // Add custom font for Vietnamese support
        doc.addFont('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.66/fonts/Roboto/Roboto-Regular.ttf', 'Roboto', 'normal');
        doc.setFont('Roboto');

        // PDF Generation
        let yPosition = 20;
        const pageWidth = doc.internal.pageSize.width;
        const margin = 20;
        const lineHeight = 7;

        // Title
        doc.setFontSize(20);
        doc.text('BÁO CÁO SO SÁNH FILE DỮ LIỆU', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;

        // File information
        doc.setFontSize(12);
        doc.text(`File 1: ${uploadedFiles.file1?.name || 'N/A'}`, margin, yPosition);
        yPosition += lineHeight;
        doc.text(`File 2: ${uploadedFiles.file2?.name || 'N/A'}`, margin, yPosition);
        yPosition += lineHeight;
        doc.text(`Ngày tạo: ${new Date().toLocaleString('vi-VN')}`, margin, yPosition);
        yPosition += 15;

        // Summary statistics
        doc.setFontSize(14);
        doc.text('TÓM TẮT KẾT QUẢ', margin, yPosition);
        yPosition += 10;

        doc.setFontSize(11);
        const summary = comparisonResults.summary;
        doc.text(`Tổng số dòng: ${summary.totalRows}`, margin, yPosition);
        yPosition += lineHeight;
        doc.text(`Dòng khớp: ${summary.matchingRows} (${((summary.matchingRows / summary.totalRows) * 100).toFixed(1)}%)`, margin, yPosition);
        yPosition += lineHeight;
        doc.text(`Dòng sai lệch: ${summary.differentRows} (${((summary.differentRows / summary.totalRows) * 100).toFixed(1)}%)`, margin, yPosition);
        yPosition += lineHeight;
        doc.text(`Tỷ lệ chính xác: ${summary.accuracyRate}%`, margin, yPosition);
        yPosition += 15;

        // Detailed differences
        if (comparisonResults.differences.length > 0) {
            doc.setFontSize(14);
            doc.text('CHI TIẾT SAI LỆCH', margin, yPosition);
            yPosition += 10;

            doc.setFontSize(10);
            comparisonResults.differences.forEach((diff, index) => {
                // Check if we need a new page
                if (yPosition > 250) {
                    doc.addPage();
                    yPosition = 20;
                }

                doc.text(`Dòng ${diff.rowNumber}: ${diff.item1?.description || 'N/A'}`, margin, yPosition);
                yPosition += lineHeight;

                if (diff.differences && diff.differences.length > 0) {
                    diff.differences.forEach(fieldDiff => {
                        const fieldNames = {
                            description: 'Mô tả',
                            quantity: 'Số lượng',
                            unit_price: 'Đơn giá',
                            amount: 'Thành tiền'
                        };

                        const fieldName = fieldNames[fieldDiff.field] || fieldDiff.field;
                        doc.text(`  - ${fieldName}: ${fieldDiff.value1} → ${fieldDiff.value2}`, margin + 5, yPosition);
                        yPosition += lineHeight;
                    });
                }
                yPosition += 3; // Extra space between entries
            });
        }

        // Save the PDF
        doc.save('comparison-report.pdf');
        showSuccessMessage('PDF report generated successfully!');

    } catch (error) {
        console.error('PDF generation error:', error);
        // Fallback to HTML export if PDF generation fails
        generateHTMLReport();
    }
}

/**
 * Load jsPDF library dynamically
 */
async function loadJSPDFLibrary() {
    return new Promise((resolve, reject) => {
        // Load jsPDF from CDN
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

/**
 * Generate HTML report as PDF fallback
 */
function generateHTMLReport() {
    const htmlContent = generateHTMLReportContent();
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    
    // Open in new window for printing/saving
    const printWindow = window.open(url, '_blank');
    printWindow.onload = function() {
        setTimeout(() => {
            printWindow.print();
        }, 500);
    };
    
    showSuccessMessage('HTML report opened. You can print or save as PDF from your browser.');
}

/**
 * Generate HTML report content
 */
function generateHTMLReportContent() {
    const summary = comparisonResults.summary;
    const timestamp = new Date().toLocaleString('vi-VN');
    
    let html = `
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo So Sánh File Dữ Liệu</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .difference { margin-bottom: 15px; padding: 10px; border-left: 4px solid #dc3545; background: #fff5f5; }
        .match { margin-bottom: 15px; padding: 10px; border-left: 4px solid #28a745; background: #f5fff5; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BÁO CÁO SO SÁNH FILE DỮ LIỆU</h1>
        <p>Ngày tạo: ${timestamp}</p>
        <p>File 1: ${uploadedFiles.file1?.name || 'N/A'}</p>
        <p>File 2: ${uploadedFiles.file2?.name || 'N/A'}</p>
    </div>

    <div class="summary">
        <h2>TÓM TẮT KẾT QUẢ</h2>
        <p><strong>Tổng số dòng:</strong> ${summary.totalRows}</p>
        <p><strong>Dòng khớp:</strong> ${summary.matchingRows} (${((summary.matchingRows / summary.totalRows) * 100).toFixed(1)}%)</p>
        <p><strong>Dòng sai lệch:</strong> ${summary.differentRows} (${((summary.differentRows / summary.totalRows) * 100).toFixed(1)}%)</p>
        <p><strong>Tỷ lệ chính xác:</strong> ${summary.accuracyRate}%</p>
    </div>

    <h2>CHI TIẾT SO SÁNH</h2>`;

    // Add detailed comparison
    const allComparisons = [...comparisonResults.matches, ...comparisonResults.differences];
    allComparisons.sort((a, b) => a.rowNumber - b.rowNumber);

    allComparisons.forEach(comparison => {
        if (comparison.status === 'match') {
            html += `
            <div class="match">
                <strong>Dòng ${comparison.rowNumber}: ✓ Khớp</strong><br>
                ${comparison.item1?.description || 'N/A'}
            </div>`;
        } else {
            html += `
            <div class="difference">
                <strong>Dòng ${comparison.rowNumber}: ✗ Sai lệch</strong><br>
                <strong>Mô tả:</strong> ${comparison.item1?.description || comparison.item2?.description || 'N/A'}<br>`;
            
            if (comparison.differences && comparison.differences.length > 0) {
                comparison.differences.forEach(diff => {
                    const fieldNames = {
                        description: 'Mô tả',
                        quantity: 'Số lượng',
                        unit_price: 'Đơn giá',
                        amount: 'Thành tiền'
                    };
                    html += `<strong>${fieldNames[diff.field]}:</strong> ${diff.value1} → ${diff.value2}<br>`;
                });
            }
            html += '</div>';
        }
    });

    html += `
    <div class="footer">
        <p>Generated by File Comparison System</p>
    </div>
</body>
</html>`;

    return html;
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    // Create a temporary success notification
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
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * Enhanced Theme System with System Preference Detection
 */

// Theme management
const THEME_STORAGE_KEY = 'file-comparison-theme-preference';
const THEME_SYSTEM = 'system';
const THEME_LIGHT = 'light';
const THEME_DARK = 'dark';

let currentThemeMode = THEME_SYSTEM;
let systemPreferenceMediaQuery = null;

/**
 * Toggle theme with cycle: System → Light → Dark → System
 */
function toggleTheme() {
    const html = document.documentElement;
    const currentMode = getCurrentThemeMode();
    
    let newMode;
    switch (currentMode) {
        case THEME_SYSTEM:
            newMode = THEME_LIGHT;
            break;
        case THEME_LIGHT:
            newMode = THEME_DARK;
            break;
        case THEME_DARK:
            newMode = THEME_SYSTEM;
            break;
        default:
            newMode = THEME_SYSTEM;
    }
    
    setThemeMode(newMode);
    updateThemeUI();
    saveThemePreference(newMode);
}

/**
 * Get current theme mode
 */
function getCurrentThemeMode() {
    return currentThemeMode;
}

/**
 * Set theme mode and apply it
 */
function setThemeMode(mode) {
    currentThemeMode = mode;
    applyTheme(mode);
}

/**
 * Apply theme based on mode
 */
function applyTheme(mode) {
    const html = document.documentElement;
    let actualTheme;
    
    if (mode === THEME_SYSTEM) {
        actualTheme = getSystemPreference();
    } else {
        actualTheme = mode;
    }
    
    html.setAttribute('data-color-scheme', actualTheme);
    html.setAttribute('data-theme-mode', mode);
    
    // Update meta theme-color for mobile browsers
    updateMetaThemeColor(actualTheme);
}

/**
 * Get system color scheme preference
 */
function getSystemPreference() {
    if (systemPreferenceMediaQuery) {
        return systemPreferenceMediaQuery.matches ? THEME_DARK : THEME_LIGHT;
    }
    // Fallback
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? THEME_DARK : THEME_LIGHT;
}

/**
 * Update UI elements based on current theme
 */
function updateThemeUI() {
    const themeButton = document.querySelector('.theme-toggle');
    const currentMode = getCurrentThemeMode();
    const actualTheme = currentMode === THEME_SYSTEM ? getSystemPreference() : currentMode;
    
    if (themeButton) {
        // Update button icon and tooltip
        let icon, tooltip;
        
        switch (currentMode) {
            case THEME_SYSTEM:
                icon = actualTheme === THEME_DARK ? '🌙' : '☀️';
                tooltip = `System (${actualTheme})`;
                break;
            case THEME_LIGHT:
                icon = '☀️';
                tooltip = 'Light mode';
                break;
            case THEME_DARK:
                icon = '🌙';
                tooltip = 'Dark mode';
                break;
        }
        
        themeButton.textContent = icon;
        themeButton.title = tooltip;
        themeButton.setAttribute('aria-label', tooltip);
    }
    
    // Update status for screen readers
    const statusElement = document.getElementById('theme-status');
    if (statusElement) {
        statusElement.textContent = `Theme: ${currentMode} (${actualTheme})`;
    }
}

/**
 * Save theme preference to localStorage
 */
function saveThemePreference(mode) {
    try {
        localStorage.setItem(THEME_STORAGE_KEY, mode);
    } catch (error) {
        console.warn('Could not save theme preference:', error);
    }
}

/**
 * Load theme preference from localStorage
 */
function loadThemePreference() {
    try {
        const saved = localStorage.getItem(THEME_STORAGE_KEY);
        return saved || THEME_SYSTEM;
    } catch (error) {
        console.warn('Could not load theme preference:', error);
        return THEME_SYSTEM;
    }
}

/**
 * Update meta theme-color for mobile browsers
 */
function updateMetaThemeColor(theme) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.name = 'theme-color';
        document.head.appendChild(metaThemeColor);
    }
    
    // Set appropriate theme colors
    const themeColors = {
        light: '#ffffff',
        dark: '#1a1a1a'
    };
    
    metaThemeColor.content = themeColors[theme] || themeColors.light;
}

/**
 * Listen for system theme changes
 */
function setupSystemThemeListener() {
    systemPreferenceMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Listen for changes
    systemPreferenceMediaQuery.addEventListener('change', (e) => {
        if (getCurrentThemeMode() === THEME_SYSTEM) {
            applyTheme(THEME_SYSTEM);
            updateThemeUI();
        }
    });
}

/**
 * Initialize theme system with system preference detection
 */
function initTheme() {
    // Load saved preference
    const savedMode = loadThemePreference();
    setThemeMode(savedMode);
    
    // Setup system theme listener
    setupSystemThemeListener();
    
    // Update UI
    updateThemeUI();
    
    // Add keyboard shortcut support
    setupThemeKeyboardShortcuts();
    
    // Add visual feedback for theme changes
    addThemeTransitionEffects();
}

/**
 * Setup keyboard shortcuts for theme switching
 */
function setupThemeKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Shift + T to toggle theme
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            toggleTheme();
        }
        
        // Ctrl/Cmd + Shift + S to set system theme
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'S') {
            e.preventDefault();
            setThemeMode(THEME_SYSTEM);
            updateThemeUI();
            saveThemePreference(THEME_SYSTEM);
        }
    });
}

/**
 * Add smooth transition effects for theme changes
 */
function addThemeTransitionEffects() {
    const style = document.createElement('style');
    style.textContent = `
        [data-color-scheme] {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }
        
        .theme-toggle {
            transition: transform 0.2s ease, opacity 0.2s ease;
        }
        
        .theme-toggle:hover {
            transform: scale(1.1);
        }
        
        .theme-toggle:active {
            transform: scale(0.95);
        }
        
        /* Theme change animation */
        @keyframes themeChange {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        
        .theme-changing {
            animation: themeChange 0.3s ease-in-out;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Get theme information for debugging
 */
function getThemeInfo() {
    return {
        currentMode: getCurrentThemeMode(),
        actualTheme: getCurrentThemeMode() === THEME_SYSTEM ? getSystemPreference() : getCurrentThemeMode(),
        systemPreference: getSystemPreference(),
        savedPreference: loadThemePreference(),
        supportsSystem: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').media !== 'not all'
    };
}

/**
 * Reset theme to system preference
 */
function resetThemeToSystem() {
    setThemeMode(THEME_SYSTEM);
    updateThemeUI();
    saveThemePreference(THEME_SYSTEM);
}

// Enhanced initialization with more robust error handling
function enhancedInitTheme() {
    try {
        initTheme();
        
        // Log theme info for debugging
        console.log('🎨 Theme initialized:', getThemeInfo());
        
        // Show initial theme notification (optional)
        if (localStorage.getItem('theme-notification-shown') !== 'true') {
            setTimeout(() => {
                const themeButton = document.querySelector('.theme-toggle');
                if (themeButton) {
                    // Add a subtle pulse animation to draw attention to theme button
                    themeButton.style.animation = 'pulse 2s ease-in-out 3';
                    setTimeout(() => {
                        themeButton.style.animation = '';
                    }, 6000);
                }
                localStorage.setItem('theme-notification-shown', 'true');
            }, 2000);
        }
        
    } catch (error) {
        console.error('Theme initialization failed:', error);
        // Fallback to basic theme setup
        document.documentElement.setAttribute('data-color-scheme', 'light');
        document.documentElement.setAttribute('data-theme-mode', 'light');
    }
}

// Demo data removed - only real user files are supported

/**
 * Initialize app
 */
document.addEventListener('DOMContentLoaded', function() {
    enhancedInitTheme();
    initializeDragAndDrop();
    // Demo button removed - only real user files
    
    // Initialize backend integration
    if (typeof window.backendAPI === 'object' && typeof window.backendAPI.initializeBackendIntegration === 'function') {
        window.backendAPI.initializeBackendIntegration();
    }
    
    // Add event listener for compare button
    const compareBtn = document.getElementById('compareBtn');
    if (compareBtn) {
        compareBtn.addEventListener('click', compareFiles);
    }

    renderPreview('file1');
    renderPreview('file2');
});