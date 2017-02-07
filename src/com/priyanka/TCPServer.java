package com.priyanka;

import java.io.*;
import java.net.*;

import com.priyanka.MainActivity;

public class TCPServer {

	public static TCPServer singleton;

	public static TCPServer getSingleton() {
		if (singleton!=null)
			return singleton;
		else {
			try {
				singleton = new TCPServer();
				return singleton;
			} catch (Exception e){
				e.printStackTrace();
				return null;
			}
		}
	}
	
	public TCPServer() throws Exception {
		String clientProblem;
		String passedString;
		ServerSocket welcomeSocket = new ServerSocket(6789);
		System.out.println("Waiting for connection on Port 6789");
		
		boolean running = true;
		
		while(running)
		{
			Socket connectionSocket = welcomeSocket.accept();
			System.out.println("Got connection on Port 6789");
			BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
			DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
			clientProblem = inFromClient.readLine();
			System.out.println("Received: " + clientProblem);
			passedString = clientProblem.toUpperCase();
			//passedString = MainActivity.toSend;
			outToClient.writeBytes(passedString);
		}
	}

}
