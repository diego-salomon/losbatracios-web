# losbatracios.com

The website for *Los Batracios*, the feature I wrote, produced and directed. It won the Audience Award at the Mammoth Lakes Film Festival in 2025.

Live at [losbatracios.com](https://losbatracios.com), and in English at [losbatracios.com/en](https://losbatracios.com/en/).

I wanted a page that looks like the film, loads fast on a phone, and turns visitors into an audience I can write to again.

## What it does

`build.py` builds the whole site from one place: the Spanish version at `/`, the English one at `/en/`, the privacy pages, the sitemap and robots, the share images, the redirects and the Cloudflare Worker. Every page has its own title and description, Open Graph tags, a canonical URL, hreflang between the two languages, and `Movie` structured data with the cast and the awards. It's plain HTML with WebP images and no framework.

The Worker runs the mailing list. It checks each sign-up with Turnstile, adds the person to Buttondown tagged with their language, and sends a welcome email.

Every channel gets its own short link (`/ig`, `/tt`, `/qr`, `/prensa`...), posters included, so Umami shows where people come from without cookies or a cookie banner. `/resena` sends people leaving a screening straight to Letterboxd. The API keys only exist as Cloudflare environment variables, and the code went through a security review before launch.

## Run it

```bash
pip install pillow
python3 build.py              # writes the site to sitio/
npx wrangler pages deploy sitio --project-name <your-project>
```

`site/` holds a copy of what's live right now. Two things aren't in the repo: the Aeonik font, which is licensed, and the press kits. The build skips them with a warning, and the text falls back to a system font. For the mailing list, set `BUTTONDOWN_API_KEY` and `TURNSTILE_SECRET_KEY` in Cloudflare and change `UMAMI_ID`, `TURNSTILE_SITEKEY` and the links at the top of `build.py` to your own.

The code comments are in Spanish.
