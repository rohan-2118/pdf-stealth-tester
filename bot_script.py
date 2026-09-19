import os
import time
import random
import string
import urllib.request
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

# Runs 5 concurrent local browser worker pipelines inside each server instance node
MAX_PARALLEL_BROWSERS = 5 

VALID_WEBSITE_PAGES = [
    "/about", "/contact", "/privacy-policy",
    "/merge-pdf", "/split-pdf", "/compress-pdf", "/organize-pdf"
]

# Randomized device parameters simulating varying real consumer hardware environments
DEVICE_PROFILES = [
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "w": 1920, "h": 1080, "os": "windows"},
    {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "w": 1440, "h": 900, "os": "macos"},
    {"ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "w": 1366, "h": 768, "os": "linux"},
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0", "w": 1536, "h": 864, "os": "windows"},
    {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15", "w": 1728, "h": 1117, "os": "macos"}
]

DYNAMIC_PROXY_POOL = []
LAST_PROXY_REFRESH = 0

def fetch_fresh_proxies():
    global DYNAMIC_PROXY_POOL, LAST_PROXY_REFRESH
    current_time = time.time()
    if DYNAMIC_PROXY_POOL and (current_time - LAST_PROXY_REFRESH) < 600:
        return DYNAMIC_PROXY_POOL
    try:
        url = "https://proxyscrape.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            proxy_data = response.read().decode('utf-8')
        fresh_list = [line.strip() for line in proxy_data.split('\n') if line.strip()]
        if fresh_list:
            DYNAMIC_PROXY_POOL = fresh_list
            LAST_PROXY_REFRESH = current_time
            return DYNAMIC_PROXY_POOL
    except Exception:
        pass
    return DYNAMIC_PROXY_POOL

def generate_organic_mouse_path(start, end):
    x1, y1 = start
    x2, y2 = end
    drift_x = random.randint(-25, 25)
    drift_y = random.randint(-25, 25)
    steps = random.randint(30, 50)
    t = np.linspace(0, 1, steps)
    x_path = x1 + (x2 - x1) * t + np.sin(t * np.pi) * drift_x
    y_path = y1 + (y2 - y1) * t + np.sin(t * np.pi) * drift_y
    path = []
    for i in range(steps):
        jitter_x = random.uniform(-0.3, 0.3) if i % 3 == 0 else 0
        jitter_y = random.uniform(-0.3, 0.3) if i % 3 == 0 else 0
        delay = random.uniform(0.006, 0.012)
        if i > (steps * 0.8): 
            delay += random.uniform(0.010, 0.025)
        path.append((x_path[i] + jitter_x, y_path[i] + jitter_y, delay))
    return path

def organic_hover(page, selector):
    try:
        element = page.locator(selector).first
        box = element.bounding_box()
        if not box: return
        current_x, current_y = random.randint(10, 150), random.randint(10, 150)
        target_x = box["x"] + random.randint(5, int(box["width"] - 5))
        target_y = box["y"] + random.randint(5, int(box["height"] - 5))
        for x, y, delay in generate_organic_mouse_path((current_x, current_y), (target_x, target_y)):
            page.mouse.move(x, y)
            time.sleep(delay)
        time.sleep(random.uniform(0.3, 0.7))
    except Exception:
        pass

def human_scroll(page):
    start_time = time.time()
    duration = random.uniform(6.0, 9.5)
    while (time.time() - start_time) < duration:
        page.evaluate(f"window.scrollBy(0, {random.randint(180, 420)});")
        time.sleep(random.uniform(0.9, 1.9))
        if random.random() < 0.2:
            page.evaluate(f"window.scrollBy(0, -{random.randint(100, 200)});")
            time.sleep(random.uniform(0.6, 1.4))

def run_isolated_device_bot(bot_id, playwright_instance):
    bot_start_time = time.time()
    base_url = "https://smartpdfconvert.online"
    
    # 1. Device Profile Randomization Configuration
    device = random.choice(DEVICE_PROFILES)
    
    # 2. IP Routing Assignment
    proxy_pool = fetch_fresh_proxies()
    proxy_args = None
    if proxy_pool:
        chosen_proxy = random.choice(proxy_pool)
        proxy_args = {"server": f"socks5://{chosen_proxy}"}
        print(f"[Bot #{bot_id}] Running Device profile [{device['os'].upper()}] on Proxy IP: {chosen_proxy}")
    
    try:
        browser = playwright_instance.chromium.launch(headless=False, proxy=proxy_args)
        
        # Enforcing unique environment dimensions and hardware agents natively
        context = browser.new_context(
            user_agent=device["ua"],
            viewport={"width": device["w"], "height": device["h"]},
            locale=random.choice(["en-US", "en-GB", "de-DE", "es-ES"]),
            timezone_id=random.choice(["America/New_York", "Europe/London", "Europe/Berlin"])
        )
        
        context.set_extra_http_headers({
            "X-Load-Test": "GitHub-Action-SequentialGrid"
        })
        
        page = context.new_page()
        
        # Journey Stage 1: Hit Homepage & scroll script compilers
        page.goto(base_url, timeout=50000, wait_until="load")
        time.sleep(random.uniform(2.5, 4.5))
        human_scroll(page)
        
        # Journey Stage 2: Pick an internal layout page route path
        chosen_page = random.choice(VALID_WEBSITE_PAGES)
        page.goto(f"{base_url}{chosen_page}", timeout=50000, wait_until="load")
        time.sleep(random.uniform(2.0, 4.0))
        human_scroll(page)
        
        # Journey Stage 3: Interact with layout targets
        # Checks if script containers are visible inside the unique device resolution box
        if page.locator('.ad-unit').first.is_visible():
            organic_hover(page, '.ad-unit')
            time.sleep(random.uniform(2.0, 4.5))
            
        # Duration Boundary Engine Safeguard
        elapsed = time.time() - bot_start_time
        if elapsed < 65.0:
            time.sleep(65.0 - elapsed)
            
        print(f"[Worker Bot #{bot_id}] Target complete. Session lifecycle closed securely.")
        context.close()
        browser.close()
        
    except Exception as e:
        print(f"[Bot #{bot_id}] Pipeline timeout bypass: {e}")

def run_manager(p):
    bot_counter = 1
    # Hard loop time frame limit optimized for short group bursts
    runtime_limit = 12 * 60 
    script_start = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_BROWSERS) as executor:
        while (time.time() - script_start) < runtime_limit:
            executor.submit(run_isolated_device_bot, bot_counter, p)
            bot_counter += 1
            time.sleep(random.uniform(14.0, 26.0))

if __name__ == "__main__":
    fetch_fresh_proxies()
    with sync_playwright() as p:
        run_manager(p)
