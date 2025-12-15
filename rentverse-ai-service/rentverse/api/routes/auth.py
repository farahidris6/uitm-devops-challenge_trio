from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import pyotp
import qrcode
import base64
from io import BytesIO
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

# JWT config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake DB
fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("password123"),
        "otp_secret": None,  # generated only when MFA is used
        "role": "user"
    }
}

# ------------------------
# Models
# ------------------------

class LoginRequest(BaseModel):
    email: str
    password: str
    mfa_type: str = "none"  # "none" | "app"

class OTPRequest(BaseModel):
    email: str
    otp: str

# ------------------------
# Helpers
# ------------------------

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def generate_qr_code(uri: str) -> str:
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ------------------------
# Routes
# ------------------------

@router.post("/login")
def login(request: LoginRequest):
    user = fake_users_db.get(request.email)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔐 MFA FLOW
    if request.mfa_type == "app":
        secret = pyotp.random_base32()
        user["otp_secret"] = secret

        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user["email"],
            issuer_name="RentVerse"
        )

        qr_code = generate_qr_code(otp_uri)

        return {
            "success": True,
            "mfa_required": True,
            "qr_code": qr_code
        }

    # 🔓 NO MFA
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return {
        "success": True,
        "token": token,
        "user": {
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.post("/verify-otp")
def verify_otp(request: OTPRequest):
    user = fake_users_db.get(request.email)
    if not user or not user.get("otp_secret"):
        raise HTTPException(status_code=401, detail="Invalid user")

    totp = pyotp.TOTP(user["otp_secret"])
    if not totp.verify(request.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    token = create_access_token({"sub": user["email"], "role": user["role"]})

    return {
        "success": True,
        "token": token
    }
