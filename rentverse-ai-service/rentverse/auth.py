import pyotp, qrcode, io, base64
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dummy user DB
users = {
    "1@3.com": {
        "password": "Password123",
        "otp_secret": None
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str
    mfa_type: str = "none"  # none | app

class OTPRequest(BaseModel):
    username: str
    otp: str

@router.post("/login")
async def login(req: LoginRequest):
    user = users.get(req.username)
    if not user or user["password"] != req.password:
        return {"success": False, "message": "Invalid credentials"}

    # 🔐 MFA FLOW
    if req.mfa_type == "app":

        # 🟢 FIRST TIME SETUP
        if not user["otp_secret"]:
            user["otp_secret"] = pyotp.random_base32()
            totp = pyotp.TOTP(user["otp_secret"])
            otp_uri = totp.provisioning_uri(
                name=req.username,
                issuer_name="RentVerse AI"
            )

            import qrcode, io, base64
            img = qrcode.make(otp_uri)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

            return {
                "mfa_required": True,
                "setup": True,
                "qr_code": base64.b64encode(buffer.getvalue()).decode(),
                "message": "Scan QR code to setup MFA"
            }

        # 🔵 ALREADY SETUP → OTP ONLY
        return {
            "mfa_required": True,
            "setup": False,
            "message": "Enter OTP"
        }

    # 🔓 NO MFA
    return {
        "success": True,
        "message": "Login successful (no MFA)"
    }


@router.post("/verify-otp")
async def verify_otp(req: OTPRequest):
    user = users.get(req.username)
    if not user or not user["otp_secret"]:
        return {"success": False, "message": "MFA not setup"}

    totp = pyotp.TOTP(user["otp_secret"])
    if not totp.verify(req.otp):
        return {"success": False, "message": "Invalid OTP"}

    return {
        "success": True,
        "message": "Login successful"
    }
