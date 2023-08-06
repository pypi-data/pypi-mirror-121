from IPython.display import display, HTML

class TableColor():
    """ Class to color table
            
    """
    
    
    def __init__(self, DataFrame):

        self.df = DataFrame
        self.lightgrey()
    
    def lightblue(self):
    
        """Function for blue lightcolor
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: lightblue; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r
		
	def lightred(self):
    
        """Function for red lightcolor
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: lightred; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r
		
	def lightgreen(self):
    
        """Function for red lightcolor
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: lightgreen; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r
		
	def yello(self):
    
        """Function for yello lightcolor
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: yellow; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r
		
	def lightgrey(self):
    
        """Function for gray lightcolor
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: lightgrey; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        return self.r
