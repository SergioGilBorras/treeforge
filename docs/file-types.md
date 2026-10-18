# File types and default icons

TreeForge selects Unicode file-type icons for native SVG, TXT and Mermaid output. The icon is chosen from the filename extension, with a category or generic-file fallback.

| File type | Extensions | Default icon |
| --- | --- | --- |
| Word processing | doc, docx, odt | 📘 |
| Spreadsheets | xls, xlsx, xlsm, ods | 📗 |
| Presentations | ppt, pptx, odp | 📙 |
| JSON and XML | json, jsonl, xml | 🧩 |
| YAML | yaml, yml | ⚙️ |
| Plain text | txt | 📃 |
| Markdown and reStructuredText | md, rst | 📝 |
| PDF | pdf | 📕 |
| Archives | zip, tar, gz, 7z, rar | 🗜️ |
| Images | jpg, jpeg, png, svg, gif, webp, bmp | 🖼️ |
| Python | py | 🐍 |
| Web and code | html, css, js, ts, sql | 🌐 / 🎨 / 🟨 / 🔷 / 🗄️ |
| Audio | mp3, wav, flac | 🎵 |
| Video | mp4, mov, mkv | 🎬 |
| Other files | unrecognized extensions | 📄 |

Some less common extensions use their category's icon rather than an extension-specific symbol. Grouped file nodes display the icon for their grouping category, which can differ from the icon of an individual file.

To use custom SVG icons in native diagrams, provide `--icons-dir` and see the [icon guide](icons.md). Icon colors can be configured independently with `TreeConfig.colors`.
