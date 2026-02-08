from rich.console import Console
from rich.table import Table


# Initialize a Console object
console = Console()


class showOutput():
    def __init__(self,output_list: list[list[str],list[list[str]]] )->print:
        if len(output_list) < 2:
            raise ValueError("output_list must have at least two elements: headers and rows")
        
        self.table = Table(title="Output", show_header=True, header_style="black on bright_yellow")
        
        # Extract headers and rows
        headers, rows_data = output_list[0], output_list[1]
        
        # Add column headers
        for field in headers:
            self.table.add_column(field, style="bold cyan", justify="left")
        
        # Ensure rows are correctly formatted
        rows = [tuple(str(item) for item in row) for row in rows_data]

        # Add rows with alternating background colors
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.table.add_row(*row, style="black on white")  # Even row
            else:
                self.table.add_row(*row, style="white on grey23")  # Odd row
        

    def display(self):
        console.print(self.table)


#show_output = ShowOutput(output_data)
#show_output.display()
