class Restaurant:
    '''
    The Restaurant object contains info for name and times the restaurant is open

    Attributes:
        name     The given name of the restaurant ex: "John's Grill"
        times    The weekly hours for the restaurant ex: "Mon-Thu, Sun 11:30 am - 9 pm", "Fri-Sat 11:30 am - 9:30 pm"
    '''
    def __init__(self, name, times):
        self.name = name
        self.times = times
 
    def __str__(self):
     return self.name 