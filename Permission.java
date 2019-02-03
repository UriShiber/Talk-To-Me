package com.example.admin.sound_wave_lesson1;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;

public class Permission {

    private Activity activity;

    public Permission(Activity activity) {this.activity = activity;}

    private static final int REQUEST_CODE = 100;

    private static String[] PERMISSION_AUDIO = {
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE,


    };

    public void verifyPermission() {
        boolean permissioned = true;
        for (String permission:PERMISSION_AUDIO) {
            int check = ActivityCompat.checkSelfPermission(activity, permission);
            if (check != PackageManager.PERMISSION_GRANTED) {
                permissioned = false;
            }
        }
        if (!permissioned) {
            ActivityCompat.requestPermissions(activity, PERMISSION_AUDIO, REQUEST_CODE);
        }
    }
}
