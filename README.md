# discord.html
ratio to those who think html bad

# Usage

- Get python/pypy
- Install required packages
- Run via `python discord_html.py <html_file>`

# Schema

Tokens must be within meta tags

`<meta name="token" content="TOKEN_STRING">`

Commands must be within h1 tags, their caller would be the tag id

`<h1 id="command_name">command response</h1>`

Bot Presences have to be in `title` tags, they will cycle if there are more than one

# Testing

- For a quick test, clone this repo, install dependencies and run `python discord_html.py demo.html`
- Type `-ping` in chat to see if bot responds
