import json
import os
import urllib.parse
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_FILE = "users.json"

# ═══════════════════════════════════════════════════════════════════════
# OAUTH CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8502")

# Google
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# Microsoft
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")
MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID", "common")


# ═══════════════════════════════════════════════════════════════════════
# GOOGLE OAUTH FLOW
# ═══════════════════════════════════════════════════════════════════════
def get_google_login_url():
    """Build the real Google OAuth2 authorization URL."""
    if not GOOGLE_CLIENT_ID:
        return None
    params = urllib.parse.urlencode({
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": "google",
    })
    return f"https://accounts.google.com/o/oauth2/v2/auth?{params}"


def verify_google_code(code: str):
    """Exchange the Google authorization code for an access token, then fetch the user's email."""
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    if resp.status_code != 200:
        print(f"[Google OAuth] Token error: {resp.text}")
        return None
    access_token = resp.json().get("access_token")
    user_resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_resp.status_code == 200:
        return user_resp.json().get("email")
    return None


# ═══════════════════════════════════════════════════════════════════════
# MICROSOFT OAUTH FLOW
# ═══════════════════════════════════════════════════════════════════════
def get_microsoft_login_url():
    """Build the real Microsoft OAuth2 authorization URL."""
    if not MICROSOFT_CLIENT_ID:
        return None
    base = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/oauth2/v2.0/authorize"
    params = urllib.parse.urlencode({
        "client_id": MICROSOFT_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile User.Read",
        "response_mode": "query",
        "state": "microsoft",
    })
    return f"{base}?{params}"


def verify_microsoft_code(code: str):
    """Exchange the Microsoft authorization code for an access token, then fetch the user's email."""
    token_url = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/oauth2/v2.0/token"
    resp = requests.post(token_url, data={
        "client_id": MICROSOFT_CLIENT_ID,
        "client_secret": MICROSOFT_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    if resp.status_code != 200:
        print(f"[Microsoft OAuth] Token error: {resp.text}")
        return None
    access_token = resp.json().get("access_token")
    user_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_resp.status_code == 200:
        data = user_resp.json()
        return data.get("mail") or data.get("userPrincipalName")
    return None


def has_oauth_credentials():
    """Return True if at least one provider's credentials are configured."""
    return bool(GOOGLE_CLIENT_ID) or bool(MICROSOFT_CLIENT_ID)

def _load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def login_user(email):
    """Logs in or registers a user. Returns the user object."""
    db = _load_db()
    if email not in db:
        # Register new user
        db[email] = {
            "email": email,
            "joined_date": datetime.now().isoformat(),
            "datasets_analyzed": 0,
            "subscription": "free", # 'free', 'monthly', 'semi_annual', 'yearly'
            "subscription_expiry": None
        }
        _save_db(db)
    return db[email]

def get_user(email):
    """Retrieve user profile."""
    return _load_db().get(email)

def increment_dataset_usage(email):
    """Increment the datasets analyzed count."""
    db = _load_db()
    if email in db:
        db[email]["datasets_analyzed"] += 1
        _save_db(db)

def upgrade_subscription(email, tier):
    """Upgrade user subscription."""
    db = _load_db()
    if email in db:
        db[email]["subscription"] = tier
        
        # Calculate expiry
        now = datetime.now()
        if tier == "monthly":
            expiry = now + timedelta(days=30)
        elif tier == "semi_annual":
            expiry = now + timedelta(days=180)
        elif tier == "yearly":
            expiry = now + timedelta(days=365)
        else:
            expiry = None
            
        db[email]["subscription_expiry"] = expiry.isoformat() if expiry else None
        _save_db(db)

def check_access(email):
    """
    Check if a user has access to analyze a dataset.
    Returns (has_access, reason, trial_status)
    """
    user = get_user(email)
    if not user:
        return False, "User not found", "None"

    if user["subscription"] != "free":
        # Check if subscription expired
        if user["subscription_expiry"]:
            expiry = datetime.fromisoformat(user["subscription_expiry"])
            if datetime.now() > expiry:
                return False, "Subscription expired. Please renew.", "Expired"
        return True, "", "Subscribed"

    # Free user limits: max 2 datasets
    if user["datasets_analyzed"] >= 2:
        return False, "You have reached the 2 dataset free limit. Please upgrade.", "Limit Reached"
        
    return True, "", f"Free Tier Active ({2 - user['datasets_analyzed']} datasets left)"
