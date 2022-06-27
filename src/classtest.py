class multi:
 
 
    def __init__(self):
 
        self.inner = self.Inner()
 
        self.innerinner = self.inner.InnerInner()
 
    def show(self):
        print("This is Outer class")
         
 
    ## inner class
    class Inner:
 
 
        def __init__(self):
 
            self.innerinner = self.InnerInner()
            self.really = 3
 
        def show_classes(self):
            print("This is Inner class")
            print(self.innerinner)
 
 
        class InnerInner:
 
            def inner_display(self, msg):
                print("InnerInner class")
                print(msg)
 
        def inner_display(self, msg):
            print("This is Inner class")
            print(msg)
 
outer=multi()
outer.show()
inner = multi.Inner()
 
 
innerinner = inner.InnerInner()
 
 
innerinner.inner_display("completed")