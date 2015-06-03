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

import com.priyanka.TCPClient;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.util.Log;
import android.os.AsyncTask;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

/**
 * Created by aditi on 5/29/15.
 */
public class MainActivity extends Activity {
    private EditText IPandPort;
    private TCPClient mTcpClient;
    private Button ConnectButton;
    private Button Session1Button;
    private Button Session2Button;
    private Button Session3Button;
    private Button Session4Button;
    private EditText ParticipantID;
    private TextView ConnectionStatus;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.start_screen);

        IPandPort = (EditText) findViewById(R.id.IPandPort);
        ConnectButton = (Button) findViewById(R.id.ConnectButton);
        ConnectionStatus = (TextView) findViewById(R.id.ConnectionStatus);

        Session1Button = (Button) findViewById(R.id.Session1Button);
        Session2Button = (Button) findViewById(R.id.Session2Button);
        Session3Button = (Button) findViewById(R.id.Session3Button);
        Session4Button = (Button) findViewById(R.id.Session4Button);


    }

    public void startMathSession(View view) {
        Intent intent = new Intent(this, com.priyanka.MathActivity.class);
        startActivity(intent);
    }

    public void connectTablet(View view){
        String ipInput = IPandPort.getText().toString();
        String ipaddress = ipInput.split(":")[0];
        //new connectTask().execute(ipaddress);

        ConnectionStatus.setText("Trying to connect to server");
    }

    public class connectTask extends AsyncTask<String,String,TCPClient> {

        private String ipaddress;
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
                    //if (message.equalsIgnoreCase("showOptions"))
                    // aditi showOptions = true;
                    // aditi currentlyPlaying = new String("");
	                    /*thread.setRunning(false);
	    				((Activity)getContext()).finish();*/

                }
            });

            if (this.validIP(message[0])){
                mTcpClient.setIpAddress(message[0]);

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
