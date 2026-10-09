# AI-Enhanced Comparison - Implementation Plan

## Tóm Tắt
Nâng độ chính xác so sánh từ **70.5%** lên **95%+** bằng AI

## Chiến Lược: 3-Tier Hybrid

### Tier 1: Structured (Fast) 
- Quality ≥80% → Dùng logic hiện tại
- Tốc độ: <0.5s, Miễn phí

### Tier 2: AI (Accurate)
- Quality <80% → Dùng AI (GPT-4/Claude)  
- Tốc độ: 2-5s, Chi phí: $0.01-0.03

### Tier 3: Hybrid (Validation)
- Chạy cả 2 → So sánh kết quả
- Tốc độ: 3-6s, Chi phí: $0.02

## Files Cần Tạo

### Phase 1: Quality Assessment
```
backend/utils/quality_assessor.py
- ConversionQualityAssessor class
- Chấm điểm 0-100% cho file conversion
- Kiểm tra: headers, column names, data density
```

### Phase 2: AI Comparator  
```
backend/comparators/ai_comparator.py
- AIComparator class
- Tích hợp OpenAI GPT-4 API
- So sánh markdown content bằng LLM
```

### Phase 3: Strategy Selector
```
backend/comparators/comparison_strategy.py
- ComparisonStrategy base class
- StructuredStrategy / AIStrategy / HybridStrategy
- Auto-select dựa trên quality score
```

### Phase 4: API Updates
```
backend/app/config.py - Thêm AI settings
backend/app/models.py - Thêm ComparisonStrategy enum
backend/api/routes/comparison.py - Update endpoint
```

### Phase 5: Frontend
```
frontend/index.html - Comparison mode selector
frontend/scripts/api_integration.js - Gửi strategy preference
frontend/scripts/diff-visualization.js - Hiển thị quality & confidence
```

## Cấu Hình Cần Thiết

### Environment Variables
```bash
OPENAI_API_KEY=sk-...
AI_PROVIDER=openai
AI_MODEL_PRIMARY=gpt-4-turbo-preview
```

### Dependencies Mới
```txt
openai>=1.12.0
tiktoken>=0.6.0
python-dotenv>=1.0.0
```

## Timeline

**Week 1:** Quality Assessor + AI Comparator  
**Week 2:** Strategy Selector + API Integration  
**Week 3:** Frontend + Testing  
**Week 4:** Deployment

## Chi Phí Ước Tính

- Small file: $0.01/comparison
- Medium file: $0.03/comparison  
- Large file: $0.06/comparison
- **Tổng:** ~$8-10/tháng (1000 comparisons)

## Rủi Ro & Giải Pháp

| Rủi Ro | Giải Pháp |
|---------|-----------|
| API downtime | Auto fallback to structured |
| High cost | Daily budget limit |
| Slow response | Timeout + async |

## Bước Tiếp Theo

1. ✅ Review plan này
2. ⏳ Lấy OpenAI API key
3. ⏳ Implement Phase 1
4. ⏳ Test accuracy
5. ⏳ Deploy

---
**Status:** Waiting for approval  
**Date:** 2025-01-16
