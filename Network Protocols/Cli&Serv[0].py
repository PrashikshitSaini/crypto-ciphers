'''
Okay lets talk about what this code is all about.
I was given an assignment in my Advance Networks Class where I had to write a client and a server code to fulfill the following requirements:

1. Checking the test grade entry from the text file and give the results back to the client.
2. Client Connects to the Server via TCP/IP on port 8001.
3. The server will then respond to the client with the message: COURSEID
4.The client will respond with a packet containing the following:
    - A four-character string representing the course subject area (E.g. COSC)
    - A sixteen-bit signed integer in the range of 1003-9993 representing the course number.  
    - A sixteen-bit signed integer in the range of 0-99 representing the section number.

5. Once this is received, the server will respond with the message: MAX SCORE
    - To which the client will respond with a packet containing the following:
    - A sixteen-bit signed integer representing the maximum possible score for the test.
    - This score will be used by the server to reject invalid scores.
    
6. The server will then respond with the following: BEGIN
7. The client will then send test scores, one per packet, in the following format:
    - An signed 32-bit integer representing the student's ID in a range from 100000-999999
    - A signed 16-bit integer representing the score on the test.

8. The client will continue to send scores, one per packet, until it is done, at which point it will send the value -1 as the student ID and as the test score. Then it will wait for the server to send its response.

9. The server will send a response in the following format:
    - One packet representing the server's analysis of the scores:

    - A thirty-two bit integer representing the client's IP address
    - A sixteen-bit integer representing the client Port number

    - A 11 character ASCII string representing the course (E.g. COSC4653-01)

    - A signed sixteen-bit integer representing the number of total scores received.
    (This value must not include the -1 value sent as a sentinal value.)

    - A signed sixteen-bit integer representing the number of valid scores received.
    - A signed sixteen-bit integer representing the low score
    - A signed sixteen-bit integer representing the high score
    - An IEEE 754 32-bit floating point value representing the average score
    - An IEEE 754 32-bit floating point value representing the standard deviation
    
10. The client will then respond with the following packet: ERRORS
To which the server will respond with a packet containing the string: ERRORS

11. Then it will send one student ID and one test score per packet in the same format as the one used by the client to send scores to the server, sending only the errors. (That is, the student IDs and test scores outside of the acceptable range of scores.)

12. When done, the server will send a student ID and score packet using -1 as the value for both values. 

NOTE: The client will send each score one at a time and will implement a random delay from 1 to 3 seconds between packets to simulate manual score entry.
'''



# -------------------------------------------------SERVER CODE--------------------------------------------------------

import socket
import struct
import threading

def handle_client(client_socket, client_address): # What is this client socket and client address? The client socket lets you send and receive data on the connnection and the client address is the address of the client(IP address and port number)
    print(f"Connection from {client_address[0]}:{client_adddress[1]}")
    client_socket.sendall(b"COURSEID") # For network transmission, we need to send bytes, not strings. So this ensures that the string is converted to bytes. This is what the server is expecting from the client to send back based on the assignment.

    course_data = client_socket.recv(8) # It will attempt to read upto 8 bytes from the socket(the client) and the rest can be read again by calling receiving again.
    course_subject, course_number, course_section = struct.unpack('!4sHH', course_data) # ! = network byte order(endian), 4s = four byte string, H = usigned short for the course number, H = unsigned short for the course section (Check the PPT by Dr. Gowing)
    course_subject = course_subject.decode().strip() # This is first converting the bytes to a string and then removing any leading or tralilin white spaces.
    print(f"Received {course_subject} {course_number} {course_section}") # This is just printing the course data for the connected client.

    client_socket.sendall(b"MAX SCORE") # This is what the server expecting from the client now and it is sending this to the client.
    max_score_data = client_socket.recv(2) # This is reading the max score from the client upto 2 bytes.
    max_score = struct.unpack('!H', max_score_data)[0]
    print(f"Received maxscore of {max_score}") # Based on the assignment the text file has the maximum score that a student can get in the course. This is that

    client_socket.sendall(b"BEGIN") # Now the server has all the info for the connected client and it is ready to receive all the students data for the connected client.

    scores = [] # This is the list of the valid score in the list
    errors =[] # And similarly this is the list of the invalid score in the list
    while True:
        score_data = client_socket.recv(6) # This is reading the score from the client upto 6 bytes.
        student_id, student_score = struct.unpack('!iH', score_data) # ! = netwrok byte order(big endian), i = signed integet for the student id, H = unsigned short for the student score
        print(f"Score received {student_id} {student_score}") # This is what the server returning on the server side as it is getting data from the client.
        if student_id == -1: # this is to check if the sentinel value has reached, it is sent by the client.
            print("Sentinel received")
            break
        if 0 <= student_score <= max_score: # this is the logic based on the text file in the given by the client side
            scores.append(student_score) # This is adding the valid score to the list
        else:
            errors.append((student_id, student_score)) # This is adding the invalid score to the list

        # At this moment this is only on the server side and not going anywhere. This is just the calculation of the scores.
        if scores:
            low_score = min(scores)
            high_score = max(scores)
            avg_score = sum(scores) / len(scores)
            variance = ((s - avg_score) ** 2 for s in scores) / len(scores)
            std_dev = variance ** 0.5
        else:
            low_score = high_score = avg_score = variance = std_dev = 0.0

        # This is the moment we send everything back to the client
        response = struct.pack('!I H 11s H H H H f f', # 
        struct.unpack("!I", socket.inet_aton(client_address[0]))[0] # This is converting the IP address to a 32 bit integer
        ,client_address[1] # This is the port number of the client
        , course_section.encode() # This is the course section with the 11 bytes(padded if necessary)
        , len(scores) + len(errors) # This is the total number of scores received from the client(even the invalid)
        , len(scores) # This is the number of valid scores
        , low_score
        , high_score
        , avg_score
        , std_dev)

        client_socket.sendall(response) # We are sending the complete response packed to the client
        client_socket.sendall(b"ERRORS") # Now we send the client that we are sending the errors the client replies with the same message
        client_socket(recv(6)) # This is the client acknowledging the message

        for student_id, student_score in errors:
            client_socket.sendall(strucnt.pack('!iH', student_id, score))
        client_socket.sendall(struct.pack('!i', -1)) 
        client_socket.close()
        print(f"Client {client_address} disconnected.")



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The AF_INET is the address family for IPv4 and SOCK_STREAM is the socket type for TCP
    server_socket.bind(("0.0.0.0", 8001)) # This is binding the server to the IP address
    server_socket.listen(5) # This is listening for the incoming connections with a backlog of 5
    print("Server listening on port 8001...")
    while True:
        client_socket, client_address = server_socket.accept() # We are accepting the inco,ing connection and setting the client socket and client address
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server() # This is calling the start_server() function to start the server




# -------------------------------------------------CLIENT CODE--------------------------------------------------------

import socket 
import struct
import time
import random
import sys

def recvall(sock, n): # this is a helper that will recieve only certain bytes upto n because most of the time all the bytes sent by the server canont be received
    data = b""
    while len(data) < n:
        packet = sock.rec(n- len(data))
        if not packet:
            break
        data += packet

    return data

def run_client(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # similar to the server this line of code is creating the client socket
    client_socket.connect(("127.0.0.1", 8001)) # This is where we tell the client to connect with the server
    recvall(client_socket, 8) # Calling the above helper function with the client socket and 8 bytes

    with open(file_path, 'r') as f: # this is used to open the text file in the read mode
        lines = f.readlines() # This is reading all the lines in the text file and storing in a list

    course_info = lines[0].strip().split() # This is first getting the first line in the text file and removing any leading or trailind white spaces and then splitting the line based on the space between the words
    max_score = int(line[1].strip()) # This gets the second line with the max score
    scores = [tuple(map(int, line.strip().split())) for line in lines[2:]] # this is converting the rest of the lines in the file to int and then mapping the student_id to the score and then storing in a list of tuples

    course_subject = course_info[0].encode() # We are encoding for the network transmission
    course_number = int(course_info[1])
    course_section = int(course_info[2])
    client_socket.sendall(struct.pack('!4sHH', course_subject, course_number, course_section)) # This is packing the info and sending it to the server in a form that the server can understand

    client_socket.rec(9) # This is the server asking for the max score
    client_socket.sendall('!H', max_score) # This is when we send the max score to the server
    client_socket.recv(5)

    for student_id, score in scores:
        time.sleep(random.randint(1, 3)) # We are simulating a human behavior by sending the info in a delay of 1 to 3 seconds
        client_socket.sendall(struct.pack('!iH', student_id, score))
    
    client_socket.sendall(struct.pack('!i', -1)) # This is where we are sending the sentinel valur to the server telling that the previous data is the last one.

    response = recvall(client_socket, 33) # This is receiving the result from the server that is expected to be 33 bytes. HOW?? Explained in the next line
    client_ip, client_port, course_id, total_scores, valid_scores, low_score, high_score, avg_score,std_dev = struct.unpack('!I H 11s H H H H f f', response) # This is the answer to the above question. Let's break it down
    # I: 4 bytes
    # H: 2 bytes
    # 11s: 11 bytes
    # H: 2 bytes
    # H: 2 bytes
    # H: 2 bytes
    # H: 2 bytes
    # f: 4 bytes
    # f: 4 bytes
    # Sum of all the above is 33 bytes
    course_id = course_id.decode().strip()
    
    # NOw we print the results to the client
    print(f"Results for {course_id}:")
    print(f"Total Scores: {total_scores}")
    print(f"Valid Scores: {valid_scores}")
    print(f"Low Score: {low_score}")
    print(f"High Score: {high_score}")
    print(f"Average Score: {avg_score:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    
    client_socket.sendall(b"ERROR") # We send the server this message to receieve the error in the file
    recvall(client_socket, 6) # This is the server acknowledging the message
    while True:
        error_data = recvall(client_socket, 6)
        if len(error_data) < 6:
            break
        student_id, score = struct.unpack('!iH', error_data)
        
        if student_id == -1:
            break
        print(f"Invalid Score - Student ID: {student_id}, Score: {score}")
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_client(sys.argv[1])
    else:
        print("Usage: python {sys.argv[0]} <file_path>")