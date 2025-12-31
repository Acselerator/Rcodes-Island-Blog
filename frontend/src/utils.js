export const stripHtml = (html) => {
  // 预处理：将块级元素结束标签替换为换行符，保留结构
  let processed = html
    .replace(/<\/p>/gi, '\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/li>/gi, '\n');
    
  const tmp = document.createElement("DIV")
  tmp.innerHTML = processed
  return (tmp.textContent || tmp.innerText || "").trim()
}
