import tkinter as tk
from tkinter import ttk
from tkinter.constants import W
from tkinter.font import Font
from ttkwidgets.autocomplete import AutocompleteEntry
from tkcalendar import DateEntry
import database as db

with open('scripts.txt') as f:
    SCRIPTS = [x.strip() for x in f.readlines()]

FONT = ('Helvetice', 14)
STT_RATE = 0.025 / 100
SEBI_TURNOVER_RATE = 0.00015 / 100
STAMP_DUTY = 0.01 / 100
TRANSACTION_CHARGES = 0.00275 / 100
GST = 18 / 100

root = tk.Tk()
root.geometry("580x730")
root.title("Brokerage calculator")
frame = ttk.Frame(root)

style = ttk.Style()

style.configure('Treeview', font = FONT, rowheight=30)
style.configure('my.Radiobutton', font = FONT)

font = {
    'font': FONT
}

script_label = ttk.Label(frame, text="script", **font)
script_var = tk.StringVar(frame)
script_entry = AutocompleteEntry(frame, textvariable=script_var, width=10, completevalues=SCRIPTS,font=FONT)
script_label.grid(row=0, column=0,pady=6, padx=30)
script_entry.grid(row=1, column=0,pady=2, padx=30)

date_label = ttk.Label(frame, text="date", **font)
date_var = tk.StringVar(frame)
date_entry = DateEntry(frame, textvariable=date_var, width=9, 
    background='darkblue', foreground='white', 
    borderwidth=2, year=2021, font=FONT)

date_label.grid(row=0, column=1,pady=6, padx=30)
date_entry.grid(row=1, column=1,pady=2, padx=30)

brokerage_label = ttk.Label(frame, text="Brokerage", **font)
brokerage_var = tk.StringVar(frame)
brokerage_entry = ttk.Entry(frame, textvariable=brokerage_var, width=10,**font)
brokerage_label.grid(row=0, column=2,pady=6, padx=30)
brokerage_entry.grid(row=1, column=2,pady=2, padx=30)

entry_price_label = ttk.Label(frame, text="Entry Price", **font)
entry_price_var = tk.StringVar(frame)
entry_price_entry = ttk.Entry(frame, textvariable=entry_price_var, width=10,**font)
entry_price_label.grid(row=2, column=0,pady=6, padx=30)
entry_price_entry.grid(row=3, column=0,pady=2, padx=30)

exit_price_label = ttk.Label(frame, text="Exit Price", **font)
exit_price_var = tk.StringVar(frame)
exit_price_entry = ttk.Entry(frame, textvariable=exit_price_var, width=10,**font)
exit_price_label.grid(row=2, column=1,pady=6, padx=30)
exit_price_entry.grid(row=3, column=1,pady=2, padx=30)

shares_label = ttk.Label(frame, text="Shares", **font)
shares_var = tk.StringVar(frame)
shares_entry = ttk.Entry(frame, textvariable=shares_var, width=10,**font)
shares_label.grid(row=2, column=2,pady=6, padx=30)
shares_entry.grid(row=3, column=2,pady=2, padx=30)


sl_amt_label = ttk.Label(frame, text="SL Price", **font)
sl_amt_var = tk.StringVar(frame)
sl_amt_entry = ttk.Entry(frame, textvariable=sl_amt_var, width=10,**font)
sl_amt_label.grid(row=4, column=0,pady=6, padx=30)
sl_amt_entry.grid(row=5, column=0,pady=2, padx=30)

buy_sell = tk.StringVar(frame, value="buy")
buy_rad = tk.Radiobutton(frame, text="Buy", variable=buy_sell,  value="buy", font=Font)
buy_rad.grid(row=5, column=1,pady=2, padx=30)

sell_rad = tk.Radiobutton(frame, text="Sell", variable=buy_sell, value="sell", font=Font)
sell_rad.grid(row=5, column=2,pady=2, padx=30)

frame.pack(pady=10)


# Tkinter Bug Work Around
if root.getvar('tk_patchLevel')=='8.6.9': #and OS_Name=='nt':
    def fixed_map(option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.
        #
        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

columns = ('Field', 'Amount')
main_tree = ttk.Treeview(root, height=12, columns=columns, show="headings")
main_tree.heading('Field', text='')
main_tree.heading('Amount', text='')    

main_tree.tag_configure(tagname="green", background="#4feb34")
main_tree.tag_configure(tagname="red", background="#f03329")

def clear():
    main_tree.delete(*main_tree.get_children())

def save():
    data = calc()
    script = script_var.get()
    date = date_var.get()
    db.save_data(script, date, data)


def calc():
    entry_price = float(entry_price_var.get())
    exit_price = float(exit_price_var.get())
    sl_price = float(sl_amt_var.get())
    buy_sell_val = buy_sell.get()
    shares = float(shares_var.get())
    brokerage_rate = float(brokerage_var.get()) / 100
    turn_over = round((entry_price * shares) + (exit_price * shares), 2)
    brokerage = round(brokerage_rate * turn_over, 2)
    stt = round(STT_RATE * turn_over, 2)
    sebi = round(SEBI_TURNOVER_RATE * turn_over, 2)
    stamp_duty = round(STAMP_DUTY * turn_over, 2)
    transaction_charges = round(TRANSACTION_CHARGES * turn_over, 2)
    gst = round(GST * brokerage, 2)
    total_tax = round(brokerage + stt + sebi + stamp_duty + transaction_charges + gst, 2)
    profit = round((exit_price - entry_price) * shares, 2) if buy_sell_val == "buy" else round((entry_price - exit_price) * shares, 2)
    loss = round((sl_price - entry_price) * shares, 2) if buy_sell_val == "buy" else round((exit_price - sl_price) * shares, 2)
    net_profit = round(profit - total_tax, 2)
    rr = abs(round(profit / loss, 2))
    return entry_price, exit_price, shares, brokerage_rate, turn_over, brokerage, stt, sebi, stamp_duty, transaction_charges, gst, total_tax, profit, loss, net_profit, rr

def display():
    data = calc()
    clear()
    main_tree.insert('', index='end', text='', values=('Turn Over', data[4]))
    main_tree.insert('', index='end', text='', values=('Brokerage', data[5]))
    main_tree.insert('', index='end', text='', values=('STT', data[6]))
    main_tree.insert('', index='end', text='', values=('SEBI CHARGE', data[7]))
    main_tree.insert('', index='end', text='', values=('Stamp Duty', data[8]))
    main_tree.insert('', index='end', text='', values=('Transaction Charges', data[9]))
    main_tree.insert('', index='end', text='', values=('GST', data[10]))
    main_tree.insert('', index='end', text='', values=('Total Tax', data[11]))
    if data[12] < 0:
        tag_val = "red" 
    else: tag_val = "green"
    if data[14] < 0:
        tag_val_net = "red" 
    else: tag_val_net = "green"
    main_tree.insert('', index='end', text='', values=('Profit', data[12]), tags=tag_val)
    main_tree.insert('', index='end', text='', values=('Loss', data[13]))
    main_tree.insert('', index='end', text='', values=('Net Profit', data[14]), tags=tag_val_net)
    main_tree.insert('', index='end', text='', values=('Risk Reward', data[15]))

main_tree.pack(pady=10)

frame_2 = tk.Frame(root)

calc_button = ttk.Button(frame_2, text="Calculate", command=display)
calc_button.grid(row = 0, column =0, padx = 30, pady = 30)

save_button = ttk.Button(frame_2, text="Save", command=save)
save_button.grid(row = 0, column = 1, padx = 5)

find_button = ttk.Button(frame_2, text="Find", command=calc)
find_button.grid(row = 0, column = 2, padx = 30)

frame_2.pack(pady=5)
root.mainloop()
