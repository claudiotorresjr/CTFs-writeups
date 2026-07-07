package com.whisperchat.app.model;

import java.util.List;

import com.google.gson.annotations.SerializedName;

public class MessageList {
    @SerializedName("messages")
    public List<Message> messages;

    @SerializedName("count")
    public int count;
}
