import subprocess

def create_server():
    proc = subprocess.Popen("/home/wow/server/bin/worldserver", stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    return proc

PROC = create_server()

while True:
    if PROC.poll() != None:
        print("Server terminated!")
        PROC = create_server()
    cmd = input("Enter GM command:")
    PROC.stdin.write(cmd)
    print(PROC.stdout.read())
