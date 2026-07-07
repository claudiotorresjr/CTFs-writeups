package com.fluidctf.messenger;

import android.app.Activity;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

public class ProfileActivity extends Activity {
    private ImageView avatarImage;
    private TextView displayName;
    private TextView statusText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        this.avatarImage = (ImageView) findViewById(R.id.img_avatar);
        this.displayName = (TextView) findViewById(R.id.txt_display_name);
        this.statusText = (TextView) findViewById(R.id.txt_status);

        UserProfile profile = UserManager.getInstance().getCurrentProfile();
        if (profile != null) {
            this.displayName.setText(profile.getDisplayName());
            this.statusText.setText(profile.getStatus());
        }
    }
}
