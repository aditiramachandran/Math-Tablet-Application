package com.priyanka;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.EditText;

/**
 * Created by alexlitoiu on 6/2/15.
 */
public class NoImeEditText extends EditText {
    public NoImeEditText(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
    @Override
    public boolean onCheckIsTextEditor() {
        return false;
    }
}