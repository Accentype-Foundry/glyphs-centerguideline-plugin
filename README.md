# Enhanced Center Guideline

A **Glyphs 3** plugin to quickly generate centered guidelines between selected objects. Works with node-to-node, node-to-guide, and guide-to-guide selections.

![Enhanced Center Guideline Screenshot](assets/images/centerguideline.png)

---

## Installation

Install via **Plugin Manager** or manually by dragging `centerguideline.glyphsPlugin` to the Glyphs 3 Plugins folder.  
Alternatively, simply download `centerguideline.glyphsPlugin` and double-click it to install.

> **Note:** Please **restart Glyphs** after installation to activate the plugin.

---

## How to find it?

Once installed and Glyphs is restarted, you’ll find the tool here:

**Edit → Enhanced Center Guideline**

---

## Usage

1. Select at least 2 nodes, 2 guides, or one of each. Works with 4 nodes as well.
2. Go to **Edit → Enhanced Center Guideline** or use the shortcut:  
   **`Cmd + Opt + Ctrl + G`**
3. Select the desired orientation from the popup dialog:  
   * **Horizontal / Vertical**  
   * **Diagonal (Perpendicular)** – Useful for slanted stems.  
   * **Diagonal (Between Lines)** – Averages the angle of selected guides.

---

## Features

* **Localized** – Supports English, Hungarian, German, French, Spanish, Portuguese, and Chinese.  
* **Context-Aware** – Calculates midpoints and angles based on your selection.  
* **Smart Diagonals** – Creates diagonal guidelines and can calculate perpendicular diagonals based on your selection for precise positioning.

---

## Requirements

* **Glyphs 3.2** or later (supports multiple principal classes).  
* **Python** must be installed and active in Glyphs Preferences.

---

## Contributing

Suggestions and bug reports are welcome! If the plugin crashes, check **Window → Macro Panel** for error logs and include them in your issue report.

---

## License

MIT License
