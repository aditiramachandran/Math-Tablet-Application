package com.priyanka;

import android.app.Activity;
import android.content.Intent;
import android.content.res.AssetManager;
import android.inputmethodservice.Keyboard;
import android.inputmethodservice.KeyboardView;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONArray;

import java.io.IOException;
import java.io.InputStream;
import java.nio.channels.NonReadableChannelException;
import com.priyanka.Questions;
import com.priyanka.Question;

public class MathActivity extends Activity {

    private final String SUBMIT_STRING = "Submit";
    private final String CORRECT_STRING = "Correct!";
    private final String NEXT_QUESTION_STRING = "Next Question";
    private final String REQUEST_HINT_STRING = "Ask robot for help!";
    private final String REQUEST_HINT_STRING1 = "Request Hint 1";
    private final String REQUEST_HINT_STRING2 = "Request Hint 2";
    private final String REQUEST_HINT_STRING3 = "Request Hint 3";
    private final String REPEAT_HINT_STRING1 = "Repeat Hint 1";
    private final String REPEAT_HINT_STRING2 = "Repeat Hint 2";
    private final String REPEAT_HINT_STRING3 = "Repeat Hint 3";
    private final String INCORRECT_POSTFIX = /* Answer */ " is incorrect! Try again!";
    private final String TITLE_PREFIX = "Question " /* number */;
    private final String INVALID_STRING_FRACTION = "Type in an answer into both boxes before submitting!";
    private final String INVALID_STRING_VALUE = "Type in an answer before submitting!";


    private TextView fractionLine;
    private com.priyanka.NoImeEditText AnswerText1;
    private com.priyanka.NoImeEditText AnswerText2;
    private TextView RightWrongLabel;
    private AutoResizeTextView CurrentQuestion;
    private Button HintButton1;
    private Button HintButton2;
    private Button HintButton3;
    private Button SubmitButton;
    private TextView TitleLabel;
    private KeyboardView mKeyboardView;
    private int sessionNum = -1;

    private Questions questions;

    public final int MAX_HINTS = 3;
    public int hintsRemaining = MAX_HINTS;

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

    private int currentQuestionIndex = -1;
    private int numberCorrect = 0;
    private int numberWrong = 0;
    private int numberHints = 0;


    public String AssetJSONFile (String filename) throws IOException {
        AssetManager manager = this.getAssets();
        InputStream file = manager.open(filename);
        byte[] formArray = new byte[file.available()];
        file.read(formArray);
        file.close();

        return new String(formArray);
    }

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        //Load JSON file
        String json_file = "sample.json";

        Bundle extras = getIntent().getExtras();
        if (extras != null){
            sessionNum = Integer.parseInt(extras.getString("sessionNum"));
            json_file = "Session"+sessionNum+".json";
        }

        String json = "";
        try {
            json = AssetJSONFile(json_file);
        } catch (IOException e){
            e.printStackTrace();
        }
        questions = new Questions(json);

        fractionLine = (TextView) findViewById(R.id.fractionLine);
        AnswerText1 = (com.priyanka.NoImeEditText) findViewById(R.id.editText1);
        AnswerText2 = (com.priyanka.NoImeEditText) findViewById(R.id.editText2);
        RightWrongLabel = (TextView) findViewById(R.id.RightWrongLabel);
        CurrentQuestion = (AutoResizeTextView) findViewById(R.id.QuestionLabel);
        HintButton1 = (Button) findViewById(R.id.hint1);
        HintButton2 = (Button) findViewById(R.id.hint2);
        HintButton3 = (Button) findViewById(R.id.hint3);
        SubmitButton = (Button) findViewById(R.id.AnswerButton);
        TitleLabel = (TextView) findViewById(R.id.TitleLabel);

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
                EditText target= AnswerText1;
                if (AnswerText2.hasFocus())    target=AnswerText2;

                if (primaryCode >= 0 && primaryCode <= 9) {
                    target.setText(target.getText().toString() + primaryCode + "");
                } else if (primaryCode == -1) {
                    if (target.getText().toString().length() > 0) {
                        String old_string = target.getText().toString();
                        int string_length = old_string.length();

                        String new_string = old_string.substring(0, string_length - 1);

                        target.setText(new_string);
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

        String format = questions.get(currentQuestionIndex).format;
        String enteredStr1 = AnswerText1.getText().toString();
        String enteredStr2 = AnswerText2.getText().toString();

        if (format.equals(Questions.FORMAT_FRACTION) &&
                (enteredStr1.equals("") || enteredStr2.equals(""))) {
            questionState = QState.INVALID;
            RightWrongLabel.setText(INVALID_STRING_FRACTION);
        } else if (format.equals(Questions.FORMAT_TEXT) && enteredStr1.equals("")){
            questionState = QState.INVALID;
            RightWrongLabel.setText(INVALID_STRING_VALUE);
        } else if (questionState == QState.INIT || questionState == QState.DISPLAYINCORRECT
                || questionState == QState.INVALID) {

            Question question = questions.get(currentQuestionIndex);

            Boolean correct = false;

            int entered1 = Integer.parseInt(enteredStr1);

            if (question.format.equals(Questions.FORMAT_FRACTION)){
                int entered2 = Integer.parseInt(enteredStr2);
                correct = question.numerator==entered1 && question.denominator==entered2;
            } else if (question.format.equals(Questions.FORMAT_TEXT)){
                correct = question.value == entered1;
            }

            //if(AnswerText.Text() == entered) {
            //include TCP server stuff
            if (correct) {
                if (com.priyanka.TCPClient.singleton != null)
                    com.priyanka.TCPClient.singleton.sendMessage("CA:" + CORRECT_STRING);
                RightWrongLabel.setText(CORRECT_STRING);
                SubmitButton.setText(NEXT_QUESTION_STRING);
                questionState = QState.DISPLAYCORRECT;
                AnswerText1.setEnabled(false);
                AnswerText2.setEnabled(false);
                mKeyboardView.setVisibility(View.INVISIBLE);
                mKeyboardView.setEnabled(false);
                numberCorrect++;
            } else {
                String incorrect_string = "";
                if (question.format.equals(Questions.FORMAT_FRACTION)){
                    int entered2 = Integer.parseInt(enteredStr2);
                    incorrect_string = entered1 + " / " + entered2 + INCORRECT_POSTFIX;
                } else if (question.format.equals(Questions.FORMAT_TEXT)) {
                    incorrect_string = entered1 + INCORRECT_POSTFIX;
                }
                //Send message
                if (com.priyanka.TCPClient.singleton != null)
                    com.priyanka.TCPClient.singleton.sendMessage("IA:" + incorrect_string);
                RightWrongLabel.setText(incorrect_string);
                questionState = QState.DISPLAYINCORRECT;
                AnswerText1.setText("");
                AnswerText2.setText("");
                numberWrong++;
                AnswerText1.requestFocus();
            }
        } else if (questionState == QState.DISPLAYCORRECT){
            NextQuestion();
        }

    }

    public void HintPressed(View view){

        Question currentQuestion = questions.get(currentQuestionIndex);

        int buttonNumber = -1;

        Button button = (Button) view;

        if      (button==HintButton1) buttonNumber = 1;
        else if (button==HintButton2) buttonNumber = 2;
        else if (button==HintButton3) buttonNumber = 3;

        int newHintButtonNumber = MAX_HINTS - hintsRemaining + 1;

        if (buttonNumber <= newHintButtonNumber){
            String hintMessage = "";
            if (buttonNumber == 1) {
                hintMessage = currentQuestion.hint1;
                HintButton1.setText(REPEAT_HINT_STRING1);
                HintButton1.setBackground(getResources().getDrawable(R.drawable.repeat_drawable));
                HintButton2.setVisibility(View.VISIBLE);
            } else if (buttonNumber == 2) {
                hintMessage = currentQuestion.hint2;
                HintButton2.setText(REPEAT_HINT_STRING2);
                HintButton2.setBackground(getResources().getDrawable(R.drawable.repeat_drawable));
                HintButton3.setVisibility(View.VISIBLE);
            } else if (buttonNumber == 3) {
                hintMessage = currentQuestion.hint3;
                HintButton3.setText(REPEAT_HINT_STRING3);
                HintButton3.setBackground(getResources().getDrawable(R.drawable.repeat_drawable));
            }

            if (com.priyanka.TCPClient.singleton != null)
                com.priyanka.TCPClient.singleton.sendMessage("H" + buttonNumber + ":" + hintMessage);
        }

        hintsRemaining--;
    }


    public void NextQuestion(){
        currentQuestionIndex++;

        RightWrongLabel.setText("");
        AnswerText1.setText("");
        AnswerText2.setText("");
        HintButton1.setVisibility(View.VISIBLE);
        HintButton2.setVisibility(View.INVISIBLE);
        HintButton3.setVisibility(View.INVISIBLE);
        HintButton1.setText(REQUEST_HINT_STRING1);
        HintButton2.setText(REQUEST_HINT_STRING2);
        HintButton3.setText(REQUEST_HINT_STRING3);
        HintButton1.setBackground(getResources().getDrawable(R.drawable.hint_drawable));
        HintButton2.setBackground(getResources().getDrawable(R.drawable.hint_drawable));
        HintButton3.setBackground(getResources().getDrawable(R.drawable.hint_drawable));

        hintsRemaining = MAX_HINTS;

        if (currentQuestionIndex >= questions.length()) {
            Intent intent = new Intent(this, com.priyanka.Completed.class);
            //send END message before displaying completed screen
            if (com.priyanka.TCPClient.singleton != null)
                com.priyanka.TCPClient.singleton.sendMessage("END:");
            startActivity(intent);
            return;
        }

        Question question = questions.get(currentQuestionIndex);
        String newQuestion = question.question;
        SubmitButton.setText(SUBMIT_STRING);
        CurrentQuestion.setText(newQuestion);
        questionState = QState.INIT;

        if (question.format.equals(Questions.FORMAT_FRACTION)){
            AnswerText1.setEnabled(true);
            fractionLine.setEnabled(true);
            AnswerText2.setEnabled(true);
            AnswerText1.setVisibility(View.VISIBLE);
            fractionLine.setVisibility(View.VISIBLE);
            AnswerText2.setVisibility(View.VISIBLE);
        } else if (question.format.equals(Questions.FORMAT_TEXT)){
            AnswerText1.setEnabled(true);
            fractionLine.setEnabled(false);
            AnswerText2.setEnabled(false);
            AnswerText2.setVisibility(View.VISIBLE);
            fractionLine.setVisibility(View.INVISIBLE);
            AnswerText2.setVisibility(View.INVISIBLE);
        }

        mKeyboardView.setVisibility(View.VISIBLE);
        mKeyboardView.setEnabled(true);
        TitleLabel.setText(TITLE_PREFIX + " " + (currentQuestionIndex + 1));

        //Send message
        if (com.priyanka.TCPClient.singleton != null)
            com.priyanka.TCPClient.singleton.sendMessage("Q:" + question.spokenQuestion);

        AnswerText1.requestFocus();
    }
}
