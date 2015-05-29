package com.priyanka;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.text.Normalizer;

public class MainActivity extends Activity {

    private EditText AnswerText;
    private TextView RightWrongLabel;
    private TextView CurrentQuestion;
    private Button HintButton;

    //States
    private enum QState {
        INIT, INVALID, DISPLAYCORRECT, DISPLAYINCORRECT
    }
    private QState questionState = QState.INIT;

    private enum HState {
        QUESTIONVIEW, HINTVIEW
    }
    private HState hintState = HState.QUESTIONVIEW;
    private int MAXHINTS = 3;
    private int hintsremaining = MAXHINTS;


    private int currentQuestionIndex = 0;
    private int totalQuestions = 10;
    private int numberCorrect = 0;
    private int numberWrong = 0;
    private int numberHints = 0;

    private String[] QuestionList;
    private int[] AnswerList;
    private static boolean hintUsed = false;
    private static boolean answerEntered = false;
    public static String toSend;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        AnswerText = (EditText) findViewById(R.id.editText);
        RightWrongLabel = (TextView) findViewById(R.id.RightWrongLabel);
        CurrentQuestion = (TextView) findViewById(R.id.QuestionLabel);
        HintButton = (Button) findViewById(R.id.HintButton);

        QuestionList = new String[10];
        AnswerList = new int[10];

        for (int i = 0; i < 10; i++) {
            String toInsert = i + " + 1 = ";
            QuestionList[i] = toInsert;
            //System.out.println("Just added " + (String) QuestionList.get(i));
        }

        for (int j = 0; j < 10; j++) {
            AnswerList[j] = j + 1;
        }

        CurrentQuestion.setText((String) QuestionList[0]);
    }

    public void AnswerButtonPress(View view){
        //String entered = String.valueOf(AnswerList[currentQuestionIndex]);
        answerEntered = true;
        int entered1 = AnswerList[currentQuestionIndex];
        int entered = Integer.parseInt(AnswerText.getText().toString());
        //if(AnswerText.Text() == entered) {
        //include TCP server stuff
        if (entered == entered1) {
            RightWrongLabel.setText("Correct!");
            numberCorrect++;
        } else {
            RightWrongLabel.setText("Incorrect!");
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
    }

    public void LoadNextQuestion(){

    }


    public void NextQuestion(View view){
        //reset whether or not a hint was asked for, if an answer was entered, and the string to set to null
        hintUsed = false;
        answerEntered = false;
        toSend = "";
        if (currentQuestionIndex == 9) {
            currentQuestionIndex = 0;
        }
        RightWrongLabel.setText("");
        AnswerText.setText("");
        HintButton.setText("Ask Robot for Help");
        if (currentQuestionIndex >= totalQuestions) {
            //set the index to the beginning again to indicate we are done
            currentQuestionIndex = 0;
        }
        String newQuestion = (String) QuestionList[currentQuestionIndex + 1];
        CurrentQuestion.setText(newQuestion);
        currentQuestionIndex++;
    }


    public void HintButtonPress(View view){
        hintUsed = true;
        HintButton.setText("Here is a hint! Try using your fingers to count.");
        hintsremaining--;
		/*} else if (dataMember.equals(Database) && eventName.equals("GotValue")) {
			Database.GotValue(tagFromWebDB, valueFromWebDB);
			if(tagFromWebDB == "") {
				QuestionList.add(valueFromWebDB);
				QuestionLabel.Text(QuestionList.get(0));
			} else {
				AnswerList = valueFromWebDB;
			}
			*/
    }
}