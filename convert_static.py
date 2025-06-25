import re


def convert_static_links(html_file_path, output_file_path):
    with open(html_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # تبدیل لینک‌های خام
    def replace_href(match):
        path = match.group(1)
        return f"href=\"{{% static '{path}' %}}\""

    def replace_src(match):
        path = match.group(1)
        return f"src=\"{{% static '{path}' %}}\""

    content = re.sub(r'href="([^"]+\.(css|js|html))"', replace_href, content)
    content = re.sub(
        r'src="([^"]+\.(js|css|png|jpg|jpeg|gif|svg|webp))"', replace_src, content
    )

    # تبدیل لینک‌های ناقص {% static ... %} که کوتیشن ندارند
    def fix_static_quotes(match):
        attr = match.group(1)
        path = match.group(2)
        return f"{attr}\"{{% static '{path}' %}}\""

    content = re.sub(
        r'(href=|src=)"\{\% static ([^\'"][^ \}]+) \%\}"', fix_static_quotes, content
    )

    # اضافه کردن load static اگر نبود
    if "{% load static %}" not in content:
        content = "{% load static %}\n" + content

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print("link has be changed ✅ ")


# استفاده
convert_static_links(
    "templates/Index/contact.html", "templates/Index/contact_converted.html"
)
convert_static_links(
    "templates/Index/about.html", "templates/Index/about_converted.html"
)
convert_static_links(
    "templates/Index/products.html", "templates/products_converted.html"
)
convert_static_links(
    "templates/Index/single-product.html",
    "templates/Index/single-product_converted.html",
)
