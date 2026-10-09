#!/usr/bin/env node
/**
 * Create various test files for comprehensive testing
 */

const fs = require('fs');
const path = require('path');

console.log('📁 Creating comprehensive test files...\n');

// Test data generators
function generateCSVData(rowCount, hasErrors = false) {
    let csv = 'STT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền\n';
    
    for (let i = 1; i <= rowCount; i++) {
        const quantity = Math.floor(Math.random() * 100) + 1;
        const unitPrice = (Math.random() * 1000 + 10).toFixed(2);
        const amount = (quantity * parseFloat(unitPrice)).toFixed(2);
        
        // Add some intentional errors for testing
        let description = `Sản phẩm kiểm thử ${i}`;
        if (hasErrors && i % 10 === 0) {
            description = ''; // Empty description
        }
        if (hasErrors && i % 15 === 0) {
            description = `@#$%^&*()${i}`; // Invalid characters
        }
        
        csv += `${i},"${description}",${quantity},${unitPrice},${amount}\n`;
    }
    
    return csv;
}

function generateLargeCSVData(rowCount = 1000) {
    let csv = 'STT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền\n';
    
    for (let i = 1; i <= rowCount; i++) {
        const quantity = Math.floor(Math.random() * 1000) + 1;
        const unitPrice = (Math.random() * 10000 + 10).toFixed(2);
        const amount = (quantity * parseFloat(unitPrice)).toFixed(2);
        
        csv += `${i},"Sản phẩm dữ liệu lớn ${i} với mô tả dài hơn để kiểm tra hiệu suất xử lý",${quantity},${unitPrice},${amount}\n`;
    }
    
    return csv;
}

function generateEdgeCaseCSV() {
    return `STT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền
1,"Sản phẩm có dấu đặc biệt: @#$%^&*()",5,100.50,502.50
2,"Sản phẩm có dấu tiếng Việt: ÁÀÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯ",10,200.75,2007.50
3,"Sản phẩm có dấu nháy đơn 'test'",3,150.25,450.75
4,"Sản phẩm có dấu nháy đôi "test"",7,300.00,2100.00
5,"Sản phẩm có dấu chấm phẩy; và dấu hai chấm:",2,400.50,801.00
6,"Sản phẩm có dấu gạch ngang - và gạch dưới_",8,500.75,4006.00
7,"Sản phẩm có dấu ngoặc đơn (test) và ngoặc vuông [test]",4,600.25,2401.00
8,"Sản phẩm có ký tự unicode: ☕ ★ ♠ ♥ ♦ ♣",6,700.00,4200.00
9,"Sản phẩm có công thức: H₂O và CO₂",1,800.50,800.50
10,"Sản phẩm có link: http://example.com/product/10",9,900.75,8106.75
`;
}

function generateMalformedCSV() {
    return `STT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền
1,Sản phẩm A,10,100.50
2,Sản phẩm B,20
3,Sản phẩm C,30,200.75,6022.50
4,Sản phẩm D
5,"Sản phẩm E có dấu phẩy trong mô tả, phần 2",40,300.25,12010.00
6,Sản phẩm F,50,400.50,20025.00
7,Sản phẩm G,60,500.75
8,Sản phẩm H,70,600.00,42000.00
`;
}

function generateEmptyAndNullCSV() {
    return `STT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền
1,,,100.50,50.25
2,Sản phẩm B,,200.75,
3,,30,,150.00
4,Sản phẩm D,40,,,
5,,50,500.75,25037.50
6,Sản phẩm F,60,600.00,
7,Sản phẩm G,,700.25,14005.00
8,,80,,32000.00
`;
}

// Create test files
const testFiles = [
    {
        name: 'test_small.csv',
        content: generateCSVData(10),
        description: 'Small CSV file (10 rows)'
    },
    {
        name: 'test_medium.csv',
        content: generateCSVData(100),
        description: 'Medium CSV file (100 rows)'
    },
    {
        name: 'test_large.csv',
        content: generateLargeCSVData(1000),
        description: 'Large CSV file (1000 rows)'
    },
    {
        name: 'test_with_errors.csv',
        content: generateCSVData(50, true),
        description: 'CSV file with intentional errors'
    },
    {
        name: 'test_edge_cases.csv',
        content: generateEdgeCaseCSV(),
        description: 'CSV file with edge cases and special characters'
    },
    {
        name: 'test_malformed.csv',
        content: generateMalformedCSV(),
        description: 'Malformed CSV file for error testing'
    },
    {
        name: 'test_empty_null.csv',
        content: generateEmptyAndNullCSV(),
        description: 'CSV file with empty and null values'
    }
];

// Create files
testFiles.forEach(file => {
    const filePath = path.join(__dirname, file.name);
    fs.writeFileSync(filePath, file.content, 'utf8');
    console.log(`✅ Created: ${file.name} (${file.content.length} bytes) - ${file.description}`);
});

// Create comparison pairs for testing
const comparisonPairs = [
    {
        file1: 'comparison_base.csv',
        file2: 'comparison_modified.csv',
        description: 'Files with intentional differences'
    },
    {
        file1: 'comparison_identical_1.csv',
        file2: 'comparison_identical_2.csv', 
        description: 'Identical files for testing'
    },
    {
        file1: 'comparison_reordered.csv',
        file2: 'comparison_reordered.csv',
        description: 'Files with different order'
    }
];

// Generate comparison files
const baseData = generateCSVData(20);
let modifiedData = generateCSVData(20).replace('Sản phẩm kiểm thử 5', 'Sản phẩm đã thay đổi 5');
modifiedData = modifiedData.replace('50,250.50,12525.00', '55,250.50,13777.50');

comparisonPairs.forEach((pair, index) => {
    let content1 = baseData;
    let content2 = baseData;
    
    if (index === 0) {
        content1 = baseData;
        content2 = modifiedData;
    } else if (index === 1) {
        content1 = baseData;
        content2 = baseData; // Identical
    } else if (index === 2) {
        // Create reordered version
        const lines = baseData.split('\n');
        const header = lines[0];
        const dataLines = lines.slice(1);
        // Shuffle data lines
        const shuffled = dataLines.sort(() => Math.random() - 0.5);
        content1 = header + '\n' + dataLines.join('\n');
        content2 = header + '\n' + shuffled.join('\n');
    }
    
    fs.writeFileSync(path.join(__dirname, pair.file1), content1, 'utf8');
    fs.writeFileSync(path.join(__dirname, pair.file2), content2, 'utf8');
    
    console.log(`✅ Created comparison pair: ${pair.file1} + ${pair.file2} - ${pair.description}`);
});

// Create a simple Excel file format simulation (CSV that Excel can open)
const excelFormatCSV = `sep=,\nSTT,Mô tả sản phẩm,Số lượng,Đơn giá,Thành tiền\n1,"Sản phẩm Excel 1",10,100.00,1000.00\n2,"Sản phẩm Excel 2",20,200.00,4000.00\n`;
fs.writeFileSync(path.join(__dirname, 'test_excel_format.csv'), excelFormatCSV, 'utf8');
console.log(`✅ Created: test_excel_format.csv - Excel compatible format`);

// Create different delimiter CSV files
const semicolonCSV = `STT;Mô tả sản phẩm;Số lượng;Đơn giá;Thành tiền\n1;"Sản phẩm dấu chấm phẩy";5;150,50;752,50\n2;"Sản phẩm khác";10;200,75;2007,50\n`;
fs.writeFileSync(path.join(__dirname, 'test_semicolon.csv'), semicolonCSV, 'utf8');
console.log(`✅ Created: test_semicolon.csv - Semicolon delimiter`);

const tabCSV = `STT\tMô tả sản phẩm\tSố lượng\tĐơn giá\tThành tiền\n1\t"Sản phẩm tab"\t5\t150.50\t752.50\n2\t"Sản phẩm khác"\t10\t200.75\t2007.50\n`;
fs.writeFileSync(path.join(__dirname, 'test_tab.csv'), tabCSV, 'utf8');
console.log(`✅ Created: test_tab.csv - Tab delimiter`);

// Create a test script summary
const summary = `
# Test Files Summary

Generated: ${new Date().toLocaleString()}

## Standard Test Files
- test_small.csv (10 rows) - Basic functionality testing
- test_medium.csv (100 rows) - Performance testing
- test_large.csv (1000 rows) - Stress testing
- test_with_errors.csv (50 rows) - Error handling testing
- test_edge_cases.csv (10 rows) - Special character handling
- test_malformed.csv - Malformed data testing
- test_empty_null.csv - Empty/null value testing

## Comparison Test Pairs
- comparison_base.csv + comparison_modified.csv - Difference detection
- comparison_identical_1.csv + comparison_identical_2.csv - Match detection
- comparison_reordered.csv (both) - Order independence testing

## Format Variations
- test_excel_format.csv - Excel compatible CSV
- test_semicolon.csv - Semicolon delimiter
- test_tab.csv - Tab delimiter

## Usage Examples
1. Load comprehensive_test.html in browser
2. Use files above for testing different scenarios
3. Test error handling with malformed files
4. Test performance with large files
5. Test special character handling with edge cases

Total files created: ${testFiles.length + comparisonPairs.length * 2 + 3}
`;

fs.writeFileSync(path.join(__dirname, 'TEST_FILES_SUMMARY.md'), summary, 'utf8');
console.log('\n📋 Created: TEST_FILES_SUMMARY.md');
console.log(`\n🎉 Successfully created ${testFiles.length + comparisonPairs.length * 2 + 3} test files!`);
console.log('\n🌐 Next steps:');
console.log('1. Open http://localhost:8080/comprehensive_test.html');
console.log('2. Upload and test various file scenarios');
console.log('3. Check browser console for detailed logs');
console.log('4. Verify error handling and performance');