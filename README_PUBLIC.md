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
