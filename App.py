from MCDP import *
from tkinter import *
from math import *
from functools import partial

attributes = []
at_variable = []
#  prompts the user to name a new decision attribute
def add_attribute():
   window = Toplevel(root)
   name_entry = Entry(window, bd = 5)
   name_entry.pack(side = BOTTOM)
   name_label = Label(window, text = "Attribute Name")
   name_label.pack(side = TOP)
   #  creates column in ranking table for an attribute
   def input_att(event):
      attname = name_entry.get()
      name_entry.delete(0, END)
      attnumber = len(attributes)
      a = attribute()
      attributes.append(a)
      attributes[attnumber].name = attname
      attribute_frame = Frame(root)
      attribute_frame.grid(row = 1, column = len(attributes)+1)
      attribute_label = Label(attribute_frame, text = attname)
      attribute_label.pack(side = TOP)
      attribute_weight_entry = Entry(attribute_frame, width = 8)
      attribute_weight_entry.pack(side = BOTTOM)
      #  associates each attribute with a weight indicating its importance
      def attweight(event):
         val = attribute_weight_entry.get()
         if val == '':
            pass
         else:
            a.weight = float(eval(val))
      attribute_weight_entry.bind("<KeyRelease>",attweight)
      at_variable.append([])
      w = []
      if len(options) > 0:
         for i in range(len(options)):
            attributes[attnumber].prefs.update({options[i] : nan})
            at_variable[attnumber].append(StringVar(root))
            at_variable[attnumber][i].set('  ')
            for s in root.grid_slaves(i+2, len(attributes)+1):
               s.destroy()
            def get_val(i, entry):
               key = options[i]
               val = at_variable[attnumber][i].get()
               att = attributes[attnumber]
               att.prefs.update({key : int(val)})
            w.append(OptionMenu(root, at_variable[attnumber][i], *list(range(1,len(options)+1)), command = partial(get_val, i)))
            w[i].grid(row = i+2, column = len(attributes)+1)
   name_entry.bind("<Return>",input_att)

options = []
#  prompts the user to name a new option as a potential decision
def add_option():
   window = Toplevel(root)
   name_entry = Entry(window, bd = 5)
   name_entry.pack( side = BOTTOM)
   name_label = Label(window, text = "Option Name")
   name_label.pack( side = TOP)
   #  creates row in ranking table for an option
   def input_opt(event):
      optname = name_entry.get()
      name_entry.delete(0, END)
      option_label = Label(root, text = optname)
      option_label.grid(row = len(options)+2, column = 1)
      exec("options.append('%s')" % optname)
      global op_variable
      op_variable = []
      w = []
      for i in range(len(attributes)):
         op_variable.append([])
         w.append([])
         for j in range(len(options)):
            op_variable[i].append(StringVar(root))
            op_variable[i][j].set('  ')
            for s in root.grid_slaves(j+2, i+2):
               s.destroy()
            def get_val(i, j, entry):
               key = options[j]
               val = op_variable[i][j].get()
               att = attributes[i]
               att.prefs.update({key : int(val)})
            w[i].append(OptionMenu(root, op_variable[i][j], *list(range(1,len(options)+1)), command = partial(get_val, i, j)))
            w[i][j].grid(row = j+2, column = i+2)
   name_entry.bind("<Return>",input_opt)
   
root = Tk()
root.minsize(width=250, height=10)
menubar = Menu(root, tearoff = 0)
#  solves the multi-criteria decision problem represented in the ranking table
def MCDP_solve():
   window = Toplevel(root)
   name_label = Label(window, text = str(MCDP(attributes).solve()))
   name_label.pack( side = TOP)
menubar.add_command(label="Solve", command = MCDP_solve)
menubar.add_command(label="New Attribute", command = add_attribute)
menubar.add_command(label="New Option", command = add_option)

root.config(menu = menubar)
root.mainloop()