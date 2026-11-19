import sys
import ipaddress
import subprocess

def copy_to_clipboard(text: str):
    try:
        proc = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        proc.communicate(text.encode('utf-8'))
        print("Output copied to your clipboard!")
    except Exception:
        print(f"Issue with copy_to_clipboard {Exception}")

def range_to_cidrs(entry: str) -> list[str]:
    entry = entry.strip()
    if not entry:
        return []
    
    if '-' in entry:
        parts = [p.strip() for p in entry.split('-')]
        if len(parts) == 2:
            try:
                start = ipaddress.IPv4Address(parts[0])
                end = ipaddress.IPv4Address(parts[1])
                return [str(net) for net in ipaddress.summarize_address_range(start, end)]
            except ValueError:
                return [entry]
        else:
            return [entry]
                
    try:
        net = ipaddress.IPv4Network(entry, strict=False)
        return [str(net)]
    except ValueError:
        return [entry]

def main():
    print("Paste your IP ranges below, then press Enter, Ctrl+Z, and Enter:\n")
    try:
        raw_input_text = sys.stdin.read()
    except KeyboardInterrupt:
        return

    subnets = []
    for line in raw_input_text.splitlines():
        line = line.strip()
        if line:
            subnets.extend(range_to_cidrs(line))

    # Deduplicate while preserving order
    seen = set()
    unique_subnets = [s for s in subnets if not (s in seen or seen.add(s))]

    output_text = "\n".join(unique_subnets)

    print("\n--- GENERATED SUBNETS ---")
    print(output_text)
    print(f"\nTotal: {len(unique_subnets)} subnets generated.")

    copy_to_clipboard(output_text)

if __name__ == "__main__":
    main()