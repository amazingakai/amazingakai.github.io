import json
import os
import re
import sys
import urllib.request
from urllib.error import URLError

BASE_URL = "https://amazingakai.github.io"


def parse_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract block between +++ (TOML) or --- (YAML)
    match = re.search(r"^(?:\+\+\+|---)\n(.*?)\n(?:\+\+\+|---)", content, re.DOTALL)
    if not match:
        return {}

    fm_text = match.group(1)

    def extract_field(field_name):
        # Matches field = "value", field = 'value', field: "value", etc.
        m = re.search(rf'^{field_name}\s*[:=]\s*[\'"](.*?)[\'"]', fm_text, re.MULTILINE)
        return m.group(1) if m else None

    def extract_tags():
        m = re.search(r'^tags\s*[:=]\s*\[(.*?)\]', fm_text, re.MULTILINE)
        if not m:
            return []
        # Find all strings inside single or double quotes
        return re.findall(r'[\'"](.*?)[\'"]', m.group(1))

    return {
        "title": extract_field("title"),
        "summary": extract_field("summary"),
        "banner": extract_field("banner"),
        "tags": extract_tags(),
    }


def main():
    api_key = os.environ.get("BUTTONDOWN_API_KEY")

    if not api_key:
        print("❌ Error: BUTTONDOWN_API_KEY is not set.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("❌ Error: You must provide a path to a markdown file.")
        print("Usage: python send_newsletter.py content/posts/my-post.md")
        sys.exit(1)

    post_path = sys.argv[1]

    if not os.path.exists(post_path):
        print(f"❌ Error: Post path '{post_path}' does not exist.")
        sys.exit(1)

    print(f"📄 Parsing post: {post_path}")
    fm = parse_frontmatter(post_path)

    title = fm.get("title", "New Blog Post")
    summary = fm.get("summary", "")
    banner = fm.get("banner", "")
    tags = fm.get("tags", [])

    # Format tags into hashtags (remove spaces inside tags)
    hashtags = " ".join([f"[#{tag.replace(' ', '')}]({BASE_URL}/tags/{tag.lower().replace(' ', '-')}/)" for tag in tags])

    # Generate the URL from the file path
    slug = os.path.basename(post_path).replace(".md", "")
    post_url = f"{BASE_URL}/posts/{slug}/"

    # Construct the Markdown Body
    markdown_lines = [f"# {title}\n"]

    if banner:
        banner_url = f"{BASE_URL}{banner}" if banner.startswith("/") else banner
        markdown_lines.append(f"![Banner Image]({banner_url})\n")

    markdown_lines.append("Hi there! 👋 I just published a new article on my blog.\n")

    if summary:
        markdown_lines.append(f"> *{summary}*\n")
    else:
        markdown_lines.append("Dive in to read the full technical breakdown and details.\n")

    if hashtags:
        markdown_lines.append(f"{hashtags}\n")

    markdown_lines.append("---\n")
    markdown_lines.append(f"**[📖 Click here to read the full post!]({post_url})**")

    body = "\n".join(markdown_lines)

    # Send to Buttondown API
    data = {"subject": f"New Post: {title}", "body": body, "status": "draft"}

    req = urllib.request.Request(
        "https://api.buttondown.email/v1/emails", data=json.dumps(data).encode("utf-8")
    )
    req.add_header("Authorization", f"Token {api_key}")
    req.add_header("Content-Type", "application/json")

    print("🚀 Sending to Buttondown...")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print("✅ Success! Draft created.")
            print("Draft ID:", res.get("id"))
    except URLError as e:
        print("❌ Failed to create email.")
        if hasattr(e, "read"):
            print("Error:", e.read().decode("utf-8"))
        else:
            print("Reason:", e.reason)
        sys.exit(1)


if __name__ == "__main__":
    main()
