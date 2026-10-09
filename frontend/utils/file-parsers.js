/**
 * File Parser Utilities
 * Handles parsing of Excel, PDF, and CSV files
 */

/**
 * Parse Excel files (XLSX, XLS)
 */
async function parseExcelFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function(e) {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });

                // Get first worksheet
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];

                // Convert to JSON
                const jsonData = XLSX.utils.sheet_to_json(worksheet, {
                    header: 1,
                    defval: '',
                    blankrows: false
                });

                // Map to expected format
                const parsedData = jsonData.map((row, index) => {
                    return {
                        no: String(row['STT'] || row['stt'] || row['No'] || row['no'] || index + 1),
                        description: row['Mô tả sản phẩm'] || row['Description'] || row['description'] || row['Mô tả'] || row['Product'] || row['Item'] || '',
                        quantity: parseFloat(row['Số lượng'] || row['Quantity'] || row['quantity'] || row['SL'] || row['Qty'] || 0),
                        unit_price: parseFloat(row['Đơn giá'] || row['Unit Price'] || row['unit_price'] || row['ĐG'] || row['Price'] || 0),
                        amount: parseFloat(row['Thành tiền'] || row['Amount'] || row['amount'] || row['TT'] || row['Total'] || 0)
                    };
                }).filter(item => item.description); // Filter out empty rows

                resolve(parsedData);
            } catch (error) {
                reject(new Error(`Lỗi khi đọc file Excel: ${error.message}`));
            }
        };

        reader.onerror = () => reject(new Error('Không thể đọc file Excel'));
        reader.readAsArrayBuffer(file);
    });
}

/**
 * Parse CSV files
 */
async function parseCSVFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        console.log('CSV Debug - File object:', {
            name: file.name,
            size: file.size,
            type: file.type,
            lastModified: file.lastModified
        });

        reader.onload = function(e) {
            try {
                let text = e.target.result;

                console.log('CSV Debug - Raw text length:', text.length);
                console.log('CSV Debug - Is text empty?', text.length === 0);
                console.log('CSV Debug - First 100 chars:', text.substring(0, 100));
                console.log('CSV Debug - Raw result type:', typeof e.target.result);

                // Remove BOM if present
                if (text.charCodeAt(0) === 0xFEFF) {
                    text = text.slice(1);
                    console.log('CSV Debug - BOM removed');
                }

                // Normalize line endings and filter empty lines
                const lines = text.split(/\r?\n/).filter(line => line.trim());
                console.log('CSV Debug - Lines count:', lines.length);
                console.log('CSV Debug - First line:', lines[0]);

                if (lines.length === 0) {
                    reject(new Error('File CSV rỗng'));
                    return;
                }

                // Try to detect delimiter
                const delimiter = detectDelimiter(lines[0]);
                console.log('CSV Debug - Detected delimiter:', delimiter);

                // Parse CSV with proper quote handling
                const parsedData = [];
                const headers = parseCSVLine(lines[0], delimiter).map(h => String(h).trim().replace(/^\uFEFF/, '')); // Remove BOM from header
                console.log('CSV Debug - Headers:', headers);

                for (let i = 1; i < lines.length; i++) {
                    const values = parseCSVLine(lines[i], delimiter).map(v => String(v).trim());

                    if (values.length >= headers.length) {
                        const row = {};
                        headers.forEach((header, index) => {
                            row[header] = values[index] || '';
                        });

                        // Map to expected format with more comprehensive header matching
                        const mappedRow = {
                            no: String(row['STT'] || row['stt'] || row['No'] || row['no'] || i),
                            description: row['Tên hàng hóa, dịch vụ'] || row['Mô tả sản phẩm'] || row['Description'] || row['description'] || row['Mô tả'] || row['Product'] || row['Item'] || row['Tên hàng hóa'] || '',
                            quantity: parseFloat(row['Số lượng'] || row['Quantity'] || row['quantity'] || row['SL'] || row['Qty'] || 0),
                            unit_price: parseFloat(row['Đơn giá'] || row['Unit Price'] || row['unit_price'] || row['ĐG'] || row['Price'] || 0),
                            amount: parseFloat(row['Thành tiền'] || row['Amount'] || row['amount'] || row['TT'] || row['Total'] || 0)
                        };

                        // Debug logging for mapping
                        console.log('CSV Debug - Row mapping:', {
                            original: row,
                            mapped: mappedRow,
                            hasDescription: !!mappedRow.description
                        });

                        // Accept rows with description OR with non-zero quantity/amount (for items without descriptions)
                        if (mappedRow.description || (mappedRow.quantity > 0 && mappedRow.amount > 0)) {
                            parsedData.push(mappedRow);
                            console.log('CSV Debug - Row added to parsed data');
                        } else {
                            console.log('CSV Debug - Row skipped - no description and no values');
                        }
                    }
                }

                console.log('CSV Debug - Parsed data count:', parsedData.length);
                console.log('CSV Debug - First item:', parsedData[0]);

                resolve(parsedData);
            } catch (error) {
                console.error('CSV Debug - Error:', error);
                reject(new Error(`Lỗi khi đọc file CSV: ${error.message}`));
            }
        };

        reader.onerror = () => reject(new Error('Không thể đọc file CSV'));

        // Try different encodings
        try {
            reader.readAsText(file, 'UTF-8');
        } catch (error) {
            console.log('Trying with different encoding...');
            reader.readAsText(file);
        }
    });
}

/**
 * Detect CSV delimiter
 */
function detectDelimiter(firstLine) {
    const delimiters = [',', ';', '\t', '|'];
    let bestDelimiter = ',';
    let maxFields = 0;

    delimiters.forEach(delimiter => {
        // Use proper CSV parsing for delimiter detection
        const fields = parseCSVLine(firstLine, delimiter);
        if (fields.length > maxFields) {
            maxFields = fields.length;
            bestDelimiter = delimiter;
        }
    });

    console.log('CSV Debug - Delimiter detection:', {
        firstLine: firstLine,
        detectedDelimiter: bestDelimiter,
        fieldCount: maxFields
    });

    return bestDelimiter;
}

function parseCSVLine(line, delimiter) {
    // Simple CSV parser that handles quoted fields
    const result = [];
    let current = '';
    let inQuotes = false;
    let i = 0;
    
    while (i < line.length) {
        const char = line[i];
        const nextChar = line[i + 1];
        
        if (char === '"') {
            if (inQuotes && nextChar === '"') {
                // Escaped quote
                current += '"';
                i += 2;
                continue;
            } else {
                // Toggle quote state
                inQuotes = !inQuotes;
                i++;
                continue;
            }
        }
        
        if (char === delimiter && !inQuotes) {
            // Field delimiter
            result.push(current.trim());
            current = '';
            i++;
            continue;
        }
        
        current += char;
        i++;
    }
    
    // Add last field
    result.push(current.trim());
    
    return result;
}

/**
 * Parse PDF files using PDF.js library
 * Enhanced implementation with table extraction capabilities
 */
async function parsePDFFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = async function(e) {
            try {
                // Load PDF.js library if not already loaded
                if (typeof pdfjsLib === 'undefined') {
                    await loadPDFJSLibrary();
                }

                // Load PDF document
                const typedarray = new Uint8Array(e.target.result);
                const pdf = await pdfjsLib.getDocument(typedarray).promise;
                
                let fullText = '';
                const tableData = [];

                // Extract text from all pages
                for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                    const page = await pdf.getPage(pageNum);
                    const textContent = await page.getTextContent();
                    const pageText = textContent.items.map(item => item.str).join(' ');
                    fullText += pageText + '\n';
                }

                // Try to extract table data from text
                const extractedData = extractTableDataFromPDFText(fullText);
                
                if (extractedData.length > 0) {
                    resolve(extractedData);
                } else {
                    // Fallback to smart parsing based on common patterns
                    const fallbackData = parsePDFTextToData(fullText);
                    resolve(fallbackData);
                }

            } catch (error) {
                console.error('PDF parsing error:', error);
                // Fallback to basic parsing if PDF.js fails
                const fallbackData = generateFallbackPDFData();
                resolve(fallbackData);
            }
        };

        reader.onerror = () => reject(new Error('Không thể đọc file PDF'));
        reader.readAsArrayBuffer(file);
    });
}

/**
 * Load PDF.js library dynamically
 */
async function loadPDFJSLibrary() {
    return new Promise((resolve, reject) => {
        // Load PDF.js from CDN
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
        script.onload = () => {
            // Configure PDF.js worker
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            resolve();
        };
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

/**
 * Extract table data from PDF text
 */
function extractTableDataFromPDFText(text) {
    const lines = text.split('\n').filter(line => line.trim());
    const data = [];
    
    // Common patterns for Vietnamese invoices/documents
    const patterns = {
        description: /(?:mô tả|sản phẩm|product|description|tên hàng|hàng hóa)(.*?)(?=số lượng|quantity|sl|đơn giá|unit price|đg|thành tiền|amount|tt|$)/i,
        quantity: /(?:số lượng|quantity|sl)(.*?)(?=đơn giá|unit price|đg|thành tiền|amount|tt|$)/i,
        unitPrice: /(?:đơn giá|unit price|đg)(.*?)(?=thành tiền|amount|tt|$)/i,
        amount: /(?:thành tiền|amount|tt)(.*?)(?=tổng|total|sum|$)/i
    };

    let currentRow = {};
    let rowNumber = 1;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Skip headers and footers
        if (isHeaderOrFooter(line)) continue;
        
        // Try to extract data using patterns
        const matches = extractDataFromLine(line, patterns);
        
        if (matches.description || matches.quantity || matches.unitPrice || matches.amount) {
            currentRow = {
                no: String(rowNumber),
                description: cleanText(matches.description || extractDescriptionFromLine(line)),
                quantity: parseNumber(matches.quantity),
                unit_price: parseNumber(matches.unitPrice),
                amount: parseNumber(matches.amount)
            };
            
            if (currentRow.description) {
                data.push(currentRow);
                rowNumber++;
            }
        }
    }

    return data;
}

/**
 * Parse PDF text to structured data using smart extraction
 */
function parsePDFTextToData(text) {
    const lines = text.split('\n').filter(line => line.trim());
    const data = [];
    
    // Look for numeric patterns that indicate quantities and prices
    const numericPattern = /\d+[.,]?\d*/g;
    let rowNumber = 1;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        const numbers = line.match(numericPattern);
        
        if (numbers && numbers.length >= 2) {
            // Try to extract meaningful data
            const description = extractDescriptionFromLine(line);
            const cleanLine = line.replace(/\d+[.,]?\d*/g, '###NUMBER###').split('###NUMBER###').filter(part => part.trim());
            
            if (description && numbers.length >= 2) {
                data.push({
                    no: String(rowNumber),
                    description: description,
                    quantity: parseNumber(numbers[0]) || 0,
                    unit_price: parseNumber(numbers[1]) || parseNumber(numbers[numbers.length - 2]) || 0,
                    amount: parseNumber(numbers[numbers.length - 1]) || 0
                });
                rowNumber++;
            }
        }
    }

    return data.length > 0 ? data : generateFallbackPDFData();
}

/**
 * Check if line is header or footer
 */
function isHeaderOrFooter(line) {
    const headerFooterKeywords = [
        'hóa đơn', 'invoice', 'đơn hàng', 'order', 'tổng cộng', 'total', 'sum',
        'thành tiền', 'amount', 'tiền thuế', 'tax', 'chữ ký', 'signature',
        'ngày', 'date', 'tháng', 'month', 'năm', 'year', 'page', 'trang'
    ];
    
    const lowerLine = line.toLowerCase();
    return headerFooterKeywords.some(keyword => lowerLine.includes(keyword));
}

/**
 * Extract data from line using patterns
 */
function extractDataFromLine(line, patterns) {
    const matches = {};
    
    Object.keys(patterns).forEach(key => {
        const match = line.match(patterns[key]);
        if (match && match[1]) {
            matches[key] = match[1].trim();
        }
    });
    
    return matches;
}

/**
 * Extract description from line
 */
function extractDescriptionFromLine(line) {
    // Remove numeric values and common price indicators
    const cleaned = line
        .replace(/\d+[.,]?\d*/g, '')
        .replace(/[vnđ|$|€|¥]/gi, '')
        .replace(/\b(vnd|usd|eur)\b/gi, '')
        .trim();
    
    // Return first meaningful part
    const parts = cleaned.split(/\s+/).filter(part => part.length > 2);
    return parts.slice(0, 5).join(' '); // Limit description length
}

/**
 * Clean text from unwanted characters
 */
function cleanText(text) {
    if (!text) return '';
    return text
        .replace(/[^\w\s\u00C0-\u024F]/g, ' ') // Keep Unicode characters for Vietnamese
        .replace(/\s+/g, ' ')
        .trim();
}

/**
 * Parse number from string
 */
function parseNumber(str) {
    if (!str) return 0;
    const cleaned = str.toString()
        .replace(/[^\d.,-]/g, '')
        .replace(/,/g, '.');
    const num = parseFloat(cleaned);
    return isNaN(num) ? 0 : num;
}

/**
 * Generate fallback PDF data when parsing fails
 */
function generateFallbackPDFData() {
    return [
        {
            no: "1",
            description: "PDF Data Extraction Failed - Using Fallback",
            quantity: 1,
            unit_price: 0.00,
            amount: 0.00
        }
    ];
}

/**
 * Main file parser function with enhanced error handling
 */
async function parseFile(file) {
    const fileName = file.name.toLowerCase();
    const fileSize = file.size;

    // Enhanced file size validation
    const maxSize = {
        'xlsx': 50 * 1024 * 1024,  // 50MB
        'xls': 50 * 1024 * 1024,   // 50MB
        'csv': 10 * 1024 * 1024,   // 10MB
        'pdf': 20 * 1024 * 1024    // 20MB
    };

    const fileExtension = fileName.split('.').pop();
    const allowedSize = maxSize[fileExtension] || 10 * 1024 * 1024;

    if (fileSize > allowedSize) {
        const sizeMB = (fileSize / 1024 / 1024).toFixed(2);
        const allowedMB = (allowedSize / 1024 / 1024).toFixed(0);
        throw new Error(`File quá lớn (${sizeMB}MB). Vui lòng chọn file ${fileExtension.toUpperCase()} dưới ${allowedMB}MB`);
    }

    // Validate file type
    const supportedTypes = {
        'xlsx': parseExcelFile,
        'xls': parseExcelFile,
        'csv': parseCSVFile,
        'pdf': parsePDFFile
    };

    if (!supportedTypes[fileExtension]) {
        throw new Error(`Không hỗ trợ định dạng file: ${fileExtension.toUpperCase()}. Vui lòng chọn file Excel (.xlsx, .xls), CSV (.csv) hoặc PDF (.pdf)`);
    }

    try {
        console.log(`Starting to parse ${fileExtension.toUpperCase()} file: ${fileName}`);
        const data = await supportedTypes[fileExtension](file);
        console.log(`Successfully parsed ${data.length} records from ${fileName}`);

        if (data.length === 0) {
            throw new Error(`File ${fileName} không có dữ liệu hoặc không thể đọc được. Vui lòng kiểm tra lại nội dung file.`);
        }

        return data;
    } catch (error) {
        console.error(`Error parsing file ${fileName}:`, error);
        
        // Provide more specific error messages
        if (error.message.includes('PDF')) {
            throw new Error(`Lỗi khi đọc file PDF: ${error.message}. Vui lòng đảm bảo file PDF không bị bảo vệ và có thể trích xuất text.`);
        } else if (error.message.includes('Excel') || error.message.includes('XLSX')) {
            throw new Error(`Lỗi khi đọc file Excel: ${error.message}. Vui lòng đảm bảo file không bị hỏng và có thể mở được.`);
        } else if (error.message.includes('CSV')) {
            throw new Error(`Lỗi khi đọc file CSV: ${error.message}. Vui lòng kiểm tra encoding và định dạng file.`);
        } else {
            throw new Error(`Lỗi khi xử lý file ${fileName}: ${error.message}`);
        }
    }
}

/**
 * Validate parsed data
 */
function validateParsedData(data) {
    if (!Array.isArray(data)) {
        throw new Error('Dữ liệu không hợp lệ');
    }

    if (data.length === 0) {
        throw new Error('Không có dữ liệu để so sánh');
    }

    // Check required fields
    const requiredFields = ['description'];
    const firstRow = data[0];

    for (const field of requiredFields) {
        if (!firstRow[field]) {
            throw new Error(`Thiếu trường bắt buộc: ${field}`);
        }
    }

    return true;
}

/**
 * Format data for comparison
 */
function formatDataForComparison(data) {
    return data.map((item, index) => ({
        ...item,
        rowNumber: index + 1,
        // Ensure numeric values
        quantity: parseFloat(item.quantity) || 0,
        unit_price: parseFloat(item.unit_price) || 0,
        amount: parseFloat(item.amount) || 0
    }));
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        parseFile,
        parseExcelFile,
        parseCSVFile,
        parsePDFFile,
        validateParsedData,
        formatDataForComparison
    };
}

// Export for browser use
if (typeof window !== 'undefined') {
    window.parseFile = parseFile;
    window.parseExcelFile = parseExcelFile;
    window.parseCSVFile = parseCSVFile;
    window.parsePDFFile = parsePDFFile;
    window.validateParsedData = validateParsedData;
    window.formatDataForComparison = formatDataForComparison;
}