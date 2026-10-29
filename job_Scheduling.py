import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import defaultdict, deque


class JobSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Scheduling System using Graphs")
        self.root.geometry("700x550")

        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.all_nodes = set()

        input_frame = tk.LabelFrame(
            root, text="Define Job Dependencies",
            padx=10, pady=10
        )
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(
            input_frame, text="Prerequisite Job (u):"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.u_entry = tk.Entry(input_frame, width=12)
        self.u_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            input_frame, text="Dependent Job (v):"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.v_entry = tk.Entry(input_frame, width=12)
        self.v_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(
            input_frame, text="Add Dependency",
            bg="green", fg="white",
            command=self.add_edge
        ).grid(row=0, column=4, padx=5, pady=5)

        action_frame = tk.Frame(root)
        action_frame.pack(fill="x", padx=15, pady=5)

        tk.Button(
            action_frame, text="Compute Job Schedule",
            bg="blue", fg="white",
            command=self.compute_schedule
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame, text="Reset Graph",
            bg="red", fg="white",
            command=self.reset_graph
        ).pack(side="left", padx=5)

        output_frame = tk.LabelFrame(
            root, text="Execution Schedule & Logs",
            padx=10, pady=10
        )
        output_frame.pack(
            fill="both", expand=True, padx=15, pady=10
        )

        self.output_area = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD,
            width=75, height=15
        )
        self.output_area.pack(fill="both", expand=True)

    def add_edge(self):
        u = self.u_entry.get().strip()
        v = self.v_entry.get().strip()

        if not u or not v:
            messagebox.showerror(
                "Error", "Fill in both job fields!"
            )
            return

        if u == v:
            messagebox.showerror(
                "Error", "A job cannot depend on itself!"
            )
            return

        if v in self.graph[u]:
            messagebox.showwarning(
                "Warning", "Dependency already exists!"
            )
            return

        self.graph[u].append(v)
        self.in_degree[u] += 0
        self.in_degree[v] += 1
        self.all_nodes.update([u, v])

        self.output_area.insert(
            tk.END,
            f"Added: Job {u} must run before Job {v}\n"
        )

        self.u_entry.delete(0, tk.END)
        self.v_entry.delete(0, tk.END)

    def compute_schedule(self):
        in_deg = self.in_degree.copy()

        queue = deque(sorted(
            node for node in self.all_nodes
            if in_deg[node] == 0
        ))
        order = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in self.graph[current]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        self.output_area.insert(tk.END, "-" * 40 + "\n")

        if len(order) == len(self.all_nodes):
            self.output_area.insert(
                tk.END, "SUCCESS: Valid Job Schedule:\n"
            )
            self.output_area.insert(
                tk.END, " -> ".join(order) + "\n"
            )
        else:
            self.output_area.insert(
                tk.END,
                "ERROR: Cycle detected! Scheduling impossible.\n"
            )

        self.output_area.insert(tk.END, "-" * 40 + "\n")
        self.output_area.see(tk.END)

    def reset_graph(self):
        self.graph.clear()
        self.in_degree.clear()
        self.all_nodes.clear()
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "Graph reset.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = JobSchedulerApp(root)
    root.mainloop()