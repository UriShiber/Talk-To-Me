package com.example.admin.sound_wave_lesson1;

import android.os.AsyncTask;
import android.widget.Toast;

import java.io.IOException;
import java.io.FileInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class MessageSender extends AsyncTask<String, Void, Byte> {

    @Override
    protected Byte doInBackground(String... voids) {
        String outputFile = voids[0];
        Socket my_socket;
        DataOutputStream dos;
        FileInputStream fis;
        byte[] my_byte_arr;
        try {
            my_socket = new Socket("192.168.1.20", 1212);
            //-------------------------------
            my_byte_arr = new byte[4096];
            dos = new DataOutputStream(my_socket.getOutputStream());
            fis = new FileInputStream(outputFile);
            int content;
            content = fis.read(my_byte_arr);
            while(content != -1){
                for(byte b : my_byte_arr){
                    dos.write(b);
                }
                content = fis.read(my_byte_arr);
            }

            //-------------------------------

        }catch (IOException e){
            e.printStackTrace();
        }
        return null;

    }
}
