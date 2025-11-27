import re
import sys
import traceback
import logging
from datetime import datetime
from urllib.parse import urlparse

import requests
import whois
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from requests.exceptions import SSLError, RequestException

# -------------------------
# Logging setup
# -------------------------
LOGFILE = "phish_check_debug.log"
logging.basicConfig(
    filename=LOGFILE,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.DEBUG,
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console.setFormatter(console_formatter)
logging.getLogger().addHandler(console)

def log_exception_context(msg: str):
    logging.error(msg)
    traceback_str = traceback.format_exc()
    logging.debug("Full traceback:\n" + traceback_str)

# -------------------------
# Helpers (more defensive)
# -------------------------
def normalize_url(raw: str) -> str:
    raw = raw.strip()
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw):
        raw = 'http://' + raw
    return raw

def get_hostname(url: str) -> str:
    try:
        p = urlparse(url)
        host = p.hostname or ''
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception as e:
        logging.debug(f"get_hostname error for url={url}: {e}")
        return ""

def looks_like_ip(hostname: str) -> bool:
    if not hostname:
        return False
    if re.match(r'^\d{1,3}(?:\.\d{1,3}){3}$', hostname):
        return True
    if ':' in hostname and any(c.isdigit() for c in hostname):
        return True
    return False

def safe_whois(hostname: str):
    """Return datetime or None. Log failures."""
    try:
        w = whois.whois(hostname)
    except Exception as e:
        logging.debug(f"whois failed for {hostname}: {e}")
        return None
    creation = getattr(w, "creation_date", None)
    if creation is None:
        logging.debug(f"whois has no creation_date for {hostname}. raw whois object keys: {list(w.keys()) if hasattr(w,'keys') else 'n/a'}")
        return None
    # handle list or single value
    if isinstance(creation, list):
        creation = creation[0] if creation else None
    if isinstance(creation, datetime):
        return creation
    if isinstance(creation, str):
        try:
            return dateparser.parse(creation)
        except Exception as e:
            logging.debug(f"dateparser failed for {creation}: {e}")
            return None
    return None

def fetch_page(url: str, timeout=8):
    """Return (html_text or None, final_url or None, tls_error_bool, fetch_error_bool)"""
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text, r.url, False, False
    except SSLError as e:
        logging.debug(f"SSLError for {url}: {e}")
        # try with verify=False to still get HTML (but mark tls_error)
        try:
            r = requests.get(url, timeout=timeout, verify=False)
            return r.text, r.url, True, False
        except Exception as e2:
            logging.debug(f"fetch fallback failed for {url}: {e2}")
            return None, None, True, True
    except RequestException as e:
        logging.debug(f"RequestException for {url}: {e}")
        return None, None, False, True
    except Exception as e:
        logging.debug(f"Unknown fetch error for {url}: {e}")
        return None, None, False, True

def extract_basic_features(html: str, final_url: str):
    try:
        soup = BeautifulSoup(html or "", "html.parser")
        features = {}
        try:
            features['title'] = (soup.title.string.strip() if soup.title and soup.title.string else "")
        except Exception:
            features['title'] = ""
        features['has_password_input'] = bool(soup.find("input", {"type": "password"}))
        features['num_forms'] = len(soup.find_all("form"))
        scripts = soup.find_all("script", src=True)
        ext_scripts = 0
        for s in scripts:
            src = s.get("src") or ""
            if src.startswith("http"):
                try:
                    src_host = urlparse(src).hostname or ""
                    if get_hostname(final_url) not in src_host:
                        ext_scripts += 1
                except Exception:
                    ext_scripts += 1
        features['num_external_scripts'] = ext_scripts
        text = soup.get_text(separator=" ").lower()
        keywords = ["verify", "account suspended", "update your", "confirm your", "login to", "click below", "unauthorized", "billing"]
        features['keyword_matches'] = [k for k in keywords if k in text]
        suspicious_form_action = False
        for f in soup.find_all("form"):
            action = f.get("action") or ""
            if action.startswith("http"):
                try:
                    action_host = urlparse(action).hostname or ""
                    if action_host and get_hostname(final_url) != action_host:
                        suspicious_form_action = True
                        break
                except Exception:
                    suspicious_form_action = True
                    break
        features['suspicious_form_action'] = suspicious_form_action
        return features
    except Exception:
        log_exception_context("extract_basic_features crashed")
        return {
            'title': '',
            'has_password_input': False,
            'num_forms': 0,
            'num_external_scripts': 0,
            'keyword_matches': [],
            'suspicious_form_action': False
        }

# -------------------------
# Analysis flow (with try/except)
# -------------------------
def analyze_url(raw_input: str):
    try:
        url = normalize_url(raw_input)
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()
        hostname = get_hostname(url)
        if not hostname:
            logging.error("Could not parse hostname from input. Please use 'example.com' or 'https://example.com'")
            return

        warnings = 0
        print(f"Checking: {hostname}")

        if looks_like_ip(hostname):
            print("[WARNING] Host looks like an IP address or IPv6 literal.")
            warnings += 1
        else:
            print(f"Hostname: {hostname}")

        if scheme == "https":
            print("[OK] Uses HTTPS scheme.")
        else:
            print("[WARNING] Not using HTTPS; this increases risk.")
            warnings += 1

        creation = safe_whois(hostname)
        if creation is None:
            print("[INFO] WHOIS creation date: unavailable (registrar/private WHOIS/rate limit).")
        else:
            age_days = (datetime.now() - creation.replace(tzinfo=None)).days
            print(f"[INFO] Domain creation date (UTC): {creation.strftime('%Y-%m-%d')}  — age: {age_days} days")
            if age_days < 30:
                print("[WARNING] Domain is very new (<30 days).")
                warnings += 1
            elif age_days < 365:
                print("[WARNING] Domain < 1 year old. Exercise caution.")

        html, final_url, tls_error, fetch_error = fetch_page(url)
        if fetch_error:
            print("[WARNING] Could not fetch the page. See log for details.")
            logging.info(f"Fetch error for {url}")
            warnings += 1
        else:
            if tls_error:
                print("[WARNING] TLS/SSL certificate error detected (invalid/expired).")
                warnings += 1
            features = extract_basic_features(html, final_url)
            print(f"[INFO] Page title: {features['title'] or '<no title>'}")
            if features['has_password_input']:
                print("[WARNING] Page contains a password input field.")
                warnings += 1
            if features['suspicious_form_action']:
                print("[WARNING] A form posts to a different domain (suspicious).")
                warnings += 1
            if features['num_external_scripts'] > 5:
                print(f"[WARNING] Many external scripts ({features['num_external_scripts']}) — check logs for script list.")
            if features['keyword_matches']:
                print("[WARNING] Suspicious keywords on page: " + ", ".join(features['keyword_matches']))
                warnings += 1

        print(f"\nSummary warnings count: {warnings}")
        if warnings >= 3:
            print("[HIGH RISK] Final verdict: HIGH RISK — do NOT enter credentials.")
        elif warnings == 2:
            print("[MEDIUM RISK] Final verdict: MEDIUM RISK — be cautious.")
        else:
            print("[LOW RISK] Final verdict: LOW RISK (heuristic).")

        logging.info(f"Analysis completed for {hostname} with warnings={warnings}")

    except Exception:
        log_exception_context("analyze_url encountered an unexpected error. Full traceback written to log.")
        print("ERROR: An unexpected error occurred. Check phish_check_debug.log for details.")

# -------------------------
# Command-line entry
# -------------------------
def main():
    try:
        if len(sys.argv) >= 2:
            user_input = sys.argv[1]
        else:
            try:
                user_input = input("Enter website URL (example.com or https://example.com): ").strip()
            except EOFError:
                print("No input provided. Usage: python fakedetector.py <url>")
                return
        analyze_url(user_input)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception:
        log_exception_context("main crashed")
        print("ERROR: critical failure. See phish_check_debug.log")

if __name__ == "__main__":
    main()