# VIDEO OUTPUTS FOLDER
**Vidéos Finales Rendues par Creatify**

## 📹 Naming Convention

**Format strict:**
```
YYYY-MM-DD_{product-handle}_{type}_v{version}.mp4
```

**Exemples:**
```
2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
2025-11-24_lower-back-brace_ba_v1.mp4
2025-11-25_magnetic-posture_demo_v1.mp4
2025-11-26_tourmaline-knee-pads_ugc_v2.mp4  (iteration)
```

---

## 🏷️ Type Abbreviations

| Code | Type Complet | Duration Typical |
|------|--------------|------------------|
| `ugc` | UGC Testimonial | 15 sec |
| `ba` | Before/After | 12 sec |
| `demo` | Product Demo | 20 sec |
| `comp` | Comparison | 25 sec |
| `edu` | Educational | 30 sec |

---

## 📊 Production Log

**File:** `production-log.md`

Chaque vidéo créée doit avoir une entrée dans le log:

```markdown
## 2025-11-23 | Tourmaline Knee Pads UGC v1

**Product:** Tourmaline Magnetic Knee Pads
**Handle:** tourmaline-knee-pads-self-heating-support
**Type:** UGC Testimonial
**Duration:** 15 sec
**Format:** 9:16 vertical (1080x1920)

**Assets Used:**
- Hero: tourmaline-knee-pads_hero_front.jpg
- Lifestyle: tourmaline-knee-pads_lifestyle_senior-outdoor.jpg

**Creatify Settings:**
- Avatar ID: #12345 (Mature woman outdoor)
- Voice ID: #67890 (Mature Female Warm EN-US)
- Music: Upbeat Soft, -18dB
- Captions: Enabled

**Script:** UGC Testimonial Template
Hook: "My knees used to ache every winter morning..."
CTA: "alphamedical.shop | -20% CODE: WARMKNEES20"

**Rendering:**
- Started: 2025-11-23 14:30
- Completed: 2025-11-23 14:45
- Time: 15 minutes
- Credit: 1/50 used

**Quality Check:**
✅ All QA passed
✅ Mobile tested
✅ Ready for Meta

**Performance (Update after campaign):**
- Campaign ID: [TBD]
- CTR: [TBD]
- CPC: [TBD]
- ROAS: [TBD]
```

---

## 📂 File Organization

**Keep organized:**
```
outputs/
├── 2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
├── 2025-11-24_lower-back-brace_ba_v1.mp4
├── 2025-11-25_magnetic-posture_demo_v1.mp4
├── production-log.md
└── backups/
    ├── 2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
    └── [archived versions]
```

**Backup strategy:**
- Toujours copier version finale dans `backups/`
- Garder versions antérieures (v1, v2) séparées
- Ne jamais overwrite sans backup

---

## ✅ Post-Download Checklist

Après download Creatify:

1. [ ] Rename selon convention (YYYY-MM-DD_{handle}_{type}_v{#}.mp4)
2. [ ] Move to outputs/ folder
3. [ ] Copy to backups/ folder
4. [ ] Watch vidéo complète 1 fois (QA final)
5. [ ] Test sur mobile (transfer + view)
6. [ ] Verify file size <100 MB (Meta limit)
7. [ ] Add entry to production-log.md
8. [ ] Update product metadata with video file name

---

## 📈 Performance Tracking

**Après upload Meta Ads:**

1. Add Campaign ID to production log
2. Track KPIs daily (first 48h critical)
3. Update log with results after 7 days
4. Document learnings for iterations

**KPIs to log:**
- CTR (Click-Through Rate)
- CPC (Cost Per Click)
- CPM (Cost Per 1000 Impressions)
- ROAS (Return on Ad Spend)
- 3-sec video view rate
- Watch time average

---

**Next:** Upload to Meta Ads Manager following campaign strategy
