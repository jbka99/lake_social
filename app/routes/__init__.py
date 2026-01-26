from flask import Blueprint
import re
from markupsafe import Markup, escape

bp = Blueprint('routes', __name__)

_url_re = re.compile(r'(?P<url>https?://[^\s]+)', re.IGNORECASE)

def linify(text: str):
    if not text:
        return ''
    s = escape(text)

    def repl(m):
        url = m.group('url')
        href = url if url.lower().startswith(('http://', 'https://')) else f'https://{url}'
        return Markup(f'<a href="{href}" target="_blank" rel="nofollow noopener noreferrer">{url}</a>')

    s = _url_re.sub(repl, s)
    s = s.replace('\n', Markup('<br>'))
    return Markup(s)

@bp.app_template_filter('linkify')
def linkify_filter(text: str):
    """Convert URLs in text to clickable links"""
    return linify(text)

@bp.app_template_filter('mentions_to_links')
def mentions_to_links_filter(text):
    """Convert @username mentions to clickable links, also processes URLs"""
    if not text:
        return ''
    
    from markupsafe import escape, Markup
    
    # First, escape the text
    escaped_text = escape(text)
    
    # Pattern: @username (alphanumeric and underscore, 1-64 chars)
    mention_pattern = r'@([a-zA-Z0-9_]{1,64})'
    
    # Pattern: URLs (http:// or https://)
    url_pattern = r'(https?://[^\s<>"\'@]+)'
    
    # Combine patterns: mentions first, then URLs
    # We'll process mentions first, then URLs in the remaining text
    parts = []
    last_end = 0
    
    # Helper function to process URLs in text
    def process_urls_in_text(text_part):
        """Process URLs in a text segment"""
        def url_repl(m):
            url = m.group('url')
            return Markup(f'<a href="{url}" target="_blank" rel="nofollow noopener noreferrer">{escape(url)}</a>')
        escaped = escape(text_part)
        return _url_re.sub(url_repl, escaped)
    
    # Process mentions first
    for match in re.finditer(mention_pattern, text):
        # Add text before mention (process URLs)
        if match.start() > last_end:
            before_text = text[last_end:match.start()]
            parts.append(process_urls_in_text(before_text))
        
        # Add mention as link
        username = match.group(1)
        url = f'/user/{username}'
        parts.append(Markup(f'<a href="{url}" class="mention">@{escape(username)}</a>'))
        
        last_end = match.end()
    
    # Add remaining text (process URLs)
    if last_end < len(text):
        remaining_text = text[last_end:]
        parts.append(process_urls_in_text(remaining_text))
    
    # Convert newlines to <br>
    result = Markup(''.join(parts))
    result = result.replace('\n', Markup('<br>'))
    
    return result

# Важно: импорты в конце, чтобы bp уже существовал
from app.routes import auth, posts, users, admin  # noqa: E402,F401