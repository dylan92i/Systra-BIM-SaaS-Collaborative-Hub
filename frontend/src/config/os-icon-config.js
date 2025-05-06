// icons.js
export function fileIcon(file) {
    if (file.is_dir) return "📁";
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext === "ifc") return "🏗️";
    if (["dwg"].includes(ext)) return "📐";
    if (["xlsx", "xls", "csv"].includes(ext)) return "📊";
    if (["pdf"].includes(ext)) return "📕";
    if (["doc", "docx"].includes(ext)) return "📝";
    if (["jpg", "jpeg", "png", "gif", "bmp", "svg"].includes(ext)) return "🖼️";
    if (["zip", "rar", "7z"].includes(ext)) return "🗜️";
    if (["js", "ts", "py", "php", "cpp", "c", "cs", "java", "json"].includes(ext)) return "💻";
    if (["txt", "md"].includes(ext)) return "📄";
    return "📄";
  }