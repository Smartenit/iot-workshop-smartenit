from Tkinter import *

class App:
  def __init__(self, master):
    self.state = StringVar()
    self.state.set('0')

    master.title('GUI Base Example ...!')
    frame = Frame(master)
    frame.pack()

    self.turn_off = Button(frame, text="OFF", fg="red", command=frame.quit)
    self.turn_off.pack(fill=X, padx=10)

    self.turn_on = Button(frame, text="ON", command=self.do_something)
    self.turn_on.pack(fill=X, padx=10)

    self.state_widget_label = Label(frame, text="State:")
    self.state_widget_label.pack(fill=X,padx=10)

    self.state_widget = Label(frame, textvariable=self.state)
    self.state_widget.pack()

  def do_something(self):
    print "hi there, everyone!"
    self.state.set(str(int(self.state.get()) + 1))

if __name__ == "__main__":
  root = Tk()
  app = App(root)
  root.mainloop()
  root.destroy()

