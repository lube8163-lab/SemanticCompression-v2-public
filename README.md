# Mim iOS App (Public Repository)

This repository is a public-safe version of Mim iOS.

## Public release notes
- Removed local user files (`xcuserdata`, `.DS_Store`) and `.git` history from the source copy.
- Removed these caption assets until redistribution rights are confirmed:
  - `SemanticCompression-v2/ML/SigLIP/Assets/caption_10k.json`
  - `SemanticCompression-v2/ML/SigLIP/Assets/caption_10k_embs.npy`

## Regenerate SigLIP2 assets with your own labels
You can generate dictionary files from your own label list.

### 1) Export SigLIP2 vision model to Core ML
```bash
python3 scripts/export_siglip2_vision_to_coreml.py \
  --model-id google/siglip2-base-patch16-224 \
  --output SigLIP2_Base_VisionCLS.mlpackage
```

### 2) Build tag dictionary from labels
Prepare `labels.json` as a JSON array of strings, then run:
```bash
python3 scripts/fixed_build_tag_dict.py \
  --labels-json labels.json \
  --output-labels SemanticCompression-v2/ML/SigLIP/Assets/styles.json \
  --output-embs SemanticCompression-v2/ML/SigLIP/Assets/styles_embs.npy
```

## T5Tokenizer workaround (for some StableDiffusion package environments)
If your environment fails around `T5Tokenizer` in `stable-diffusion` package sources, use the patched file included here:
- `patches/T5Tokenizer.swift`

Usage:
1. Locate the package file in your local checkout of the Stable Diffusion package (the file named `T5Tokenizer.swift`).
2. Replace that file content with `patches/T5Tokenizer.swift` from this repository.
3. Clean build folder and rebuild.

This workaround disables that tokenizer path and is intended for this app configuration where it is not used.

## Original project overview
https://github.com/lube8163-lab/mim-ios
