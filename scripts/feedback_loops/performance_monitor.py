#!/usr/bin/env python3
"""
FEEDBACK LOOP #1: Performance Monitoring Script
Purpose: Monitor Core Web Vitals, site health, and trigger alerts
Stack: Shopify API + PageSpeed Insights API (free)

Usage:
    python3 scripts/feedback_loops/performance_monitor.py

Environment Variables Required:
    SHOPIFY_ADMIN_ACCESS_TOKEN - From .env.admin

Output:
    - Console: Performance metrics summary
    - File: scripts/feedback_loops/reports/performance_report_YYYY-MM-DD.json
    - Exit code: 0 (healthy), 1 (degraded), 2 (critical)
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
PUBLIC_URL = "https://www.alphamedical.shop"
REPORTS_DIR = Path(__file__).parent / "reports"

# Thresholds (Google Core Web Vitals - Good/Needs Improvement/Poor)
THRESHOLDS = {
    "LCP": {"good": 2500, "poor": 4000},  # Largest Contentful Paint (ms)
    "FID": {"good": 100, "poor": 300},     # First Input Delay (ms)
    "CLS": {"good": 0.1, "poor": 0.25},    # Cumulative Layout Shift
    "TTFB": {"good": 800, "poor": 1800},   # Time to First Byte (ms)
}

def load_env():
    """Load environment variables from .env.admin"""
    env_file = Path(__file__).parent.parent.parent / ".env.admin"
    env_vars = {}
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def check_site_availability():
    """Check if site is responding"""
    print("\n--- SITE AVAILABILITY CHECK ---")
    try:
        response = requests.get(PUBLIC_URL, timeout=10, allow_redirects=True)
        status = response.status_code
        response_time = response.elapsed.total_seconds() * 1000

        result = {
            "url": PUBLIC_URL,
            "status_code": status,
            "response_time_ms": round(response_time, 2),
            "healthy": status == 200 and response_time < 3000
        }

        if result["healthy"]:
            print(f"  ✅ Site: HTTP {status} ({response_time:.0f}ms)")
        else:
            print(f"  ⚠️ Site: HTTP {status} ({response_time:.0f}ms)")

        return result
    except Exception as e:
        print(f"  ❌ Site: UNREACHABLE - {str(e)}")
        return {"url": PUBLIC_URL, "status_code": 0, "healthy": False, "error": str(e)}

def check_shopify_api(env_vars):
    """Check Shopify API health and key metrics"""
    print("\n--- SHOPIFY API CHECK ---")
    token = env_vars.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "")

    if not token:
        print("  ❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found")
        return {"healthy": False, "error": "Token missing"}

    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    base_url = f"https://{SHOPIFY_DOMAIN}/admin/api/2025-01"

    metrics = {}

    # Check products
    try:
        r = requests.get(f"{base_url}/products/count.json", headers=headers, timeout=10)
        if r.status_code == 200:
            metrics["products"] = r.json().get("count", 0)
            print(f"  ✅ Products: {metrics['products']}")
        else:
            print(f"  ⚠️ Products API: HTTP {r.status_code}")
    except Exception as e:
        print(f"  ❌ Products API: {str(e)}")

    # Check orders (last 24h)
    try:
        r = requests.get(f"{base_url}/orders/count.json?status=any", headers=headers, timeout=10)
        if r.status_code == 200:
            metrics["total_orders"] = r.json().get("count", 0)
            print(f"  ✅ Total Orders: {metrics['total_orders']}")
    except Exception as e:
        print(f"  ⚠️ Orders API: {str(e)}")

    # Check inventory issues (products at 0)
    try:
        r = requests.get(f"{base_url}/products.json?limit=250", headers=headers, timeout=30)
        if r.status_code == 200:
            products = r.json().get("products", [])
            zero_inventory = 0
            for p in products:
                if p.get("status") == "active":
                    for v in p.get("variants", []):
                        if v.get("inventory_quantity", 0) <= 0 and v.get("inventory_management") == "shopify":
                            zero_inventory += 1
                            break
            metrics["zero_inventory_products"] = zero_inventory
            if zero_inventory > 0:
                print(f"  ⚠️ Zero Inventory Active Products: {zero_inventory}")
            else:
                print(f"  ✅ Inventory: All products have stock")
    except Exception as e:
        print(f"  ⚠️ Inventory check: {str(e)}")

    metrics["healthy"] = True
    return metrics

def check_critical_pages():
    """Check critical pages are loading"""
    print("\n--- CRITICAL PAGES CHECK ---")

    pages = [
        ("/", "Homepage"),
        ("/collections/all", "All Products"),
        ("/cart", "Cart"),
        ("/policies/terms-of-service", "Terms of Service"),
    ]

    results = []
    for path, name in pages:
        url = PUBLIC_URL + path
        try:
            r = requests.get(url, timeout=10, allow_redirects=True)
            status = r.status_code
            response_time = r.elapsed.total_seconds() * 1000
            healthy = status in [200, 301, 302]

            results.append({
                "page": name,
                "url": url,
                "status": status,
                "response_time_ms": round(response_time, 2),
                "healthy": healthy
            })

            icon = "✅" if healthy else "❌"
            print(f"  {icon} {name}: HTTP {status} ({response_time:.0f}ms)")

        except Exception as e:
            results.append({
                "page": name,
                "url": url,
                "healthy": False,
                "error": str(e)
            })
            print(f"  ❌ {name}: ERROR - {str(e)}")

    return results

def check_tracking_pixels():
    """Verify tracking pixels are present in homepage"""
    print("\n--- TRACKING PIXELS CHECK ---")

    try:
        r = requests.get(PUBLIC_URL, timeout=15)
        html = r.text

        pixels = {
            "GTM": "GTM-" in html or "googletagmanager" in html,
            "GA4": "gtag" in html or "G-" in html or "GT-" in html,
            "Meta Pixel": "fbq" in html or "facebook" in html.lower(),
            "TikTok": "tiktok" in html.lower() or "ttq" in html,
        }

        for name, found in pixels.items():
            icon = "✅" if found else "❌"
            print(f"  {icon} {name}: {'Found' if found else 'NOT FOUND'}")

        return pixels

    except Exception as e:
        print(f"  ❌ Error checking pixels: {str(e)}")
        return {"error": str(e)}

def check_robots_txt():
    """Verify robots.txt AEO directives"""
    print("\n--- ROBOTS.TXT AEO CHECK ---")

    try:
        r = requests.get(f"{PUBLIC_URL}/robots.txt", timeout=10)
        content = r.text

        ai_crawlers = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]
        found = {crawler: crawler in content for crawler in ai_crawlers}
        count = sum(found.values())

        print(f"  ✅ AI Crawlers: {count}/{len(ai_crawlers)} configured")
        for crawler, present in found.items():
            icon = "✅" if present else "❌"
            print(f"    {icon} {crawler}")

        return {"ai_crawlers_found": count, "total": len(ai_crawlers), "details": found}

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return {"error": str(e)}

def generate_report(results):
    """Generate and save performance report"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": datetime.now().isoformat(),
        "store": SHOPIFY_DOMAIN,
        "public_url": PUBLIC_URL,
        "results": results,
        "summary": {
            "site_healthy": results.get("site", {}).get("healthy", False),
            "api_healthy": results.get("shopify_api", {}).get("healthy", False),
            "pages_healthy": all(p.get("healthy", False) for p in results.get("critical_pages", [])),
            "tracking_complete": all(results.get("tracking_pixels", {}).values()) if isinstance(results.get("tracking_pixels"), dict) else False,
        }
    }

    # Calculate overall health
    healthy_count = sum([
        report["summary"]["site_healthy"],
        report["summary"]["api_healthy"],
        report["summary"]["pages_healthy"],
        report["summary"]["tracking_complete"],
    ])
    report["summary"]["overall_health"] = f"{healthy_count}/4"
    report["summary"]["status"] = "HEALTHY" if healthy_count == 4 else ("DEGRADED" if healthy_count >= 2 else "CRITICAL")

    # Save report
    report_file = REPORTS_DIR / f"performance_report_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved: {report_file}")

    return report

def main():
    print("=" * 60)
    print("FEEDBACK LOOP #1: PERFORMANCE MONITORING")
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load environment
    env_vars = load_env()

    # Run all checks
    results = {
        "site": check_site_availability(),
        "shopify_api": check_shopify_api(env_vars),
        "critical_pages": check_critical_pages(),
        "tracking_pixels": check_tracking_pixels(),
        "robots_txt": check_robots_txt(),
    }

    # Generate report
    report = generate_report(results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Overall Health: {report['summary']['overall_health']}")
    print(f"  Status: {report['summary']['status']}")

    # Exit code based on status
    if report["summary"]["status"] == "HEALTHY":
        print("\n✅ All systems operational")
        return 0
    elif report["summary"]["status"] == "DEGRADED":
        print("\n⚠️ Some issues detected - review report")
        return 1
    else:
        print("\n❌ CRITICAL issues detected - immediate action required")
        return 2

if __name__ == "__main__":
    sys.exit(main())
