from IPython.display import display, HTML

class TableColor():
    """ Class to color table
            
    """
    
    
    def __init__(self, DataFrame):
                
        self.df = DataFrame
    
    def red(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: lightblue; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r