# Public Release Notes

This folder is a GitHub-safe copy of the original repository.

## What was removed/adjusted
- Removed `.git` history and local user files (`xcuserdata`, `.DS_Store`).
- Removed large caption assets below until redistribution rights are confirmed:
  - `SemanticCompression-v2/ML/SigLIP/Assets/caption_10k.json`
  - `SemanticCompression-v2/ML/SigLIP/Assets/caption_10k_embs.npy`

## Runtime behavior
- The app code already handles missing embedding assets by skipping that tagger path.
- If you want full caption tagging, restore those two files only after license/source verification.

## Optional: Regenerate SigLIP2 assets

You can regenerate dictionary assets with your own labels.

### 1) Export SigLIP2 vision model to Core ML
```bash
python3 scripts/export_siglip2_vision_to_coreml.py \
  --model-id google/siglip2-base-patch16-224 \
  --output SigLIP2_Base_VisionCLS.mlpackage
```

### 2) Build tag dictionary from your label list
Prepare `labels.json` (JSON array of strings), then run:
```bash
python3 scripts/fixed_build_tag_dict.py \
  --labels-json labels.json \
  --output-labels SemanticCompression-v2/ML/SigLIP/Assets/styles.json \
  --output-embs SemanticCompression-v2/ML/SigLIP/Assets/styles_embs.npy
```
