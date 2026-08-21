"""
전체 사이트 빌드: 연봉 실수령액 계산기 + 성과급 계산기 + sitemap.xml
사이트에 계산기를 새로 추가할 때마다 이 파일에 generate 모듈을 import해서 main()을 호출하면 됨.
"""
import os
import generate
import generate_bonus

OUTPUT_DIR = generate.OUTPUT_DIR
BASE_URL = generate.BASE_URL


def build_sitemap():
    urls = [
        f"{BASE_URL}/{fname}"
        for fname in sorted(os.listdir(OUTPUT_DIR))
        if fname.endswith(".html")
    ]
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>"""
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"sitemap.xml 갱신 완료 ({len(urls)}개 URL)")


def main():
    generate.main()
    generate_bonus.main()
    build_sitemap()


if __name__ == "__main__":
    main()
