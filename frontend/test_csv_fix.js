// Quick test script to verify CSV parsing fix
console.log('Testing CSV parsing fix...');

// Test data that matches the problematic format
const sampleCSV = `STT,"Tên hàng hóa, dịch vụ",Đơn vị,Số lượng,Đơn giá,Thành tiền
1,Canxi Carbonate Coated 1500T,kg,500,75000,37500000
2,Talc Powder 325 mesh,kg,200,120000,24000000`;

// Test the parseCSVLine function
function parseCSVLine(line, delimiter) {
    const result = [];
    let current = '';
    let inQuotes = false;
    let i = 0;
    
    while (i < line.length) {
        const char = line[i];
        const nextChar = line[i + 1];
        
        if (char === '"') {
            if (inQuotes && nextChar === '"') {
                current += '"';
                i += 2;
                continue;
            } else {
                inQuotes = !inQuotes;
                i++;
                continue;
            }
        }
        
        if (char === delimiter && !inQuotes) {
            result.push(current.trim());
            current = '';
            i++;
            continue;
        }
        
        current += char;
        i++;
    }
    
    result.push(current.trim());
    return result;
}

// Test parsing
const lines = sampleCSV.split('\n');
const delimiter = ',';
const headers = parseCSVLine(lines[0], delimiter);
console.log('Headers:', headers);

const firstDataRow = parseCSVLine(lines[1], delimiter);
console.log('First data row:', firstDataRow);

// Test mapping
const row = {};
headers.forEach((header, index) => {
    row[header] = firstDataRow[index] || '';
});

console.log('Row object:', row);

// Test the mapping logic
const mappedRow = {
    no: String(row['STT'] || row['stt'] || row['No'] || row['no'] || 1),
    description: row['Tên hàng hóa, dịch vụ'] || row['Mô tả sản phẩm'] || row['Description'] || row['description'] || '',
    quantity: parseFloat(row['Số lượng'] || row['Quantity'] || row['quantity'] || 0),
    unit_price: parseFloat(row['Đơn giá'] || row['Unit Price'] || row['unit_price'] || 0),
    amount: parseFloat(row['Thành tiền'] || row['Amount'] || row['amount'] || 0)
};

console.log('Mapped row:', mappedRow);
console.log('Has description:', !!mappedRow.description);
console.log('Test completed!');