package com.example.admin.sound_wave_lesson1;


import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Locale;

// for recording sound------------------
import android.os.Environment;
import android.media.MediaRecorder;
import android.media.MediaPlayer;
import android.media.AudioRecord;
import android.media.AudioFormat;
import java.io.FileOutputStream;
//--------------------------------------



public class MainActivity extends AppCompatActivity {
// for record button --------------------------
    private boolean isPressed;
    private MediaRecorder myAudioRecorder;
    int BufferSize;
    private String outputFile = null;
    private int counter = 0;
    private MediaPlayer mediaPlayer;
    // --------------------------------------------

    class MyServerThread implements Runnable
    {
        Socket my_socket;
        ServerSocket server_socket;
        InputStreamReader input_stream_reader;
        BufferedReader bufferedReader;
        String num_of_words;
        Handler h = new Handler();
        boolean flag = true;

        @Override
        public void run() {
            try{
                server_socket = new ServerSocket(2121);
                while (flag){
                    my_socket = server_socket.accept();
                    input_stream_reader = new InputStreamReader(my_socket.getInputStream());
                    bufferedReader = new BufferedReader(input_stream_reader);
                    num_of_words = bufferedReader.readLine();

                    h.post(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(), num_of_words,
                                    Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // run ------------------------------------------------------
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // permission -----------------------------------------------
        Permission p = new Permission(this);
        p.verifyPermission();
        //-----------------------------------------------------------
        final Thread myThread = new Thread(new MyServerThread());
        myThread.start();
        // for record button ----------------------------------------
        ImageButton RecordButtonImage = findViewById(R.id.RecordButtonImage);
        isPressed = false;
        // for recording --------------------------------------------
        myAudioRecorder = new MediaRecorder();
        myAudioRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        myAudioRecorder.setOutputFormat(MediaRecorder.OutputFormat.DEFAULT);
        myAudioRecorder.setAudioEncoder(MediaRecorder.OutputFormat.DEFAULT);
        //-----------------------------------------------------------
        // for playing ----------------------------------------------

        // ----------------------------------------------------------
        RecordButtonImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // first time we click on the record button - start recording
                // second time we click on the record button - stop recording, send audio file to
                // the server and wait for a response
                if (!isPressed) {
                    mediaPlayer = new MediaPlayer();
                    String fileName = String.format(Locale.ENGLISH, "/AudioRecording%d.3gpp", counter);
                    Toast.makeText(MainActivity.this, fileName,
                            Toast.LENGTH_LONG).show();
                    outputFile = Environment.getExternalStorageDirectory().getAbsolutePath()
                            + fileName;
                    counter++;
                    //do recording
                    Toast.makeText(MainActivity.this, "Recording started",
                            Toast.LENGTH_LONG).show();
                    try {
                        myAudioRecorder.setOutputFile(outputFile);
                        myAudioRecorder.prepare();
                        myAudioRecorder.start();

                    } catch (IllegalStateException ise) {
                        ise.printStackTrace();
                    } catch (IOException ioe) {
                        ioe.printStackTrace();
                    }
                        isPressed = true;

                } else if (isPressed) {
                    try {
                        myAudioRecorder.stop();
                        myAudioRecorder.release();
                        myAudioRecorder = null;
                    } catch (IllegalStateException ise) {
                        ise.printStackTrace();
                    }
                    Toast.makeText(MainActivity.this, "Recording Completed",
                            Toast.LENGTH_LONG).show();
                    try {
                        // play the recorded audio -------------------------------------
                        mediaPlayer.setDataSource(outputFile);
                        mediaPlayer.prepare();
                        mediaPlayer.start();
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                    // -------------------------------------------------------------
                    isPressed = false;
                    send(outputFile);
                    // now i need to send the AudioSavePathInDevice to the server and receive a
                    // text file.

                    }
                }
                private void send(String outputFile) {
                    MessageSender message_sender = new MessageSender();
                    message_sender.execute(outputFile);
                }
            });
        }
}

