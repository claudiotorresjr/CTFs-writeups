package com.whisperchat.app.ui;

import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

import com.whisperchat.app.R;
import com.whisperchat.app.data.ApiClient;
import com.whisperchat.app.model.MessageList;
import com.whisperchat.app.model.Session;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SettingsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        // Staff-only console entry. Hidden for normal accounts, but the
        // backend never checks anything beyond the shared API key, so the
        // route it opens is reachable by anyone replaying that key.
        View adminEntry = findViewById(R.id.admin_console_entry);
        adminEntry.setVisibility(Session.current().isAdmin() ? View.VISIBLE : View.GONE);
        adminEntry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loadAdminFeed();
            }
        });
    }

    private void loadAdminFeed() {
        // GET /api/admin/messages returns every channel, including the
        // private ops thread that holds the quarterly vault recovery code.
        ApiClient.get().getAdminMessages().enqueue(new Callback<MessageList>() {
            @Override
            public void onResponse(Call<MessageList> call, Response<MessageList> response) {
                if (response.isSuccessful() && response.body() != null) {
                    renderMessages(response.body());
                }
            }

            @Override
            public void onFailure(Call<MessageList> call, Throwable t) {
                showError(t);
            }
        });
    }

    private native void renderMessages(MessageList messages);

    private native void showError(Throwable t);
}
