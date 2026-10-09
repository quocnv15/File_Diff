# 🚀 UPDATE-DOC - Quick Reference (Tham Khảo Nhanh)

## 📋 Các Lệnh Phổ Biến Nhất

### **Hàng ngày (5 phút)**
```bash
./update-doc git-changes    # Map thay đổi git chưa commit
./update-doc status         # Kiểm tra trạng thái documentation
```

### **Phân tích sâu (15 phút)**
```bash
python3 doc_mapper.py analyze    # Analysis chi tiết 496 components
./update-doc sync --force        # Full synchronization
```

### **Khi cần API documentation**
```bash
./update-doc api-docs    # Generate API docs từ backend (port 8001)
```

### **Setup lần đầu**
```bash
./update-doc init        # Khởi tạo cấu trúc .agent
./update-doc sync        # Full sync
```

## 🎯 Tình Huống Sử Dụng

| Tình huống | Lệnh cần chạy | Thời gian |
|------------|--------------|----------|
| **Sau khi code xong** | `./update-doc git-changes` | 30 giây |
| **Trước khi commit** | `./update-doc git-changes`<br/>`git add .agent/` | 1 phút |
| **Review hàng tuần** | `python3 doc_mapper.py analyze`<br/>`./update-doc sync` | 10 phút |
| **Backend thay đổi** | `./update-doc api-docs` | 30 giây |
| **Check status** | `./update-doc status` | 15 giây |

## 📊 Kết Quả Hiện Tại

- ✅ **21 documentation files** đã được tạo
- ✅ **496 code components** đã được phân tích
- ✅ **41 git changes** đã được mapped
- ✅ **Backend API integration** đang hoạt động
- ✅ **Complexity analysis** sẵn sàng

## 🔗 Files Quan Trọng

| File | Mục đích | Đường dẫn |
|------|----------|-----------|
| **Main README** | Documentation index | `.agent/readme.md` |
| **Git Changes** | Thay đổi chưa commit | `.agent/reports/uncommitted_changes.md` |
| **Code Analysis** | Component analysis | `.agent/reports/code_analysis.md` |
| **API Docs** | API documentation | `.agent/system/api_endpoints_generated.md` |
| **Architecture** | System structure | `.agent/system/architecture_current.md` |

## 🚨 Quick Troubleshooting

| Vấn đề | Solution |
|---------|----------|
| **Permission denied** | `chmod +x update-doc doc_mapper.py` |
| **Backend not running** | Start backend: `cd backend && python main.py` |
| **Git not found** | Install git hoặc dùng `./update-doc scan` |
| **Python not found** | Dùng `python doc_mapper.py analyze` |

## 💡 Tips Hiệu Quả

### **Daily 5-minute routine**
```bash
./update-doc git-changes && ./update-doc status
```

### **Weekly comprehensive check**
```bash
python3 doc_mapper.py analyze && ./update-doc sync --force
```

### **Pre-commit checklist**
```bash
./update-doc git-changes
git add .agent/
git commit -m "Update docs for feature changes"
```

## 📱 Mobile Friendly Commands

Khi trên mobile/ssh:
```bash
# Quick check
./update-doc status | head -10

# Git changes only  
./update-doc git-changes | tail -5

# API docs status
ls -la .agent/system/api_*.md
```

## 🔥 Pro Tips

1. **Use `--dry-run` first**: `./update-doc scan --dry-run`
2. **Verbose when debugging**: `./update-doc sync --verbose`
3. **Check timestamps**: `ls -la .agent/reports/`
4. **Backup before major changes**: `cp -r .agent .agent.backup`

---

**Need more help?** → See `HUONG_DAN_SU_DUNG_UPDATE_DOC.md` for detailed guide

**Remember**: 5 minutes daily saves hours of confusion later! 🎯