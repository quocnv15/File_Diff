/**
 * Enhanced Diff Visualization Module
 */

// Current diff view state
let currentDiffView = 'side-by-side';

// Navigation state
let currentDiffIndex = 0;
let allDiffLines = [];
let highlightedLines = [];

// Tooltip state
let activeTooltip = null;

/**
 * Switch between different diff views
 */
function switchDiffView(viewType) {
    currentDiffView = viewType;

    // Update button states
    document.querySelectorAll('.diff-view-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Hide all views
    const sideBySideView = document.getElementById('sideBySideView');
    const unifiedView = document.getElementById('unifiedView');
    const tableView = document.getElementById('tableView');

    if (sideBySideView) sideBySideView.style.display = 'none';
    if (unifiedView) unifiedView.style.display = 'none';
    if (tableView) tableView.style.display = 'none';

    // Show selected view
    switch(viewType) {
        case 'side-by-side':
            const sideBySideBtn = document.getElementById('sideBySideBtn');
            if (sideBySideBtn) {
                sideBySideBtn.classList.add('active');
                if (sideBySideView) sideBySideView.style.display = 'grid';
            }
            break;
        case 'unified':
            const unifiedBtn = document.getElementById('unifiedBtn');
            if (unifiedBtn) {
                unifiedBtn.classList.add('active');
                if (unifiedView) {
                    unifiedView.style.display = 'block';
                    generateUnifiedDiff();
                }
            }
            break;
        case 'table':
            const tableViewBtn = document.getElementById('tableViewBtn');
            if (tableViewBtn) {
                tableViewBtn.classList.add('active');
                if (tableView) tableView.style.display = 'block';
            }
            break;
    }
}

/**
 * Generate side-by-side diff view
 */
function generateSideBySideDiff(data1, data2) {
    const file1Content = document.getElementById('file1DiffContent');
    const file2Content = document.getElementById('file2DiffContent');

    if (!file1Content || !file2Content) return;

    file1Content.innerHTML = '';
    file2Content.innerHTML = '';

    const maxLength = Math.max(data1.length, data2.length);

    for (let i = 0; i < maxLength; i++) {
        const item1 = data1[i];
        const item2 = data2[i];

        if (!item1) {
            // File 1 has fewer rows
            const line1 = createDiffLine('', i + 1, 'empty');
            const line2 = createDiffLine(formatDataItem(item2), i + 1, 'added');
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);
        } else if (!item2) {
            // File 2 has fewer rows
            const line1 = createDiffLine(formatDataItem(item1), i + 1, 'removed');
            const line2 = createDiffLine('', i + 1, 'empty');
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);
        } else {
            // Compare items
            const comparison = compareDataItems(item1, item2);
            const line1 = createDiffLine(formatDataItem(item1), i + 1, comparison.status, comparison.diff1);
            const line2 = createDiffLine(formatDataItem(item2), i + 1, comparison.status, comparison.diff2);
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);
        }
    }
}

/**
 * Generate unified diff view
 */
function generateUnifiedDiff() {
    const unifiedContent = document.getElementById('unifiedDiffContent');
    if (!unifiedContent) return;

    unifiedContent.innerHTML = '';

    // Access global comparisonResults if available
    if (typeof comparisonResults === 'undefined' || !comparisonResults) return;

    const allComparisons = [...comparisonResults.matches, ...comparisonResults.differences];
    allComparisons.sort((a, b) => a.rowNumber - b.rowNumber);

    allComparisons.forEach(comparison => {
        const line = createUnifiedDiffLine(comparison);
        unifiedContent.appendChild(line);
    });
}

/**
 * Create a diff line element
 */
function createDiffLine(content, lineNumber, type, highlights = null) {
    const line = document.createElement('div');
    line.className = `diff-line ${type}`;

    if (type !== 'empty') {
        const lineNumberEl = document.createElement('div');
        lineNumberEl.className = 'diff-line-number';
        lineNumberEl.textContent = lineNumber;

        const contentEl = document.createElement('div');
        contentEl.className = 'diff-line-content';

        if (highlights) {
            contentEl.innerHTML = highlightDifferences(content, highlights);
        } else {
            contentEl.textContent = content;
        }

        line.appendChild(lineNumberEl);
        line.appendChild(contentEl);
    } else {
        // Empty line for spacing
        const spacer = document.createElement('div');
        spacer.style.height = '24px';
        line.appendChild(spacer);
    }

    return line;
}

/**
 * Create unified diff line
 */
function createUnifiedDiffLine(comparison) {
    const line = document.createElement('div');
    line.className = `diff-line ${comparison.status}`;

    const leftNumber = document.createElement('div');
    leftNumber.className = 'diff-line-number';
    leftNumber.textContent = comparison.item1 ? comparison.rowNumber : '';

    const rightNumber = document.createElement('div');
    rightNumber.className = 'diff-line-number';
    rightNumber.textContent = comparison.item2 ? comparison.rowNumber : '';

    const content = document.createElement('div');
    content.className = 'diff-line-content';

    if (comparison.status === 'match') {
        content.textContent = formatDataItem(comparison.item1);
    } else if (comparison.status === 'difference') {
        if (comparison.item1 && comparison.item2) {
            content.innerHTML = `<span class="diff-removed-text">${formatDataItem(comparison.item1)}</span> → <span class="diff-added-text">${formatDataItem(comparison.item2)}</span>`;
        } else if (comparison.item1) {
            content.innerHTML = `<span class="diff-removed-text">${formatDataItem(comparison.item1)}</span>`;
        } else {
            content.innerHTML = `<span class="diff-added-text">${formatDataItem(comparison.item2)}</span>`;
        }
    }

    line.appendChild(leftNumber);
    line.appendChild(rightNumber);
    line.appendChild(content);

    return line;
}

/**
 * Format data item for display
 */
function formatDataItem(item) {
    if (!item) return '';
    return `${item.description || ''} | SL: ${item.quantity || 0} | ĐG: ${item.unit_price || 0} | TT: ${item.amount || 0}`;
}

/**
 * Compare two data items
 */
function compareDataItems(item1, item2) {
    const result = {
        status: 'match',
        diff1: null,
        diff2: null
    };

    const tolerance = {
        quantity: 0.1,
        unit_price: 0.01,
        amount: 0.01
    };

    ['description', 'quantity', 'unit_price', 'amount'].forEach(field => {
        const val1 = item1[field];
        const val2 = item2[field];

        if (typeof val1 === 'number' && typeof val2 === 'number') {
            const diff = Math.abs(val1 - val2);
            if (diff > tolerance[field] || 0) {
                result.status = 'modified';
                if (!result.diff1) result.diff1 = {};
                if (!result.diff2) result.diff2 = {};
                result.diff1[field] = val1;
                result.diff2[field] = val2;
            }
        } else if (val1 !== val2) {
            result.status = 'modified';
            if (!result.diff1) result.diff1 = {};
            if (!result.diff2) result.diff2 = {};
            result.diff1[field] = val1;
            result.diff2[field] = val2;
        }
    });

    return result;
}

/**
 * Highlight differences in content
 */
function highlightDifferences(content, highlights) {
    if (!highlights) return content;

    let highlighted = content;

    Object.keys(highlights).forEach(field => {
        const value = highlights[field];
        const fieldNames = {
            description: 'Mô tả',
            quantity: 'SL',
            unit_price: 'ĐG',
            amount: 'TT'
        };

        const regex = new RegExp(`(${fieldNames[field]}: ${value})`, 'g');
        highlighted = highlighted.replace(regex, '<span class="diff-removed-text">$1</span>');
    });

    return highlighted;
}

/**
 * Export diff report
 */
function exportDiff() {
    // Access global comparisonResults if available
    if (typeof comparisonResults === 'undefined' || !comparisonResults) {
        alert('Vui lòng thực hiện so sánh trước khi xuất diff!');
        return;
    }

    console.log('Exporting diff with comparisonResults:', comparisonResults);
    console.log('comparisonResults structure:', {
        matches: comparisonResults.matches,
        differences: comparisonResults.differences,
        detailed_differences: comparisonResults.detailed_differences,
        type: {
            matches: typeof comparisonResults.matches,
            differences: typeof comparisonResults.differences,
            detailed_differences: typeof comparisonResults.detailed_differences
        }
    });

    let diffContent = 'DIFF REPORT\n';
    diffContent += '=' .repeat(50) + '\n\n';
    diffContent += `Generated: ${new Date().toLocaleString()}\n\n`;

    // Handle different possible structures of comparisonResults
    let allComparisons = [];
    
    if (comparisonResults.matches && Array.isArray(comparisonResults.matches)) {
        allComparisons.push(...comparisonResults.matches);
        console.log(`Added ${comparisonResults.matches.length} matches`);
    } else {
        console.log('No matches array found or matches is not an array');
    }
    
    if (comparisonResults.differences && Array.isArray(comparisonResults.differences)) {
        allComparisons.push(...comparisonResults.differences);
        console.log(`Added ${comparisonResults.differences.length} differences`);
    } else {
        console.log('No differences array found or differences is not an array');
    }
    
    // Fallback: if no structured data, try to extract from other properties
    if (allComparisons.length === 0) {
        console.log('Trying to extract data from alternative structure');
        
        // Try to get data from detailed_differences or other properties
        if (comparisonResults.detailed_differences && Array.isArray(comparisonResults.detailed_differences)) {
            allComparisons = comparisonResults.detailed_differences.map((diff, index) => ({
                rowNumber: diff.row_number || index + 1,
                status: diff.severity || 'difference',
                item1: { value1: diff.value1, field: diff.field },
                item2: { value2: diff.value2, field: diff.field },
                differences: [diff]
            }));
            console.log(`Extracted ${allComparisons.length} items from detailed_differences`);
        }
    }
    
    if (allComparisons.length === 0) {
        alert('Không có dữ liệu so sánh hợp lệ để xuất diff!');
        return;
    }
    
    console.log(`Processing ${allComparisons.length} comparison items`);
    
    allComparisons.sort((a, b) => (a.rowNumber || 0) - (b.rowNumber || 0));

    allComparisons.forEach(comparison => {
        diffContent += `Line ${comparison.rowNumber}: `;

        if (comparison.status === 'match') {
            diffContent += `✓ ${formatDataItem(comparison.item1)}\n`;
        } else if (comparison.status === 'difference') {
            diffContent += `⚠ ${formatDataItem(comparison.item1)} → ${formatDataItem(comparison.item2)}\n`;
        }

        if (comparison.differences && comparison.differences.length > 0) {
            comparison.differences.forEach(diff => {
                diffContent += `  - ${diff.field}: ${diff.value1} → ${diff.value2}\n`;
            });
        }
    });

    // Create and download file
    const blob = new Blob([diffContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'diff-report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * Enhanced diff highlighting with better visual indicators
 */
function highlightDifferencesEnhanced(content, highlights) {
    if (!highlights) return content;

    let highlighted = content;
    const fieldNames = {
        description: 'Mô tả',
        quantity: 'SL',
        unit_price: 'ĐG',
        amount: 'TT'
    };

    Object.keys(highlights).forEach(field => {
        const value = highlights[field];
        const regex = new RegExp(`(${fieldNames[field]}: ${value})`, 'g');
        highlighted = highlighted.replace(regex, `<span class="diff-modified-text">$1</span>`);
    });

    return highlighted;
}

/**
 * Navigation functions for diff lines
 */
function navigateDiff(direction) {
    if (allDiffLines.length === 0) return;

    switch(direction) {
        case 'first':
            currentDiffIndex = 0;
            break;
        case 'prev':
            currentDiffIndex = Math.max(0, currentDiffIndex - 1);
            break;
        case 'next':
            currentDiffIndex = Math.min(allDiffLines.length - 1, currentDiffIndex + 1);
            break;
        case 'last':
            currentDiffIndex = allDiffLines.length - 1;
            break;
    }

    scrollToDiffLine(currentDiffIndex);
    updateNavigationState();
}

function scrollToDiffLine(index) {
    const line = allDiffLines[index];
    if (line) {
        line.scrollIntoView({ behavior: 'smooth', block: 'center' });
        highlightLine(line);
    }
}

function highlightLine(line) {
    // Remove previous highlights
    document.querySelectorAll('.diff-line.highlighted').forEach(el => {
        el.classList.remove('highlighted');
    });

    // Add highlight to current line
    line.classList.add('highlighted');

    // Flash animation
    line.style.animation = 'none';
    setTimeout(() => {
        line.style.animation = 'pulse 1s ease-in-out';
    }, 10);
}

function updateNavigationState() {
    const prevBtn = document.querySelector('[onclick="navigateDiff(\'prev\')"]');
    const nextBtn = document.querySelector('[onclick="navigateDiff(\'next\')"]');

    if (prevBtn) prevBtn.disabled = currentDiffIndex === 0;
    if (nextBtn) nextBtn.disabled = currentDiffIndex === allDiffLines.length - 1;
}

/**
 * Search functionality
 */
function searchDiff(query) {
    clearSearch();

    if (!query.trim()) return;

    const regex = new RegExp(query, 'gi');
    const allLines = document.querySelectorAll('.diff-line-content');

    allLines.forEach(line => {
        const content = line.textContent;
        if (regex.test(content)) {
            line.parentElement.classList.add('search-highlight');
            highlightedLines.push(line.parentElement);
        }
    });

    if (highlightedLines.length > 0) {
        scrollToDiffLine(0);
        showSearchResults(highlightedLines.length, query);
    }
}

function clearSearch() {
    document.querySelectorAll('.search-highlight').forEach(el => {
        el.classList.remove('search-highlight');
    });
    highlightedLines = [];
    hideSearchResults();

    const searchInput = document.getElementById('diffSearchInput');
    if (searchInput) searchInput.value = '';
}

function showSearchResults(count, query) {
    showTooltip(`Tìm thấy ${count} kết quả cho "${query}"`, 'info');
}

function hideSearchResults() {
    hideTooltip();
}

/**
 * Enhanced tooltip system
 */
function showTooltip(message, type = 'info', element = null) {
    hideTooltip();

    const tooltip = document.createElement('div');
    tooltip.className = 'diff-tooltip show';
    tooltip.innerHTML = `
        <div class="diff-tooltip-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
        <div class="diff-tooltip-content">${message}</div>
    `;

    document.body.appendChild(tooltip);
    activeTooltip = tooltip;

    // Position tooltip
    if (element) {
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 10) + 'px';
    } else {
        tooltip.style.left = '50%';
        tooltip.style.top = '50px';
        tooltip.style.transform = 'translateX(-50%)';
    }

    // Auto hide after 3 seconds
    setTimeout(() => {
        hideTooltip();
    }, 3000);
}

function hideTooltip() {
    if (activeTooltip) {
        activeTooltip.classList.remove('show');
        setTimeout(() => {
            if (activeTooltip && activeTooltip.parentNode) {
                activeTooltip.parentNode.removeChild(activeTooltip);
            }
            activeTooltip = null;
        }, 200);
    }
}

/**
 * Enhanced diff line generation with better formatting
 */
function createDiffLineEnhanced(content, lineNumber, type, highlights = null, comparison = null) {
    const line = document.createElement('div');
    line.className = `diff-line ${type}`;

    // Add hover effect for better interactivity
    line.addEventListener('mouseenter', function() {
        this.classList.add('hover');
        if (comparison) {
            const tooltipMessage = getLineTooltipMessage(comparison);
            showTooltip(tooltipMessage, 'info', this);
        }
    });

    line.addEventListener('mouseleave', function() {
        this.classList.remove('hover');
        hideTooltip();
    });

    if (type !== 'empty') {
        const lineNumberEl = document.createElement('div');
        lineNumberEl.className = 'diff-line-number';
        lineNumberEl.textContent = lineNumber;

        const contentEl = document.createElement('div');
        contentEl.className = 'diff-line-content';

        if (highlights) {
            contentEl.innerHTML = highlightDifferencesEnhanced(content, highlights);
        } else {
            contentEl.textContent = content;
        }

        line.appendChild(lineNumberEl);
        line.appendChild(contentEl);
    } else {
        // Empty line for spacing
        const spacer = document.createElement('div');
        spacer.style.height = '24px';
        line.appendChild(spacer);
    }

    return line;
}

function getLineTooltipMessage(comparison) {
    if (comparison.status === 'match') {
        return 'Dòng này khớp hoàn toàn giữa hai file';
    } else if (comparison.differences && comparison.differences.length > 0) {
        const diffDetails = comparison.differences.map(diff => {
            const fieldNames = {
                description: 'Mô tả',
                quantity: 'Số lượng',
                unit_price: 'Đơn giá',
                amount: 'Thành tiền'
            };
            return `${fieldNames[diff.field]}: ${String(diff.value1)} → ${String(diff.value2)}`;
        }).join('\n');
        return `Sai lệch detected:\n${diffDetails}`;
    }
    return 'Dòng có sự thay đổi';
}

/**
 * Enhanced side-by-side diff generation
 */
function generateSideBySideDiffEnhanced(data1, data2) {
    const file1Content = document.getElementById('file1DiffContent');
    const file2Content = document.getElementById('file2DiffContent');

    if (!file1Content || !file2Content) return;

    file1Content.innerHTML = '';
    file2Content.innerHTML = '';
    allDiffLines = [];

    const maxLength = Math.max(data1.length, data2.length);

    for (let i = 0; i < maxLength; i++) {
        const item1 = data1[i];
        const item2 = data2[i];

        if (!item1) {
            // File 1 has fewer rows
            const line1 = createDiffLineEnhanced('', i + 1, 'empty');
            const line2 = createDiffLineEnhanced(formatDataItem(item2), i + 1, 'added', null, {status: 'added', item2: item2});
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);
            allDiffLines.push(line2);
        } else if (!item2) {
            // File 2 has fewer rows
            const line1 = createDiffLineEnhanced(formatDataItem(item1), i + 1, 'removed', null, {status: 'removed', item1: item1});
            const line2 = createDiffLineEnhanced('', i + 1, 'empty');
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);
            allDiffLines.push(line1);
        } else {
            // Compare items
            const comparison = compareDataItems(item1, item2);
            const line1 = createDiffLineEnhanced(formatDataItem(item1), i + 1, comparison.status, comparison.diff1, comparison);
            const line2 = createDiffLineEnhanced(formatDataItem(item2), i + 1, comparison.status, comparison.diff2, comparison);
            file1Content.appendChild(line1);
            file2Content.appendChild(line2);

            if (comparison.status !== 'match') {
                allDiffLines.push(line1, line2);
            }
        }
    }

    // Show navigation controls if there are differences
    if (allDiffLines.length > 0) {
        const navigation = document.getElementById('diffNavigation');
        if (navigation) {
            navigation.style.display = 'flex';
        }
        updateNavigationState();
    }
}

/**
 * Enhanced comparison with better diff detection
 */
function compareDataItemsEnhanced(item1, item2) {
    const result = {
        status: 'match',
        diff1: null,
        diff2: null,
        differences: []
    };

    const tolerance = {
        quantity: 0.1,
        unit_price: 0.01,
        amount: 0.01
    };

    ['description', 'quantity', 'unit_price', 'amount'].forEach(field => {
        const val1 = item1[field];
        const val2 = item2[field];

        if (typeof val1 === 'number' && typeof val2 === 'number') {
            const diff = Math.abs(val1 - val2);
            if (diff > tolerance[field] || 0) {
                result.status = 'modified';
                result.differences.push({
                    field: field,
                    value1: val1,
                    value2: val2,
                    difference: diff,
                    severity: field === 'amount' ? 'critical' : 'warning'
                });
                if (!result.diff1) result.diff1 = {};
                if (!result.diff2) result.diff2 = {};
                result.diff1[field] = val1;
                result.diff2[field] = val2;
            }
        } else if (val1 !== val2) {
            result.status = 'modified';
            result.differences.push({
                field: field,
                value1: val1,
                value2: val2,
                severity: 'info'
            });
            if (!result.diff1) result.diff1 = {};
            if (!result.diff2) result.diff2 = {};
            result.diff1[field] = val1;
            result.diff2[field] = val2;
        }
    });

    return result;
}

/**
 * Add CSS animation keyframes
 */
function addDiffAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(33, 128, 141, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(33, 128, 141, 0); }
            100% { box-shadow: 0 0 0 0 rgba(33, 128, 141, 0); }
        }

        .diff-line.highlighted {
            background: rgba(33, 128, 141, 0.1) !important;
            border-left: 4px solid var(--color-primary) !important;
        }

        .diff-line.search-highlight {
            background: rgba(245, 158, 11, 0.15) !important;
            border-left: 4px solid var(--color-warning) !important;
        }

        .diff-line.search-highlight .diff-line-number {
            background: rgba(245, 158, 11, 0.25) !important;
            color: var(--color-warning) !important;
        }
    `;
    document.head.appendChild(style);
}

// Initialize animations
addDiffAnimations();

// Enhanced global functions
window.navigateDiff = navigateDiff;
window.searchDiff = searchDiff;
window.clearSearch = clearSearch;
window.showTooltip = showTooltip;
window.hideTooltip = hideTooltip;

// Override existing functions with enhanced versions
window.switchDiffView = switchDiffView;
window.generateSideBySideDiff = generateSideBySideDiffEnhanced;
window.generateUnifiedDiff = generateUnifiedDiff;
window.exportDiff = exportDiff;