# 📊 File Comparison Frontend

Vietnamese web interface for comparing Excel, PDF, and CSV files with intelligent diff visualization.

## 🎨 Features

### 1. **Enhanced Diff Visualization**
- **Side-by-side view**: So sánh 2 file song song với màu sắc phân biệt
- **Unified view**: Hiển thị tất cả thay đổi trong một pane
- **Table view**: Xem dạng bảng biểu truyền thống

### 2. **Advanced Statistics**
- Enhanced statistics cards với gradient và icons
- Diff summary badges hiển thị số lượng thêm/xóa/thay đổi
- Real-time percentage calculations

### 3. **Interactive Features**
- Drag & drop file upload
- Theme toggle (light/dark mode)
- Responsive design
- Loading states và animations

### 4. **Export Functionality**
- Export to Excel (CSV format)
- Export to PDF (planned)
- Export diff report (text format)

## 📁 Cấu trúc thư mục

```
frontend/
├── index.html              # File HTML chính
├── README.md               # Documentation
├── styles/                 # CSS stylesheets
│   ├── main.css           # Styles chính (variables, base, components)
│   ├── diff.css           # Styles cho diff visualization
│   └── fonts.css          # Font local fallback
├── scripts/               # JavaScript modules
│   ├── main.js            # Module chính (file handling, comparison)
│   └── diff-visualization.js  # Module diff visualization
├── utils/                 # Utility functions
│   └── helpers.js         # Các hàm trợ giúp (format, validation)
└── components/            # Reusable components (cho tương lai)
```

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local backend server running on port 8000

### Running the Frontend

1. **Start the backend server:**
   ```bash
   cd ../backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the frontend:**
   - Simply open `index.html` in your web browser
   - Or serve with a local web server:
     ```bash
     # Using Python
     python -m http.server 3000

     # Using Node.js
     npx serve .

     # Using PHP
     php -S localhost:3000
     ```

3. **Access the application:**
   - Local server: http://localhost:3000
   - Direct file: file:///path/to/frontend/index.html

## Project Structure

```
frontend/
├── index.html              # Main application file
├── css/                    # Stylesheets (to be extracted)
├── js/                     # JavaScript modules (to be extracted)
├── assets/                 # Static assets
│   └── Hệ Thống So Sánh File Dữ Liệu_files/
│       └── css2            # Font CSS file
├── components/             # Reusable components (future)
└── README.md               # This file
```

## File Upload Support

- **PDF Documents**: `.pdf` files up to 50MB
- **Excel Spreadsheets**: `.xlsx`, `.xls` files
- **CSV Files**: `.csv` files with auto-detection

## Comparison Modes

- **Products**: Compare product catalogs and specifications
- **Invoices**: Validate invoice data against source documents
- **Contracts**: Compare contract terms and conditions
- **Custom**: User-defined comparison rules

## API Integration

The frontend communicates with the backend through REST API endpoints:

```javascript
// File upload
const formData = new FormData();
formData.append('file', file);
await fetch('/api/files/upload', { method: 'POST', body: formData });

// File comparison
await fetch('/api/comparison/compare', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ file1_id, file2_id, options })
});

// Export results
await fetch(`/api/export/comparison/${comparison_id}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ export_format: 'excel' })
});
```

## Browser Compatibility

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Features in Detail

### Upload Interface
- Drag and drop file upload
- File validation and preview
- Progress indicators
- Error handling

### Comparison Results
- Statistical overview cards
- Detailed comparison table
- Difference highlighting
- Export options

### Export Options
- **Excel**: Detailed spreadsheet with highlighting
- **PDF**: Professional report format
- **HTML**: Interactive web report
- **CSV**: Raw data for further analysis

### Configuration Options
- Exact match vs. fuzzy matching
- Tolerance settings for numerical values
- Field mapping customization
- Comparison type selection

## Development

### Code Structure
- **HTML**: Semantic markup with accessibility features
- **CSS**: Custom CSS variables for theming
- **JavaScript**: ES6+ with modern APIs
- **No Framework**: Vanilla JavaScript for simplicity

### Styling
- CSS custom properties for consistent theming
- Responsive grid layouts
- Component-based CSS organization
- Cross-browser compatibility

### JavaScript Features
- Async/await for API calls
- File API for uploads
- Modern DOM manipulation
- Error boundary handling

## Performance

- **Lazy Loading**: Components loaded on demand
- **Optimized Assets**: Compressed CSS and fonts
- **Caching**: Browser caching for static assets
- **Bundle Size**: Minimal dependencies

## Security

- **CORS**: Proper CORS configuration
- **File Validation**: Client-side file type checking
- **Data Sanitization**: XSS prevention
- **HTTPS**: Secure communication (production)

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Ensure backend server is running on port 8000
   - Check CORS configuration in backend

2. **File Upload Not Working**
   - Verify file format is supported
   - Check file size limits
   - Ensure browser supports File API

3. **Comparison Results Not Showing**
   - Check browser console for errors
   - Verify API responses are successful
   - Ensure files were processed successfully

### Debug Mode

Enable debug mode by adding `?debug=true` to the URL:
- Additional console logging
- Error details displayed
- Performance metrics shown

## 🧹 Clean Up đã thực hiện

- ✅ Xóa các thư mục trống (`css/`, `js/`, `assets/`)
- ✅ Di chuyển font file vào `styles/fonts.css`
- ✅ Tối ưu cấu trúc thư mục
- ✅ Cập nhật HTML paths
- ✅ Documentation mới

## 🔜 Future Enhancements

- **Component Extraction**: Extract reusable components
- **State Management**: Implement proper state management
- **Progressive Web App**: PWA capabilities
- **Offline Support**: Service worker implementation
- **Real-time Updates**: WebSocket integration

## License

MIT License - see LICENSE file for details.