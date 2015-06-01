package com.priyanka;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.text.Normalizer;

public class MainActivity extends Activity {

    private final String SUBMIT_STRING = "Submit";
    private final String CORRECT_STRING = "Correct!";
    private final String NEXT_QUESTION_STRING = "Next Question";
    private final String INCORRECT_STRING = "Incorrect!";
    private final String REQUEST_HINT_STRING = "Ask robot for help!";


    private EditText AnswerText;
    private TextView RightWrongLabel;
    private TextView CurrentQuestion;
    private Button HintButton;
    private Button SubmitButton;

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
    public static String toSend;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        AnswerText = (EditText) findViewById(R.id.editText);
        RightWrongLabel = (TextView) findViewById(R.id.RightWrongLabel);
        CurrentQuestion = (TextView) findViewById(R.id.QuestionLabel);
        HintButton = (Button) findViewById(R.id.HintButton);
        SubmitButton = (Button) findViewById(R.id.AnswerButton);

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
        SubmitButton.setText(SUBMIT_STRING);
    }

    public void AnswerButtonPress(View view) {

        if (questionState == QState.INIT || questionState == QState.DISPLAYINCORRECT
                || questionState == QState.INVALID) {
            //String entered = String.valueOf(AnswerList[currentQuestionIndex]);
            int correct_answer = AnswerList[currentQuestionIndex];
            int entered = Integer.parseInt(AnswerText.getText().toString());
            //if(AnswerText.Text() == entered) {
            //include TCP server stuff
            if (entered == correct_answer) {
                RightWrongLabel.setText(CORRECT_STRING);
                SubmitButton.setText(NEXT_QUESTION_STRING);
                questionState = QState.DISPLAYCORRECT;
                numberCorrect++;
            } else {
                RightWrongLabel.setText(INCORRECT_STRING);
                questionState = QState.DISPLAYINCORRECT;
                numberWrong++;
            }
        } else if (questionState == QState.DISPLAYCORRECT){
            NextQuestion();
        }
    }

    public void NextQuestion(){
        //reset whether or not a hint was asked for, if an answer was entered, and the string to set to null
        toSend = "";
        if (currentQuestionIndex == 9) {
            currentQuestionIndex = 0;
        }
        RightWrongLabel.setText("");
        AnswerText.setText("");
        HintButton.setText(REQUEST_HINT_STRING);
        if (currentQuestionIndex >= totalQuestions) {
            //set the index to the beginning again to indicate we are done
            currentQuestionIndex = 0;
        }
        String newQuestion = (String) QuestionList[currentQuestionIndex + 1];
        SubmitButton.setText(SUBMIT_STRING);
        CurrentQuestion.setText(newQuestion);
        currentQuestionIndex++;
        questionState = QState.INIT;
    }


    public void HintButtonPress(View view){
        HintButton.setText("Here is a hint! Try using your fingers to count.");
        hintsremaining--;

    }
}