#!/usr/bin/env python3
"""Subdomain Enumeration Tool.

Author: Faraz Mustafa Seyed
"""
import argparse
import asyncio
import csv
import json
import sys
try:
    import aiodns
except ImportError:
    print("Install aiodns: pip install aiodns"); sys.exit(1)

def load_wordlist(path):
    with open(path) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

async def resolve_subdomain(resolver, sub, domain):
    fqdn = f"{sub}.{domain}"
    try:
        result = await resolver.query(fqdn, "A")
        return fqdn, result[0].host
    except: return fqdn, None

async def run_enum(domain, wordlist, concurrency=50):
    resolver = aiodns.DNSResolver()
    sem = asyncio.Semaphore(concurrency)
    async def bounded(sub):
        async with sem: return await resolve_subdomain(resolver, sub, domain)
    tasks = [bounded(sub) for sub in wordlist]
    results = []
    for coro in asyncio.as_completed(tasks):
        fqdn, ip = await coro
        if ip: results.append((fqdn, ip))
    return results

def main():
    p = argparse.ArgumentParser(description="Subdomain Enumeration")
    p.add_argument("domain")
    p.add_argument("-w", "--wordlist", required=True)
    p.add_argument("-c", "--concurrency", type=int, default=50)
    p.add_argument("--json")
    args = p.parse_args()
    wordlist = load_wordlist(args.wordlist)
    results = asyncio.run(run_enum(args.domain, wordlist, args.concurrency))
    if args.json:
        with open(args.json,"w") as f: json.dump([{"sub":f,"ip":ip} for f,ip in results], f, indent=2)
    for f, ip in sorted(results): print(f"  {f:45s} -> {ip}")
    print(f"\nFound {len(results)} subdomains")

if __name__ == "__main__": main()
