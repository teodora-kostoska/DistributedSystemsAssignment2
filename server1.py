from xmlrpc.server import SimpleXMLRPCServer
import socket
import os
from _thread import *
import xml.etree.ElementTree as eTree 


#Initialize socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 9000
#Bind the socket to host and port
try:
    serverSocket.bind((host, port))
    print("Socket listening on port 9000...")
#Catch exceptions
except socket.error as e:
    print(str(e))
#Listen to up to 5 clients
serverSocket.listen(5)

#Used to send correct data to the client side. Also used to check whether file exists yet.
def text(topic, data, note, timestamp):
    if(os.path.exists("db.xml")):
        #If file exists check whether values with similar title are in file, if there are return those, if there aren't append them to file
        add_to_file(topic, data, note, timestamp)
        text = read_from_file(topic)
        text1 = text
    else:
        #Create the file and append the value sent by client
        create_file(topic, data, note, timestamp)
        text = read_from_file(topic)
        text1 = text
    return text1

#If file doesn't exist create file
def create_file(topic, data, note, timestamp):
    root = eTree.Element("Data")

    topic_value = eTree.Element("topic")
    root.append(topic_value)
    topic_value.set("name", topic)

    data_value0 = eTree.SubElement(topic_value, "note")
    data_value0.text = note

    data_value = eTree.SubElement(data_value0, "text")
    data_value.text = data

    data_value2 = eTree.SubElement(data_value0, "timestamp")
    data_value2.text = timestamp

    tree = eTree.ElementTree(root)
    with open ("db.xml", "wb") as files :
        tree.write(files)

#Read the data from the xml file
def read_from_file(topic):
    tree = eTree.parse("db.xml")
    root = tree.getroot()
    text = ""
    for child in root:
        if(child.attrib["name"] == topic):
            text = text + "Topic: " + str(topic) + "\n\n"
            for values in child.iter("note"):
                text = text + "Timestamp: " + str(values[1].text) + ".\n"
                text = text + "Description: "+ str(values.text) + "\n"
                text = text + str(values[0].text) + ".\n"
    return text

#If file already exists append the data accordingly
def add_to_file(topic, data,note, timestamp):
    tree = eTree.parse("db.xml")
    root = tree.getroot()
    keep_track = 0 #Keep track of whether topic was in the file
    for child in root: 
        if(child.attrib["name"] == topic):
            data_value0 = eTree.SubElement(child, "note")
            data_value0.text = note
            data_value = eTree.SubElement(data_value0, "text")
            data_value.text = data

            data_value2 = eTree.SubElement(data_value0, "timestamp")
            data_value2.text = timestamp
            keep_track = 1
    #If it wasn't in the file, add it to the file
    if(keep_track == 0):
        topic_value = eTree.Element("topic")
        root.append(topic_value)
        topic_value.set("name", topic)

        data_value0 = eTree.SubElement(topic_value, "note")
        data_value0.text = note

        data_value = eTree.SubElement(data_value0, "text")
        data_value.text = data

        data_value2 = eTree.SubElement(data_value0, "timestamp")
        data_value2.text = timestamp

    tree = eTree.ElementTree(root)
    with open ("db.xml", "wb") as files :
        tree.write(files)
    
    

#Define function to create multiple threads
def multi_thread(connection):
    connection.send(str.encode('Server is working:'))
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(text, "text")
    server.serve_forever()

#List of clients
client_list = []
while True:
    Client, address = serverSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_thread, (Client, ))
    client_list.append(Client)
serverSocket.close()
