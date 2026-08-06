import os
import tempfile
import torch
import numpy as np
import rasterio

from dataloader import bands_mean, bands_std
from unet_plus_plus import UNetPlusPlus

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_PATH = os.path.join(BASE_DIR, "trained_models", "best_model_marine_debris.pth")
SAMPLE_PATH = os.path.join(BASE_DIR, "sample_data", "S2_9-10-17_16PEC_0.tif")


def load_model(device):
    model = UNetPlusPlus(input_bands=11, output_classes=11, hidden_channels=16)
    model_path = CHECKPOINT_PATH
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model checkpoint not found at {model_path}")

    checkpoint = torch.load(model_path, map_location=device)
    # Support checkpoint being a state_dict or a dict with keys
    if isinstance(checkpoint, dict):
        # common keys: 'state_dict' or exactly the state_dict
        if 'state_dict' in checkpoint:
            state = checkpoint['state_dict']
        elif 'model_state_dict' in checkpoint:
            state = checkpoint['model_state_dict']
        else:
            state = checkpoint
    else:
        state = checkpoint

    model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model


def preprocess_image(image, device):
    img = np.array(image).astype(np.float32)
    nan_mask = np.isnan(img)
    mean_values = np.tile(bands_mean[:, None, None], (1, img.shape[1], img.shape[2]))
    img = np.where(nan_mask, mean_values, img)
    img = (img - bands_mean[:, None, None]) / bands_std[:, None, None]
    img_tensor = torch.tensor(img).unsqueeze(0).to(device)
    return img_tensor


def predict_and_save(sample_path, out_path=None, device=None):
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with rasterio.open(sample_path) as ds:
        img = ds.read()  # (bands, h, w)
        transform = ds.transform
        crs = ds.crs.to_wkt() if ds.crs else None

    if img.shape[0] != 11:
        raise ValueError(f"Expected 11 bands, found {img.shape[0]}")

    model = load_model(device)
    img_tensor = preprocess_image(img, device)

    with torch.no_grad():
        logits = model(img_tensor)
        probs = torch.softmax(logits, dim=1)
        pred = torch.argmax(probs, dim=1).squeeze(0).cpu().numpy()
        mapped = (pred + 1).astype('uint8')

    if out_path is None:
        out_path = os.path.join(tempfile.gettempdir(), 'sample_prediction.tif')

    profile = {
        'driver': 'GTiff',
        'height': mapped.shape[0],
        'width': mapped.shape[1],
        'count': 1,
        'dtype': 'uint8',
        'transform': transform,
        'crs': crs
    }

    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(mapped, 1)

    return out_path


if __name__ == '__main__':
    sample = SAMPLE_PATH
    print('Using sample:', sample)
    try:
        out = predict_and_save(sample)
        print('Prediction saved to', out)
    except Exception as e:
        print('Error:', e)
