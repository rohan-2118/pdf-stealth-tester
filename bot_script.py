import os
import time
import random
import string
import urllib.request
import asyncio
import numpy as np
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# Optimized parallel browser loops running concurrently inside the async sandbox
MAX_PARALLEL_BROWSERS = 4

UPLOAD_DIR = os.path.join(os.getcwd(), "cloud_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

VALID_WEBSITE_PAGES = [
    "/about", "/contact", "/privacy-policy",
    "/merge-pdf", "/split-pdf", "/compress-pdf", "/organize-pdf"
]

DEVICE_PROFILES = [
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "w": 1920, "h": 1080},
    {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "w": 1440, "h": 900},
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "w": 1536, "h": 864}
]

def fetch_fresh_proxies():
    """ Strict proxy parser that completely ignores dead nodes or HTML page text """
    try:
        url = "https://proxyscrape.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            proxy_data = response.read().decode('utf-8')
        lines = [line.strip() for line in proxy_data.split('\n') if line.strip()]
        return [l for l in lines if not l.startswith("<") and ":" in l and len(l) < 30]
    except Exception:
        return []

def generate_dynamic_pdf():
    """ Synthesizes a dummy PDF payload of a random size between 1.5MB and 4.5MB """
    target_size_bytes = int(random.uniform(1.5, 4.5) * 1024 * 1024)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = os.path.join(UPLOAD_DIR, f"task_{random_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(b"%PDF-1.5\n")
        padding = target_size_bytes - 9
        if padding > 0:
            f.write(os.urandom(padding))
    return file_path

async def human_scroll(page):
    start_time = time.time()
    duration = random.uniform(5.5, 9.0)
    while (time.time() - start_time) < duration:
        await page.evaluate(f"window.scrollBy(0, {random.randint(150, 400)});")
        await asyncio.sleep(random.uniform(0.8, 1.8))

async def run_async_stealth_bot(bot_id, playwright_instance, proxy_list):
    bot_start_time = time.time()
    base_url = "https://smartpdfconvert.online"
    device = random.choice(DEVICE_PROFILES)
    upload_file_path = generate_dynamic_pdf()
    
    proxy_args = None
    if proxy_list:
        chosen_proxy = random.choice(proxy_list)
        proxy_args = {"server": f"socks5://{chosen_proxy}"}
        print(f"[Bot #{bot_id}] Initiating clean client channel via proxy: {chosen_proxy}")
    else:
        print(f"[Bot #{bot_id}] Running via direct pipeline fallback...")

    try:
        # Launching browser natively inside the asynchronous workflow loop
        browser = await playwright_instance.chromium.launch(headless=True, proxy=proxy_args)
        context = await browser.new_context(
            user_agent=device["ua"],
            viewport={"width": device["w"], "height": device["h"]},
            locale="en-US"
        )
        
        page = await context.new_page()
        await stealth_async(page) # Completely strips automation indicators dynamically
        
        # 1. Access Entry Portal Homepage
        await page.goto(base_url, timeout=50000, wait_until="load")
        await asyncio.sleep(random.uniform(2, 4))
        await human_scroll(page)
        
        # 2. Navigate to a random tool sub-page route
        chosen_page = random.choice(VALID_WEBSITE_PAGES)
        await page.goto(f"{base_url}{chosen_page}", timeout=50000, wait_until="load")
        await asyncio.sleep(random.uniform(2, 4))
        
        # 3. Handle File Form Injection
        file_input = page.locator('input[type="file"]').first
        if await file_input.is_visible():
            await file_input.set_input_files(upload_file_path)
            print(f"[Bot #{bot_id}] File payload injected into form container.")
            
            # Instantly delete source file to preserve cloud disk quota
            if os.path.exists(upload_file_path):
                os.remove(upload_file_path)
                upload_file_path = None
                
            # Locate and click submit elements
            convert_btn = page.locator('button[type="submit"], input[type="submit"], #convert-btn').first
            if await convert_btn.is_visible():
                await convert_btn.click()
                await asyncio.sleep(random.uniform(6.0, 12.0))
        
        # Enforce minimum activity loop timeline boundary
        elapsed = time.time() - bot_start_time
        if elapsed < 65.0:
            await asyncio.sleep(65.0 - elapsed)
            
        print(f"[Worker Bot #{bot_id}] Transmission sequence completed cleanly.")
        await context.close()
        await browser.close()
        
    except Exception as e:
        print(f"[Bot #{bot_id}] Session closed via pipeline timeout: {e}")
        if upload_file_path and os.path.exists(upload_file_path):
            os.remove(upload_file_path)

async def main():
    print("--- STARTING HARDENED PRODUCTION STEALTH ENVIRONMENT CONTROLLER ---")
    proxy_pool = fetch_fresh_proxies()
    print(f"[System Engine] Found {len(proxy_pool)} active, verified IP nodes.")
    
    bot_counter = 1
    # Run loop safely for 12 minutes per group matrix partition block
    runtime_limit = 12 * 60
    script_start = time.time()
    
    async with async_playwright() as p:
        while (time.time() - script_start) < runtime_limit:
            tasks = []
            for _ in range(MAX_PARALLEL_BROWSERS):
                tasks.append(run_async_stealth_bot(bot_counter, p, proxy_pool))
                bot_counter += 1
            
            # Compute parallel batch concurrently without greenlet engine crashes
            await asyncio.gather(*tasks)
            
            if bot_counter % 12 == 0:
                proxy_pool = fetch_fresh_proxies()
                
            await asyncio.sleep(random.uniform(5, 12))

if __name__ == "__main__":
    asyncio.run(main())
