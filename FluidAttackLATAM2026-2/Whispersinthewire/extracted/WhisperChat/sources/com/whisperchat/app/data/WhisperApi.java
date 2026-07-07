package com.whisperchat.app.data;

import com.whisperchat.app.model.Message;
import com.whisperchat.app.model.MessageList;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;

/* Retrofit service describing every WhisperChat backend route.
 * Generated from the v1 API contract; not every method is wired to UI. */
public interface WhisperApi {
    @GET("api/messages")
    Call<MessageList> getMessages(@Query("recipient") String recipient);

    @POST("api/messages")
    Call<Message> sendMessage(@Body Message message);

    /* Admin console feed: every channel, including private staff threads.
     * Reached from SettingsActivity only when the account is staff, but the
     * call carries the same shared API key as everything else. */
    @GET("api/admin/messages")
    Call<MessageList> getAdminMessages();
}
