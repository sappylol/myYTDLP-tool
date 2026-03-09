import src.cmds as cmds

LOOP = True
print('WELCOME TO MyYTDLP Tool\nuse "help" for show commands')

while LOOP:
    x = input(">>> ").split(" ", 1)
    if x[0].lower() == "exit":
        exit()
    if not x:
        continue
    if x[0] not in cmds.commands:
        print('invalid command :d, try "help"')
        continue

    cmd = getattr(cmds, x[0])

    if len(x) > 1:
        y = cmd(x[1])
    else:
        y = cmd()

    if y is not None:
        print(y)
