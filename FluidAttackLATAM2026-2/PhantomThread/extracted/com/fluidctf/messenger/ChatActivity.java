package com.fluidctf.messenger;

import android.app.Activity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.ListView;

public class ChatActivity extends Activity {
    private ListView messageList;
    private EditText messageInput;
    private int conversationId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        this.conversationId = getIntent().getIntExtra("conversation_id", -1);
        this.messageList = (ListView) findViewById(R.id.message_list);
        this.messageInput = (EditText) findViewById(R.id.message_input);

        if (this.conversationId == -1) {
            finish();
            return;
        }

        loadMessages(this.conversationId);
    }

    private void loadMessages(int conversationId) {
        MessageAdapter adapter = new MessageAdapter(this, conversationId);
        this.messageList.setAdapter(adapter);
    }
}
