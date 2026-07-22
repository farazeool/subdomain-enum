# subdomain-enum

> Concurrent subdomain enumeration with DNS resolution and clean CLI output.

## Features

- ⚡ Async DNS resolution with asyncio
- 📋 Wordlist-based discovery
- 🌐 Wildcard detection
- 📊 CSV/JSON output

## Usage

```bash
pip install -r requirements.txt
python3 subenum.py example.com -w wordlist.txt
python3 subenum.py example.com -w wordlist.txt --json
```

## Why I built this

I needed a fast, concurrent subdomain enumerator for security assessments.

— Faraz

## License
MIT — © 2026 Faraz Mustafa Seyed