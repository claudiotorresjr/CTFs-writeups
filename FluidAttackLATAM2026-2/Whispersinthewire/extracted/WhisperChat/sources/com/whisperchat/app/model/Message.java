package com.whisperchat.app.model;

import com.google.gson.annotations.SerializedName;

public class Message {
    @SerializedName("id")
    public String id;

    @SerializedName("sender")
    public String sender;

    @SerializedName("recipient")
    public String recipient;

    @SerializedName("body")
    public String body;

    @SerializedName("timestamp")
    public String timestamp;

    @SerializedName("private")
    public boolean isPrivate;
}
