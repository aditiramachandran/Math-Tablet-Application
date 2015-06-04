package com.priyanka;

import org.json.JSONObject;

/**
 * Created by alexlitoiu on 6/4/2015.
 */
public class Question {
    public String question;
    public String spokenQuestion;
    public String type;
    public String format;
    public String difficulty;

    public String hint1;
    public String hint2;
    public String hint3;

    public int value;
    public int numerator;
    public int denominator;

    public Question (JSONObject question){
        try {
            this.question = question.getString(Questions.KEY_QUESTION);
            spokenQuestion = question.getString(Questions.KEY_SPOKEN_QUESTION);
            type = question.getString(Questions.KEY_TYPE);
            difficulty = question.getString(Questions.KEY_DIFFICULTY_LEVEL);
            format = question.getString(Questions.KEY_FORMAT);

            // answer is stored in a Json object
            JSONObject a = question.getJSONObject(Questions.KEY_ANSWER);
            // find the answer based on the format
            if (format.equals(Questions.FORMAT_FRACTION)) {
                numerator = a.getInt(Questions.KEY_NUMERATOR);
                denominator = a.getInt(Questions.KEY_DENOMINATOR);
            } else if (format.equals(Questions.FORMAT_TEXT)) {
                value = a.getInt(Questions.KEY_VALUE);
            }

            JSONObject h = question.getJSONObject(Questions.KEY_HINTS);

            hint1 = h.getString(Questions.KEY_HINT1);
            hint2 = h.getString(Questions.KEY_HINT2);
            hint3 = h.getString(Questions.KEY_HINT3);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
