def calculate_risk(results):
    score = 0
    reasons = []

    # 🔴 1. HTML phishing detection
    if results.get("html_analysis"):
        score += 3
        reasons.append("HTML link mismatch detected")

    # 🔴 2. Suspicious domains (WHOIS errors or very new domains)
    for domain in results.get("whois", []):
        if "error" in domain:
            score += 2
            reasons.append(f"Domain {domain.get('domain')} not registered or invalid")
        else:
            age = domain.get("domain_age_days")

            if isinstance(age, int):
                if age < 30:
                    score += 3
                    reasons.append(f"Domain {domain['domain']} is very new (<30 days)")
                elif age < 90:
                    score += 2
                    reasons.append(f"Domain {domain['domain']} is new (<90 days)")

    # 🔴 3. SPF / DMARC issues
    for auth in results.get("email_auth", []):
        spf = auth.get("spf", {})
        dmarc = auth.get("dmarc", {})

        if "error" in spf or spf.get("spf_record") == "Not found":
            score += 1
            reasons.append(f"Missing SPF for {auth['domain']}")

        if "error" in dmarc or dmarc.get("dmarc_record") == "Not found":
            score += 1
            reasons.append(f"Missing DMARC for {auth['domain']}")

    # 🔴 4. URL shortener usage
    for url in results.get("iocs", {}).get("urls", []):
        if "bit.ly" in url or "tinyurl" in url:
            score += 1
            reasons.append("URL shortener detected")

    # 🔴 5. Suspicious keywords (basic)
    suspicious_words = ["login", "verify", "account", "urgent", "password"]

    for url in results.get("expanded_urls", []):
        for word in suspicious_words:
            if word in url.lower():
                score += 1
                reasons.append(f"Suspicious keyword '{word}' in URL")
                break

    # 🎯 FINAL CLASSIFICATION
    if score >= 6:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": level,
        "risk_points": score,
        "risk_reasons": list(set(reasons))  # remove duplicates
    }