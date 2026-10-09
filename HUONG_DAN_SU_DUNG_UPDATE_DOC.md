# 📚 Hướng Dẫn Sử Dụng Hệ Thống Documentation Update

## 🎯 Mục Đích

Hệ thống `update-doc` được tạo ra để tự động hóa việc mapping thông tin từ source code và các file chưa commit vào thư mục `.agent`, giúp team luôn có documentation cập nhật nhất.

## 🛠️ Các Công Cụ Có Sẵn

### 1. `update-doc` (Script chính)
- **Mục đích**: Nhanh chóng cập nhật documentation và mapping git changes
- **Ngôn ngữ**: Bash script
- **Tốt nhất cho**: Các tác vụ nhanh, đơn giản

### 2. `doc_mapper.py` (Script nâng cao)
- **Mục đích**: Phân tích code sâu và component mapping chi tiết
- **Ngôn ngữ**: Python
- **Tốt nhất cho**: Deep analysis, complexity metrics, dependency tracking

## 🚀 Bắt Đầu Nhanh

### Cài đặt và Khởi tạo
```bash
# 1. Kiểm tra quyền execute
chmod +x update-doc doc_mapper.py

# 2. Khởi tạo hệ thống documentation
./update-doc init

# 3. Chạy analysis đầy đủ
./update-doc sync --force

# 4. Kiểm tra trạng thái
./update-doc status
```

### Sử dụng hàng ngày
```bash
# Sau khi thay đổi code
./update-doc git-changes

# Cập nhật specific components
./update-doc scan

# Generate API docs (nếu backend thay đổi)
./update-doc api-docs
```

## 📋 Chi Tiết Các Lệnh

### Lệnh `update-doc`

| Lệnh | Mô tả | Ví dụ sử dụng |
|------|-------|---------------|
| `init` | Khởi tạo cấu trúc .agent | `./update-doc init` |
| `scan` | Map source code sang docs | `./update-doc scan --dry-run` |
| `git-changes` | Map các thay đổi git chưa commit | `./update-doc git-changes` |
| `api-docs` | Generate API documentation | `./update-doc api-docs --verbose` |
| `architecture` | Cập nhật architecture docs | `./update-doc architecture` |
| `sync` | Full synchronization | `./update-doc sync --force` |
| `clean` | Dọn dẹp file tạm | `./update-doc clean` |
| `status` | Hiển thị trạng thái documentation | `./update-doc status` |

### Lệnh `doc_mapper.py`

| Lệnh | Mô tả | Ví dụ sử dụng |
|------|-------|---------------|
| `analyze` | Full code analysis | `python3 doc_mapper.py analyze` |
| `git` | Git changes analysis | `python3 doc_mapper.py git` |
| `components` | Component analysis only | `python3 doc_mapper.py components` |

## 🗂️ Cấu Trúc File Được Tạo Ra

```
.agent/
├── readme.md                           # Documentation chính
├── system/                             # System docs (12 files)
│   ├── api_documentation.md           # API routes mapping
│   ├── processors.md                  # File processors docs
│   ├── data_models.md                 # Data models docs
│   ├── frontend_scripts.md            # Frontend components
│   ├── frontend_styles.md             # CSS styles docs
│   ├── architecture_current.md        # Architecture hiện tại
│   ├── api_analysis.md                # Advanced API analysis
│   ├── openapi_spec.json              # OpenAPI spec
│   └── api_endpoints_generated.md     # Generated API docs
├── reports/                            # Analysis reports (3 files)
│   ├── uncommitted_changes.md         # Git changes report
│   ├── code_analysis.md               # Code components analysis
│   └── git_changes.md                 # Git changes analysis
├── mappings/                           # Code-to-doc mappings
│   ├── file_map.json                  # File mapping structure
│   └── component_mappings.json        # Component mappings
├── sops/                              # Standard Operating Procedures
├── templates/                         # Documentation templates
├── tasks/                             # Feature documentation
└── logs/                              # Documentation logs
```

## 🔄 Workflow Sử Dụng

### 1. Setup lần đầu
```bash
# Clone hoặc navigate đến project
cd /path/to/your/project

# Khởi tạo documentation system
./update-doc init

# Chạy analysis đầy đủ lần đầu
./update-doc sync --force
```

### 2. Workflow phát triển hàng ngày
```bash
# Sau khi code changes
./update-doc git-changes

# Cập nhật specific components nếu cần
./update-doc scan

# Generate API docs nếu backend thay đổi
./update-doc api-docs
```

### 3. Comprehensive Analysis (Hàng tuần)
```bash
# Chạy deep code analysis
python3 doc_mapper.py analyze

# Full documentation sync
./update-doc sync --force

# Check status
./update-doc status
```

### 4. Trước khi commit
```bash
# Document current changes
./update-doc git-changes

# Advanced analysis nếu cần
python3 doc_mapper.py analyze

# Review generated documentation
ls -la .agent/reports/
```

## 📊 Các Tính Năng Nâng Cao

### Code Complexity Analysis
Python mapper cung cấp:
- **Cyclomatic Complexity**: Đo độ phức tạp của code
- **Dependency Tracking**: Xác định dependencies của functions/classes
- **Documentation Coverage**: Hiển thị components có docstrings
- **Component Statistics**: Tổng số classes, functions, complexity trung bình

### Git Integration
- **Uncommitted Changes**: Auto map new/modified/deleted files
- **File Previews**: Content previews cho new text files
- **Change Summaries**: Thống kê các thay đổi
- **Timestamp Tracking**: Thời điểm changes được documented

### API Documentation
- **Route Detection**: Auto discovery FastAPI endpoints
- **OpenAPI Integration**: Fetch specs từ running backend
- **Interactive Docs**: Links đến Swagger/ReDoc interfaces
- **Endpoint Categorization**: Group routes theo functionality

## 🎯 Các Use Cases Thực Tế

### 1. Phát triển feature mới
```bash
# Sau khi implement feature mới
./update-doc scan
./update-doc git-changes

# Document components mới
python3 doc_mapper.py analyze
```

### 2. Chuẩn bị code review
```bash
# Generate comprehensive documentation
./update-doc sync --force
python3 doc_mapper.py analyze

# Review component changes
cat .agent/reports/code_analysis.md
```

### 3. Project handover
```bash
# Complete documentation generation
./update-doc sync --force
python3 doc_mapper.py analyze

# Create documentation package
tar -czf documentation_$(date +%Y%m%d).tar.gz .agent/
```

### 4. Architecture review
```bash
# Update architecture documentation
./update-doc architecture

# Review component structure
cat .agent/system/architecture_current.md
```

## 🔧 Tùy Chỉnh và Cá Nhân Hóa

### Thêm Documentation Types mới
Edit `update-doc` script để thêm mapping functions:
```bash
# Thêm mapping function mới
map_custom_component() {
    # Custom mapping logic ở đây
}
```

### Mở rộng Python Analysis
Modify `doc_mapper.py` để thêm analysis features:
```python
def custom_analysis(self, file_path: Path) -> List[CodeComponent]:
    # Custom analysis logic ở đây
    pass
```

## 🚨 Xử Lý Vấn Đề Thường Gặp

### Các lỗi phổ biến

1. **Permission Denied**
   ```bash
   chmod +x update-doc doc_mapper.py
   ```

2. **Git Not Found**
   ```bash
   # Install git hoặc skip git features
   ./update-doc scan  # thay vì git-changes
   ```

3. **Python Not Found**
   ```bash
   # Dùng python thay vì python3
   python doc_mapper.py analyze
   ```

4. **Backend Not Running cho API Docs**
   ```bash
   # Start backend trước
   cd backend && python main.py
   # Sau đó chạy API docs generation
   ./update-doc api-docs
   ```

### Debug Mode
```bash
# Enable verbose output
./update-doc sync --verbose

# Dry run mode (không tạo thay đổi)
./update-doc scan --dry-run
```

## 📈 Best Practices

1. **Chạy trước commits**: Luôn document changes trước khi commit
2. **Regular Sync**: Chạy full sync hàng tuần để docs luôn current
3. **Review Generated Docs**: Kiểm tra accuracy của auto-generated content
4. **Version Control**: Commit documentation files cùng với code
5. **Team Communication**: Share documentation status với team members

## 🔗 Integration với Development Workflow

### Pre-commit Hook (Tùy chọn)
```bash
# Thêm vào .git/hooks/pre-commit
#!/bin/bash
./update-doc git-changes
python3 doc_mapper.py analyze
git add .agent/
```

### CI/CD Pipeline Integration
```yaml
# Ví dụ GitHub Actions step
- name: Update Documentation
  run: |
    ./update-doc sync --force
    python3 doc_mapper.py analyze
    git add .agent/
```

## 📞 Hỗ Trợ và Troubleshooting

Khi gặp vấn đề:
1. Kiểm tra guide này trước
2. Chạy `./update-doc status` để diagnostics
3. Review generated logs trong `.agent/logs/`
4. Test với `--dry-run` flag trước

## 💡 Mẹo Sử Dụng Hiệu Quả

### Daily Workflow (5 phút)
```bash
./update-doc git-changes    # 1 phút
./update-doc status         # 30 giây
# Review changes            # 3.5 phút
```

### Weekly Review (15 phút)
```bash
./update-doc sync --force   # 2 phút
python3 doc_mapper.py analyze # 5 phút
# Review reports             # 8 phút
```

### Pre-commit Checklist
- [ ] `./update-doc git-changes`
- [ ] `python3 doc_mapper.py analyze` (nếu cần)
- [ ] Review `.agent/reports/`
- [ ] Add `.agent/` files to commit

## 🎉 Tổng Kết

Hệ thống documentation update được thiết kế để **enhance, không replace** good documentation practices. Luôn review và supplement automatically generated documentation với human insights.

**Remember**: Good documentation = Happy developers! 😊

---

**Câu hỏi thường gặp:**

**Q: Khi nào nên chạy update-doc?**  
A: Sau mỗi thay đổi code quan trọng, trước khi commit, và hàng tuần.

**Q: File generated có cần edit manually không?**  
A: Có thể edit để bổ sung thông tin, nhưng đừng edit phần auto-generated.

**Q: Có thể custom output format không?**  
A: Có, edit scripts để modify output theo nhu cầu.

**Q: System có hoạt động với mọi loại project không?**  
A: Hoạt động tốt nhất với Python/JavaScript projects, có thể custom cho types khác.