# File types and default icons

TreeForge recognizes files by extension and assigns expressive Unicode icons when rendering native SVG, TXT trees or Mermaid node labels.

| Family | Extensions | Icon |
| --- | --- | --- |
| Microsoft Word and OpenDocument | doc, docx, odt | 📘 |
| Excel and spreadsheets | xls, xlsx, xlsm, ods | 📗 |
| PowerPoint and presentations | ppt, pptx, odp | 📙 |
| Structured data | json, jsonl, xml, yaml, yml | 🧩 |
| Plain text | txt | 📃 |
| Markdown | md, rst | 📝 |
| PDF | pdf | 📕 |
| Compressed archives | zip, tar, gz, 7z, rar | 🗜️ |
| Images | jpg, jpeg, png, svg, gif, webp, bmp | 🖼️ |
| Python | py | 🐍 |
| Web and code | html, css, js, ts, sql | 🌐 / 🎨 / 🟨 / 🔷 / 🗄️ |
| Audio | mp3, wav | 🎵 |
| Video | mp4, mov | 🎬 |
| Unknown extensions | other | 📄 |

Groups of multiple files use their category icon. For custom native SVG icons, add `xlsx.svg`, `json.svg`, `zip.svg`, etc. to an icon directory and pass `--icons-dir`. Lookup proceeds by extension, category, then general file/folder fallback.

Colors can be configured independently of icons by extension or category using `TreeConfig.colors`.
