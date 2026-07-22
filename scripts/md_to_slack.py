#!/usr/bin/env python3
"""GitHub 마크다운 파일을 슬랙 mrkdwn 텍스트로 변환한다.

사용법:
    python scripts/md_to_slack.py 기술동향/AI-에이전트/2026-07-21-하네스-엔지니어링.md
    python scripts/md_to_slack.py <파일.md> --repo-url https://github.com/21-Arbiter/Tech_Storage --out out.txt

표와 mermaid 다이어그램은 슬랙 메시지에 그대로 렌더링할 수 없으므로,
표는 불릿 리스트로 변환하고 다이어그램은 원본 링크 안내로 대체한다.
"""
import argparse
import io
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BOLD_TOKEN = "\x00BOLD\x00"


def strip_mermaid(text: str) -> str:
    def repl(m) -> str:
        return "\n_(다이어그램은 원본 링크에서 확인해 주세요)_\n"

    return re.sub(r"```mermaid.*?```", repl, text, flags=re.DOTALL)


def convert_code_fences(text: str) -> str:
    # mermaid 이외의 코드 블록은 슬랙도 ``` 그대로 지원하므로 유지
    return text


def convert_tables(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _is_table_row(line) and i + 1 < len(lines) and _is_table_sep(lines[i + 1]):
            header = _split_row(line)
            i += 2
            rows = []
            while i < len(lines) and _is_table_row(lines[i]):
                rows.append(_split_row(lines[i]))
                i += 1
            out.append("")
            n = min(len(header), max((len(r) for r in rows), default=0))
            for row in rows:
                lead_text = re.sub(r"\*\*(.*?)\*\*", r"\1", row[0]).strip() if row else ""
                lead = f"{BOLD_TOKEN}{lead_text}{BOLD_TOKEN}" if lead_text else ""
                rest = [row[j] for j in range(1, n) if j < len(row) and row[j].strip()]
                line_out = "• " + lead
                if rest:
                    line_out += " → " + " → ".join(rest)
                out.append(line_out)
            out.append("")
        else:
            out.append(line)
            i += 1
    return "\n".join(out)


def _is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def _is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line))


def _split_row(line: str) -> list:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def convert_headers(text: str) -> str:
    def repl(m) -> str:
        title = m.group(2).strip()
        return f"\n{BOLD_TOKEN}{title}{BOLD_TOKEN}\n"

    return re.sub(r"^(#{1,6})\s+(.*)$", repl, text, flags=re.MULTILINE)


def convert_links(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r"<\2|\1>", text)
    # 저장소 내부 상대경로 링크는 슬랙에서 못 여니 텍스트만 남긴다
    text = re.sub(r"\[([^\]]+)\]\((?!https?://)[^\)]+\)", r"\1", text)
    return text


def convert_bold_italic(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: BOLD_TOKEN + m.group(1) + BOLD_TOKEN, text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"_\1_", text)  # 밑줄 이탤릭은 슬랙과 동일, 그대로 둠
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"_\1_", text)  # 남은 단일 별표(이탤릭)는 밑줄로
    text = text.replace(BOLD_TOKEN, "*")
    return text


def convert_bullets(text: str) -> str:
    return re.sub(r"^(\s*)-\s+", r"\1• ", text, flags=re.MULTILINE)


def strip_hr(text: str) -> str:
    return re.sub(r"^---+$", "", text, flags=re.MULTILINE)


def convert(text: str) -> str:
    text = strip_mermaid(text)
    text = convert_tables(text)
    text = convert_headers(text)
    text = convert_links(text)
    text = convert_bold_italic(text)  # 원본 **/* 변환 + 위에서 심어둔 BOLD_TOKEN을 최종적으로 *로 치환
    text = convert_bullets(text)
    text = strip_hr(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("md_file", type=Path, help="변환할 마크다운 파일 경로")
    parser.add_argument("--out", type=Path, default=None, help="결과를 저장할 파일 (기본: 표준출력)")
    args = parser.parse_args()

    text = args.md_file.read_text(encoding="utf-8")
    result = convert(text)

    if args.out:
        args.out.write_text(result, encoding="utf-8")
        print(f"저장 완료: {args.out}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
