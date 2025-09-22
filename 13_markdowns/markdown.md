# Markdown Cheatsheet

## 📖 What is Markdown?

Markdown is a lightweight markup language for creating formatted text using a plain-text editor. It’s widely used for documentation, blog posts, and notes because of its simplicity and readability. It converts simple symbols into rich text formatting.

---

## 1. Headings

Headings create titles and section headers in your document. There are six levels of headings, from largest to smallest.

### Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

**Best Practice:** Always include a space between the `#` sign and the heading text.

---

## 2. Paragraphs and Line Breaks

- **Paragraphs:** Use a blank line to separate paragraphs.

```markdown
This is the first paragraph.

This is the second paragraph.
```

- **Line Breaks:** End a line with two or more spaces or use the `<br>` tag.

```markdown
This is the first line.  
This is the second line.
```

---

## 3. Emphasis (Bold & Italic)

- *Italic:* `*italic*` or `_italic_`
- **Bold:** `**bold**` or `__bold__`
- ***Bold + Italic:*** `***bold italic***`

```markdown
*italic text*
**bold text**
***bold and italic***
```

---

## 4. Blockquotes

Blockquotes highlight quoted text.

```markdown
> This is a blockquote.
>
> > Nested blockquote
```

---

## 5. Lists

- **Ordered List:**
```markdown
1. First item
2. Second item
3. Third item
```

- **Unordered List:**
```markdown
* Item one
* Item two
```

- **Nested List:**
```markdown
1. Parent
    * Child
```

---

## 6. Code

- **Inline Code:**
```markdown
The `ls -l` command lists files.
```

- **Code Block:**
\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

---

## 7. Links

- **Basic Link:** `[Google](https://www.google.com)`
- **Link with Title:** `[Google](https://www.google.com "Go to Google")`

---

## 8. Images

- **Basic Image:**
```markdown
![Alt Text](https://example.com/image.jpg "Optional Title")
```

- **Clickable Image:**
```markdown
[![Alt Text](https://example.com/image.jpg)](https://example.com)
```

---

## 9. Horizontal Rules

```markdown
---
***
___
```

---

## 10. Escaping Characters

Use a backslash (`\`) to show Markdown symbols as plain text.

```markdown
\*This text is not italic*.
\_This text is not italic_.
```

---

✅ With this cheatsheet, you can quickly write well-formatted Markdown for your notes, blogs, or documentation.
