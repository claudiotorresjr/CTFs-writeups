package com.fluidctf.messenger;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;

public class MainActivity extends Activity {
    private ListView conversationList;
    private Button settingsButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.conversationList = (ListView) findViewById(R.id.conversation_list);
        this.settingsButton = (Button) findViewById(R.id.btn_settings);

        loadConversations();

        this.settingsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, SettingsActivity.class);
                startActivity(intent);
            }
        });

        this.conversationList.setOnItemClickListener((parent, view, position, id) -> {
            Intent chatIntent = new Intent(MainActivity.this, ChatActivity.class);
            chatIntent.putExtra("conversation_id", (int) id);
            startActivity(chatIntent);
        });
    }

    private void loadConversations() {
        ConversationAdapter adapter = new ConversationAdapter(this);
        this.conversationList.setAdapter(adapter);
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadConversations();
    }
}
