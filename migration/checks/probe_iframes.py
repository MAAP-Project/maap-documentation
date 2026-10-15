import sys, asyncio, json
from playwright.async_api import async_playwright
PAGES = sys.argv[2:]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await b.new_context(viewport={"width":1400,"height":1000})
        for pg in PAGES:
            page = await ctx.new_page()
            await page.goto(sys.argv[1].rstrip('/') + '/' + pg, wait_until="networkidle", timeout=90000)
            await page.wait_for_timeout(4000)
            print("==", pg)
            for i, fr in enumerate(page.frames):
                if fr == page.main_frame: continue
                try:
                    info = await fr.evaluate("""() => ({
                        url: location.href.slice(0,60), srcdoc: !!window.frameElement && !!window.frameElement.srcdoc,
                        leaflet: document.querySelectorAll('.leaflet-container').length,
                        tilesLoaded: document.querySelectorAll('.leaflet-tile-loaded').length,
                        tilesAll: document.querySelectorAll('.leaflet-tile').length,
                        htmlwidgets: document.querySelectorAll('.html-widget, [id^=htmlwidget]').length,
                        scripts: document.scripts.length,
                        bodyText: document.body ? document.body.innerText.slice(0,80) : null,
                        w: document.documentElement.clientWidth, h: document.documentElement.clientHeight,
                    })""")
                    el = await fr.frame_element()
                    box = await el.bounding_box()
                    attrs = await el.evaluate("e => ({sandbox: e.getAttribute('sandbox'), width: e.getAttribute('width'), height: e.getAttribute('height'), style: e.getAttribute('style'), cls: e.className})")
                    print(f"  frame {i}: {json.dumps(info)} box={box} attrs={attrs}")
                except Exception as e:
                    print(f"  frame {i}: ERR {e}")
            await page.close()
        await b.close()
asyncio.run(main())
