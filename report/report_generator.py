import json

def generate_report(data, output_file="report.json"):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Report saved to {output_file}")