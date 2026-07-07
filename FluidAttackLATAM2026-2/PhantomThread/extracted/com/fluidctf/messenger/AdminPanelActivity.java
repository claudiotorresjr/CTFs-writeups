package com.fluidctf.messenger;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class AdminPanelActivity extends Activity {
    private TextView adminInfo;
    private TextView flagDisplay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin_panel);

        this.adminInfo = (TextView) findViewById(R.id.txt_admin_info);
        this.flagDisplay = (TextView) findViewById(R.id.txt_flag_display);

        this.adminInfo.setText("Admin Panel - Diagnostic Mode");
        fetchAdminFlag();
    }

    private void fetchAdminFlag() {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                try {
                    URL url = new URL(BuildConfig.API_BASE_URL + "/api/admin/flag");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    conn.setRequestProperty("X-Admin-Token", BuildConfig.ADMIN_TOKEN);
                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(conn.getInputStream())
                    );
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    reader.close();
                    return sb.toString();
                } catch (Exception e) {
                    return "Error: " + e.getMessage();
                }
            }

            @Override
            protected void onPostExecute(String result) {
                flagDisplay.setText(result);
            }
        }.execute();
    }
}
