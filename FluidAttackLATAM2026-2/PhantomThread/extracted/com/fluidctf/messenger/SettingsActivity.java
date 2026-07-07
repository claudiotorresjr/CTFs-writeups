package com.fluidctf.messenger;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Switch;
import android.widget.TextView;

public class SettingsActivity extends Activity {
    private Switch notificationsSwitch;
    private Switch darkModeSwitch;
    private TextView profileLink;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        this.notificationsSwitch = (Switch) findViewById(R.id.switch_notifications);
        this.darkModeSwitch = (Switch) findViewById(R.id.switch_dark_mode);
        this.profileLink = (TextView) findViewById(R.id.link_profile);

        SharedPreferencesHelper prefs = new SharedPreferencesHelper(this);
        this.notificationsSwitch.setChecked(prefs.getNotificationsEnabled());
        this.darkModeSwitch.setChecked(prefs.getDarkModeEnabled());

        this.profileLink.setOnClickListener(v -> {
            Intent intent = new Intent(SettingsActivity.this, ProfileActivity.class);
            startActivity(intent);
        });
    }
}
