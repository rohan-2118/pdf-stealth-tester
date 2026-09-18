import os
import time
import random
import string
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests

MAX_PARALLEL_WORKERS = 15 

VALID_WEBSITE_PAGES = [
    "/about", "/contact", "/privacy-policy",
    "/merge-pdf", "/split-pdf", "/compress-pdf", "/organize-pdf", 
    "/rotate-pdf", "/remove-pages", "/crop-pdf", "/repair-pdf",
    "/word-to-pdf", "/powerpoint-to-pdf", "/excel-to-pdf", "/jpg-to-pdf", "/html-to-pdf",
    "/pdf-to-word", "/pdf-to-powerpoint", "/pdf-to-excel", "/pdf-to-jpg", "/pdf-to-pdfa", "/pdf-to-markdown",
    "/edit-pdf", "/add-page-numbers", "/watermark-pdf", "/ocr-pdf",
    "/unlock-pdf", "/protect-pdf", "/sign-pdf", "/redact-pdf", "/compare-pdf"
]

DYNAMIC_PROXY_POOL = []
LAST_PROXY_REFRESH = 0

def fetch_fresh_proxies():
    global DYNAMIC_PROXY_POOL, LAST_PROXY_REFRESH
    current_time = time.time()
    if DYNAMIC_PROXY_POOL and (current_time - LAST_PROXY_REFRESH) < 900:
        return DYNAMIC_PROXY_POOL
    try:
        url = "https://proxyscrape.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as response:
            proxy_data = response.read().decode('utf-8')
        fresh_list = [line.strip() for line in proxy_data.split('\n') if line.strip()]
        if fresh_list:
            DYNAMIC_PROXY_POOL = fresh_list
            LAST_PROXY_REFRESH = current_time
            return DYNAMIC_PROXY_POOL
    except Exception:
        pass
    return DYNAMIC_PROXY_POOL

def run_stealth_network_bot(bot_id):
    bot_start_time = time.time()
    base_url = "https://smartpdfconvert.online"
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    proxy_pool = fetch_fresh_proxies()
    proxy_dict = None
    if proxy_pool:
        chosen_proxy = random.choice(proxy_pool)
        proxy_dict = {"http": f"socks5://{chosen_proxy}", "https": f"socks5://{chosen_proxy}"}

    session = requests.Session(impersonate="chrome")
    
    try:
        session.get(base_url, proxies=proxy_dict, timeout=25)
        time.sleep(random.uniform(5.0, 8.5)) 
        
        chosen_journey = random.sample(VALID_WEBSITE_PAGES, k=4)
        exploration_pages = chosen_journey[:-1]
        final_tool_page = chosen_journey[-1]
        
        for page in exploration_pages:
            session.get(f"{base_url}{page}", proxies=proxy_dict, timeout=25)
            time.sleep(random.uniform(5.5, 9.0))
            
        session.get(f"{base_url}{final_tool_page}", proxies=proxy_dict, timeout=25)
        time.sleep(random.uniform(2.0, 4.0))
        
        pdf_size = int(random.uniform(0.5, 4.5) * 1024 * 1024)
        mock_pdf_bytes = os.urandom(pdf_size)
        
        files = {'file': (f'test_{unique_id}.pdf', mock_pdf_bytes, 'application/pdf')}
        data = {'outputFormat': 'docx'}
        
        session.post(f"{base_url}/api/convert", files=files, data=data, proxies=proxy_dict, timeout=35)
        time.sleep(random.uniform(6.0, 10.0))
        
        session.get(base_url, proxies=proxy_dict, timeout=25)
        
        elapsed = time.time() - bot_start_time
        if elapsed < 60.0:
            time.sleep(60.0 - elapsed)
            
        print(f"[Worker Bot #{bot_id}] Completed journey successfully in {time.time() - bot_start_time:.1f}s.")
        
    except Exception:
        pass

if __name__ == "__main__":
    fetch_fresh_proxies()
    bot_counter = 1
    runtime_limit = 45 * 60
    script_start = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_WORKERS) as executor:
        while (time.time() - script_start) < runtime_limit:
            executor.submit(run_stealth_network_bot, bot_counter)
            bot_counter += 1
            time.sleep(random.uniform(1.0, 2.5))
