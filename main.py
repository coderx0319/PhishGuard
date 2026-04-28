import os
import logging

from dotenv import load_dotenv
from parser.email_parser import parse_email
from parser.extractor import extract_iocs
from intel import virustotal, abuseipdb
from report.report_generator import generate_report
from utils.url_shortener import unshorten_url
from analysis.html_analyzer import analyze_html
from intel.whois_lookup import get_whois
from utils.domain_utils import extract_domain
from intel.email_auth import check_spf, check_dmarc
from analysis.risk_analyzer import calculate_risk

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    try:
        logging.info("Starting phishing email analysis...")

        # Step 1: Parse email
        email_path = "samples/uploaded.eml"
        email_data = parse_email(email_path)
        logging.info("Email parsed successfully")

        # Step 2: Combine headers + body
        combined_text = str(email_data["headers"]) + email_data["body"]

        # Step 3: Extract IOCs
        iocs = extract_iocs(combined_text)
        logging.info(f"Extracted {len(iocs['urls'])} URLs and {len(iocs['ips'])} IPs")

        # Step 4: Expand URLs (FIRST)
        expanded_urls = []
        for url in iocs["urls"]:
            try:
                expanded = unshorten_url(url)
                expanded_urls.append(expanded)
            except Exception as e:
                logging.warning(f"Failed to expand URL {url}: {e}")
                expanded_urls.append(url)

        # Step 5: WHOIS lookup (AFTER expansion)
        whois_results = []
        seen_domains = set()

        for url in expanded_urls:
            try:
                domain = extract_domain(url)

                if domain not in seen_domains:
                    seen_domains.add(domain)
                    whois_data = get_whois(domain)
                    whois_results.append(whois_data)

            except Exception as e:
                whois_results.append({
                    "url": url,
                    "error": str(e)
                })

        # Step 6: SPF and DMARC Logic
        email_auth_results = []

        for domain_data in whois_results:
            domain = domain_data.get("domain")

            if not domain:
               continue

            try:
                spf = check_spf(domain)
                dmarc = check_dmarc(domain)

                email_auth_results.append({
                     "domain": domain,
                     "spf": spf,
                     "dmarc": dmarc
        })

            except Exception as e:
              email_auth_results.append({
              "domain": domain,
              "error": str(e)
        }) 
               
        # Step 7: HTML phishing analysis
        try:
            html_results = analyze_html(email_data["body"])
            logging.info(f"HTML analysis found {len(html_results)} suspicious links")
        except Exception as e:
            logging.error(f"HTML analysis failed: {e}")
            html_results = []

        # Step 8: Threat intelligence enrichment
        vt_results = []
        ab_results = []

        # IP checks
        for ip in iocs["ips"]:
            try:
                vt_results.append(virustotal.check_ip(ip))
            except Exception as e:
                logging.warning(f"VirusTotal IP check failed for {ip}: {e}")

            try:
                ab_results.append(abuseipdb.check_ip(ip))
            except Exception as e:
                logging.warning(f"AbuseIPDB check failed for {ip}: {e}")

        # URL checks (only if API key exists)
        if os.getenv("VT_API_KEY"):
            for url in expanded_urls:
                try:
                    vt_results.append(virustotal.check_url(url))
                except Exception as e:
                    logging.warning(f"VirusTotal URL check failed for {url}: {e}")
        else:
            logging.warning("VirusTotal API key not set. Skipping VT checks.")

        # Step 9: Final results
        results = {
            "iocs": iocs,
            "expanded_urls": expanded_urls,
            "whois": whois_results,
            "email_auth": email_auth_results,
            "html_analysis": html_results,
            "threat_intel": {
                "virustotal": vt_results,
                "abuseipdb": ab_results
            },
            "attachments": email_data.get("attachments", [])
        }

        # Final Risk Analysis
        risk_data = calculate_risk(results)

        # Add to results
        results.update(risk_data)

        #Step 10: Generate report
        generate_report(results)
        logging.info("Report generated successfully")

    except Exception as e:
        logging.critical(f"Fatal error: {e}")


if __name__ == "__main__":
    main()