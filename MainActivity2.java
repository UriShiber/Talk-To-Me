package com.example.admin.sound_wave_lesson1;

import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;
import java.io.IOException;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;

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
    public static final int RequestPermissionCode = 1;
// --------------------------------------------

    //Requesting run-time permissions

    //Create placeholder for user's consent to record_audio permission.
    //This will be used in handling callback
    private void requestPermission() {
        ActivityCompat.requestPermissions(MainActivity.this, new
                String[]{WRITE_EXTERNAL_STORAGE, RECORD_AUDIO}, RequestPermissionCode);
    }
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String  permissions[], @NonNull int[] grantResults) {
        switch (requestCode) {
            case RequestPermissionCode:
                if (grantResults.length> 0) {
                    boolean StoragePermission = grantResults[0] ==
                            PackageManager.PERMISSION_GRANTED;
                    boolean RecordPermission = grantResults[1] ==
                            PackageManager.PERMISSION_GRANTED;

                    if (StoragePermission && RecordPermission) {
                        Toast.makeText(MainActivity.this, "Permission Granted",
                                Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(MainActivity.this,"Permission Denied !!!",Toast.LENGTH_LONG).show();
                    }
                }
                break;
        }
    }

    public boolean checkPermission() {
        int result = ContextCompat.checkSelfPermission(getApplicationContext(),
                WRITE_EXTERNAL_STORAGE);
        int result1 = ContextCompat.checkSelfPermission(getApplicationContext(),
                RECORD_AUDIO);
        return result == PackageManager.PERMISSION_GRANTED &&
                result1 == PackageManager.PERMISSION_GRANTED;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // run ------------------------------------------------------
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // for record button ----------------------------------------
        ImageButton RecordButtonImage = findViewById(R.id.RecordButtonImage);
        isPressed = false;
        // for recording --------------------------------------------
        if (checkPermission()) {
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
                        outputFile = Environment.getExternalStorageDirectory().getAbsolutePath()
                                + String.format("/AudioRecording %1$s.3gp", getString(counter));
                        myAudioRecorder.setOutputFile(outputFile);
                        //do recording
                        try {
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
                    }
                    if (isPressed) {
                        myAudioRecorder.stop();
                        myAudioRecorder.release();
                        myAudioRecorder = null;
                        Toast.makeText(MainActivity.this, "Recording Completed",
                                Toast.LENGTH_LONG).show();
                        try {
                            // play the recorded audio -------------------------------------
                            mediaPlayer.setDataSource(outputFile);
                            mediaPlayer.start();
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                        // -------------------------------------------------------------
                        isPressed = false;
                        // now i need to send the AudioSavePathInDevice to the server and receive a
                        // text file.
                    /*
                    try {
                        socket = new Socket(socket_ip, socket_port);
                        buffer = new byte[AudioSavePathInDevice.length()];
                        fIS = new FileInputStream(AudioSavePathInDevice);
                        bIS = new BufferedInputStream(fIS);
                        bIS.read(buffer,0,buffer.length);
                        fOS = new FileOutputStream(socket.getOutputStream());
                        os = new DataOutputStream(socket.getOutputStream());
                        // what we receive
                        is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    } catch (UnknownHostException e) {
                        System.err.println("Don't know about host: " + socket_ip);
                    } catch (IOException e) {
                        System.err.println("Couldn't get I/O for the connection to: " + socket_ip);
                    }
                    if (socket == null || os == null || is == null) {
                        System.err.println("Something is wrong. One variable is null.");
                        return;
                    }
                    try {
                        /*
                        while (true) {
                            System.out.print("Enter an integer (0 to stop connection, -1 to stop server): ");
                            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                            String keyboardInput = br.readLine();
                            os.writeBytes(keyboardInput + "\n");

                            int n = Integer.parseInt(keyboardInput);
                            if (n == 0 || n == -1) {
                                break;
                            }


                        String responseLine = is.readLine();
                        System.out.println("Server returns its square as: " + responseLine);

                        os.close();
                        is.close();
                        socket.close();
                    } catch (UnknownHostException e) {
                        System.err.println("Trying to connect to unknown host: " + e);
                    } catch (IOException e) {
                        System.err.println("IOException:  " + e);
                    }
                    */
                    }
                }
            });
        } else {
            requestPermission();
        }
        }
    }

