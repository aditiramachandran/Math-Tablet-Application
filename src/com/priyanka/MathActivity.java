package com.priyanka;

import android.app.Activity;
import android.inputmethodservice.Keyboard;
import android.inputmethodservice.KeyboardView;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MathActivity extends Activity {

    private final String SUBMIT_STRING = "Submit";
    private final String CORRECT_STRING = "Correct!";
    private final String NEXT_QUESTION_STRING = "Next Question";
    private final String REQUEST_HINT_STRING = "Ask robot for help!";
    private final String INCORRECT_POSTFIX = /* Answer */ " is incorrect! Try again!";
    private final String TITLE_PREFIX = "Question " /* number */;
    private final String INVALID_STRING = "Type in an answer before submitting!";

    private com.priyanka.NoImeEditText AnswerText;
    private TextView RightWrongLabel;
    private TextView CurrentQuestion;
    private Button HintButton;
    private Button SubmitButton;
    private TextView TitleLabel;
    private KeyboardView mKeyboardView;
    private int sessionNum = -1;

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


    private int currentQuestionIndex = -1;
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

        AnswerText = (com.priyanka.NoImeEditText) findViewById(R.id.editText);
        RightWrongLabel = (TextView) findViewById(R.id.RightWrongLabel);
        CurrentQuestion = (TextView) findViewById(R.id.QuestionLabel);
        HintButton = (Button) findViewById(R.id.HintButton);
        SubmitButton = (Button) findViewById(R.id.AnswerButton);
        TitleLabel = (TextView) findViewById(R.id.TitleLabel);

        //get session num from previous activity
        Bundle extras = getIntent().getExtras();
        if (extras != null){
            sessionNum = Integer.parseInt(extras.getString("sessionNum"));
            
        }
        System.out.println("session number is: " + sessionNum);

        QuestionList = new String[totalQuestions];
        AnswerList = new int[totalQuestions];

        for (int i = 0; i < totalQuestions; i++) {
            String toInsert = i + " + 1 = ";
            QuestionList[i] = toInsert;
            //System.out.println("Just added " + (String) QuestionList.get(i));
        }

        for (int j = 0; j < totalQuestions; j++) {
            AnswerList[j] = j + 1;
        }



        Keyboard mKeyboard= new Keyboard(getApplicationContext(), R.xml.numbers_keyboard);

        // Lookup the KeyboardView
        mKeyboardView= (KeyboardView)findViewById(R.id.keyboardview);
        // Attach the keyboard to the view
        mKeyboardView.setKeyboard(mKeyboard);
        // Do not show the preview balloons
        mKeyboardView.setPreviewEnabled(false);

        mKeyboardView.setOnKeyboardActionListener(new KeyboardView.OnKeyboardActionListener() {
            @Override
            public void onKey(int primaryCode, int[] keyCodes) {
                //Here check the primaryCode to see which key is pressed
                //based on the android:codes property
                if (primaryCode >= 0 && primaryCode <= 9) {
                    AnswerText.setText(AnswerText.getText().toString() + primaryCode + "");
                } else if (primaryCode == -1) {
                    if (AnswerText.getText().toString().length() > 0) {
                        String old_string = AnswerText.getText().toString();
                        int string_length = old_string.length();

                        String new_string = old_string.substring(0, string_length - 1);

                        AnswerText.setText(new_string);
                    }
                }
            }

            @Override
            public void onPress(int arg0) {
            }

            @Override
            public void onRelease(int primaryCode) {
            }

            @Override
            public void onText(CharSequence text) {
            }

            @Override
            public void swipeDown() {
            }

            @Override
            public void swipeLeft() {
            }

            @Override
            public void swipeRight() {
            }

            @Override
            public void swipeUp() {
            }
        });

        NextQuestion();
    }

    public void AnswerButtonPress(View view) {


        if (AnswerText.getText().equals("")){
            System.out.println("--->"+AnswerText.getText());
            questionState = QState.INVALID;
            RightWrongLabel.setText(INVALID_STRING);

        } else if (questionState == QState.INIT || questionState == QState.DISPLAYINCORRECT
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
                AnswerText.setEnabled(false);
                mKeyboardView.setVisibility(View.INVISIBLE);
                mKeyboardView.setEnabled(false);
                numberCorrect++;
            } else {
                String incorrect_string = entered + INCORRECT_POSTFIX;
                RightWrongLabel.setText(incorrect_string);
                questionState = QState.DISPLAYINCORRECT;
                AnswerText.setText("");
                numberWrong++;
            }
        } else if (questionState == QState.DISPLAYCORRECT){
            NextQuestion();
        }
    }

    public void NextQuestion(){
        //reset whether or not a hint was asked for, if an answer was entered, and the string to set to null
        toSend = "";
        currentQuestionIndex++;

        RightWrongLabel.setText("");
        AnswerText.setText("");
        HintButton.setText(REQUEST_HINT_STRING);
        if (currentQuestionIndex >= totalQuestions) {
            //set the index to the beginning again to indicate we are done
            currentQuestionIndex = 0;
        }
        String newQuestion = (String) QuestionList[currentQuestionIndex];
        SubmitButton.setText(SUBMIT_STRING);
        CurrentQuestion.setText(newQuestion);
        questionState = QState.INIT;
        AnswerText.setEnabled(true);
        mKeyboardView.setVisibility(View.VISIBLE);
        mKeyboardView.setEnabled(true);
        TitleLabel.setText(TITLE_PREFIX + " " + (currentQuestionIndex + 1));

        //Send message
        if (com.priyanka.TCPClient.singleton != null)
            com.priyanka.TCPClient.singleton.sendMessage(newQuestion);
    }

    public void HintButtonPress(View view){
        HintButton.setText("Here is a hint! Try using your fingers to count.");
        hintsremaining--;

    }
}