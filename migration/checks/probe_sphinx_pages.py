import sys, asyncio, json
from playwright.async_api import async_playwright
BASE = sys.argv[1].rstrip('/')
OUT = sys.argv[2]
PAGES = [
 "index.html",
 "technical_tutorials.html",
 "release_notes.html",
 "system_reference_guide/personal_access_tokens.html",
 "technical_tutorials/user_data/stac_metadata.html",
 "technical_tutorials/search/collections.html",
 "system_reference_guide/work_with_git.html",
 "technical_tutorials/visualization/visualizing_titiler-pgstac.html",
 "technical_tutorials/working_with_r/visualizing_with_titiler-pgstac.html",
 "technical_tutorials/working_with_r/vector_data_visualization.html",
 "technical_tutorials/access/direct_access.html",
 "technical_tutorials/search/searching_the_stac_catalog.html",
 "getting_started/about_maap.html",
 "technical_tutorials/visualization/visualize_lonboard.html",
 "science/GEDI/GEDI_L2A.html",
 "science/ATL08/ATL08.html",
 "technical_tutorials/working_with_r/access_aws_maap.html",
 "science/HLS/HLSL30.html",
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await b.new_context(viewport={"width":1400,"height":1000})
        report = {}
        for pg in PAGES:
            page = await ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            url = f"{BASE}/{pg}"
            try:
                await page.goto(url, wait_until="networkidle", timeout=90000)
            except Exception as e:
                errs.append(f"goto: {e}")
            await page.wait_for_timeout(2500)
            name = pg.replace('/','__').replace('.html','')
            await page.screenshot(path=f"{OUT}/{name}.png", full_page=True)
            info = await page.evaluate("""() => ({
                title: document.title,
                iframes: document.querySelectorAll('iframe').length,
                leaflet: document.querySelectorAll('.leaflet-container').length,
                leafletTiles: document.querySelectorAll('.leaflet-tile-loaded').length,
                htmlwidgets: document.querySelectorAll('.html-widget, [id^=htmlwidget]').length,
                imgs: document.querySelectorAll('img').length,
                brokenImgs: [...document.querySelectorAll('img')].filter(i=>i.complete && i.naturalWidth===0).length,
                outputs: document.querySelectorAll('.nboutput, .output, .jp-OutputArea').length,
                tables: document.querySelectorAll('table').length,
                xarray: document.querySelectorAll('.xr-wrap').length,
                sup: document.querySelectorAll('sup').length,
                h1: document.querySelector('h1') ? document.querySelector('h1').innerText : null,
                textLen: document.body.innerText.length,
            })""")
            info["errors"] = errs[:15]
            report[pg] = info
            await page.close()
        await b.close()
        json.dump(report, open(f"{OUT}/report.json","w"), indent=1)
        for k,v in report.items(): print(k, json.dumps({kk:vv for kk,vv in v.items() if kk!='errors'}), '| errs:', len(v['errors']))
asyncio.run(main())
