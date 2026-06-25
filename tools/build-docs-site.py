# build-docs-site.py — docs/*.md 학습자료를 자체완결형 정적 HTML로 변환 (GitHub Pages 배포용)
#   출력(레포 root): roadmap.html, lab-setup.html, project-fifo.html, goals.html
#   - 의존성: python-markdown만. CDN/JS 0 → 오프라인·어디서나 동작.
#   - 내부 앵커는 GitHub 호환 slug, 문서 간 .md 링크는 .html로 치환.
import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import markdown
from pathlib import Path

ROOT = Path(r"C:\Workspace\semiconductor\semiconductor-verification-masterclass")

# (소스 md, 출력 html, 페이지 제목)
DOCS = [
    ("docs/학습-로드맵.md",        "roadmap.html",     "검증 엔지니어 학습 로드맵"),
    ("docs/실습환경-셋업.md",      "lab-setup.html",   "실습 환경 셋업"),
    ("docs/미니프로젝트-01-FIFO.md","project-fifo.html","미니프로젝트 ① 동기 FIFO"),
    ("docs/원본-학습목표.md",      "goals.html",       "원본 학습 목표"),
]
# 문서 간 링크(.md) → .html 치환표
LINKMAP = {
    "학습-로드맵.md": "roadmap.html",
    "실습환경-셋업.md": "lab-setup.html",
    "미니프로젝트-01-FIFO.md": "project-fifo.html",
    "원본-학습목표.md": "goals.html",
}

def gh_slug(value, separator="-"):
    """GitHub 헤딩 앵커와 동일 규칙(유니코드 유지, 구두점/이모지 제거)."""
    s = value.strip().lower()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)  # 한글/영숫자/_/공백/- 만 남김
    s = s.replace(" ", separator)
    return s

TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#0a0e16; --panel:#121a29; --panel2:#172236; --line:#22304a;
  --ink:#e8eef7; --muted:#b7c2d4; --dim:#8493ab;
  --accent:#38e1c6; --accent2:#5b9cff; --warn:#ffce6b; --good:#5ee6a0; --danger:#ff7a85;
  --code:#0b1220;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Segoe UI',system-ui,sans-serif;
  line-height:1.7;-webkit-text-size-adjust:100%}
.topbar{position:sticky;top:0;z-index:20;background:rgba(10,14,22,.82);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);padding:11px 18px;display:flex;gap:12px;align-items:center;font-size:14px}
.topbar a{color:var(--dim);text-decoration:none;border:1px solid var(--line);background:var(--panel);
  padding:6px 12px;border-radius:9px;white-space:nowrap}
.topbar a:hover{color:var(--ink);border-color:var(--accent)}
.topbar .t{color:var(--muted);font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.wrap{max-width:880px;margin:0 auto;padding:30px 20px 100px}
h1,h2,h3,h4{line-height:1.25;font-weight:800;letter-spacing:-.01em}
h1{font-size:clamp(26px,5vw,38px);margin:.2em 0 .5em}
h2{font-size:clamp(20px,3.5vw,27px);margin:1.7em 0 .6em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
h3{font-size:clamp(17px,2.6vw,20px);margin:1.5em 0 .5em;color:#dfe8f5}
h4{font-size:16px;margin:1.2em 0 .4em;color:var(--muted)}
p{margin:.7em 0}
a{color:var(--accent2)}
a:hover{color:var(--accent)}
strong{color:#fff}
em{color:var(--good);font-style:normal}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
code{font-family:'JetBrains Mono','Cascadia Code','D2Coding',Consolas,monospace;
  background:var(--panel2);color:var(--accent);padding:2px 6px;border-radius:5px;font-size:.88em}
pre{background:var(--code);border:1px solid var(--line);border-radius:12px;padding:15px 17px;overflow:auto}
pre code{background:none;color:#cfe0f5;padding:0;font-size:13.5px;line-height:1.6}
blockquote{margin:1.1em 0;padding:12px 16px;border-left:3px solid var(--accent);
  background:linear-gradient(180deg,rgba(56,225,198,.07),transparent);border-radius:0 10px 10px 0;color:var(--muted)}
blockquote p{margin:.35em 0}
ul,ol{padding-left:1.35em;margin:.6em 0}
li{margin:.32em 0}
li::marker{color:var(--accent)}
table{width:100%;border-collapse:collapse;margin:1.1em 0;font-size:14.5px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
th{background:var(--panel2);color:var(--accent);font-weight:700;white-space:nowrap}
tr:nth-child(even) td{background:rgba(255,255,255,.018)}
.toc{margin:1.4em 0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:6px 18px}
.toc>summary{cursor:pointer;font-weight:700;color:var(--accent);padding:8px 0;list-style:none}
.toc>summary::before{content:"▸ ";color:var(--dim)}
.toc[open]>summary::before{content:"▾ "}
.toc ul{font-size:14px}
.toc a{color:var(--muted);text-decoration:none}
.toc a:hover{color:var(--accent)}
.footer{max-width:880px;margin:0 auto;padding:24px 20px 60px;color:var(--dim);font-size:13px;border-top:1px solid var(--line)}
@media(max-width:560px){ table{font-size:13px} th,td{padding:7px 9px} .wrap{padding:22px 14px 80px} }
</style>
</head>
<body>
<div class="topbar">
  <a href="index.html">← 강의 홈</a>
  <span class="t">__TITLE__</span>
</div>
<div class="wrap">
__TOC__
__CONTENT__
</div>
<div class="footer">반도체 검증 마스터클래스 · 학습 자료 · 이 페이지는 <code>docs/*.md</code>에서 자동 생성됩니다.</div>
</body>
</html>
"""

def convert(md_text):
    # 체크박스
    md_text = re.sub(r"(?m)^(\s*)-\s\[ \]\s", r"\1- ☐ ", md_text)
    md_text = re.sub(r"(?m)^(\s*)-\s\[[xX]\]\s", r"\1- ☑ ", md_text)
    # 문서 간 .md 링크 → .html
    for mdname, html in LINKMAP.items():
        md_text = md_text.replace("(" + mdname + ")", "(" + html + ")")
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"],
        extension_configs={"toc": {"slugify": gh_slug, "permalink": False}},
    )
    body = md.convert(md_text)
    toc = md.toc  # <div class="toc">...<ul>...
    return body, toc

def main():
    for src, out, title in DOCS:
        md_text = (ROOT / src).read_text(encoding="utf-8")
        body, toc = convert(md_text)
        toc_html = ""
        # toc(md.toc)는 <div class="toc"><ul>..</ul></div> 형태 → details로 감싸 접이식
        m = re.search(r"<ul.*</ul>", toc, re.S)
        if m and m.group(0).strip() and "<li" in m.group(0):
            toc_html = '<details class="toc" open><summary>목차</summary>' + m.group(0) + "</details>"
        page = (TEMPLATE
                .replace("__TITLE__", title)
                .replace("__TOC__", toc_html)
                .replace("__CONTENT__", body))
        (ROOT / out).write_text(page, encoding="utf-8")
        print(f"  OK  {src}  ->  {out}  ({len(page)//1024} KB)")

if __name__ == "__main__":
    main()
