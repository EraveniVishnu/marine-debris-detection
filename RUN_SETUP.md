**How to set up and run locally (Windows / cross-platform)**

1) Recommended: use Conda (Miniconda) to install GDAL/rasterio:

   ```powershell
   conda create -n mardeb python=3.10 gdal rasterio -c conda-forge
   conda activate mardeb
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2) If you don't use conda (system Python):

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3) Ensure the trained model checkpoint is present at:

   `semantic_segmentation/unet/trained_models/best_model_marine_debris.pth`

4) Run the Streamlit app:

   ```powershell
   streamlit run semantic_segmentation/unet/app.py
   ```

Notes:
- If you want GPU acceleration, install PyTorch following instructions at https://pytorch.org according to your CUDA version.
- On Windows, installing `rasterio` and `gdal` via pip is error-prone; prefer conda-forge.
- The repo already contains a `.devcontainer` that launches the app in a container if you use VS Code Codespaces or Dev Containers.
