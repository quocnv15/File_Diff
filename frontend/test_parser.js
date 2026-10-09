#!/usr/bin/env node
/**
 * Test script for file parsers
 */

const fs = require('fs');
const path = require('path');

// Mock DOM environment
global.window = {};
global.document = {};

// Load XLSX library (simulated)
console.log('Testing file parser logic...\n');

// Test CSV parsing
const csvData = fs.readFileSync('test_file1.csv', 'utf8');
console.log('CSV file content (first 200 chars):');
console.log(csvData.substring(0, 200) + '...\n');

// Test CSV delimiter detection
const firstLine = csvData.split('\n')[0];
const delimiters = [',', ';', '\t', '|'];
let bestDelimiter = ',';
let maxFields = 0;

delimiters.forEach(delimiter => {
    const fields = firstLine.split(delimiter);
    if (fields.length > maxFields) {
        maxFields = fields.length;
        bestDelimiter = delimiter;
    }
});

console.log(`Detected delimiter: "${bestDelimiter}"`);
console.log(`Number of fields: ${maxFields}`);

// Parse CSV manually to test logic
const lines = csvData.split('\n').filter(line => line.trim());
const headers = lines[0].split(bestDelimiter).map(h => h.trim().replace(/^\uFEFF/, '')); // Remove BOM

console.log('\nHeaders detected:');
headers.forEach((header, index) => {
    console.log(`${index + 1}. "${header}"`);
});

// Test data mapping
if (lines.length > 1) {
    const firstDataRow = lines[1].split(bestDelimiter).map(v => v.trim());
    const row = {};
    headers.forEach((header, index) => {
        row[header] = firstDataRow[index] || '';
    });

    console.log('\nFirst data row:');
    console.log('Raw data:', firstDataRow);
    console.log('Mapped to object:', row);

    // Test mapping to expected format
    const mappedRow = {
        no: String(row['STT'] || row['stt'] || row['No'] || row['no'] || 1),
        description: row['Mô tả sản phẩm'] || row['description'] || row['Mô tả'] || row['Product'] || row['Item'] || '',
        quantity: parseFloat(row['Số lượng'] || row['quantity'] || row['Quantity'] || row['SL'] || row['Qty'] || 0),
        unit_price: parseFloat(row['Đơn giá'] || row['unit_price'] || row['Unit Price'] || row['ĐG'] || row['Price'] || 0),
        amount: parseFloat(row['Thành tiền'] || row['amount'] || row['Amount'] || row['TT'] || row['Total'] || 0)
    };

    console.log('\nMapped result:');
    console.log('No:', mappedRow.no);
    console.log('Description:', mappedRow.description);
    console.log('Quantity:', mappedRow.quantity);
    console.log('Unit Price:', mappedRow.unit_price);
    console.log('Amount:', mappedRow.amount);

    console.log('\n✓ CSV parsing logic test completed successfully!');
} else {
    console.log('❌ No data rows found in CSV');
}