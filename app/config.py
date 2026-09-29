# ==========================================
# ComicCraft - Configuration
# ==========================================

import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False


# Load variables from .env
load_dotenv()


# ==========================================
# API KEYS
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

HF_API_KEY = os.getenv(
    "HF_API_KEY"
)


# ==========================================
# AI MODEL CONFIGURATION
# ==========================================

GEMINI_FLASH_MODEL = (
    "gemini-1.5-flash"
)

GEMINI_PRO_MODEL = (
    "gemini-1.5-pro"
)

STABLE_DIFFUSION_MODEL = (
    "runwayml/stable-diffusion-v1-5"
)


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

PANELS_FOLDER = (
    "static/panels"
)

EXPORT_FOLDER = (
    "static/exports"
)

TEMPLATES_FOLDER = (
    "templates"
)


# ==========================================
# COMIC CONFIGURATION
# ==========================================

NUMBER_OF_PANELS = 5


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

APP_TITLE = (
    "ComicCraft - AI Comic Story Creator"
)

APP_VERSION = "1.0.0"

DEBUG = True


# ==========================================
# VALIDATE API KEYS
# ==========================================

def validate_config():

    missing_keys = []

    if not GEMINI_API_KEY:
        missing_keys.append(
            "GEMINI_API_KEY"
        )

    if not HF_API_KEY:
        missing_keys.append(
            "HF_API_KEY"
        )

    if missing_keys:

        raise ValueError(
            "Missing environment variables: "
            + ", ".join(missing_keys)
        )


# ==========================================
# CONFIGURATION SUMMARY
# ==========================================

def get_config():

    return {
        "app_title": APP_TITLE,
        "app_version": APP_VERSION,
        "gemini_flash_model":
            GEMINI_FLASH_MODEL,
        "gemini_pro_model":
            GEMINI_PRO_MODEL,
        "stable_diffusion_model":
            STABLE_DIFFUSION_MODEL,
        "number_of_panels":
            NUMBER_OF_PANELS,
        "panels_folder":
            PANELS_FOLDER,
        "export_folder":
            EXPORT_FOLDER,
    }