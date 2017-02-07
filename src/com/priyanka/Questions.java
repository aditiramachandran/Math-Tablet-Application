package com.priyanka;

import com.priyanka.Question;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;

import java.io.FileReader;
import java.util.ArrayList;

/**
 * Created by alexlitoiu on 6/4/2015.
 */
public class Questions {

    // define constants for all of the keys
    public static final String SOURCE_TEXT = "Sample Source";
    public static final String KEY_QUESTION = "Question";
    public static final String KEY_SPOKEN_QUESTION = "Spoken Question";
    public static final String KEY_TYPE = "Type";
    public static final String KEY_SPOKEN_TYPE = "Spoken Type";
    public static final String KEY_DIFFICULTY_LEVEL = "Difficulty Level";
    public static final String KEY_FORMAT = "Format";
    public static final String KEY_ANSWER = "Answer";
    public static final String KEY_NUMERATOR = "Numerator";
    public static final String KEY_DENOMINATOR = "Denominator";
    public static final String KEY_VALUE = "Value";
    public static final String KEY_HINTS = "Hints";
    public static final String KEY_HINT1 = "Hint1";
    public static final String KEY_HINT2 = "Hint2";
    public static final String KEY_HINT3 = "Hint3";
    public static final String KEY_SPOKENHINT1 = "Spoken Hint1";
    public static final String KEY_SPOKENHINT2 = "Spoken Hint2";
    public static final String KEY_SPOKENHINT3 = "Spoken Hint3";
    public static final String KEY_SPOKEN_ANSWER = "Spoken Answer";
    public static final String KEY_EXPLANATION = "Written Explanation";
    public static final String KEY_SPOKEN_EXPLANATION = "Spoken Explanation";


    public static final String FORMAT_FRACTION = "fraction";
    public static final String FORMAT_TEXT = "value";

    ArrayList<Question> questions = new ArrayList<Question>();

    public Questions(String contents) {
        try {
            JSONArray jsonQuestions = new JSONArray(contents);

            for (int i = 0; i < jsonQuestions.length(); i++) {
                JSONObject q = jsonQuestions.getJSONObject(i);

                Question newQuestion = new Question(q);
                questions.add(newQuestion);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public int length(){
        return questions.size();
    }

    public Question get(int i){
        return questions.get(i);
    }
}
