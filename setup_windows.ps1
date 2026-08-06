<#
Setup script for Windows (PowerShell).
This script guides creation of a conda environment with GDAL/rasterio and installs Python deps.

Run as: Open PowerShell (Admin if needed) and execute:
    .\setup_windows.ps1

The script does NOT force-install software. It will detect if conda exists and print commands to run.
#>
Write-Host "=== Marine Debris Detection Setup (Windows) ===" -ForegroundColor Cyan

function Has-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

if (-not (Has-Command conda)) {
    Write-Host "Conda (Miniconda/Anaconda) not found. Recommended for GDAL/rasterio on Windows." -ForegroundColor Yellow
    Write-Host "Please install Miniconda: https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Yellow
    Write-Host "Or press Enter to continue with system Python/pip (GDAL may fail)."
    Read-Host
}

Write-Host "Recommended steps (copy/paste and run in an elevated PowerShell):" -ForegroundColor Green
Write-Host "1) Create conda environment with GDAL and rasterio (conda-forge):" -ForegroundColor White
Write-Host "   conda create -n mardeb python=3.10 gdal rasterio -c conda-forge" -ForegroundColor Gray
Write-Host "2) Activate the environment:" -ForegroundColor White
Write-Host "   conda activate mardeb" -ForegroundColor Gray
Write-Host "3) From project root, install Python packages from requirements.txt:" -ForegroundColor White
Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "4) (Optional) If you want PyTorch with CUDA, follow https://pytorch.org/get-started/locally/" -ForegroundColor White

Write-Host "If you prefer to use system Python (not recommended for GDAL), run:" -ForegroundColor Yellow
Write-Host "   python -m pip install --upgrade pip" -ForegroundColor Gray
Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray

Write-Host "Notes:" -ForegroundColor Cyan
Write-Host " - `rasterio` and `gdal` are installed via conda-forge to handle native dependencies." -ForegroundColor Gray
Write-Host " - `streamlit` is included in requirements.txt." -ForegroundColor Gray
Write-Host " - Ensure `semantic_segmentation/unet/trained_models/best_model_marine_debris.pth` exists before running the app." -ForegroundColor Gray

Write-Host "Setup script finished. Ask me to run the conda/pip commands for you if you want me to execute them now." -ForegroundColor Green
