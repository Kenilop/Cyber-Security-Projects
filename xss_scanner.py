import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

class XSSScanner:
    def __init__(self, master):
        self.master = master
        master.title("XSS Scanner")

        self.label = tk.Label(master, text="Enter HTML to scan for XSS or a URL:")
        self.label.pack()

        self.text_area = scrolledtext.ScrolledText(master, width=80, height=10)
        self.text_area.pack()

        self.url_label = tk.Label(master, text="Enter URL to scan:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=80)
        self.url_entry.pack()

        self.fetch_button = tk.Button(master, text="Fetch HTML", command=self.fetch_html)
        self.fetch_button.pack()

        self.scan_button = tk.Button(master, text="Scan", command=self.scan_xss)
        self.scan_button.pack()

        self.result_label = tk.Label(master, text="Results:")
        self.result_label.pack()

        self.result_area = scrolledtext.ScrolledText(master, width=80, height=10)
        self.result_area.pack()

    def fetch_html(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, response.text)
            else:
                messagebox.showerror("Error", "Failed to fetch HTML. Status code: " + str(response.status_code))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def scan_xss(self):
        html_content = self.text_area.get("1.0", tk.END)
        results = self.check_for_xss(html_content)
        self.result_area.delete("1.0", tk.END)
        self.result_area.insert(tk.END, results)

    def check_for_xss(self, html):
        xss_patterns = [
            "<script.*?>.*?</script>",
            "javascript:",
            "onerror=",
            "onload=",
            "onclick=",
            "onmouseover=",
            "onfocus=",
            "onblur=",
            "onchange=",
            "oninput=",
            "onkeydown=",
            "onkeyup=",
            "onkeypress=",
            "onmousedown=",
            "onmouseup=",
            "onmousemove=",
            "onmouseout=",
            "onmouseenter=",
            "onmouseleave="
        ]
        
        found_vulnerabilities = []
        for pattern in xss_patterns:
            if pattern in html:
                found_vulnerabilities.append(pattern)

        if found_vulnerabilities:
            return "Potential XSS vulnerabilities found:\n" + "\n".join(found_vulnerabilities)
        else:
            return "No XSS vulnerabilities found."

if __name__ == "__main__":
    root = tk.Tk()
    xss_scanner = XSSScanner(root)
    root.mainloop()
