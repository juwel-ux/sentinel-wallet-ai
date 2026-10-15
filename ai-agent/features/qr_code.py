"""
QR Code module - Generate QR codes for wallet addresses.
"""

import os


def generate_qr(address, filename="wallet_qr.png"):
    """Generate a QR code for a wallet address."""
    try:
        import qrcode
    except ImportError:
        print("[QR] Install: pip install qrcode[pil]")
        return None
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(address)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "qr")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    img.save(filepath)
    print(f"[QR] Generated: {filepath}")
    return filepath


def print_qr_ascii(address):
    """Print a QR code in the terminal (ASCII)."""
    try:
        import qrcode
    except ImportError:
        print(f"[QR] Address: {address}")
        return
    
    qr = qrcode.QRCode()
    qr.add_data(address)
    qr.make(fit=True)
    qr.print_ascii()
