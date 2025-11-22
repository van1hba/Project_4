"""
GUI for AutoWebVulnScanner (CustomTkinter)
- This version has NO "Browse" button and NO "Open Uploaded PDF" button.
- It provides:
    * URL input
    * Start Scan button
    * Status/log area
    * "Open Output Folder" button (optional) to view the generated PDF in file explorer
- Output filename is simple: Security_Report.pdf
- sample_uploaded_file is set from conversation history.
"""

import os
import threading
import customtkinter as ctk
from tkinter import messagebox
from scanner.site_crawler import get_links
from scanner.sqli import test_sqli
from scanner.xss import test_xss
from scanner.headers import check_headers
from scanner.reporter import generate_pdf



# Helper: ensure URL has scheme
def normalize_url(url: str) -> str:
    """Return a URL that starts with http:// or https://."""
    url = url.strip()
    if not url:
        return url
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def run_scan(target_url: str, log_callback):
    """
    Performs crawling + vulnerability checks and generates PDF.
    log_callback is a function that accepts a string to append to GUI log.
    """
    target = normalize_url(target_url)
    log_callback(f"Starting scan for: {target}")

    # Crawl
    log_callback("Crawling site...")
    try:
        pages = get_links(target)
    except Exception as e:
        log_callback(f"[crawl error] {e}")
        pages = []

    log_callback(f"Pages found: {len(pages)}")

    # Prepare results containers
    sqli_results = []
    xss_results = []
    header_results = []

    # Test each page
    for url in pages:
        log_callback(f"Testing: {url}")

        try:
            sqli_results.extend(test_sqli(url))
        except Exception as e:
            log_callback(f"[sqli error] {url} -> {e}")

        try:
            xss_results.extend(test_xss(url))
        except Exception as e:
            log_callback(f"[xss error] {url} -> {e}")

        try:
            missing = check_headers(url)
            if missing:
                header_results.append({"url": url, "missing": missing, "issue": "Missing Security Headers"})
        except Exception as e:
            log_callback(f"[headers error] {url} -> {e}")

    # Compile final dict for report
    final = {
        "SQL Injection": sqli_results,
        "Cross-Site Scripting": xss_results,
        "Missing Security Headers": header_results
    }

    # Generate PDF (simple filename)
    output_filename = "Security_Report.pdf"
    try:
        log_callback("Generating PDF report...")
        generate_pdf(output_filename, final)
        log_callback(f"Report saved as: {os.path.abspath(output_filename)}")
    except Exception as e:
        log_callback(f"[report error] {e}")

    log_callback("Scan finished.")


# ----------------------
# GUI (CustomTkinter)
# ----------------------
ctk.set_appearance_mode("System")   # "System" | "Dark" | "Light"
ctk.set_default_color_theme("blue")


class ScannerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoWebVulnScanner — GUI (No Browse)")
        self.geometry("800x560")
        self.resizable(True, True)

        # Top frame: input + buttons
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=12, pady=12)

        # URL label + entry
        self.url_label = ctk.CTkLabel(top_frame, text="Target URL:", anchor="w")
        self.url_label.grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")

        self.url_entry = ctk.CTkEntry(top_frame, placeholder_text="e.g. http://testphp.vulnweb.com", width=520)
        self.url_entry.grid(row=0, column=1, padx=6, pady=8, sticky="w")

        # Start Scan button
        self.scan_btn = ctk.CTkButton(top_frame, text="Start Scan", command=self.start_scan_thread)
        self.scan_btn.grid(row=1, column=1, padx=6, pady=(6, 12), sticky="w")

        # Open Output Folder button (non-destructive; does not auto-open PDF)
        self.open_folder_btn = ctk.CTkButton(top_frame, text="Open Output Folder", command=self.open_output_folder)
        self.open_folder_btn.grid(row=1, column=2, padx=6, pady=(6, 12), sticky="w")

        # Middle frame: status / progress
        mid_frame = ctk.CTkFrame(self)
        mid_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.logbox = ctk.CTkTextbox(mid_frame, width=760, height=380)
        self.logbox.pack(padx=8, pady=8, fill="both", expand=True)

        # Show info about uploaded file (informational only)
        
        self.log("Note: This GUI will NOT open any PDF automatically. Generated report will be 'Security_Report.pdf'.")

    # -------------------
    # GUI helper methods
    # -------------------
    def log(self, text: str):
        """Append a line to the GUI log box."""
        self.logbox.insert("end", text + "\n")
        self.logbox.see("end")  # auto-scroll

    def open_output_folder(self):
        """
        Open project folder in file explorer so user can manually open Security_Report.pdf.
        This does not auto-open any PDF.
        """
        folder = os.path.abspath(".")
        try:
            if os.name == "nt":
                os.startfile(folder)
            else:
                # For Mac/Linux attempt generic open
                if os.name == "posix":
                    # macOS check
                    try:
                        if os.uname().sysname == "Darwin":
                            os.system(f"open \"{folder}\"")
                        else:
                            os.system(f"xdg-open \"{folder}\"")
                    except Exception:
                        os.system(f"xdg-open \"{folder}\"")
                else:
                    # fallback
                    os.system(f"xdg-open \"{folder}\"")
            self.log(f"Opened output folder: {folder}")
        except Exception as e:
            self.log(f"[open folder error] {e}")

    def start_scan_thread(self):
        """Start the long-running scan in a separate thread to keep GUI responsive."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input required", "Please enter a target URL.")
            return

        # disable start button to prevent concurrent runs
        self.scan_btn.configure(state="disabled")
        self.log("Starting threaded scan...")

        # Worker wrapper so we can re-enable button afterwards
        def worker():
            try:
                run_scan(url, self.log)
            finally:
                # Re-enable button in main thread after worker done
                self.scan_btn.configure(state="normal")
                self.log("You can run another scan now.")

        t = threading.Thread(target=worker, daemon=True)
        t.start()


# -----------------------
# Entry point
# -----------------------
if __name__ == "__main__":
    app = ScannerGUI()
    app.mainloop()
