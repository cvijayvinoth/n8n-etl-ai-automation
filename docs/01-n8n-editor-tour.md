# n8n Editor Tour: Complete Workspace Navigation

The n8n editor is a node-based visual workflow automation workspace designed for technical teams to build, test, monitor, and deploy complex backend logic.

---

## 1. Canvas and Workspace Architecture

The n8n workspace is divided into five core sections:

```text
+-------------------------------------------------------------------------------+
| Top Bar: [Workflow Title] [Tags] [Status: Active/Inactive] [Share] [Save]     |
+-------------------------------------------------------------------------------+
| Left Rail:       |                     CANVAS VIEW                           |
| - Workflows      |                                                            |
| - Credentials    |    [Trigger Node] ---> [Action Node] ---> [Output Node]    |
| - Executions     |                                                            |
| - Variables      |                                                            |
| - Settings       |                                                            |
+------------------+------------------------------------------------------------+
| Bottom Toolbar:  [Zoom In/Out] [Fit to Screen] [Execution History] [Test Step]|
+-------------------------------------------------------------------------------+
```

### Key UI Components
1. **Top Navigation Bar**:
   - **Workflow Status Toggle**: Switches between `Active` (production webhook/cron listening) and `Inactive`.
   - **Save & Version Control**: Saves manual checkpoints and tracks version history.
   - **Execution Settings**: Lets you configure error handling, timeouts, retry counts, and binary data modes.
2. **Infinite Canvas**:
   - Pan by dragging the background or holding `Space + Left Click`.
   - Zoom using the mouse scroll wheel or canvas buttons (`+`, `-`, `Reset`).
3. **Node Configuration Panel**:
   - Double-clicking any node opens the node inspection modal with separate tabs for **Parameters**, **Input Data**, and **Output Data**.
4. **Bottom Execution Bar**:
   - **Test step**: Triggers execution from a specific node using cached data.
   - **Test workflow**: Runs the entire workflow end-to-end in debug mode.

---

## 2. Inspecting Data Streams: Input vs. Output

n8n passes data between nodes as an **array of JSON objects** (accompanied by an optional binary payload):

```text
Input Item 0: { "json": { "id": 1, "name": "Deepa" } }
Input Item 1: { "json": { "id": 2, "name": "Kavitha" } }
```

Within the node modal, you can switch between three data views:
- **Schema / Table View**: Displays records in a clean tabular grid with column types.
- **JSON View**: Displays raw nested JSON objects.
- **Binary View**: Displays binary metadata (MIME type, file size, download link) when handling files (CSVs, images, PDFs).

---

## 3. Pin Data (Testing Without Re-Running Triggers)

When building complex workflows with external triggers (e.g., forms, webhooks, third-party APIs), you don't need to trigger the real event every time:
1. Run the trigger node once.
2. Click the **Pin Data** icon (📌) on the output pane.
3. The data is saved in editor state, allowing you to test downstream transformation and logic nodes repeatedly without regenerating real-world events.

---

## 4. Essential Keyboard Shortcuts

| Shortcut (Mac) | Shortcut (Windows/Linux) | Action |
| :--- | :--- | :--- |
| `Cmd + S` | `Ctrl + S` | Save workflow |
| `Tab` | `Tab` | Open Node Selection Drawer |
| `Delete` / `Backspace` | `Del` / `Backspace` | Delete selected node or connection |
| `Cmd + D` | `Ctrl + D` | Duplicate selected node |
| `Space + Drag` | `Space + Drag` | Pan canvas |
| `Cmd + Z` / `Cmd + Shift + Z` | `Ctrl + Z` / `Ctrl + Y` | Undo / Redo canvas changes |
