package com.example.admin.sound_wave_lesson1;


import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;
import java.io.IOException;
import java.util.Locale;

/*
import android.os.Handler;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.*;
import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;
import java.io.FileInputStream;
import java.io.BufferedInputStream;
*/
// for recording sound------------------
import android.os.Environment;
import android.media.MediaRecorder;
import android.media.MediaPlayer;
//--------------------------------------


public class MainActivity extends AppCompatActivity {
    /*
// for client ---------------------------------
    private String socket_ip = "127.0.0.1";
    private int socket_port = 8080;
    private DataOutputStream os = null;
    private BufferedReader is = null;
    private Socket socket;
    private FileInputStream fIS;
    private BufferedInputStream bIS;
    private byte [] buffer;
    */
// --------------------------------------------
// for record button --------------------------
    private boolean isPressed;
    private MediaRecorder myAudioRecorder;
    private String outputFile = null;
    private int counter = 0;
    private MediaPlayer mediaPlayer;
    // --------------------------------------------


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // run ------------------------------------------------------
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // permission -----------------------------------------------
        Permission p = new Permission(this);
        p.verifyPermission();
        //-----------------------------------------------------------
        // for record button ----------------------------------------
        ImageButton RecordButtonImage = findViewById(R.id.RecordButtonImage);
        isPressed = false;
        // for recording --------------------------------------------
        myAudioRecorder = new MediaRecorder();
        myAudioRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        myAudioRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        myAudioRecorder.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB);
        //-----------------------------------------------------------
        // for playing ----------------------------------------------
        mediaPlayer = new MediaPlayer();
        // ----------------------------------------------------------
        RecordButtonImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // first time we click on the record button - start recording
                // second time we click on the record button - stop recording, send audio file to
                // the server and wait for a response
                if (!isPressed) {
                    counter++;
                    String fileName = String.format(Locale.ENGLISH, "/AudioRecording%d.3gp", counter);
                    Toast.makeText(MainActivity.this, fileName,
                            Toast.LENGTH_LONG).show();
                    outputFile = Environment.getExternalStorageDirectory().getAbsolutePath()
                            + fileName;
                    //do recording
                    try {
                        myAudioRecorder.setOutputFile(outputFile);
                        myAudioRecorder.prepare();
                        myAudioRecorder.start();
                    } catch (IllegalStateException ise) {
                        ise.printStackTrace();
                    } catch (IOException ioe) {
                        ioe.printStackTrace();
                    }
                    Toast.makeText(MainActivity.this, "Recording started",
                            Toast.LENGTH_LONG).show();

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
                    // now i need to send the AudioSavePathInDevice to the server and receive a
                    // text file.
                    }
                }
            });
        }
    }

