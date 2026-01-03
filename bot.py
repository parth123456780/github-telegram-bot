"""
====================================================
🤖 GitHub Ultimate Telegram Bot (v3.0)
----------------------------------------------------
👨‍💻 Developer : SANJIT CHAURASIYA
📱 Telegram  : @SANJIT_CHAURASIYA
🛠️ Purpose  : Full-featured GitHub Management
✅ Features  : 25+ Commands + Smart Usage Help
====================================================
"""

import logging
import html
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from github import Github, GithubException

# =========================
# ⚙️ CONFIGURATION
# =========================
TELEGRAM_TOKEN = " Enter Here Your Bot Token"
GITHUB_TOKEN = None  # Optional: Add your GitHub Token for higher limits

# Initialize GitHub
g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# =========================
# 🛠️ UTILITY FUNCTIONS
# =========================
async def safe_reply(update: Update, msg: str):
    """Sends HTML messages safely."""
    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)

def escape(text):
    """Escapes HTML characters."""
    return html.escape(str(text)) if text else "N/A"

async def send_usage(update, command, args_format, example):
    """Sends the standard Usage/Example message."""
    msg = (
        f"⚠️ <b>Missing Arguments</b>\n\n"
        f"Usage: /{command} &lt;{args_format}&gt;\n"
        f"Example: <code>/{command} {example}</code>"
    )
    await safe_reply(update, msg)

def get_repo_arg(context):
    return context.args[0] if context.args else None

# =========================
# 📋 MAIN MENU
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "<b>🤖 GitHub Ultimate Bot - Command List</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>🔹 Core Features</b>\n"
        "🔍 /search query - Search Repos\n"
        "👤 /user username - User Profile\n"
        "📂 /repo owner/name - Repo Details\n"
        "🐞 /issues owner/name - Open Issues\n"
        "📄 /files owner/name - File Structure\n"
        "📈 /trending - Hottest Repos\n"
        "🏆 /contributors owner/name - Top Coders\n"
        "⬇️ /clone owner/name - Clone Command\n\n"
        "<b>🆕 Advanced Features</b>\n"
        "📊 /stats owner/name - Deep Statistics\n"
        " 🗣️ /languages owner/name - Language Breakdown\n"
        "📝 /commits owner/name - Recent Commits\n"
        " 🚀 /releases owner/name - Latest Releases\n"
        "📜 /license owner/name - License Info\n"
        " 🌿 /branches owner/name - Branch List\n"
        "🔀 /pulls owner/name - Open PRs\n"
        " 👁️ /watchers owner/name - Subscriber Count\n"
        "🍴 /forks owner/name - Fork List\n"
        " 📘 /readme owner/name - Readme Preview\n\n"
        "<b> ℹ️ Bot Info</b>\n"
        "⏳ /rate_limit - API Usage\n"
        "🏓 /ping - Health Check\n"
        "ℹ️ /about - Developer Info\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Developed by @SANJIT_CHAURASIYA</i>"
    )
    await safe_reply(update, msg)

# =========================
# 🔍 SEARCH & DISCOVERY
# =========================
async def search_repos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "search", "query", "machine learning")
    
    query = " ".join(context.args)
    try:
        results = g.search_repositories(query=query, sort="stars", order="desc")
        msg = f"<b>🔍 Search Results for '{escape(query)}'</b>\n\n"
        for repo in results[:5]:
            msg += f"⭐ <b>{repo.stargazers_count}</b> - <a href='{repo.html_url}'>{escape(repo.full_name)}</a>\n"
        await safe_reply(update, msg)
    except Exception as e: await safe_reply(update, f"❌ Error: {e}")

async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Trending doesn't need args, but we handle it safely
    try:
        date_since = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        results = g.search_repositories(query=f"created:>{date_since}", sort="stars", order="desc")
        msg = f"<b>🔥 Trending Repositories (Since {date_since})</b>\n\n"
        for repo in results[:5]:
            msg += f"🚀 <a href='{repo.html_url}'>{escape(repo.full_name)}</a>\n⭐ {repo.stargazers_count} stars | 🗣️ {escape(repo.language)}\n\n"
        await safe_reply(update, msg)
    except Exception as e: await safe_reply(update, f"❌ Error: {e}")

# =========================
# 👤 USER & REPO INFO
# =========================
async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "user", "username", "torvalds")
    
    try:
        user = g.get_user(context.args[0])
        msg = (
            f"<b>👤 Profile: {escape(user.login)}</b>\n"
            f"📛 Name: {escape(user.name)}\n"
            f"🏢 Company: {escape(user.company)}\n"
            f"📍 Location: {escape(user.location)}\n"
            f"👥 Followers: {user.followers} | Following: {user.following}\n"
            f"📦 Public Repos: {user.public_repos}\n"
            f"🔗 <a href='{user.html_url}'>View on GitHub</a>"
        )
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ User not found.")

async def get_repo_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "repo", "owner/repo", "tensorflow/tensorflow")
    
    try:
        repo = g.get_repo(context.args[0])
        msg = (
            f"<b>📂 {escape(repo.full_name)}</b>\n"
            f"📝 {escape(repo.description)}\n\n"
            f"⭐ Stars: {repo.stargazers_count}\n"
            f"🍴 Forks: {repo.forks_count}\n"
            f"👁️ Watchers: {repo.subscribers_count}\n"
            f"🐞 Issues: {repo.open_issues_count}\n"
            f"🗣️ Language: {repo.language}\n"
            f"🔗 <a href='{repo.html_url}'>Repository Link</a>"
        )
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Repository not found.")

# =========================
# 📂 CONTENT & FILES
# =========================
async def get_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "files", "owner/repo", "pytorch/pytorch")
    
    try:
        repo = g.get_repo(context.args[0])
        contents = sorted(repo.get_contents(""), key=lambda x: x.type)
        msg = f"<b>📄 File Structure for {escape(repo.name)}</b>\n\n"
        for i, c in enumerate(contents):
            if i > 15: 
                msg += "<i>...and more</i>"
                break
            icon = "📁" if c.type == "dir" else "📄"
            msg += f"{icon} <a href='{c.html_url}'>{escape(c.name)}</a>\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching files.")

# =========================
# 🐞 ISSUES & PRS
# =========================
async def get_issues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "issues", "owner/repo", "facebook/react")

    try:
        repo = g.get_repo(context.args[0])
        issues = repo.get_issues(state="open")
        msg = f"<b>🐞 Open Issues for {escape(repo.name)}</b>\n"
        for i, issue in enumerate(issues[:5], 1):
            msg += f"{i}. <a href='{issue.html_url}'>{escape(issue.title)}</a>\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ No open issues found.")

async def pulls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "pulls", "owner/repo", "django/django")

    try:
        repo = g.get_repo(context.args[0])
        prs = repo.get_pulls(state="open")
        msg = f"<b>🔀 Open Pull Requests</b>\n"
        for pr in prs[:5]:
            msg += f"- <a href='{pr.html_url}'>{escape(pr.title)}</a>\n"
        if not msg.strip() or "href" not in msg: msg = "✅ No open Pull Requests."
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching PRs.")

# =========================
# 📊 STATS & CONTRIBUTORS
# =========================
async def get_contributors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "contributors", "owner/repo", "opencv/opencv")

    try:
        repo = g.get_repo(context.args[0])
        users = repo.get_contributors()
        msg = f"<b>🏆 Top Contributors for {escape(repo.name)}</b>\n"
        for i, user in enumerate(users[:5], 1):
            msg += f"{i}. <b>{escape(user.login)}</b> - {user.contributions} commits\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching contributors.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "stats", "owner/repo", "python/cpython")

    try:
        repo = g.get_repo(context.args[0])
        msg = (
            f"<b>📊 Stats: {escape(repo.name)}</b>\n"
            f"📏 Size: {repo.size} KB\n"
            f"🕎 Network: {repo.network_count}\n"
            f"👀 Subscribers: {repo.subscribers_count}\n"
            f"📅 Updated: {repo.updated_at.strftime('%Y-%m-%d')}\n"
            f"🛡️ Branch: {repo.default_branch}"
        )
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching stats.")

# =========================
# 📝 ADVANCED COMMANDS
# =========================
async def languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "languages", "owner/repo", "flutter/flutter")

    try:
        repo = g.get_repo(context.args[0])
        langs = repo.get_languages()
        total = sum(langs.values())
        msg = f"<b>🗣️ Language Breakdown</b>\n"
        for l, b in langs.items():
            percent = (b / total) * 100
            msg += f"🔹 {l}: {percent:.1f}%\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching languages.")

async def commits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "commits", "owner/repo", "bitcoin/bitcoin")

    try:
        repo = g.get_repo(context.args[0])
        commits = repo.get_commits()
        msg = f"<b>📝 Recent Commits</b>\n"
        for c in commits[:5]:
            msg += f"▪️ <code>{c.sha[:7]}</code> - {escape(c.commit.message[:40])}...\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching commits.")

async def releases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "releases", "owner/repo", "microsoft/vscode")

    try:
        repo = g.get_repo(context.args[0])
        rels = repo.get_releases()
        msg = f"<b>🚀 Latest Releases</b>\n"
        for r in rels[:5]:
            msg += f"📦 <a href='{r.html_url}'>{escape(r.title or r.tag_name)}</a>\n"
        if "📦" not in msg: msg = "❌ No releases found."
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching releases.")

async def branches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "branches", "owner/repo", "pallets/flask")

    try:
        repo = g.get_repo(context.args[0])
        msg = f"<b>🌿 Branches</b>\n"
        for b in repo.get_branches()[:10]:
            msg += f"- {escape(b.name)}\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching branches.")

async def license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "license", "owner/repo", "mit-pdos/xv6-public")

    try:
        repo = g.get_repo(context.args[0])
        lic = repo.get_license()
        await safe_reply(update, f"<b>📜 License:</b> {escape(lic.license.name)}")
    except Exception: await safe_reply(update, "❌ No license file found.")

# =========================
# 🛠️ EXTRA TOOLS
# =========================
async def get_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "clone", "owner/repo", "torvalds/linux")

    try:
        repo = g.get_repo(context.args[0])
        msg = f"⬇️ <b>Clone Command:</b>\n\nClick to copy:\n<code>git clone {repo.clone_url}</code>"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Repo not found.")

async def get_watchers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "watchers", "owner/repo", "vuejs/vue")

    try:
        repo = g.get_repo(context.args[0])
        msg = f"<b>👁️ Watchers (Total: {repo.subscribers_count})</b>\n\n"
        for sub in repo.get_subscribers()[:5]:
             msg += f"- {escape(sub.login)}\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching watchers.")

async def get_forks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "forks", "owner/repo", "nodejs/node")

    try:
        repo = g.get_repo(context.args[0])
        msg = f"<b>🍴 Forks (Total: {repo.forks_count})</b>\nRecent:\n"
        for fork in repo.get_forks()[:5]:
            msg += f"- <a href='{fork.html_url}'>{escape(fork.full_name)}</a>\n"
        await safe_reply(update, msg)
    except Exception: await safe_reply(update, "❌ Error fetching forks.")

async def readme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await send_usage(update, "readme", "owner/repo", "axios/axios")

    try:
        repo = g.get_repo(context.args[0])
        content = repo.get_readme().decoded_content.decode()[:800]
        await safe_reply(update, f"<b>📘 README Preview:</b>\n\n{escape(content)}...")
    except Exception: await safe_reply(update, "❌ README not available.")

# =========================
# ℹ️ SYSTEM COMMANDS
# =========================
async def rate_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = g.get_rate_limit().core
    msg = f"<b>⏳ GitHub API Rate Limit</b>\nRemaining: {rate.remaining}/{rate.limit}\nResets at: {rate.reset.strftime('%H:%M:%S')} UTC"
    await safe_reply(update, msg)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, "🏓 <b>Pong!</b> Bot is online and healthy.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, "👨‍💻 <b>Developer:</b> SANJIT CHAURASIYA\n📱 <b>Telegram:</b> @SANJIT_CHAURASIYA")

# =========================
# 🚀 APP EXECUTION
# =========================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Handlers Mapping
    handlers = [
        ("start", start),
        ("search", search_repos),
        ("user", get_user),
        ("repo", get_repo_details),
        ("issues", get_issues),
        ("files", get_files), ("content", get_files),
        ("trending", trending),
        ("contributors", get_contributors),
        ("clone", get_clone),
        ("stats", stats),
        ("languages", languages),
        ("commits", commits),
        ("releases", releases),
        ("license", license),
        ("branches", branches),
        ("pulls", pulls),
        ("watchers", get_watchers),
        ("forks", get_forks),
        ("readme", readme),
        ("rate_limit", rate_limit),
        ("ping", ping),
        ("about", about)
    ]

    for cmd, func in handlers:
        app.add_handler(CommandHandler(cmd, func))

    print("✅ GitHub Ultimate Bot Running... | Developed by SANJIT CHAURASIYA")
    app.run_polling()
