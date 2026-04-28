import whois
from datetime import datetime


def format_date(value):
    """
    Clean WHOIS date formatting:
    Handles list, single datetime, or None
    """
    if isinstance(value, list):
        value = value[0]

    if value:
        return str(value)

    return "N/A"


def calculate_domain_age(creation_date):
    """
    Calculate domain age in days
    """
    try:
        if creation_date == "N/A":
            return "Unknown"

        # Convert string → datetime
        created = datetime.fromisoformat(creation_date.replace("Z", "+00:00"))

        # Calculate age
        now = datetime.now(created.tzinfo)
        age_days = (now - created).days

        return age_days

    except Exception:
        return "Unknown"


def get_whois(domain):
    try:
        w = whois.whois(domain)

        creation_date = format_date(w.creation_date)
        expiration_date = format_date(w.expiration_date)

        return {
            "domain": domain,
            "registrar": str(w.registrar) if w.registrar else "N/A",
            "creation_date": creation_date,
            "expiration_date": expiration_date,
            "domain_age_days": calculate_domain_age(creation_date)
        }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }