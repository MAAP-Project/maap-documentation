import asyncio, sys
from playwright.async_api import async_playwright
BASE=sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
TESTS = [
 "/system_reference_guide/jobs_maappy.html#Passing-Credentials-for-Other-Services-into-Jobs-(Secrets-Management)",
 "/technical_tutorials/search/catalog.html",
 "/science/GEDI/GEDI_L2A.html",
 "/getting_started.html",
 "/system_reference_guide/custom-environments.html#Custom-environments",
 "/technical_tutorials/working_with_r/find_data_in_r.html",
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        page = await b.new_page()
        for t in TESTS:
            await page.goto(BASE + t, wait_until="networkidle")
            await page.wait_for_timeout(1500)
            url = page.url
            frag = url.split('#',1)[1] if '#' in url else ''
            ok = await page.evaluate("h => h ? !!document.getElementById(h) : true", frag)
            title = await page.title()
            y = await page.evaluate("window.scrollY")
            print(f"{t}\n   -> {url.replace(BASE,'')}  anchor-exists={ok} scrollY={y} title={title[:50]!r}")
        await b.close()
asyncio.run(main())
