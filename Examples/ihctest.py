"""
Test example showing how to use the ihcsdk to connect to the ihc controller
"""
from sys import argv
from ihcsdk.ihccontroller import IHCController

def on_ihc_change(ihcid, value):
    """Callback when ihc resource changes"""
    print("Resource change " + str(ihcid) + "->" + str(value))

def main():
    """Do the test"""
    if len(argv) != 5:
        print("Syntax: ihctest ihcurl username password resourceid")
        exit()
    url = argv[1]
    resid = int(argv[4])
    ihc = IHCController(url, argv[2], argv[3])
# Un-comment the line below to use pycurl connection
#    ihc.client.connection = IHCCurlConnection( url)
    if not ihc.authenticate():
        print("Authenticate failed")
        exit()

    print("Authenticate succeeded\r\n")

    # read project
    project = ihc.get_project()
    if project is False:
        print("Failed to read project")
    else:
        print("Project downloaded successfully")

    log = ihc.client.get_user_log()
    if log:
        print("log: " + log)

    runtimevalue = ihc.get_runtime_value(resid)
    print("Runtime value: " + str(runtimevalue))
    ihc.set_runtime_value_bool(resid, not runtimevalue)
    runtimevalue = ihc.get_runtime_value(resid)
    print("Runtime value: " + str(runtimevalue))

    #ihc.client.enable_runtime_notifications( resid)
    #changes = ihc.client.wait_for_resource_value_changes( 10)
    #print( repr( changes))

    ihc.add_notify_event(resid, on_ihc_change)

    input()

main()
