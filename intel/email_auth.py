import dns.resolver

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')

        for record in answers:
            record_str = record.to_text()

            if "v=spf1" in record_str:
                return {
                    "domain": domain,
                    "spf_record": record_str
                }

        return {
            "domain": domain,
            "spf_record": "Not found"
        }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }


def check_dmarc(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')

        for record in answers:
            record_str = record.to_text()

            if "v=DMARC1" in record_str:
                return {
                    "domain": domain,
                    "dmarc_record": record_str
                }

        return {
            "domain": domain,
            "dmarc_record": "Not found"
        }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }