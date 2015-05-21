package com.priyanka.mathtabapp;

import java.io.BufferedReader;

import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

//import com.priyanka.mathtabapp.TCPServer;
import com.google.devtools.simple.runtime.components.Component;
import com.google.devtools.simple.runtime.components.HandlesEventDispatching;
import com.google.devtools.simple.runtime.components.android.Button;
import com.google.devtools.simple.runtime.components.android.Form;
import com.google.devtools.simple.runtime.components.android.HorizontalArrangement;
import com.google.devtools.simple.runtime.components.android.Label;
import com.google.devtools.simple.runtime.components.android.TextBox;
//import com.google.devtools.simple.runtime.components.android.TinyWebDB;
import com.google.devtools.simple.runtime.events.EventDispatcher;

public class MainActivity extends Form implements HandlesEventDispatching {
	
	private Label QuestionLabel;
	private HorizontalArrangement HorizontalArrangement1;
	private Label AnswerPromptLabel;
	private TextBox AnswerText;
	private Label RightWrongLabel;
	private Label CurrentQuestion;
	private HorizontalArrangement HorizontalArrangement2;
	private Button AnswerButton;
	private Button NextButton;
	private HorizontalArrangement HorizontalArrangement3;
	private Button HintButton;
	//private TinyWebDB Database;
	private int currentQuestionIndex = 0;
	private int totalQuestions = 10;
	private int numberCorrect = 0;
	private int numberWrong = 0;
	private int numberHints = 0;
	@SuppressWarnings("rawtypes")
	private String[] QuestionList;
	private int[] AnswerList;
	private static boolean hintUsed = false;
	private static boolean answerEntered = false;
	public static String toSend;
	
	private int backgroundImageHeight = 600;
	private int backgroundImageWidth = 1024;
	//private String tagFromWebDB;
	//private Object valueFromWebDB;
	
	//TCP connection
	/*public static void main(String argv[]) throws Exception {
		String clientProblem;
		String passedString;
		ServerSocket welcomeSocket = new ServerSocket(6789);
		
		while(true)
		{
			Socket connectionSocket = welcomeSocket.accept();
			BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
			DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
			clientProblem = inFromClient.readLine();
			System.out.println("Received: " + clientProblem);
			passedString = toSend;
			if (answerEntered == true) {
				outToClient.writeBytes(passedString);
			}
		}
	} */
	
	 void $define() {
		
		this.ScreenOrientation("portrait");
		this.Title("Tablet App");
		this.BackgroundColor(COLOR_NONE);
		this.BackgroundImage("backApp.png");
		this.Scrollable(false);
		
		QuestionLabel = new Label(this);
		QuestionLabel.Text("Math Problem: ");
		QuestionLabel.FontSize(20.0f);
		QuestionLabel.Width(LENGTH_FILL_PARENT);
		QuestionLabel.TextAlignment(Component.ALIGNMENT_NORMAL);
		QuestionLabel.TextColor(Component.COLOR_BLACK);
		
		HorizontalArrangement1 = new HorizontalArrangement(this);
		HorizontalArrangement1.Width(LENGTH_FILL_PARENT);
		HorizontalArrangement1.Height(LENGTH_FILL_PARENT);
		
		AnswerPromptLabel = new Label(HorizontalArrangement1);
		AnswerPromptLabel.Text("Enter Answer: ");
		AnswerPromptLabel.TextColor(Component.COLOR_BLACK);
		
		AnswerText = new TextBox(HorizontalArrangement1);
		AnswerText.Hint("Please enter an answer!");
		AnswerText.TextAlignment(Component.ALIGNMENT_NORMAL);
		AnswerText.TextColor(Component.COLOR_BLACK);
		
		RightWrongLabel = new Label(this);
		RightWrongLabel.Text("Correct/Incorrect");
		RightWrongLabel.FontSize(14.0f);
		RightWrongLabel.TextAlignment(Component.ALIGNMENT_NORMAL);
		RightWrongLabel.TextColor(Component.COLOR_BLACK);
		
		CurrentQuestion = new Label(this);
		CurrentQuestion.Text("BLANK INITIALLY");
		CurrentQuestion.TextColor(Component.COLOR_BLACK);
		
		HorizontalArrangement2 = new HorizontalArrangement(this);
		HorizontalArrangement2.Width(LENGTH_FILL_PARENT);
		HorizontalArrangement2.Height(LENGTH_FILL_PARENT);
		
		AnswerButton = new Button(HorizontalArrangement2);
		AnswerButton.Text("Submit");
		AnswerButton.TextAlignment(Component.ALIGNMENT_CENTER);
		
		NextButton = new Button(HorizontalArrangement2);
		NextButton.Text("Next");
		NextButton.TextAlignment(Component.ALIGNMENT_CENTER);
		
		HorizontalArrangement3 = new HorizontalArrangement(this);
		HorizontalArrangement3.Width(LENGTH_FILL_PARENT);
		HorizontalArrangement3.Height(LENGTH_FILL_PARENT);
		
		HintButton = new Button(HorizontalArrangement3);
		HintButton.Text("Hint");
		HintButton.TextAlignment(Component.ALIGNMENT_CENTER);
		
		//Database = new TinyWebDB(this);
		
		QuestionList = new String[10];
		AnswerList = new int[10];
		//List<String> QuestionList = new ArrayList<String>(totalQuestions);
		//List<Integer> AnswerList = new ArrayList<Integer>(totalQuestions);
		
		for(int i = 0; i < 10; i++) {
			String toInsert = i + " + 1 = ";
			QuestionList[i] = toInsert;
			//System.out.println("Just added " + (String) QuestionList.get(i));
		}
		
		for (int j = 0; j < 10; j++) {
			AnswerList[j] = j + 1;
		}
		
		CurrentQuestion.Text((String) QuestionList[0]);
		
		//EventDispatcher.registerEventForDelegation(this, "Screen1", "Initialize");
		
		EventDispatcher.registerEventForDelegation(this, "NextButton", "Click");
		
		EventDispatcher.registerEventForDelegation(this, "AnswerButton", "Click");
		
		EventDispatcher.registerEventForDelegation(this, "HintButton", "Click");
		
		//EventDispatcher.registerEventForDelegation(this, "Database", "GotValue");
		
	}

	@Override
	public void dispatchEvent(Object dataMember, String dataMemberName,
			String eventName, Object[] args) {
		if(dataMember.equals(NextButton) && eventName.equals("Click")) {
			/* reset whether or not a hint was asked for, if an answer was entered, and the string to set to null */
			hintUsed = false;
			answerEntered = false;
			toSend = "";
			if (currentQuestionIndex == 9) {
				currentQuestionIndex = 0;
			}
			RightWrongLabel.Text("");
			AnswerText.Text("");
			HintButton.Text("Hint");
			if(currentQuestionIndex >= totalQuestions) {
				//set the index to the beginning again to indicate we are done
				currentQuestionIndex = 0;
			}
			String newQuestion = (String) QuestionList[currentQuestionIndex + 1];
			CurrentQuestion.Text(newQuestion);
			currentQuestionIndex++;
		} else if (dataMember.equals(AnswerButton) && eventName.equals("Click")) {
			//String entered = String.valueOf(AnswerList[currentQuestionIndex]);
			answerEntered = true;
			int entered1 = AnswerList[currentQuestionIndex];
			int entered = Integer.parseInt(AnswerText.Text());
			//if(AnswerText.Text() == entered) {
			//include TCP server stuff
			if (entered == entered1) {
				RightWrongLabel.Text("Correct!");
				numberCorrect++;
			} else {
				RightWrongLabel.Text("Incorrect!");
				numberWrong++;
			}
			//send to the robot the formatted string
			//determine the help flag
			int helpFlag;
			if (hintUsed == true) {
				helpFlag = 1;
			} else {
				helpFlag = 0;
			}
			toSend = currentQuestionIndex + " " + helpFlag + " " + entered1 + " " + entered;
			//outToClient.writeBytes(toSend);
		} else if (dataMember.equals(HintButton) && eventName.equals("Click")) {
			hintUsed = true;
			HintButton.Text("Here is a hint! Try using your fingers to count.");
			numberHints++;
		/*} else if (dataMember.equals(Database) && eventName.equals("GotValue")) {
			Database.GotValue(tagFromWebDB, valueFromWebDB);
			if(tagFromWebDB == "") {
				QuestionList.add(valueFromWebDB);
				QuestionLabel.Text(QuestionList.get(0));
			} else {
				AnswerList = valueFromWebDB;
			}
			*/
		} else {
			return;
		}
	}
	}
