import sys, asyncio, json
from playwright.async_api import async_playwright
BASE = sys.argv[1].rstrip('/'); OUT = sys.argv[2]
PAGES = [
 "", "technical-tutorials/searching/", "technical-tutorials/search/collections/",
 "system-reference-guide/work-with-git/",
 "technical-tutorials/visualization/visualizing-titiler-pgstac/",
 "technical-tutorials/working-with-r/visualizing-with-titiler-pgstac/",
 "technical-tutorials/working-with-r/vector-data-visualization/",
 "technical-tutorials/access/direct-access/",
 "technical-tutorials/search/searching-the-stac-catalog/",
 "getting-started/about-maap/",
 "technical-tutorials/visualization/visualize-lonboard/",
 "science/gedi/gedi-l2a/", "science/atl08/atl08/",
 "technical-tutorials/working-with-r/access-aws-maap/", "science/hls/hlsl30/",
 "system-reference-guide/custom-environments/",
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await b.new_context(viewport={"width":1400,"height":1000})
        report = {}
        for pg in PAGES:
            page = await ctx.new_page(); errs = []
            page.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            url = f"{BASE}/{pg}"
            try: await page.goto(url, wait_until="networkidle", timeout=90000)
            except Exception as e: errs.append(f"goto: {e}")
            await page.wait_for_timeout(3000)
            name = (pg.strip('/').replace('/','__') or 'index')
            await page.screenshot(path=f"{OUT}/{name}.png", full_page=True)
            info = await page.evaluate("""() => ({
                title: document.title,
                iframes: document.querySelectorAll('iframe').length,
                leaflet: document.querySelectorAll('.leaflet-container').length,
                leafletTiles: document.querySelectorAll('.leaflet-tile-loaded').length,
                htmlwidgets: document.querySelectorAll('.html-widget, [id^=htmlwidget]').length,
                imgs: document.querySelectorAll('img').length,
                brokenImgs: [...document.querySelectorAll('img')].filter(i=>i.complete && i.naturalWidth===0).length,
                tables: document.querySelectorAll('table').length,
                xarray: document.querySelectorAll('.xr-wrap').length,
                sup: document.querySelectorAll('sup').length,
                h1: document.querySelector('h1') ? document.querySelector('h1').innerText : null,
                textLen: document.body.innerText.length,
                scriptsInMain: document.querySelectorAll('main script').length,
            })""")
            info["errors"] = errs[:15]; report[pg] = info; await page.close()
        await b.close()
        json.dump(report, open(f"{OUT}/report.json","w"), indent=1)
        for k,v in report.items():
            e=v.pop('errors'); print(k or '/', json.dumps(v))
            for x in e[:5]: print('      ERR', x[:220])
asyncio.run(main())
