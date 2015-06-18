package com.priyanka;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.util.Log;
import android.os.AsyncTask;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;

/**
 * Created by aditi on 5/29/15.
 */
public class MainActivity extends Activity implements View.OnClickListener {
    private EditText iPandPort;
    private TCPClient mTcpClient;
    private Button connectButton;
    private Button session1Button;
    private Button session2Button;
    private Button session3Button;
    private Button session4Button;
    private EditText participantID;
    private TextView connectionStatus;
    private RadioButton controlRB;
    private RadioButton adaptiveRB;
    private int sessionNum;
    private int expGroup;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.start_screen);

        iPandPort = (EditText) findViewById(R.id.IPandPort);
        connectButton = (Button) findViewById(R.id.ConnectButton);
        connectionStatus = (TextView) findViewById(R.id.ConnectionStatus);

        participantID = (EditText) findViewById(R.id.ParticipantID);
        participantID.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                participantID.setText("");
            }
        });

        session1Button = (Button) findViewById(R.id.Session1Button);
        session2Button = (Button) findViewById(R.id.Session2Button);
        session3Button = (Button) findViewById(R.id.Session3Button);
        session4Button = (Button) findViewById(R.id.Session4Button);

        session1Button.setOnClickListener(this);
        session2Button.setOnClickListener(this);
        session3Button.setOnClickListener(this);
        session4Button.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        if (v == session1Button)
            sessionNum = 1;
        else if (v == session2Button)
            sessionNum = 2;
        else if (v == session3Button)
            sessionNum = 3;
        else if (v == session4Button)
            sessionNum = 4;

        startMathSession(v);
    }

    public void connected() {
        connectionStatus.setText("Connected.");
    }

    public void startMathSession(View view) {
        Intent intent = new Intent(this, com.priyanka.MathActivity.class);
        intent.putExtra("sessionNum", ""+sessionNum);
        intent.putExtra("expGroup", ""+expGroup);
        String pid = participantID.getText().toString();
        intent.putExtra("participantID", pid);
        //send message to computer to convey session starting
        if (com.priyanka.TCPClient.singleton != null) {
            String startMessage = "START;" + "-1;-1;" + pid + "," + sessionNum + "," + expGroup;
            mTcpClient.sendMessage(startMessage);
        }
        startActivity(intent);
    }

    public void onRadioButtonClicked(View view){
        boolean checked = ((RadioButton) view).isChecked();
        // Check which radio button was clicked
        switch(view.getId()) {
            case R.id.controlRB:
                if (checked)
                    expGroup = 0;
                    break;
            case R.id.adaptiveRB:
                if (checked)
                    expGroup = 1;
                    break;
        }
    }

    public void connectTablet(View view){
        String ipInput = iPandPort.getText().toString();
        String ipaddress = ipInput.split(":")[0];
        String ipport = ipInput.split(":")[1];
        ConnectTask connectTask = new ConnectTask();
        connectTask.owner = this;
        connectTask.execute(ipaddress, ipport);

        connectionStatus.setText("Trying to connect to server");
    }

    public class ConnectTask extends AsyncTask<String,String,TCPClient> {

        private String ipaddress;
        public MainActivity owner;
        @Override
        protected TCPClient doInBackground(String... message) {

            //we create a TCPClient object and
            mTcpClient = new TCPClient(new TCPClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                    onProgressUpdate(message);

                    Log.e("MainActivity", "Message received from server: hiding options");

                    // showMoodMeter = false;
                    //if (message.equalsIgnoreCase("done"))
                    //    showOptions = true;
                    // aditi currentlyPlaying = new String("");
	                    /*thread.setRunning(false);
	    				((Activity)getContext()).finish();*/

                }
            }, owner);

            if (this.validIP(message[0])){
                mTcpClient.setIpAddress(message[0]);
                mTcpClient.setIpPortVar(Integer.parseInt(message[1]));
                //if valid, write ip in text file
                BufferedWriter writer = null;
                try
                {
                    writer = new BufferedWriter(new FileWriter("/sdcard/Movies/ip.txt"));
                    writer.write(message[0]);
                }
                catch (IOException e)
                {
                }
                finally
                {
                    try
                    {
                        if ( writer != null)
                            writer.close( );
                    }
                    catch ( IOException e)
                    {
                    }
                }

            } else {  //if not valid IP, try to read the one from the text file
                String ipaddress = null;
                BufferedReader br = null;
                try {
                    br = new BufferedReader(new FileReader("/sdcard/Movies/ip.txt"));
                } catch (FileNotFoundException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                try {
                    String savedIP = br.readLine();
                    br.close();
                    if (this.validIP(savedIP))
                        mTcpClient.setIpAddress(savedIP);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            // mTcpClient.setIpAddress(message[0]);
            TCPClient.singleton = mTcpClient;
            mTcpClient.run();

            return null;
        }

        public boolean validIP(String ip) {
            if (ip == null || ip.isEmpty()) return false;
            ip = ip.trim();
            if ((ip.length() < 6) & (ip.length() > 15)) return false;

            try {
                Pattern pattern = Pattern.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
                Matcher matcher = pattern.matcher(ip);
                return matcher.matches();
            } catch (PatternSyntaxException ex) {
                return false;
            }
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            //in the arrayList we add the messaged received from server
            // arrayList.add(values[0]);
            // notify the adapter that the data set has changed. This means that new message received
            // from server was added to the list
            //mAdapter.notifyDataSetChanged();
        }
    }
}