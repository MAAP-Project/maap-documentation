import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await b.new_context(viewport={"width":1400,"height":1000})
        page = await ctx.new_page()
        await page.goto(sys.argv[1], wait_until="networkidle", timeout=90000)
        await page.wait_for_timeout(4000)
        r = await page.evaluate("""() => {
          const out = {leaflet: [], widgets: [], iframes: []};
          document.querySelectorAll('.leaflet-container').forEach(e => { const b=e.getBoundingClientRect(); out.leaflet.push([Math.round(b.width), Math.round(b.height)]); });
          document.querySelectorAll('.html-widget').forEach(e => { const b=e.getBoundingClientRect(); out.widgets.push([Math.round(b.width), Math.round(b.height), e.getAttribute('style')]); });
          document.querySelectorAll('iframe').forEach(e => { const b=e.getBoundingClientRect(); out.iframes.push([Math.round(b.width), Math.round(b.height), e.getAttribute('style'), e.className]); });
          const main = document.querySelector('main, .document, [role=main]'); const mb = main ? main.getBoundingClientRect() : null;
          out.contentWidth = mb ? Math.round(mb.width) : null;
          return out; }""")
        print(json.dumps(r, indent=1))
        await b.close()
asyncio.run(main())
