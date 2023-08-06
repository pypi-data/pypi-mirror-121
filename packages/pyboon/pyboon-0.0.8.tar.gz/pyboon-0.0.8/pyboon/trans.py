from  openpyxl import  Workbook 

def csv2xl(csvfile):
    # 实例化
    wb = Workbook()
    # 激活 worksheet
    ws = wb.active

    from pyboon import x,f

    txt = f.read(csvfile)
    # print()

    for line in txt.split("\n"):
        print(line)
        ws.append(line.split(","))


    wb.save(csvfile.replace(".csv",".xlsx"))
